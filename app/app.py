#inventoryApp
#j quick 12/13/2021 v0.1
#main app

import sys
import modules.dbTools as db
import modules.views as views

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle('inventoryApp v0.1')
        self.setGeometry(500,250,800,500)
        menubar = self.menuBar()

        #Actions for MenuBar

        #File Menu Actions

        quitAct = QAction("Quit", self)
        quitAct.triggered.connect(qApp.quit)

        #Create Menu Actions

        createItemAct = QAction("Item", self)
        createItemAct.triggered.connect(self.showCreateItem)

        createLocationAct = QAction("Location", self)
        createLocationAct.triggered.connect(self.showCreateLocation)

        #Edit Menu Actions

        editItemAct = QAction("Item", self)
        editItemAct.triggered.connect(self.showEditItem)

        editLocationAct = QAction("Location", self)
        editLocationAct.triggered.connect(self.showEditLocation)

        #View Menu Actions

        viewStacksAct = QAction("Stock", self)
        viewStacksAct.triggered.connect(self.showStockList)

        viewLocationsAct = QAction("Locations", self)
        viewLocationsAct.triggered.connect(self.showLocationList)

        viewItemsAct = QAction("Items", self)
        viewItemsAct.triggered.connect(self.showItemList)
        
        #Menu bar items
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(quitAct)

        createMenu = menubar.addMenu('Create')
        createMenu.addAction(createItemAct)
        createMenu.addAction(createLocationAct)

        editMenu = menubar.addMenu('Edit')
        editMenu.addAction(editItemAct)
        editMenu.addAction(editLocationAct)

        viewMenu = menubar.addMenu('View')
        viewMenu.addAction(viewStacksAct)
        viewMenu.addAction(viewItemsAct)
        viewMenu.addAction(viewLocationsAct)

        #Status Bar - INCOMPLETE

        status = self.statusBar()
        self.statusContent = QLabel("System Ready")
        status.addWidget(self.statusContent)

        #Sets default central widget

        central = views.stockListWindow()
        self.setCentralWidget(central)

    def showCreateItem(self):
        window = views.createItemWindow()
        self.setCentralWidget(window)

    def showEditItem(self):
        window = views.editItemWindow()
        self.setCentralWidget(window)

    def showStockList(self):
        window = views.stockListWindow()
        self.setCentralWidget(window)
    
    def showLocationList(self):
        print("DEBUG: locationListWindow under construction...")
        QMessageBox.information(self, "Error", "This feature is under construction and not yet available.")
        #window = views.locationListWindow()
        #self.setCentralWidget(window)
    
    def showCreateLocation(self):
        #print("DEBUG: createLocationWindow under construction...")
        #QMessageBox.information(self, "Error", "This feature is under construction and not yet available.")
        window = views.createLocationWindow()
        self.setCentralWidget(window)

    def showItemList(self):
        print("DEBUG: itemListWindow under construction...")
        QMessageBox.information(self, "Error", "This feature is under construction and not yet available.")
        #window = views.itemListWindow()
        #self.setCentralWidget(window)
    
    def showEditLocation(self):
        print("DEBUG: editLocationWindow under construction...")
        QMessageBox.information(self, "Error", "This feature is under construction and not yet available.")
        #window = views.editLocationWindow()
        #self.setCentralWidget(window)
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = mainWindow()
    mainwindow.show()
    sys.exit(app.exec_())