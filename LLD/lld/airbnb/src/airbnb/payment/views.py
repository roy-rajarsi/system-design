from flows.payment.payment_initiation_flow import PaymentInitiationFlow
from listing.models import Listing
from .models import Payment
from .serializers import PaymentSerializer

from django.contrib.auth.models import User
from django.db import connection
from logging import Logger, getLogger, DEBUG, ERROR, INFO
from rest_framework.views import APIView
from rest_framework.authentication import BaseAuthentication, BasicAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from typing import Any, Dict, List, Optional


logger: Logger = getLogger(name=__name__)


class PaymentApi(APIView):

    authentication_classes: List[BaseAuthentication] = [BasicAuthentication]
    permission_classes: List[BasePermission] = [IsAuthenticated]

    def get(self, request: Request, order_id: Optional[str] = None, format: Optional[str] = None) -> Response:
        logger.log(level=DEBUG, msg=f'Request {request} with order_id: {order_id} received')

        response_payload: Dict[str, Any] = {'message': str(), 'payment': None}
        status: int = HTTP_200_OK
        if order_id is None:
            response_payload['message'] = 'Please send in an order_id for getting Payment Details'
        else:
            try:
                payment: Payment = Payment.objects.get(order_id=order_id)
                response_payload['message'] = 'Payment Instance Found'
                response_payload['payment'] = PaymentSerializer(instance=payment).data
                logger.log(level=INFO, msg=f'Query Executed : {connection.queries}')
                logger.log(level=DEBUG, msg=f'Response: (data={response_payload}, status={status}')
            except Payment.DoesNotExist as exception:
                response_payload['message'] = f'Payment with order_id: {order_id} does not exist'
                status = HTTP_404_NOT_FOUND
                logger.log(level=DEBUG, msg=f'Payment with order_id: {order_id} does not exist \n {str(exception)}', exc_info=True)

        return Response(data=response_payload, status=status)

    def post(self, request: Request, format: Optional[str] = None) -> Response:
        logger.log(level=DEBUG, msg=f'Request Received: {request.data}')
        try:
            user: Optional[User] = request.user
            listing: Optional[Listing] = Listing.objects.get(id=request.data.get('listing_id', None))
            amount: Optional[float] = request.data.get('amount', None)
            currency: Optional[str] = request.data.get('currency', None)
            response: Dict[str, Any] = PaymentInitiationFlow().process_request(request={
                'user': user,
                'listing': listing,
                'amount': amount,
                'currency': currency
            })
            logger.log(level=DEBUG, msg=f'Response: {response}')
            return Response(data=response, status=HTTP_201_CREATED)
        except Exception as exception:
            logger.log(level=ERROR, msg=f'Exception Occurred: {exception}', exc_info=True)
            return Response(data={'exception': str(exception)}, status=HTTP_400_BAD_REQUEST)
