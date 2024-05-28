from mongodb_odm.mongodbcollection import MongoDbCollection
from mongodb_odm.mongodbdocument import MongoDbDocument

from django.contrib.auth.models import User
from django.db import models
from threading import Lock
from typing import final, List, Optional


class Group(models.Model):

    id: models.AutoField = models.AutoField(primary_key=True)
    name: models.CharField = models.CharField(max_length=30, blank=False)
    admin_user: models.ForeignKey = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __repr__(self) -> str:
        return f'Group_{self.id}'


class GroupToUserListIdMapping(models.Model):

    id: models.AutoField = models.AutoField(primary_key=True)
    group: models.ForeignKey = models.ForeignKey(to=Group, on_delete=models.CASCADE)
    user_list_id: models.AutoField = models.AutoField()

    class Meta:
        indexes: List[models.Index] = [models.Index(fields=['group'])]

    def __repr__(self) -> str:
        return f'GroupToUserListMapping_{self.id}: {self.group}'


class GroupToMoneyOwedInGroupIdMapping(models.Model):

    id: models.AutoField = models.AutoField(primary_key=True)
    group: models.ForeignKey = models.ForeignKey(to=Group, on_delete=models.CASCADE)
    money_owed_in_group_id: models.AutoField()

    class Meta:
        indexes: List[models.Index] = [models.Index(fields=['group'])]

    def __repr__(self) -> str:
        return f'GroupToMoneyOwedInGroupIdMapping_{self.id}: {self.group}'


@final
class UserListInGroupMap(MongoDbCollection):

    __collection_instantiation_lock: Lock = Lock()
    __user_list_in_group: Optional['UserListInGroupMap'] = None
    __collection_name: str = 'user_list_in_group'

    def __new__(cls, *args, **kwargs) -> 'UserListInGroupMap':

        if cls.__user_list_in_group is None:
            cls.__collection_instantiation_lock.acquire(blocking=True, timeout=-1)

            if cls.__user_list_in_group is None:
                cls.__user_list_in_group = super().__new__(cls=cls)

            cls.__collection_instantiation_lock.release()

        return cls.__user_list_in_group

    def __init__(self) -> None:
        super().__init__(collection_name=UserListInGroupMap.__collection_name)


@final
class MoneyOwedInGroupMap(MongoDbCollection):

    __collection_instantiation_lock: Lock = Lock()
    __money_owed_in_group_map: Optional['MoneyOwedInGroupMap'] = None
    __collection_name: str = 'money_owed_in_group_map'

    def __new__(cls, *args, **kwargs) -> 'MoneyOwedInGroupMap':

        if cls.__money_owed_in_group_map is None:
            cls.__collection_instantiation_lock.acquire(blocking=True, timeout=-1)

            if cls.__money_owed_in_group_map is None:
                cls.__money_owed_in_group_map = super().__new__(cls=cls)

            cls.__collection_instantiation_lock.release()

        return cls.__money_owed_in_group_map

    def __init__(self) -> None:
        super().__init__(collection_name=MoneyOwedInGroupMap.__collection_name)
