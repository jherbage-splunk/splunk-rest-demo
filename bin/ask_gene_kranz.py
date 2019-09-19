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


    # These operations define the scope of the allowed macros with the args expected for each macro (we need the args to check if their values are provided)
    # The args array needs to be in the order the args are passed to the macro
    operations={
      "test": {
                "macro": "test_virga-api",
                "args": ["stack","info"]
              },
      "test_no_args": {
                "macro": "test_virga-api"
              },
    }

    # default timeout to wait for search to complete - can be overridden by user up the max specified here - we will kill your search if you reach the max!
    max_search_timeout=180
    search_timeout=30
    polling_interval=5

    def __init__(self, command_line, command_arg):
        PersistentServerConnectionApplication.__init__(self)

    def handle(self, in_string):

        try:
          query=json.loads(in_string)["query"]

          try:
            timeout=self.get_search_timeout(query)
            operation=self.check_op(query)
            macro=self.operations[operation]["macro"]
            expected_args=[]
            if "args" in self.operations[operation]:
              expected_args=self.operations[operation]["args"]

            args=self.check_macro_args(query,expected_args)
          except Exception as e:
            return {'payload': str(e),'status': 500}

        except:
          return {'payload': "Unexpected error - malformed request", 'status': 500}

        sessionKey = auth.getSessionKey('admin','changeme')
        url_path="/services/search/jobs"
        url_args={"search": "`"+macro+"("+args+")`"}
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

        return {'payload': job_state,  # Payload of the request.
                'status': 200          # HTTP status code
        }

    def check_search_finish(self,timeout,path,sessionKey):
      # note the time now as we wont wait beyond now + timeout
      timeout_time=int(time.time())+timeout
      job_state=self.get_job_state(path,sessionKey)
       
      while not job_state in ['DONE','FAILED']:
        time.sleep(self.polling_interval) 
        # if we run out of time cancel the search
        if int(time.time()) > timeout_time:
          splunk.rest.simpleRequest(path,sessionKey=sessionKey,postargs=None,method='DELETE',raiseAllErrors=True)
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

      if operation not in self.operations:
        return self.return_error("operation "+operation+" is not supported")
      else:
        return operation
    
    def get_search_timeout(self,query):
    
      timeout=self.search_timeout
      for i in range(len(query)):
        if query[i][0] == 'search_timeout':
          timeout=int(query[i][1])
    
      if timeout > self.max_search_timeout:
        return self.return_error("search_timeout is greater than permitted max value of "+str(self.max_search_timeout))
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
