from typing import Any, Optional


class PaymentAttributesInvalidException(Exception):

    def __init__(self, attribute_name: str, attribute_value: Any, listing_price: Optional[float] = None, valid_values: Optional[Any] = None) -> None:
        self.message: str
        if attribute_name == 'amount':
            self.message = (f'Payment Attribute {attribute_name} has value {attribute_value}'
                            f'\n'
                            f'Payment Attribute {attribute_name} must have value >= 0') if listing_price is None else \
                (f'Payment Attribute {attribute_name} has value {attribute_value}'
                 f'\n'
                 f'Payment Attribute {attribute_name} must have value = Listing Price : {listing_price}')
        elif attribute_name == 'currency':
            self.message = (f'Payment Attribute {attribute_name} has value {attribute_value}'
                            f'\n'
                            f'Payment Attribute {attribute_name} must have values {valid_values}')
        super().__init__(self.message)
