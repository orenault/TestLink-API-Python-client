from testlink import TestlinkAPIGeneric, TestlinkAPIClient, TestLinkHelper


class TestlinkAPILibrary(object):
    """Robot Framework test library for testing TestLink-API-Python-client, 
    a Python XML-RPC client for TestLink.
    
    Best way to configure SERVER_URL and DEVKEY is to define them via enviroment
    TESTLINK_API_PYTHON_SERVER_URL and TESTLINK_API_PYTHON_DEVKEY from outside
    """
    
    ROBOT_LIBRARY_SCOPE = 'TEST_SUITE'

    def __init__(self, client_class='TestlinkAPIClient', server_url=None, devkey=None ):
        self._client_class = client_class
        self._server_url  = server_url
        self._devkey      = devkey
        self.api_client   = None
 
    def create_api_client(self, client_class='TestlinkAPIClient', 
                          server_url=None, devkey=None):
        """Creates a new TestLink-API-Python-client (XMLRPC), using Python class 
        TestlinkAPIClient or TestlinkAPIGeneric. 
        """

        a_server_url  = server_url or self._server_url
        a_devkey      = devkey or self._devkey
        a_helper = TestLinkHelper(a_server_url, a_devkey)
        
        a_class_name  = client_class or self._client_class
        a_api_class   = globals()[a_class_name]
        self.api_client  = a_helper.connect(a_api_class)
        return self.api_client 
        
    def call_api_method(self, method_name, *args):
        """Calls a TestLink API method and returns TestLinks server response.
        """
        
        # this is an extended version of the BuiltIn keyword "Call Method"
                 
        client = self.api_client
        try:
            method = getattr(client, method_name)
        except AttributeError:
            raise RuntimeError("TLAPI Client '%s' does not have a method '%s'"
                               % (client.__class__.__name__, method_name))

        # split positional and optional args
        # condition optional args: argname=argvalue
        # FIXME LC: real ugly code
        posargs=[]
        optargs={}
        for a_arg in args:
            if '=' in a_arg:
                l = a_arg.split('=')
                optargs[l[0]]=l[1]
            else:
                posargs.append(a_arg)
            
        return method(*posargs, **optargs)
