import threading


class RequestMiddleware:
    """
        this requestmiddleware will help us get the request object right from
        the models and signals.
    """

    def __init__(self, get_response, thread_local=threading.local()):
        self.get_response = get_response
        self.thread_local = thread_local

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        self.thread_local.current_request = request

        return self.get_response(request)
