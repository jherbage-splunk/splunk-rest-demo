import os
import time
import re
import sys
import splunk
import splunk.auth as auth
import json

if sys.platform == "win32":
    import msvcrt
    # Binary mode is required for persistent mode on Windows.
    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stderr.fileno(), os.O_BINARY)

from splunk.persistconn.application import PersistentServerConnectionApplication




class VirgaApi(PersistentServerConnectionApplication):

    def __init__(self, command_line, command_arg):
        PersistentServerConnectionApplication.__init__(self)
        apifilepath = os.path.join(os.environ['SPLUNK_HOME'], 'etc', 'apps', 'virga-api', 'bin', "apiconf.json")
        with open(apifilepath) as json_data_file:
          self.cfg = json.load(json_data_file)

    def handle(self, in_string):

        try:
          query=json.loads(in_string)["query"]

          try:
            timeout=self.get_search_timeout(query)
            operation=self.check_op(query)
            macro=self.cfg['operations'][operation]["macro"]
            expected_args=[]
            if "args" in self.cfg['operations'][operation]:
              expected_args=self.cfg['operations'][operation]["args"]

            args=self.check_macro_args(query,expected_args)
          except Exception as e:
            return {'payload': str(e),'status': 500}

        except:
          return {'payload': "Unexpected error - malformed request", 'status': 500}

        in_args = self.parse_in_string(in_string)
        sessionKey = in_args['session']['authtoken']
        url_path="/services/search/jobs"
        if len(args) > 0:
          url_args={"search": "`"+macro+"("+args+")`"}
        else:
          url_args={"search": "`"+macro+"`"}
        try:
          serverContent = splunk.rest.simpleRequest(url_path,sessionKey=sessionKey,postargs=url_args,method='POST',raiseAllErrors=True)
        except Exception as ex:
          # get the error text if we can
          if 'text' in ex:
            error=ex['text']
          else:
            error=ex.message
          return {'payload': "Error starting search job: "+str(ex), 'status': 500}

        # Extract the job id whcih looks like this for example "location":"/services/search/jobs/1568890228.1"
        path_re=re.search('[\'\"]location[\'\"]\s*:\s*[\'\"](.*?)[\'\"]', str(serverContent), re.IGNORECASE)
        if path_re:
          url_path=path_re.group(1)
        else:
          return {'payload': "Error starting search job - did not get the search ID returned from "+str(serverContent), 'status': 500}
        job_state=self.check_search_finish(timeout,url_path,sessionKey)
       
        # Did the job fail?
        if not job_state == 'DONE':
          return {'payload': "Search failed. Job state is "+job_state, 'status': 500}

        # return the output of the job
        try:
          jobOutput=splunk.rest.simpleRequest(url_path+"/results?output_mode=json",sessionKey=sessionKey,postargs=None,method='GET',raiseAllErrors=True) 
          jobOutput=json.loads(str(jobOutput[1]))

          if 'results' in jobOutput:
            jobOutput=json.dumps(jobOutput['results'], indent=4)
          else:
            jobOutput="no results"
        except Exception as e:
          return {'payload': "Error getting results from the job: "+str(e), 'status': 500} 

        # return the result
        return {'payload': jobOutput,  # Payload of the request.
                'status': 200          # HTTP status code
        }

    def check_search_finish(self,timeout,path,sessionKey):
      # note the time now as we wont wait beyond now + timeout
      timeout_time=int(time.time())+timeout
      job_state=self.get_job_state(path,sessionKey)
       
      while not job_state in ['DONE','FAILED']:
        time.sleep(self.cfg['polling_interval']) 
        # if we run out of time cancel the search
        if int(time.time()) > timeout_time:
          splunk.rest.simpleRequest(path,sessionKey=sessionKey,postargs=None,method='DELETE',raiseAllErrors=True)
          job_state="TIMEOUT"
          break
        else:
          job_state=self.get_job_state(path,sessionKey)
      return job_state     

    def get_job_state(self,path,sessionKey):
      job_details=splunk.rest.simpleRequest(path,sessionKey=sessionKey,postargs=None,method='GET',raiseAllErrors=True)
      state_re=re.search('dispatchState[\'\"]>(\w+?)<', str(job_details), re.IGNORECASE)
      if state_re:
        job_state=state_re.group(1)
      else:
        job_state="unknown"
      return job_state

    def return_error(self,error):
      raise Exception(error)

    def check_op(self,query):
      # extract the operation argument
      operation=None
      for i in range(len(query)):
        if query[i][0] == 'operation':
          operation=query[i][1]
      if operation is None:
        return self.return_error("operation is a mandatory parameter")
      else:
        operation=operation

      if operation not in self.cfg['operations']:
        return self.return_error("operation "+operation+" is not supported")
      else:
        return operation
    
    def get_search_timeout(self,query):
    
      timeout=self.cfg['search_timeout']
      for i in range(len(query)):
        if query[i][0] == 'search_timeout':
          timeout=int(query[i][1])
    
      if timeout > self.cfg['max_search_timeout']:
        return self.return_error("search_timeout is greater than permitted max value of "+str(self.cfg['max_search_timeout']))
      else:
        return timeout

    def check_macro_args(self,query,expected_args):
      # check the query args
      arg_values=[]
      for i in range(len(expected_args)):
        arg_value=None
        for j in range(len(query)):
          if query[j][0] == expected_args[i]:
            arg_value=query[j][1]
        if arg_value is None:
          return self.return_error("argument "+expected_args[i] + " is mandatory for this operation")
        else:
          arg_values.append(arg_value)

      return "\""+"\",\"".join(arg_values)+"\""

    def parse_in_string(self, in_string):

      params = json.loads(in_string)

      params['method'] = params['method'].lower()

      params['form_parameters'] = self.convert_to_dict(params.get('form', []))
      params['query_parameters'] = self.convert_to_dict(params.get('query', []))

      return params

    def convert_to_dict(self, query):
      parameters = {}

      for key, val in query:

        # If the key is already in the list, but the existing entry isn't a list then make the
        # existing entry a list and add thi one
        if key in parameters and not isinstance(parameters[key], list):
          parameters[key] = [parameters[key], val]

        # If the entry is already included as a list, then just add the entry
        elif key in parameters:
          parameters[key].append(val)

        # Otherwise, just add the entry
        else:
          parameters[key] = val

      return parameters
