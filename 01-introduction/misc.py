import ifcopenshell
import os

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


if __name__ == '__main__':
    iterate_through_all_entities(ifc_model=model)
    print_all_entity_types(ifc_model=model)
