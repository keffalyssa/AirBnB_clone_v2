#!/usr/bin/python3
"""Unittests for the DBStorage class"""
import os
import unittest


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 "DBStorage tests only run with db storage")
class TestDBStorage(unittest.TestCase):
    """Tests for DBStorage"""

    def test_has_all(self):
        """DBStorage has an all method"""
        from models.engine.db_storage import DBStorage
        self.assertTrue(hasattr(DBStorage, "all"))

    def test_has_new(self):
        """DBStorage has a new method"""
        from models.engine.db_storage import DBStorage
        self.assertTrue(hasattr(DBStorage, "new"))

    def test_has_save(self):
        """DBStorage has a save method"""
        from models.engine.db_storage import DBStorage
        self.assertTrue(hasattr(DBStorage, "save"))

    def test_has_delete(self):
        """DBStorage has a delete method"""
        from models.engine.db_storage import DBStorage
        self.assertTrue(hasattr(DBStorage, "delete"))

    def test_has_reload(self):
        """DBStorage has a reload method"""
        from models.engine.db_storage import DBStorage
        self.assertTrue(hasattr(DBStorage, "reload"))


if __name__ == "__main__":
    unittest.main()
