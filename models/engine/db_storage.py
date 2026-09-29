#!/usr/bin/python3
"""This module defines the DBStorage class for hbnb clone"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base


class DBStorage:
    """Manages storage of hbnb models in a MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Creates the engine from the environment variables"""
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(user, pwd, host, db),
            pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def _classes(self):
        """Returns the mapped classes by name"""
        from models.state import State
        from models.city import City
        return {'State': State, 'City': City}

    def all(self, cls=None):
        """Returns a dictionary of objects, optionally filtered by class"""
        classes = self._classes()
        if cls is None:
            to_query = list(classes.values())
        else:
            if isinstance(cls, str):
                cls = classes.get(cls)
            to_query = [cls] if cls in classes.values() else []
        result = {}
        for klass in to_query:
            for obj in self.__session.query(klass).all():
                result[klass.__name__ + '.' + obj.id] = obj
        return result

    def new(self, obj):
        """Adds obj to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables and a new session"""
        self._classes()
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine,
                               expire_on_commit=False)
        self.__session = scoped_session(factory)

    def close(self):
        """Closes the current session"""
        self.__session.remove()
