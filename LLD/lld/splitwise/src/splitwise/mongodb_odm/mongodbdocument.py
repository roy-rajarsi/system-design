from datetime import date, datetime
from decimal import Decimal
from typing import Dict, List, Optional, Union


class MongoDbDocument:

    def __init__(self, data: Dict[str, Union[bool, Decimal, int, str, date, datetime, 'MongoDbDocument']]) -> None:
        self.__data: Dict[str, Union[bool, Decimal, int, str, date, datetime, 'MongoDbDocument']] = data

    def get_value_from_key(self, key: str) -> Optional[Union[bool, Decimal, int, str, date, datetime, 'MongoDbDocument']]:
        return self.__data.get(key, None)

    def set_value_for_key(self, key: str, value: Union[bool, Decimal, int, str, date, datetime, 'MongoDbDocument']) -> None:
        self.__data[key] = value

    def get_keys(self) -> List[str]:
        return list(self.__data.keys())

    def get_key_value_pairs(self) -> Dict[str, Union[bool, Decimal, int, str, date, datetime, 'MongoDbDocument']]:
        return self.__data

    def __repr__(self) -> str:
        return f'MongoDbDocument({self.__data})'
