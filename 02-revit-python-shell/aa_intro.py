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

### Task Dialogs & Units Conversion
total_area_sqf = 0

for room in col_rooms:
    total_area_sqf += room.Area

print(total_area_sqf)

total_area_sqm = UnitUtils.ConvertFromInternalUnits(total_area_sqf, UnitTypeId.SquareMeters)

# TaskDialog Class; a dialog box that can be used to display information and receive input from the user
message = TaskDialog
text = "Total area of all rooms in the building:\n {} sqm\n {} sqf".format(
    round(total_area_sqm, 1), round(total_area_sqf, 1))
message.Show("Total Area Calculation", text)

### Element Selection
# Autodesk.Revit.UI.Selection.Selection object
selection = uidoc.Selection # assumes the user has already selected elements in the Revit session
elements = []
for el_id in selection.GetElementIds():
    elements.append(doc.GetElement(el_id))

for el in elements:
    if el.Category.Name == 'Walls':
        print(el.IsStackedWall)

active_view = uidoc.ActiveView
col_selection = FilteredElementCollector(doc, active_view.Id). \
    OfCategory(BuiltInCategory.OST_RoomTags).WhereElementIsNotElementType().ToElementIds()

# SetElementIds selects the elements
user_selection = uidoc.Selection.SetElementIds(col_selection) # elements in Revit will be selected

### Transactions - context-like objects that guard any changes made to a Revit model
t = Transaction(doc)
t.Start('Apply Level code to room parameter') # this string is for information

# Assume there is a user defined Revit parameter 'MT_RoomLevel'
# Assume Room Level parameter follows the convention 'Level 00'
for room in col_rooms:
    # The below needs to be put inside of a transaction, otherwise an exception will be thrown
    room.LookupParameter('MT_RoomLevel').Set(room.Level.Name[6:])

t.Commit()

### pyRevit
# Create a user input list
from pyrevit.forms import SelectFormList

items = ['item1', 'item2', 'item3']
SelectFormList.show(items, button_name='Select Item')

### Deleting Elements
# Autodesk.Revit.DB.ViewSheet object
col_sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets). \
    WhereElementIsNotElementType().ToElements() 

t = Transaction(doc)
t.Start('Delete Sheets')

for sheet in col_sheets:
    if sheet.SheetNumber != 'XX':
        for view in sheet.GetAllPlacedViews():
            doc.Delete(view) # ONLY if you want to delete the associated views!!!
        doc.Delete(sheet.Id)

t.Commit()
