import os
import sys
import json
import logging

if sys.platform == "win32":
    import msvcrt
    # Binary mode is required for persistent mode on Windows.
    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stderr.fileno(), os.O_BINARY)

logfile = os.sep.join([os.environ['SPLUNK_HOME'], 'var', 'log', 'splunk', 'persistent_handler.log'])
logging.basicConfig(filename=logfile,level=logging.DEBUG)

from splunk.persistconn.application import PersistentServerConnectionApplication

def flatten_query_params(params):
    # Query parameters are provided as a list of pairs and can be repeated, e.g.:
    #
    #   "query": [ ["arg1","val1"], ["arg2", "val2"], ["arg1", val2"] ]
    #
    # This function simply accepts only the first parameter and discards duplicates and is not intended to provide an
    # example of advanced argument handling.
    flattened = {}
    for i, j in params:
        flattened[i] = flattened.get(i) or j
    return flattened


class MultiformatPersistentHandler(PersistentServerConnectionApplication):

    def __init__(self, command_line, command_arg):
        PersistentServerConnectionApplication.__init__(self)

    def handle(self, in_string):

        request = json.loads(in_string)
        query_params = flatten_query_params(request['query'])

        input_string = query_params.get('input')
        output_format = query_params.get('format')

        logging.debug('QUERY_PARAMS: %s', str(query_params))

        payload = None
        err_payload = json.dumps({ 'payload': None })

        if not input_string or not output_format:
            return err_payload

        reversed_input = input_string[::-1]

        if output_format == 'json':
            # Returning a list or object invokes JSON output
            payload = { 'payload': [ reversed_input ] }
        elif output_format == 'raw':
            # Returning the raw string invokes "raw" output
            payload = { 'payload': reversed_input }
        else:
            # Return a different HTTP status code if we have no acceptable format.
            return err_payload

        logging.debug('PAYLOAD: %s', str(payload))

        return json.dumps(payload)