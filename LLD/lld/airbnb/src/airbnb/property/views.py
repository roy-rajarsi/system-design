from .models import Property
from .serializers import PropertySerializer

from django.core.validators import ValidationError
from logging import Logger, getLogger, DEBUG, ERROR, WARNING
from rest_framework.authentication import BaseAuthentication, BasicAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from typing import Any, Dict, List, Optional


logger: Logger = getLogger(name=__name__)


class PropertyApi(APIView):

    authentication_classes: List[BaseAuthentication] = [BasicAuthentication]
    permission_classes: List[BasePermission] = [IsAuthenticated]

    def get(self, request: Request, property_id: Optional[int], format: Optional[str] = None) -> Response:
        logger.log(level=DEBUG, msg=f'Request {request} with property_id: {property_id} received')

        response_payload: Dict[str, Any] = {'message': str(), 'property': None}
        status: int = HTTP_200_OK
        if property_id is None:
            response_payload['message'] = 'Please send in a property_id for getting Property Details'
        else:
            try:
                property_: Property = Property.objects.get(property_id=property_id)
                response_payload['message'] = 'Property Instance Found'
                response_payload['property'] = PropertySerializer(instance=property_).data
            except Property.DoesNotExist as exception:
                response_payload['message'] = f'Property with property_id: {property_id} does not exist'
                status = HTTP_404_NOT_FOUND
                logger.log(level=DEBUG, msg=f'Property with property_id: {property_id} does not exist \n {str(exception)}', exc_info=True)

        return Response(data=response_payload, status=status)

    def post(self, request: Request, format: Optional[str] = None) -> Response:
        logger.log(level=DEBUG, msg=f'Request {request} with payload: {request.data} received')

        response_payload: Dict[str, Any] = {'message': str()}
        status: int = HTTP_201_CREATED
        property_serializer: PropertySerializer = PropertySerializer(data=request.data.get('property'))
        try:
            property_serializer.is_valid(raise_exception=True)
            property_: Property = property_serializer.save()
            response_payload['message'] = f'Property with property_id: {property_.property_id} is created'
        except ValidationError as exception:
            logger.log(level=ERROR, msg=f'Validation Error: \n {str(exception)}', exc_info=True)
            response_payload['message'] = f'Validation Error: \n {str(exception)}'
            status = HTTP_400_BAD_REQUEST

        logger.log(level=DEBUG, msg=f'Response(data={response_payload}, status={status})')
        return Response(data=response_payload, status=status)

    def put(self, request: Request, format: Optional[str] = None) -> Response:
        logger.log(level=DEBUG, msg=f'Request {request} with payload {request.data} received')
        response_payload: Dict[str, Any] = {'message': str()}
        status: int = HTTP_200_OK

        try:
            property_instance: Property = Property.objects.get(property_id=request.data.get('property_id'))
            updates: Optional[Dict[str, Any]] = request.data.get('updates', None)
            if updates is None:
                logger.log(level=WARNING, msg=f'Updates is empty')
            property_serializer: PropertySerializer = PropertySerializer(instance=property_instance, data=updates, partial=True)
            property_serializer.is_valid(raise_exception=True)
            property_serializer.save()
            response_payload['message'] = f'Updates are done on Property with property_id: {property_instance.property_id}'
        except ValidationError as exception:
            logger.log(level=ERROR, msg=f'Validation Error: \n {str(exception)}', exc_info=True)
            response_payload['message'] = f'Validation Error: \n {str(exception)}'
            status = HTTP_400_BAD_REQUEST
        except Property.DoesNotExist as exception:
            logger.log(level=ERROR, msg=f'Property with property_id: {request.data.get("property_id")} does not exist', exc_info=True)
            response_payload['message'] = f'Property with property_id: {request.data.get("property_id")} does not exist'
            status = HTTP_404_NOT_FOUND

        logger.log(level=DEBUG, msg=f'Response(data={response_payload} status={status})')
        return Response(data=response_payload, status=status)

    def delete(self, request: Request, format: Optional[str] = None) -> Response:
        logger.log(level=DEBUG, msg=f'Request {request} with payload {request.data} received')
        response_payload: Dict[str, Any] = {'message': str()}
        status: int = HTTP_200_OK

        try:
            property_instance: Property = Property.objects.get(property_id=request.data.get('property_id'))
            property_instance.delete()
            response_payload['message'] = f'Property with property_id: {request.data.get("id")}'
        except Property.DoesNotExist as exception:
            logger.log(level=ERROR, msg=f'Property with property_id: {request.data.get("property_id")} does not exist \n {str(exception)}', exc_info=True)
            response_payload['message'] = f'Property with property_id: {request.data.get("property_id")} does not exist \n {str(exception)}'
            status = HTTP_404_NOT_FOUND

        logger.log(level=DEBUG, msg=f'Response(data={response_payload}, status={status})')
        return Response(data=response_payload, status=status)
