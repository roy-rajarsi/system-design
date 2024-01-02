from abc import ABC, abstractmethod
from typing import Any
from copy import deepcopy


class AuthResponse(ABC):

    """ Base Authentication and Authorization Response """

    def __init__(self, response: dict[str, Any]) -> None:
        self._response: dict[str, Any] = response

    def get_response_as_dict(self) -> dict[str, Any]:
        return deepcopy(self._response)

    @staticmethod
    @abstractmethod
    def validate_response(response: dict[str, Any]) -> None:
        pass

    def __repr__(self) -> str:
        return f"{self.get_response_as_dict()}"


class UserNameValidationResponse(AuthResponse):

    """ Authentication Response Class for Username Validation Request """

    def __init__(self, response: dict[str, Any]) -> None:
        UserNameValidationResponse.validate_response(response=response)
        super().__init__(response=response)

    @staticmethod
    def validate_response(response: dict[str, Any]) -> None:
        if response.get('user_id', None) is None:
            raise Exception("No UserId in UserNameValidationResponse")


class PasswordValidationResponse(AuthResponse):

    """ Authentication Response Class for Username Validation Request """

    def __init__(self, response: dict[str, Any]) -> None:
        PasswordValidationResponse.validate_response(response=response)
        super().__init__(response=response)

    @staticmethod
    def validate_response(response: dict[str, Any]) -> None:
        if response.get('user_id', None) is None:
            raise Exception("No UserId in PasswordValidationResponse")
        if response.get('password_matched', None) is None:
            raise Exception("No PasswordMatched Status in PasswordValidationResponse")


class PermissionGrantResponse(AuthResponse):

    """ Authorization Response Class for Permission Grant Response """

    def __init__(self, response: dict[str, Any]) -> None:
        PermissionGrantResponse.validate_response(response=response)
        super().__init__(response=response)

    @staticmethod
    def validate_response(response: dict[str, Any]) -> None:
        if response.get('user_id', None) is None:
            raise Exception("No UserId in PermissionGrantResponse")
        if response.get('permission_granted', None) is None:
            raise Exception("No Permission Granted Status in PermissionGrantResponse")
        if response.get('permissions', None) is None:
            raise Exception("No Permission List in PermissionGrantResponse")


class RateLimitResponse(AuthResponse):

    """ Authentication Request Class for Rate Limit Response """

    def __init__(self, response: dict[str, Any]) -> None:
        RateLimitResponse.validate_response(response=response)
        super().__init__(response=response)

    @staticmethod
    def validate_response(response: dict[str, Any]) -> None:
        if response.get('user_id', None) is None:
            raise Exception("No UserId in RateLimitResponse")
        if response.get('already_logged_in_status', None) is None:
            raise Exception("No LoginStatus in RateLimitResponse")
