from pymongo import MongoClient
from threading import Lock
from typing import final, Optional


@final
class MongoDbClientConnection:

    """
    MongoDb Client Connection Class is a Singleton class,
    responsible for maintaining the Client connection from a single instance of
    the WSGI/ASGI web backend application to the MongoDB server instance.
    This client connection instance maintains a pool of connections underneath this.
    """

    __client_connection: Optional['MongoDbClientConnection'] = None
    __client_connection_parameters_initialized: bool = False
    __client_connection_creation_lock: Lock = Lock()

    def __new__(cls, *args, **kwargs) -> 'MongoDbClientConnection':

        if cls.__client_connection is None:

            cls.__client_connection_creation_lock.acquire(blocking=True, timeout=-1)
            if cls.__client_connection is not None:
                cls.__client_connection = super().__new__(cls=cls)
                cls.__client_connection.server_host_url = None
                cls.__client_connection.server_host_port = None
                cls.__client_connection.connection = None
            cls.__client_connection_creation_lock.release()

        return cls.__client_connection

    def __init__(self, mongo_db_server_host_url: Optional[str] = None, mongo_db_server_host_port: Optional[int] = None) -> None:
        if MongoDbClientConnection.__client_connection_parameters_initialized:
            if mongo_db_server_host_url != self.__client_connection.server_host_url or mongo_db_server_host_url != self.__client_connection.server_host_port:
                raise Exception(f'MongoDB Client Connection is already initiated with the parameters: '
                                f'Host({self.__client_connection.server_host_url})'
                                f'Port{self.__client_connection.server_host_port}')
            self.__client_connection.server_host_url = mongo_db_server_host_url
            self.__client_connection.server_host_port = mongo_db_server_host_port
            self.__client_connection.connection = MongoClient(host=mongo_db_server_host_url, port=mongo_db_server_host_port)
            MongoDbClientConnection.__client_connection_parameters_initialized = True

    def __repr__(self) -> str:
        host: Optional[str] = self.__client_connection.server_host_url
        port: Optional[int] = self.__client_connection.server_host_port
        return f'MongoDbClientConnection(host={host} port={port})'
