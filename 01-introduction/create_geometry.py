import ifcopenshell
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
    WALL = 'IfcWall'
    WINDOW = 'IfcWindow'


def set_project_units(ifc_file, unit_type: str, prefix: str) -> None:
    """
    All coordinates in IFC are stored using project units.
    This means that prior to creating Object Placements or 
    Representations you have to define a project length unit as a minimum.
    """
    import ifcopenshell.api.root
    import ifcopenshell.api.unit
    # You need a project before you can assign units.
    ifcopenshell.api.root.create_entity(ifc_file, ifc_class="IfcProject")

    length = ifcopenshell.api.unit.add_si_unit(ifc_file, unit_type=unit_type, prefix=prefix)
    ifcopenshell.api.unit.assign_unit(ifc_file, units=[length])

    # Alternatively, you may specify without any arguments to automatically
    # create millimeters, square meters, and cubic meters as a convenience for
    # ifcopenshell.api.unit.assign_unit(ifc_file)


def set_obj_placement(ifc_file, ifc_entity) -> None:
    """The recommended way to set an Object Placement is to specify the placement as a 4x4 matrix"""
    import numpy
    import ifcopenshell.api.root
    import ifcopenshell.api.geometry

    wall = ifcopenshell.api.root.create_entity(ifc_file, ifc_class=ifc_entity)

    # Create a 4x4 identity matrix. This matrix is at the origin with no rotation.
    matrix = numpy.eye(4)

    # Rotate the matix 90 degrees anti-clockwise around the Z axis (i.e. in plan).
    # Anti-clockwise is positive. Clockwise is negative.
    matrix = ifcopenshell.util.placement.rotation(90, "Z") @ matrix

    # Set the X, Y, Z coordinates. Notice how we rotate first then translate.
    # This is because the rotation origin is always at 0, 0, 0.
    matrix[:,3][0:3] = (2, 3, 5)

    # Set our wall's Object Placement using our matrix.
    # `is_si=True` states that we are using SI units instead of project units.
    ifcopenshell.api.geometry.edit_object_placement(ifc_file, product=wall, matrix=matrix, is_si=True)


def representation_context_example(ifc_model) -> None:
    """
    As an object may have multiple Representations, we need to use
    Representation Contexts to distinguish the purpose and intended context of each Representation.
    """
    import ifcopenshell.api.context
    # If we plan to store 3D geometry in our IFC model, we have to setup a "Model" context.
    model3d = ifcopenshell.api.context.add_context(ifc_model, context_type="Model")

    # And/Or, if we plan to store 2D geometry, we need a "Plan" context
    plan = ifcopenshell.api.context.add_context(ifc_model, context_type="Plan")

    # Set up the subcontexts with each of the geometric "purposes" we plan to store in our model.
    # "Body" is by far the most important and common context, as most IFC models are assumed to be viewable in 3D.
    body = ifcopenshell.api.context.add_context(ifc_model,
        context_type="Model", context_identifier="Body", target_view="MODEL_VIEW", parent=model3d)

    # The 3D Axis subcontext is important if any "axis-based" parametric geometry is going to be created.
    # A beam, or column may be drawn using a single 3D axis line, and for this we need an Axis subcontext.
    ifcopenshell.api.context.add_context(ifc_model,
        context_type="Model", context_identifier="Axis", target_view="GRAPH_VIEW", parent=model3d)

    # It's also important to have a 2D Axis subcontext for things like walls and claddings
    # which can be drawn using a 2D axis line.
    ifcopenshell.api.context.add_context(ifc_model,
        context_type="Plan", context_identifier="Axis", target_view="GRAPH_VIEW", parent=plan)

    # The 3D Box subcontext is useful for clash detection or shape analysis, or even lazy-loading of large models.
    ifcopenshell.api.context.add_context(ifc_model,
        context_type="Model", context_identifier="Box", target_view="MODEL_VIEW", parent=model3d)

    # A 2D annotation subcontext for plan views are important for door swings, window cuts, and symbols 
    # for equipment like GPOs, fire extinguishers, and so on.
    ifcopenshell.api.context.add_context(ifc_model,
        context_type="Plan", context_identifier="Annotation", target_view="PLAN_VIEW", parent=plan)

    # You may also create 2D annotation subcontexts for sections and elevation views.
    ifcopenshell.api.context.add_context(ifc_model,
        context_type="Plan", context_identifier="Annotation", target_view="SECTION_VIEW", parent=plan)
    ifcopenshell.api.context.add_context(ifc_model,
        context_type="Plan", context_identifier="Annotation", target_view="ELEVATION_VIEW", parent=plan)


if __name__ == '__main__':
    set_project_units(ifc_file=model, unit_type='LENGTHUNIT', prefix='MILLI')
