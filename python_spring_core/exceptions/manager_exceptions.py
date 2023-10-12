"""
    This module contains exceptions raised in the ApplicationContext class
"""

"""
    This exception is raised if an object can't be created in the create_objects() 
    method in the ApplicationContext
"""
class ObjectCreationFailed(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)