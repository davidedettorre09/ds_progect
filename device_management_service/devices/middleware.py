import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class AuthLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger.info("=== AuthLoggingMiddleware ===")
        logger.info(f"Authorization Header: {request.headers.get('Authorization')}")
        logger.info(f"request.user: {request.user}")
        logger.info(f"request.auth: {request.auth}")
