import json
import logging

import allure
from allure_commons.types import AttachmentType
from requests import Response

from core.models.base_models import Request
from core.utils.utils import get_response_content

logger = logging.getLogger(__name__)


def logs_middleware(handler, request: Request) -> Response:
    logger.debug(f"Request Headers:\n{request.headers}")
    if request.json_data is not None:
        logging.debug(f"Request Body:\n{json.dumps(request.json_data, indent=2)}")
    if request.data is not None:
        logging.debug(f"Request Body:\n{str(request.data)}")
    if request.auth is not None:
        logging.debug(f"Request Body:\n{str(request.auth)}")

    response: Response = handler(request)
    response_content = get_response_content(response)

    logger.debug(f"Response Code:\n{str(response.status_code)}")
    if isinstance(response_content, dict):
        logger.debug(f"Response Body:\n{json.dumps(response_content, indent=2)}")
    else:
        logger.debug(f"Response Body:\n{response_content}")

    return response


def allure_attachments_middleware(handler, request: Request):
    allure.attach(f"{request.method} {request.path}\n{request.headers}", name="Request", attachment_type=AttachmentType.TEXT)
    if request.json_data is not None:
        allure.attach(json.dumps(request.json_data, indent=2), name="Request Body", attachment_type=AttachmentType.JSON)
    if request.data is not None:
        allure.attach(str(request.data), name="Request Body", attachment_type=AttachmentType.TEXT)
    if request.auth is not None:
        allure.attach(str(request.auth), name="Request Body", attachment_type=AttachmentType.TEXT)

    response: Response = handler(request)
    response_content = get_response_content(response)

    allure.attach(str(response.status_code), name="Response Code", attachment_type=AttachmentType.TEXT)
    if isinstance(response_content, dict):
        allure.attach(json.dumps(response_content, indent=2), name="Response Body", attachment_type=AttachmentType.JSON)
    else:
        allure.attach(str(response_content), name="Response Body", attachment_type=AttachmentType.TEXT)

    return response
