from typing import Type
from python_spring_core.core.manager import manage


@manage
class RouteMapper:

    mappings = {
        "GET":{},
        "POST":{},
        "PUT":{},
        "DELETE":{},
        "PATCH":{},
        "HEAD":{}
    }

    @classmethod
    def controller(cls, controller: Type):
        setattr(controller, "__is_controller__", True)
        return controller
    
    @classmethod
    def get(cls, route: str = "/"):
        def decorator(func):
            setattr(func, '__route__', route)
            setattr(func, '__verb__', 'GET')
            return func
        return decorator

    @classmethod
    def post(cls, route: str = "/"):
        def decorator(func):
            setattr(func, '__route__', route)
            setattr(func, '__verb__', 'POST')
            return func
        return decorator
    
    @classmethod
    def put(cls, route: str = "/"):
        def decorator(func):
            setattr(func, '__route__', route)
            setattr(func, '__verb__', 'PUT')
            return func
        return decorator

    @classmethod
    def delete(cls, route: str = "/"):
        def decorator(func):
            setattr(func, '__route__', route)
            setattr(func, '__verb__', 'DELETE')
            return func
        return decorator

    @classmethod
    def head(cls, route: str = "/"):
        def decorator(func):
            setattr(func, '__route__', route)
            setattr(func, '__verb__', 'HEAD')
            return func
        return decorator
