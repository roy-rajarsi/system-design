from abc import ABC, abstractmethod
from typing import Any
from copy import deepcopy


class AuthRequest(ABC):

    """ Base Authentication and Authorization Request Class """

    def __init__(self, request: dict[str, Any]) -> None:
        self._request: dict[str, Any] = request

    def get_request_as_dict(self) -> dict[str, Any]:
        return deepcopy(self._request)

    @staticmethod
    @abstractmethod
    def validate_request(request: dict[str, Any]) -> None:
        pass

    def __repr__(self) -> str:
        return f"{self.get_request_as_dict()}"


class UserNameValidationRequest(AuthRequest):

    """ Authentication Request Class for Username Validation Request """

    def __init__(self, request: dict[str, Any]) -> None:
        UserNameValidationRequest.validate_request(request=request)
        super().__init__(request=request)

    @staticmethod
    def validate_request(request: dict[str, Any]) -> None:
        if request.get('username', None) is None:
            raise Exception("No Username in UserNameValidationRequest")


class PasswordValidationRequest(AuthRequest):

    """ Authentication Request Class for Password Validation Request """

    def __init__(self, request: dict[str, Any]) -> None:
        self.validate_request(request=request)
        super().__init__(request=request)

    @staticmethod
    def validate_request(request: dict[str, Any]) -> None:
        if request.get('user_id', None) is None:
            raise Exception("No UserId in PasswordValidationRequest")
        if request.get('password', None) is None:
            raise Exception("No Password in PasswordValidationRequest")


class PermissionGrantRequest(AuthRequest):

    """ Authorization Request Class for Permission Grant Request """

    def __init__(self, request: dict[str, Any]) -> None:
        PermissionGrantRequest.validate_request(request=request)
        super().__init__(request=request)

    @staticmethod
    def validate_request(request: dict[str, Any]) -> None:
        if request.get('user_id', None) is None:
            raise Exception("No UserId in Permission Grant Request")
        if request.get('password_matched', None) is None:
            raise Exception("No Password Matched Status in Permission Grant Request")


class RateLimitRequest(AuthRequest):

    """ Authentication Request Class for Rate Limit Request """

    def __init__(self, request: dict[str, Any]):
        RateLimitRequest.validate_request(request=request)
        super().__init__(request=request)

    @staticmethod
    def validate_request(request: dict[str, Any]) -> None:
        if request.get('user_id', None) is None:
            raise Exception("No UserId in RateLimitRequest")
        if request.get('password', None) is None:
            raise Exception("No Password in RateLimitRequest")
