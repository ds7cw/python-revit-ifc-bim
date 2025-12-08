import ifcopenshell
import ifcopenshell.util.selector
import os

from enum import Enum

# cd into this directory before running the main.py file
current_wd = os.getcwd()
# Download IFC model from https://docs.ifcopenshell.org/ifcopenshell-python/hello_world.html
IFC_FILE_NAME = 'AC20-FZK-Haus.ifc'
IFC_FILE_PATH = os.path.join(current_wd, IFC_FILE_NAME)

model = ifcopenshell.open(IFC_FILE_PATH)


class IfcElementEnum(Enum):
    DOOR = 'IfcDoor'
    SLAB = 'IfcSlab'
    WALL = 'IfcWall'
    WINDOW = 'IfcWindow'


def print_concrete_elements_of_categories(ifc_file, *categories, material) -> None:
    """The material filter checks any assigned IfcMaterial with a matching name"""
    query = ', '.join(categories) + ', material={}'.format(material)
    asd = ifcopenshell.util.selector.filter_elements(ifc_file=ifc_file, query=query)
    [print(el) for el in asd]


def print_name_attribute_of_entity(ifc_file, entity_type):
    """Get the Name attribute of the entity's type"""
    wall = ifc_file.by_type(entity_type)[0]
    name_attr = ifcopenshell.util.selector.get_element_value(wall, 'type.Name')
    print('Name attribute: {}'.format(name_attr))


if __name__ == '__main__':
    print_concrete_elements_of_categories(
        model, IfcElementEnum.DOOR.value, IfcElementEnum.WINDOW.value, material='Holz')
    print_name_attribute_of_entity(model, IfcElementEnum.SLAB.value)
