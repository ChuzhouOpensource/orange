from django.utils.deprecation import MiddlewareMixin

import logging
import time


class LogMiddleware(MiddlewareMixin):
    start = 0

    def process_request(self, request):
        self.start = time.time()

    def process_response(self, request, response):
        cost_timer = time.time() - self.start

        logger = logging.getLogger("django")
        if cost_timer > 0.5:
            logger.warning(f"请求路径: {request.path} 耗时{cost_timer}秒")

        return response