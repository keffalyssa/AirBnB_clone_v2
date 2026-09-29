#!/usr/bin/python3
"""Unittests for the HBNBCommand console (FileStorage only)"""
import os
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 "console tests are for FileStorage")
class TestHBNBCommand(unittest.TestCase):
    """Tests for the console commands"""

    def setUp(self):
        """Start each test with empty storage"""
        storage.all().clear()

    def tearDown(self):
        """Remove the file created by the tests"""
        storage.all().clear()
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def run_cmd(self, line):
        """Run a console command and return what it printed"""
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd(line)
        return out.getvalue().strip()

    def test_quit(self):
        """quit stops the console"""
        with self.assertRaises(SystemExit):
            HBNBCommand().onecmd("quit")

    def test_EOF(self):
        """EOF stops the console"""
        with patch('sys.stdout', new=StringIO()):
            with self.assertRaises(SystemExit):
                HBNBCommand().onecmd("EOF")

    def test_emptyline(self):
        """An empty line prints nothing"""
        self.assertEqual(self.run_cmd(""), "")

    def test_create_missing_class(self):
        """create without a class name"""
        self.assertEqual(self.run_cmd("create"), "** class name missing **")

    def test_create_invalid_class(self):
        """create with an unknown class"""
        self.assertEqual(self.run_cmd("create MyModel"),
                         "** class doesn't exist **")

    def test_create_valid(self):
        """create adds a new object to storage"""
        obj_id = self.run_cmd("create BaseModel")
        self.assertTrue(len(obj_id) > 0)
        self.assertIn("BaseModel." + obj_id, storage.all())

    def test_show_missing_class(self):
        """show without a class name"""
        self.assertEqual(self.run_cmd("show"), "** class name missing **")

    def test_show_invalid_class(self):
        """show with an unknown class"""
        self.assertEqual(self.run_cmd("show MyModel"),
                         "** class doesn't exist **")

    def test_show_missing_id(self):
        """show without an id"""
        self.assertEqual(self.run_cmd("show User"),
                         "** instance id missing **")

    def test_show_no_instance(self):
        """show with an id that does not exist"""
        self.assertEqual(self.run_cmd("show User 1234"),
                         "** no instance found **")

    def test_show_valid(self):
        """show prints the object"""
        obj_id = self.run_cmd("create User")
        self.assertIn(obj_id, self.run_cmd("show User " + obj_id))

    def test_destroy_missing_class(self):
        """destroy without a class name"""
        self.assertEqual(self.run_cmd("destroy"), "** class name missing **")

    def test_destroy_invalid_class(self):
        """destroy with an unknown class"""
        self.assertEqual(self.run_cmd("destroy MyModel"),
                         "** class doesn't exist **")

    def test_destroy_missing_id(self):
        """destroy without an id"""
        self.assertEqual(self.run_cmd("destroy User"),
                         "** instance id missing **")

    def test_destroy_no_instance(self):
        """destroy with an id that does not exist"""
        self.assertEqual(self.run_cmd("destroy User 1234"),
                         "** no instance found **")

    def test_destroy_valid(self):
        """destroy removes the object from storage"""
        obj_id = self.run_cmd("create User")
        self.run_cmd("destroy User " + obj_id)
        self.assertNotIn("User." + obj_id, storage.all())

    def test_all_invalid_class(self):
        """all with an unknown class"""
        self.assertEqual(self.run_cmd("all MyModel"),
                         "** class doesn't exist **")

    def test_all_valid(self):
        """all prints the objects of a class"""
        obj_id = self.run_cmd("create State")
        self.assertIn(obj_id, self.run_cmd("all State"))

    def test_update_missing_class(self):
        """update without a class name"""
        self.assertEqual(self.run_cmd("update"), "** class name missing **")

    def test_update_invalid_class(self):
        """update with an unknown class"""
        self.assertEqual(self.run_cmd("update MyModel"),
                         "** class doesn't exist **")

    def test_update_missing_id(self):
        """update without an id"""
        self.assertEqual(self.run_cmd("update User"),
                         "** instance id missing **")

    def test_update_no_instance(self):
        """update with an id that does not exist"""
        self.assertEqual(self.run_cmd("update User 1234"),
                         "** no instance found **")

    def test_update_valid(self):
        """update changes an attribute"""
        obj_id = self.run_cmd("create User")
        self.run_cmd('update User {} first_name "Teta"'.format(obj_id))
        obj = storage.all()["User." + obj_id]
        self.assertEqual(obj.first_name, "Teta")

    def test_create_params_string(self):
        """create sets a string param, underscores become spaces"""
        obj_id = self.run_cmd('create Place name="My_little_house"')
        obj = storage.all()["Place." + obj_id]
        self.assertEqual(obj.name, "My little house")

    def test_create_params_escaped_quote(self):
        """create keeps an escaped double quote inside a string"""
        obj_id = self.run_cmd('create Place name="a\\"b"')
        obj = storage.all()["Place." + obj_id]
        self.assertEqual(obj.name, 'a"b')

    def test_create_params_integer(self):
        """create sets an integer param"""
        obj_id = self.run_cmd("create Place number_rooms=4")
        obj = storage.all()["Place." + obj_id]
        self.assertEqual(obj.number_rooms, 4)
        self.assertIsInstance(obj.number_rooms, int)

    def test_create_params_float(self):
        """create sets a float param"""
        obj_id = self.run_cmd("create Place latitude=37.77")
        obj = storage.all()["Place." + obj_id]
        self.assertEqual(obj.latitude, 37.77)
        self.assertIsInstance(obj.latitude, float)

    def test_create_params_invalid_skipped(self):
        """create skips a param it cannot recognize"""
        obj_id = self.run_cmd(
            'create Place bad=abc name="Home" price_by_night=300')
        obj = storage.all()["Place." + obj_id]
        self.assertFalse(hasattr(obj, "bad"))
        self.assertEqual(obj.name, "Home")
        self.assertEqual(obj.price_by_night, 300)

    def test_create_params_missing_equals(self):
        """create skips a param that has no equal sign"""
        obj_id = self.run_cmd('create Place junk name="Home"')
        obj = storage.all()["Place." + obj_id]
        self.assertFalse(hasattr(obj, "junk"))
        self.assertEqual(obj.name, "Home")


if __name__ == "__main__":
    unittest.main()
