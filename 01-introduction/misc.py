import ifcopenshell
import ifcopenshell.util.element
import os

from enum import Enum


class IfcElementTypeEnum(Enum):
    BEAM = 'IfcBeamType'
    SLAB = 'IfcSlabType'
    WALL = 'IfcWallType'
    WINDOW = 'IfcWindowType'


class IfcElementEnum(Enum):
    BEAM = 'IfcBeam'
    SLAB = 'IfcSlab'
    WALL = 'IfcWall'
    WINDOW = 'IfcWindow'


# cd into this directory before running the main.py file
current_wd = os.getcwd()
# Download IFC model from https://docs.ifcopenshell.org/ifcopenshell-python/hello_world.html
IFC_FILE_NAME = 'AC20-FZK-Haus.ifc'
IFC_FILE_PATH = os.path.join(current_wd, IFC_FILE_NAME)

print(current_wd)
print(IFC_FILE_PATH)

model = ifcopenshell.open(IFC_FILE_PATH)
print(model.schema) # IFC4


def iterate_through_all_entities(ifc_model) -> None:
    """IFC file opened through IfcOpenShell is iterable"""
    for inst in ifc_model:
        if inst.is_a("IfcWindow"):
            # Prints out entire entity as it appears in IFC file
            print("The STEP entity is:", inst)
            # Prints attributes dict  e.g. name, type, id, description
            print("INFO:", inst.get_info())
            # Get instance type e.g. IfcWallStandardCase
            print("INSTANCE TYPE:", inst.is_a())
            # Get instance name. Ensure the instance has attribute Name first
            # For more information check submodule: ifcopenshell.entity_instance
            if hasattr(inst, "Name"):
                print(inst.Name)
            break # delete this line to iterate through all instances


def print_all_entity_types(ifc_model) -> None:
    """Get all entity types used in the model"""
    types = set(entity.is_a() for entity in ifc_model)

    for t in sorted(types):
        print(t)


def print_all_types_of_category(ifc_model, element_type: str) -> None:
    """
    Print details about every element type of a particular category
    
    Parameters:
    - ifc_model: An IfcOpenShell model object.
    - element_type: The IFC class name to filter by ('IfcWallType', 'IfcDoorType').
    """
    for el in ifc_model.by_type(element_type):
        print("The {} element is: {}".format(element_type, el))
        print("The name of the {} is: {}".format(element_type, el.Name))


def print_all_instances_of_type(ifc_model, element_type) -> None:
    """Get and print all occurrences of a type"""
    for el_type in ifc_model.by_type(element_type):
        print("{} is: {}".format(element_type, el_type.Name))
        elements = ifcopenshell.util.element.get_types(el_type)
        print("There are {} of this type".format(len(elements)))
        for el in elements:
            print("The name is", el.Name)


def print_type_of_element(ifc_model, instance_description: str) -> None:
    """Get and print the type of an element"""
    instance = ifc_model.by_type(instance_description)[0]
    instance_type = ifcopenshell.util.element.get_type(instance)
    print("The type of {} is {}".format(
        instance.Name, instance_type.Name))


def print_properties_of_element(ifc_model, instance_description: str) -> None:
    """Get and print the properties & quantities of an entity type"""
    element = model.by_type(instance_description)[0]
    element_type = ifcopenshell.util.element.get_type(element)
    import pdb; pdb.set_trace()
    # Get all properties and quantities as a dictionary
    psets = ifcopenshell.util.element.get_psets(element_type)
    print(psets)

    # Get all properties and quantities of the wall, including inherited type properties
    psets_plus_inherited = ifcopenshell.util.element.get_psets(element)
    print(psets_plus_inherited)

    # Get only properties and not quantities
    print(ifcopenshell.util.element.get_psets(element, psets_only=True))

    # Get only quantities and not properties
    print(ifcopenshell.util.element.get_psets(element, qtos_only=True))


def find_spatial_container_of_element(ifc_model, instance_description: str) -> None:
    """
    Find the spatial container of an element
    Walls are typically located on a storey i.e. Level 1
    Equipment might be located in spaces, etc
    """
    element = model.by_type(instance_description)[0]
    container = ifcopenshell.util.element.get_container(element)
    print("The element {} is located on {}".format(element.Name, container.Name))


if __name__ == '__main__':
    # iterate_through_all_entities(ifc_model=model)
    # print_all_entity_types(ifc_model=model)
    # print_all_types_of_category(
    #     ifc_model=model, element_type=IfcElementTypeEnum.WINDOW.value)
    # print_all_instances_of_type(
    #     ifc_model=model, element_type=IfcElementTypeEnum.WINDOW.value)
    # print_type_of_element(
    #     ifc_model=model, instance_description=IfcElementEnum.SLAB.value)
    # print_properties_of_element(
    #     ifc_model=model, instance_description=IfcElementEnum.WALL.value)
    find_spatial_container_of_element(
        ifc_model=model, instance_description=IfcElementEnum.WALL.value)
