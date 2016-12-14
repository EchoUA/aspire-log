from activity_log.utilities import activity_log
from django.conf import settings

EXCLUDE_URLS = getattr(settings, 'EXCLUDE_URLS', [])
USER_AFFECTED_MODELS = getattr(settings, 'USER_AFFECTED_MODELS', [])


class GetUserActivityMiddleware(object):
    def check_url(self, url):
        for i in EXCLUDE_URLS:
            if i in url:
                return False
        return True

    def process_response(self, request, response):
        # import pdb; pdb.set_trace()
        if self.check_url(request.path):
            if 'login' in request.path:
                activity_log(request, response, security=True)
            else:
                activity_log(request, response)
        return response
