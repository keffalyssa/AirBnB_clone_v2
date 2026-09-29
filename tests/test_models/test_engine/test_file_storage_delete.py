#!/usr/bin/python3
"""Unittests for FileStorage.delete and FileStorage.all(cls)"""
import os
import unittest
from models.engine.file_storage import FileStorage
from models.state import State
from models.city import City


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 "FileStorage tests only run with file storage")
class TestFileStorageDelete(unittest.TestCase):
    """Tests for delete and the optional class filter of all"""

    def setUp(self):
        """Start each test with empty storage"""
        self.fs = FileStorage()
        self.fs.all().clear()

    def tearDown(self):
        """Clean storage and remove the JSON file"""
        self.fs.all().clear()
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_all_no_class(self):
        """all() without a class returns every object"""
        self.fs.new(State())
        self.fs.new(City())
        self.assertEqual(len(self.fs.all()), 2)

    def test_all_with_class(self):
        """all(cls) returns only objects of that class"""
        self.fs.new(State())
        self.fs.new(City())
        result = self.fs.all(State)
        self.assertEqual(len(result), 1)
        for obj in result.values():
            self.assertIsInstance(obj, State)

    def test_all_with_class_name(self):
        """all(cls) also accepts the class name as a string"""
        self.fs.new(State())
        self.fs.new(City())
        self.assertEqual(len(self.fs.all("City")), 1)

    def test_delete_object(self):
        """delete removes the object from storage"""
        state = State()
        self.fs.new(state)
        self.fs.delete(state)
        self.assertNotIn("State." + state.id, self.fs.all())

    def test_delete_keeps_others(self):
        """delete removes only the given object"""
        a = State()
        b = State()
        self.fs.new(a)
        self.fs.new(b)
        self.fs.delete(a)
        self.assertNotIn("State." + a.id, self.fs.all())
        self.assertIn("State." + b.id, self.fs.all())

    def test_delete_none(self):
        """delete(None) does nothing"""
        self.fs.new(State())
        self.fs.delete(None)
        self.assertEqual(len(self.fs.all()), 1)

    def test_delete_missing_object(self):
        """delete of an object not in storage does not fail"""
        self.fs.delete(State())
        self.assertEqual(len(self.fs.all()), 0)


if __name__ == "__main__":
    unittest.main()
