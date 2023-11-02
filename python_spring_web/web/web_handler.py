"""
    This class will be used to pass data from http requests to the proper method/s and 
    then return the response
"""

from typing import Callable, Type

from python_spring_core.core.manager import manage


@manage
class WebHandler:

    registered_controllers: dict = {}

    mapped_methods: dict = {
        "GET": {},
        "POST": {},
        "PUT": {},
        "PATCH": {},
        "DELETE": {}
    }

    def __init__(self) -> None:
        self.controller_methods: dict = {}

    @classmethod
    def register_controller(cls, controller: Type):
        print("register controller called")
        cls.registered_controllers[controller.__name__] = controller
        return controller

    def add_method(self, method_name: str, method: Callable):
        self.controller_methods[method_name] = method

    def get_methods_from_controllers(self, *args):
        for controller in args:
            for attribute_name in dir(controller):
                if attribute_name.startswith("_"):
                    continue
                method = getattr(controller, attribute_name)
                if callable(method):
                    self.add_method(attribute_name, method)

    
    @classmethod
    def get(cls, func: Callable):
        cls.mapped_methods["GET"][func.__name__] = func
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    @classmethod
    def put(cls, func: Callable):
        cls.mapped_methods["GET"][func.__name__] = func
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    @classmethod
    def post(cls, func: Callable):
        cls.mapped_methods["GET"][func.__name__] = func
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    @classmethod
    def patch(cls, func: Callable):
        cls.mapped_methods["GET"][func.__name__] = func
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    @classmethod
    def delete(cls, func: Callable):
        cls.mapped_methods["GET"][func.__name__] = func
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper