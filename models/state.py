#!/usr/bin/python3
"""This is the state class"""
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """This is the class for State"""
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', backref='state',
                              cascade='all, delete, delete-orphan')
    else:
        @property
        def cities(self):
            """Getter attribute that returns the list of City instances"""
            from models import storage
            city_list = []
            for city in storage.all("City").values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
