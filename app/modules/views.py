#views.py
#Definitions for GUI screens for use in main app

import modules.dbTools as db

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class stockListWindow(QWidget):
    def __init__(self):
        super().__init__()
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)
        self.searchBar = QLineEdit()
        self.searchBar.returnPressed.connect(self.searchTable)
        self.searchButton = QPushButton("Search")
        self.searchButton.clicked.connect(self.searchTable)
        self.refreshButton = QPushButton("Clear")
        self.refreshButton.clicked.connect(self.refreshTable)
        #listHeaders = QLabel(f"{'Part'.ljust(7,' ')}     {'Batch'.ljust(10,' ')}{'Qty'.ljust(7,' ')}{'Unit'.ljust(5,' ')}{'Location'.ljust(10,' ')}{'Expiration'.ljust(15, ' ')}")
        

        self.stockTable = QTableWidget()
        self.stockTable.setColumnCount(6)
        #stockTable.setRowCount(len(stockList))


        #dispList = QListWidget()

        grid_layout.addWidget(self.searchBar, 0, 0, 1, 4)
        grid_layout.addWidget(self.searchButton, 0, 4, 1, 1)
        grid_layout.addWidget(self.refreshButton, 0, 5, 1, 1)
        #grid_layout.addWidget(listHeaders, 1, 0, 1, 4)
        #grid_layout.addWidget(dispList, 2, 0, 5, 6)
        grid_layout.addWidget(self.stockTable, 2, 0, 5, 6)

        self.generateTable(None)

    def generateTable(self, query):
        self.stockTable.clear()
        stockList = db.getStockList(query)
        labels=['Part', 'Batch', 'Qty', 'Unit', 'Location', 'Expiration']
        self.stockTable.setHorizontalHeaderLabels(labels)
        if len(stockList) == 0:
            QMessageBox.information(self, "Alert", f"Search returned no results.")
        else:
            row = 0
            for item in stockList:
                part = QTableWidgetItem(f"{item['partNumber']}")
                qty = QTableWidgetItem(f"{item['qty']}")
                unit = QTableWidgetItem(f"{item['unit']}")
                batch = QTableWidgetItem(f"{item['batch']}")
                expiration = QTableWidgetItem(f"{item['expiration']}")
                location = QTableWidgetItem(f"{item['location']}")

                self.stockTable.insertRow(row)
                self.stockTable.setItem(row, 0, part)
                self.stockTable.setItem(row, 1, batch)
                self.stockTable.setItem(row, 2, qty)
                self.stockTable.setItem(row, 3, unit)
                self.stockTable.setItem(row, 4, location)
                self.stockTable.setItem(row, 5, expiration)

                
        #dispList.itemClicked.connect(self.clicked)
        self.stockTable.itemClicked.connect(self.clicked)

    def clicked(self, item):
        row = self.stockTable.row(item)
        data = [self.stockTable.item(row, 0).text(), self.stockTable.item(row, 1).text(), self.stockTable.item(row, 2).text(), self.stockTable.item(row, 3).text(), self.stockTable.item(row, 4).text(), self.stockTable.item(row, 5).text()]
        QMessageBox.information(self, "DEBUG", f"DEBUG: Showing data for {data[0]} - {data[1]} - {data[2]} - {data[3]} - {data[4]} - {data[5]}")
        
    def searchTable(self):
        query = self.searchBar.text()
        self.refreshTable()
        if query == '':
            msgReply = QMessageBox.question(self, 'Continue?', 'Empty search term will return all results, continue?', QMessageBox.Yes|QMessageBox.No)
            if msgReply == QMessageBox.Yes:
                query = None
                print(f"DEBUG: search pressed with empty search bar -- all Results...")
                self.generateTable(query)
            else:
                print("DEBUG: User cancelled search operation...")        
        else:
            print(f"DEBUG: search pressed with query = {query}...")
            self.generateTable(query)

    def refreshTable(self):
        print("DEBUG: table refreshed...")
        for i in range(self.stockTable.rowCount()):
            self.stockTable.removeRow(i)
   

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

#INCOMPLETE
class locationListWindow(QWidget):
    def __init__(self):
        None

#INCOMPLETE
class createLocationWindow(QWidget):
    def __init__(self):
        None

#INCOMPLETE
class editLocationWindow(QWidget):
    def __init__(self):
        None

#INCOMPLETE
class itemListWindow(QWidget):
    def __init__(self):
        None