from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

# get current Autodesk Revit project that can interface & interact with settings
# and operations in the UI
uidoc = __revit__.ActiveUIDocument # Autodesk.Revit.UI.UIDocument object

# get current Revit database document from the active UI document / session
doc = __revit__.ActiveUIDocument.Document # Autodesk.Revit.DB.Document object

### Filtering
# Autodesk.Revit.DB.FilteredElementCollector object
# OfCategory applies an ElementCategoryFilter to the collector; takes BuiltInCategory Enum type
# WhereElementIsNotElementType excludes element types and only returns instances
col_rooms = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType()

# [print(room) for room in col_rooms] # Autodesk.Revit.DB.Architecture.Room object

### Access Properties & Parameters
# https://revitapidocs.com/2025

for room in col_rooms:
    if room.LookupParameter('Department').AsString() == 'Circulation':
        print(room.LookupParameter('Name').AsString(), room.Number, room.Level, room.BaseOffset ,room.Area)

# alternative 'Name' property getter: room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
# alternative 'Department' property getter: room.get_Parameter(BuiltInParameter.ROOM_DEPARTMENT).AsString()
# use room.GetParameters('Name') in case there are multiple 'Name' Properties
