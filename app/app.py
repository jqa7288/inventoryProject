#inventoryApp
#j quick 12/13/2021 v0.1
#main app gui

import sys
import modules.dbTools as db

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle('inventoryApp v0.1')
        self.setGeometry(500,250,500,500)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("File")
        
        quitAct = QAction("Quit", self)
        quitAct.triggered.connect(qApp.quit)

        fileMenu.addAction(quitAct)

        actions = self.menuBar().addMenu("Actions")

        createItemAct = QAction("Create Item", self)
        createItemAct.triggered.connect(self.showCreateScreen)

        editItemAct = QAction("Edit Item", self)
        editItemAct.triggered.connect(self.showEditScreen)

        actions.addAction(createItemAct)
        actions.addAction(editItemAct)
        actions.addAction("Issue / Receive Items")
        actions.addAction("Edit Locations")

        status = self.statusBar()
        self.statusContent = QLabel("System Ready")
        status.addWidget(self.statusContent)

        central = appWindow()
        self.setCentralWidget(central)

    def showCreateScreen(self):
        window = createItemWindow()
        self.setCentralWidget(window)

    def showEditScreen(self):
        window = editItemWindow()
        self.setCentralWidget(window)

class appWindow(QWidget):
    def __init__(self):
        super().__init__()
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)
        searchBar = QLineEdit()
        searchButton = QPushButton("Search")



        dispList = QListWidget()
        for x in range(10):
            dispList.addItem(f"Item {x}\n--Description for Item {x}--\n")
        
        button2=QPushButton('Button 2')
        button3=QPushButton('Button 3')
        grid_layout.addWidget(searchBar, 0, 0, 1, 4)
        grid_layout.addWidget(searchButton, 0, 5, 1, 1)
        grid_layout.addWidget(dispList, 1, 0, 5, 6)
        grid_layout.addWidget(button2, 7, 0, 1, 3)
        grid_layout.addWidget(button3, 7, 4, 1, 2)

class createItemWindow(QWidget):
    def __init__(self):
        super().__init__()
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        self.partNum = QLineEdit()
        self.description = QLineEdit()
        self.expiration = QLineEdit()

        self.unit = QComboBox()
        self.unit.addItem("EA")
        self.unit.addItem("GAL")
        self.unit.addItem("oz")
        self.unit.addItem("SI")
        self.unit.addItem("SF")
        self.unit.addItem("Lbs")
        self.unit.addItem("CF")

        self.createButton = QPushButton("Create Item")
        self.createButton.clicked.connect(self.createItem)
        
        grid_layout.addWidget(QLabel("Part Number: "), 0, 0, 1, 2)
        grid_layout.addWidget(self.partNum, 0, 2, 1, 4)
        
        grid_layout.addWidget(QLabel("Description: "), 1, 0, 1, 2)
        grid_layout.addWidget(self.description, 1, 2, 1, 4)

        grid_layout.addWidget(QLabel("Expiration: "), 2, 0, 1, 2)
        grid_layout.addWidget(self.expiration, 2, 2, 1, 4)

        grid_layout.addWidget(QLabel("Unit of Measure: "), 3, 0, 1, 2)
        grid_layout.addWidget(self.unit, 3, 2, 1, 4)
       
        grid_layout.addWidget(self.createButton, 4, 2, 1, 3)
        
        
    def createItem(self):
        item = db.item(self.partNum.text(), self.description.text(), self.expiration.text(), self.unit.currentText())
        res = item.pushItemRecord(db.items)


class editItemWindow(QWidget):
    def __init__(self):
        super().__init__()
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        self.searchBar = QLineEdit()
        self.searchButton = QPushButton("Search")
        self.searchButton.clicked.connect(self.getPart)

        self.partNum = QLineEdit()
        self.description = QLineEdit()
        self.expiration = QLineEdit()

        self.unit = QComboBox()
        self.unit.addItem("EA")
        self.unit.addItem("GAL")
        self.unit.addItem("oz")
        self.unit.addItem("SI")
        self.unit.addItem("SF")
        self.unit.addItem("Lbs")
        self.unit.addItem("CF")

        self.editButton = QPushButton("Save Changes")
        self.editButton.clicked.connect(self.updateItem)
        
        grid_layout.addWidget(self.searchBar, 0, 0, 1, 4)
        grid_layout.addWidget(self.searchButton, 0, 4, 1, 2)

        grid_layout.addWidget(QLabel("Part Number: "), 1, 0, 1, 2)
        grid_layout.addWidget(self.partNum, 1, 2, 1, 4)
        
        grid_layout.addWidget(QLabel("Description: "), 2, 0, 1, 2)
        grid_layout.addWidget(self.description, 2, 2, 1, 4)

        grid_layout.addWidget(QLabel("Expiration: "), 3, 0, 1, 2)
        grid_layout.addWidget(self.expiration, 3, 2, 1, 4)

        grid_layout.addWidget(QLabel("Unit of Measure: "), 4, 0, 1, 2)
        grid_layout.addWidget(self.unit, 4, 2, 1, 4)
       
        grid_layout.addWidget(self.editButton, 5, 2, 1, 3)
        
        
    def updateItem(self):
        if self.searchBar.text() == "":
            blkalert = QMessageBox.question(self, 'Error', "Please search for part with search bar before making changes.", QMessageBox.Ok)
        else:
            msgReply = QMessageBox.question(self, 'Continue?', "Commit changes to part number?", QMessageBox.Yes | QMessageBox.No)
            if msgReply == QMessageBox.Yes:
                query = {'partNumber': self.searchBar.text()}
                newValues = {"$set":{"partNumber": self.partNum.text(),"description": self.description.text(),"expiration": self.expiration.text(),"unit": self.unit.currentText()}}
                res = db.items.update_one(query, newValues)
                print(f"Docs updated = {res.matched_count}")
                blkalert = QMessageBox.question(self, 'Success', f"{res.matched_count} part document(s) updated!", QMessageBox.Ok)


            else:
                print("Update Canceled by User....")

    def getPart(self):
        query = self.searchBar.text()
        print(f"Query Term: {query}")
        result = list(db.items.find({'partNumber': query}))
        if len(result) > 0:
            self.partNum.setText(result[0]['partNumber'])
            self.description.setText(result[0]['description'])
            self.expiration.setText(result[0]['expiration'])
            if result[0]['unit'] == 'EA':
                self.unit.setCurrentIndex(0)
            if result[0]['unit'] == 'GAL':
                self.unit.setCurrentIndex(1)
            if result[0]['unit'] == 'oz':
                self.unit.setCurrentIndex(2)
            if result[0]['unit'] == 'SI':
                self.unit.setCurrentIndex(3)
            if result[0]['unit'] == 'SF':
                self.unit.setCurrentIndex(4)
            if result[0]['unit'] == 'Lbs':
                self.unit.setCurrentIndex(5)
            if result[0]['unit'] == 'CF':
                self.unit.setCurrentIndex(6)

        else:
            print("No Results...") 
            msgBox = QMessageBox.question(self, 'Error', "No results found for that part number!", QMessageBox.Ok)
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = mainWindow()
    mainwindow.show()
    sys.exit(app.exec_())