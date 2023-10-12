import pytest
from python_spring_core.core.manager import ApplicationContext, manage
from python_spring_core.exceptions.manager_exceptions import ObjectCreationFailed
from python_spring_core.tests.data_for_tests.test_data import Dependency, MissingNoneDefault, Reciever

"""
    MANAGE FUNCTION TESTS BELOW
"""
def test_manage_positive():
    ApplicationContext.managed_classes = set()
    manage(Dependency)
    assert (Dependency.__name__, Dependency) in ApplicationContext.managed_classes

"""
    FIND_MODULES_IN_PROJECT METHOD TESTS BELOW
"""

def test_find_modules_in_project_positive():
    ApplicationContext.modules = set()
    ApplicationContext.find_modules_in_project()
    assert len(ApplicationContext.modules) == 1 #currently 3, will need to change if source code changes

"""
    FIND_CLASSES_TO_MANAGE METHOD TESTS BELOW
"""

def test_find_classes_to_manage_positive():
    ApplicationContext.modules = set()
    ApplicationContext.managed_classes = set()
    ApplicationContext.modules.add(("managed_module","python_spring_core\\tests\\classes_for_tests\\managed_module.py"))
    ApplicationContext.find_classes_to_manage()
    assert len(ApplicationContext.managed_classes) == 1

"""
    CREATE_OBJECTS METHOD TESTS BELOW
"""

def test_create_objects_positive():
    ApplicationContext.managed_classes = {("Dependency", Dependency), ("Reciever", Reciever)}
    ApplicationContext.create_objects()
    assert len(ApplicationContext.managed_objects) == 2

def test_create_objects_negative_rasies_ObjectCreationFailed():
    with pytest.raises(ObjectCreationFailed):
        ApplicationContext.managed_classes = {("Dependency", Dependency), ("Reciever", Reciever), ("MissingNoneDefault", MissingNoneDefault)}
        ApplicationContext.create_objects()

"""
    ASSIGN_DEPENDENCIES METHOD TESTS BELOW
"""

def test_assign_dependencies_positive():
    ApplicationContext.managed_objects = {
        "Dependency":Dependency(),
        "Reciever":Reciever()
    }
    ApplicationContext.assign_dependencies()
    assert type(ApplicationContext.managed_objects["Reciever"].dependency) == Dependency