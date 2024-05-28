from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from typing import Any, Optional


class AmountOwedInGroupMap(APIView):

    def get(self, request: Request, format: Optional[Any] = None) -> Response:
        pass

    def post(self, request: Request, format: Optional[Any] = None) -> Response:
        # Creation of AmountOwedMapInGroup
        pass

    def patch(self, request: Request, format: Optional[Any] = None) -> Response:
        # Adding new Expense or settling new expense. So edit the map
        # group exchange_type, map_generation strategy
        pass