import ifcopenshell
import os

# cd into this directory before running the main.py file
current_wd = os.getcwd()
# Download IFC model from https://docs.ifcopenshell.org/ifcopenshell-python/hello_world.html
IFC_FILE_NAME = 'AC20-FZK-Haus.ifc'
IFC_FILE_PATH = os.path.join(current_wd, IFC_FILE_NAME)

print(current_wd)
print(IFC_FILE_PATH)

if os.path.isfile(IFC_FILE_PATH):
    model = ifcopenshell.open(IFC_FILE_PATH)
    print(model.schema) # IFC4

walls = model.by_type('IfcWall')
print(len(walls)) # 13

for wall in walls:
    print(wall)
    #15042=IfcWallStandardCase(
    # '2XPyKWY018sA1ygZKgQPtU',#12,'Wand-Int-ERDG-4',$,$,#14983,#15037,'BC6F0F70-6195-495E-A2-FC-239713029DB1',$)

# model.by_type('IfcWall')[0].is_a()
# 'IfcWallStandardCase'

# model.by_type('IfcWall')[0].Name
# 'Wand-Int-ERDG-4'

# print(dir(model))
# print(dir(model.by_type('IfcWall')[0]))

wall_type_attributes = [
    'ConnectedFrom', 'ConnectedTo', 'ContainedInStructure', 'Declares', 'Decomposes', 'Description',
    'FillsVoids', 'GlobalId', 'HasAssignments', 'HasAssociations', 'HasContext', 'HasCoverings',
    'HasOpenings', 'HasProjections', 'InterferesElements', 'IsConnectionRealization', 'IsDeclaredBy',
    'IsDecomposedBy', 'IsDefinedBy', 'IsInterferedByElements', 'IsNestedBy', 'IsTypedBy', 'Name',
    'Nests', 'ObjectPlacement', 'ObjectType', 'OwnerHistory', 'PredefinedType', 'ProvidesBoundaries',
    'ReferencedBy', 'ReferencedInStructures', 'Representation', 'Tag', '__annotations__', '__class__',
    '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
    '__getattr__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__',
    '__init__', '__init_subclass__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__',
    '__reduce__', '__reduce_ex__', '__repr__', '__rge__', '__rgt__', '__rle__', '__rlt__',
    '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__',
    'attribute_name', 'attribute_type', 'compare', 'file', 'get_info', 'get_info_2', 'id', 'is_a',
    'is_entity', 'method_list', 'to_string', 'unwrap_value', 'walk', 'wrap_value'
]

wall = model.by_type('IfcWall')[0]
print("Wall is a IFC Wall: {}".format(wall.is_a('IfcWall'))) # True
print("Wall is a IFC Element: {}".format(wall.is_a('IfcElement'))) # True
print("Wall is a IFC Window: {}".format(wall.is_a('IfcWindow'))) # False
print("Wall id: {}".format(wall.id()))
print("Wall Name: {}".format(wall.Name))
print(wall.get_info()) # get all attributes

# Get all properties & quantities of an object
# import ifcopenshell.util
# import ifcopenshell.util.element
# print(ifcopenshell.util.element.get_psets(wall))

# Display elements related to a particular object
print(wall.IsDefinedBy)
print(model.get_inverse(wall))

# Modify data and save model as new IFC file
# wall.Name = 'New-Wall-Name'
# model.write(os.path.join(current_wd, 'New-Ifc-Model.ifc'))

# Create new IFC model from scratch
# new_ifc_model = ifcopenshell.file() # optional argument schema='IFC4'

# Create new element (blank attributes) inside of a model
# new_wall = model.createIfcWall() # option 1
# new_wall = model.create_entity('IfcWall') # option 2
