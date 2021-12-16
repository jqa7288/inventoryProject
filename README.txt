----------inventoryApp(WT)----------
J Quick - 12-13-21

This is an app designed to practice GUI, database, and data analysis in python by creating a basic inventory tracking application connected to a MongoDB database, using PyQT5 for the GUI.

---VERSION NOTES---
v0.1 - 12/13/21 - J Quick
Item creation and editing is functioning, but creation is missing a success alert so it will create the part in the database but not indicate that anything happened, added that to the TODO. Basic GUI is set up, with some placeholder menu options for screens that have not been completed yet. Initial commit on the project has everything mentioned so far.

v0.2 - 12/15/21 - J Quick
Added placeholders for all functions up to this point and completed those already started. Listwindow completed, main menu refactored, replaced QList with QTable for view functions.

v0.3 - 12/16/21 - J Quick
Working version of createLocationWindow is completed and basic testing passed.


---TODO---

- Add view locations, view items windows
- Add edit window for locations
- Add click on item to go to detail/edit window
- Add issue/recieve functions
- Add analysis/reporting/printing? functions