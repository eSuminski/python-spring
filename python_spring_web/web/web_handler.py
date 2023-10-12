"""
    This class will be used to pass data from http requests to the proper method/s and 
    then return the response
"""

from typing import Callable


class WebHandler:
    
    @classmethod
    def get(cls, func: Callable):
        pass

    @classmethod
    def put(cls, func: Callable):
        pass

    @classmethod
    def post(cls, func: Callable):
        pass

    @classmethod
    def patch(cls, func: Callable):
        pass

    @classmethod
    def delete(cls, func: Callable):
        pass