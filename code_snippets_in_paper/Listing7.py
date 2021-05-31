def find_library(name)->Union[str, None]:...

class CDLL(object):
    def __init__(self, name:str, mode=DEFAULT_MODE, handle=  None, use_errno=False, use_last_error=False):...

libssl_name = ctypes.util.find_library('ssl')
# libssl_name: Union[str, None] = ctypes.util.find_library('ssl')
libssl = ctypes.CDLL(libssl_name)
