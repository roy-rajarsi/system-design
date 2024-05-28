from enum import Enum


class RequestType(Enum):

    HTTP_REQUEST_TYPE_GET = 'GET',
    HTTP_REQUEST_TYPE_POST = 'POST',
    HTTP_REQUEST_TYPE_PATCH = 'PATCH',
    HTTP_REQUEST_TYPE_PUT = 'PUT',
    HTTP_REQUEST_TYPE_DELETE = 'DELETE'
