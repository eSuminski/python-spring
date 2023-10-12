"""
    let's see if we can make a python version of the application context
"""
import os
import platform
import importlib
import inspect
import sys
from typing import Type

from python_spring_core.exceptions.manager_exceptions import ObjectCreationFailed

"""
    we will use this method to decorate any classes the Application Context needs to 
    manage. Because class decorator methods execute when the class is defined we can
    instantiate our managed objects and add them to the managed_classes dictionary
    when they get initially defined

    For this to work, an init method needs to have a type annotation on any dependencies,
    and the parameters need to have a default value of None. See the following example:

    def __init__(self, dao:DaoClass=None) -> None:
        # code
"""
def manage(cls: Type):
    if (cls.__name__, cls) not in ApplicationContext.managed_classes:
        ApplicationContext.managed_classes.add((cls.__name__, cls))
    return cls

class ApplicationContext:

    # holds modules with managed resources
    modules: set = set()

    # holds all class names and data that need to be managed
    managed_classes: set = set()

    # holds the actual objects and references to them
    managed_objects: dict = dict()

    @classmethod
    def start(cls):
        cls.find_modules_in_project()
        cls.find_classes_to_manage()
        cls.create_objects()
        cls.assign_dependencies()


    """
        step 1: find the modules with classes to be managed in them

        The easiest way to do this for now is to check for modules that start with the 
        phrase "managed_". This is to avoid searching through all modules in the 
        application, since your managed modules are going to be in the code you wrote, 
        not your virtual environments or other Python path locations
    """
    @classmethod
    def find_modules_in_project(cls):
        searched_dirs = set()
        path: str
        for path in sys.path: 
            if platform.python_version() not in path:              
                # Traverse the directory tree starting from the current path reference
                root: str
                dirs: list[str]
                files: list[str]
                for root, dirs, files in os.walk(path):
                    # Remove subdirectories that have already been searched
                    # the slice syntax on dirs lets us create a copy of the original dirs
                    # that we can make changes to that are reflected in the loop
                    dirs[:] = [d for d in dirs if os.path.join(root, d) not in searched_dirs]
                    # Iterate over all files in the current directory
                    for file in files:
                        # Check if the file is a Python file and starts with managed_
                        if file.endswith('.py') and file.startswith("managed_"):
                            # Extract the module name from the file name
                            module_name = os.path.splitext(file)[0]
                            # Get the relative path to the module
                            rel_path = os.path.relpath(os.path.join(root, file), path)
                            # Add the module name and path to the list of modules
                            cls.modules.add((module_name, rel_path))
                    # update the searched directory set before moving to the next loop iteration
                    searched_dirs.add(root)
    
    """
        Step 2: grab the class data that needs to be managed

        If the module starts with "managed_" we will assume one or more classes
        in the module need to be managed, so we will import the modules and let
        the manage() function add the appropriate classes to the managed classes
        set in the ApplicationContext.
    """
    @classmethod
    def find_classes_to_manage(cls):
        # Declare variables to hold module name and path
        module_name : str
        path: str
        # Iterate over the modules in cls.modules
        for module_name, path in cls.modules:
            # Replace backslashes with dots in the path
            path = path.replace("\\", ".")
            # Replace ".py" with an empty string in the fully qualified module name
            module_name = path[:-3]
            # Import the module using importlib.import_module()
            importlib.import_module(module_name, path)
    
    """
        Step 3: create objects of all managed classes. They should start with all fields
        set to None by default
    """
    @classmethod
    def create_objects(cls):
        class_name: str
        class_data: Type
        for class_name, class_data in cls.managed_classes:
            try:
                cls.managed_objects[class_name] = class_data()
            except TypeError as e:
                raise ObjectCreationFailed(f"There was a problem initializing {e.__cause__.__class__.__name__}: did you set the default value of your dependencies to \"None\"?")


    """
        Step 4: assign objects to their propper fields
    """
    @classmethod
    def assign_dependencies(cls):
        obj: Type
        for obj in cls.managed_objects.values():
            param: inspect.Parameter
            for param in inspect.signature(obj.__init__).parameters.values():
                    key: str
                    for key in cls.managed_objects.keys():
                        if key in str(param.annotation):
                            setattr(obj,param.name,cls.managed_objects[key])