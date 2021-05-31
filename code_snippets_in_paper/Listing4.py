CustomHTTPSConnection = None
if hasattr(httplib, 'HTTPSConnection') and hasattr(urllib_request, 'HTTPSHandler'):
    class CustomHTTPSConnection(httplib.HTTPSConnection):
        def __init__(self, *args, **kwargs): 
            ...

###Possible annotation strategy
CustomHTTPSConnection:Union[None, Type[CustomHTTPSConnectionClass]] = None

if hasattr(httplib, 'HTTPSConnection') and hasattr(urllib_request, 'HTTPSHandler'):
    class CustomHTTPSConnectionClass(httplib.HTTPSConnection):
        def __init__(self, *args, **kwargs): 
            ...

CustomHTTPSConnection = CustomHTTPSConnectionClass