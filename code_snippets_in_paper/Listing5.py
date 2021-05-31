try:
    import httplib
except ImportError:
	# Python 3
    import http.client as httplib #type:ignore
    ### Fix to mitigate type errors
    ##import http.client as httpclienttemp
    ##httplib = httpclienttemp