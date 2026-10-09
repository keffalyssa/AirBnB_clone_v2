#!/usr/bin/python3
""" Console Module """
import cmd
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ HBNB console """
    prompt = '(hbnb) '
    classes = {
        'BaseModel': BaseModel, 'User': User, 'State': State,
        'City': City, 'Amenity': Amenity, 'Place': Place,
        'Review': Review
    }

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        """Overriding the emptyline method"""
        pass

    def do_EOF(self, line):
        """EOF command to exit the program"""
        print("")
        return True

    def do_create(self, line):
        """Creates a new instance of a class, saves it, and prints the id."""
        args = line.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        kwargs = {}
        for arg in args[1:]:
            if "=" in arg:
                key, value = arg.split("=", 1)
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1].replace('_', ' ')
                    value = value.replace('\\"', '"')
                elif '.' in value:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        pass
                kwargs[key] = value

        try:
            instance = self.classes[class_name](**kwargs)
            instance.save()
            print(instance.id)
        except Exception as e:
            # Mu gihe ForeignKey cyangwa ibindi byanze, nti bikwiriye gusohora crash itariyo
            return

    def do_show(self, line):
        """Prints the string representation of an instance"""
        args = line.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        all_objs = models.storage.all()
        if key in all_objs:
            print(all_objs[key])
        else:
            print("** no instance found **")

    def do_all(self, line):
        """Prints all string representation of all instances"""
        args = line.split()
        obj_list = []
        if len(args) == 0:
            for obj in models.storage.all().values():
                obj_list.append(str(obj))
            print(obj_list)
        elif args[0] in self.classes:
            for key, obj in models.storage.all().items():
                if key.startswith(args[0]):
                    obj_list.append(str(obj))
            print(obj_list)
        else:
            print("** class doesn't exist **")

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id"""
        args = line.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        all_objs = models.storage.all()
        if key in all_objs:
            del all_objs[key]
            models.storage.save()
        else:
            print("** no instance found **")
