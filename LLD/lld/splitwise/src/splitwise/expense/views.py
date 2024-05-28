from serializers import ExpenseSerializer, GroupExpenseSerializer, NonGroupExpenseSerializer

from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from typing import Optional, Any


class GroupExpenseView(APIView):

    def post(self, request: Request, format: Optional[Any] = None) -> Response:

        expense_details: Optional[ExpenseSerializer] = ExpenseSerializer(data=request.data.get('expense', None))
        group_expense_details: Optional[GroupExpenseSerializer] = GroupExpenseSerializer(data=request.data.)
        try:
            expense_details.is_valid(raise_exception=True)
            group_expense_details.is_valid(raise_exception=True)
        except ValidationError:
            return Response(data={}, status=HTTP_400_BAD_REQUEST)









