

from PyQt4.QtCore import QModelIndex,QEvent
from PyQt4 import QtGui
from grass import script
import subprocess


class TreeComboBox(QtGui.QComboBox):
    def __init__(self, gtask, codeDict, flagList, codeDictChanger, codeStringChanger, parent=None):#, *args):
        super(TreeComboBox,self).__init__(parent)#*args)

        self.__skip_next_hide = False

        tree_view = QtGui.QTreeView(self)
        tree_view.setFrameShape(QtGui.QFrame.NoFrame)
        tree_view.setEditTriggers(tree_view.NoEditTriggers)
        tree_view.setAlternatingRowColors(True)
        tree_view.setSelectionBehavior(tree_view.SelectRows)
        #tree_view.setWordWrap(True)
        tree_view.setAllColumnsShowFocus(True)
        self.setView(tree_view)
        self.setEditable(True)
        self.setModel(self.getModel(gtask))
        self.textChanged.connect(lambda: self.changeCommand(gtask, flagList, self, codeDictChanger,
                                                            codeStringChanger)) # see in parameters.py

        self.view().viewport().installEventFilter(self)

    def showPopup(self):
        self.setRootModelIndex(QModelIndex())
        super(TreeComboBox,self).showPopup()

    def hidePopup(self):
        self.setRootModelIndex(self.view().currentIndex().parent())
        #self.setCurrentIndex(self.view().currentIndex().row())
        if self.__skip_next_hide:
            self.__skip_next_hide = False
        else:
            super(TreeComboBox,self).hidePopup()

    def selectIndex(self, index):
        self.setRootModelIndex(index.parent())
        self.setCurrentIndex(index.row())

    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseButtonPress and object is self.view().viewport():
            index = self.view().indexAt(event.pos())
            self.__skip_next_hide = not self.view().visualRect(index).contains(event.pos())
        return False

    def getModel(self,gtask):
        mapsets = script.mapsets(search_path = True)
        model = QtGui.QStandardItemModel()
        #model.__init__(parent=None)
        model.setParent(self)
        for mapset in mapsets:
            parent_item = QtGui.QStandardItem('Mapset: '+mapset)
            parent_item.setSelectable(False)
            list = script.core.list_pairs(gtask['prompt'])
            for map in list:
                if mapset in map:
                    parent_item.appendRow(QtGui.QStandardItem('%s@%s' %(map[0],map[1])))
            model.appendRow(parent_item)

        return model


class BrowseFile(QtGui.QWidget):
    def __init__(self, gtask, codeDict, flagList, codeDictChanger, codeStringChanger, parent=None):
        super(BrowseFile,self).__init__(parent)

        layout=QtGui.QHBoxLayout()
        self.line=QtGui.QLineEdit()
        button = QtGui.QPushButton('Browse')
        button.clicked.connect(self.selectFile)

        button.setMinimumSize(button.sizeHint())
        self.line.setMinimumSize(self.line.sizeHint())

        layout.addWidget(self.line)
        layout.addWidget(button)
        self.setLayout(layout)

        self.line.textChanged.connect(lambda: self.changeCommand(gtask, flagList,
                                                         self.line, codeDictChanger, codeStringChanger)) # see in parameters.py

    def selectFile(self):

        filePath = QtGui.QFileDialog.getOpenFileName(self, 'Select file')
        if filePath:
            self.line.setText(filePath)
        else:
            return


class MultipleValues(QtGui.QGroupBox):
    def __init__(self, gtask, codeDict, flagList, codeDictChanger, codeStringChanger):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(MultipleValues,self).__init__()

        defaultBoxes = gtask['default'].split(',')

        i=0
        if not gtask['values_desc']:
            layout=QtGui.QHBoxLayout()
            for item in gtask['values']:
                box=QtGui.QCheckBox(item)
                box.setObjectName(gtask['values'][i])
                if box.objectName() in defaultBoxes:
                    box.setChecked(True)
                layout.addWidget(box)
                box.stateChanged.connect(lambda: self.changeCommand(gtask, flagList,
                                                             layout, codeDictChanger, codeStringChanger)) # see in parameters.py
                i=i+1
        else:
            layout=QtGui.QVBoxLayout()
            layout.setSpacing(0)
            for item in gtask['values_desc']:
                box=QtGui.QCheckBox(item)
                box.setObjectName(gtask['values'][i])
                if box.objectName() in defaultBoxes:
                    box.setChecked(True)
                layout.addWidget(box)
                box.stateChanged.connect(lambda: self.changeCommand(gtask, flagList,
                                                             layout, codeDictChanger, codeStringChanger)) # see in parameters.py
                i=i+1

        layout.addStretch()
        self.setLayout(layout)

class Layers(QtGui.QComboBox):
    def __init__(self, gtask, codeDict, flagList, codeDictChanger, codeStringChanger):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(Layers,self).__init__()

        self.setEditable(True)

        self.gtask = gtask
        self.codeDict=codeDict

        if gtask['default']:
            self.setEditText(gtask['default'])

        self.textChanged.connect(lambda: self.changeCommand(gtask, flagList, self, codeDictChanger, codeStringChanger))

    def getLayers(self):

        self.clear()

        if self.gtask['element']=='layer_all':
            self.addItem('-1')

        try:
            layers = script.vector_db(map=self.codeDict['input'])
            for layer in layers:
                self.addItem(str(layer))
        except:
            if self.count()==0:
                self.addItem('')

    def showPopup(self):
        text=self.currentText()
        self.getLayers()
        super(Layers,self).showPopup()
        if text in [self.itemText(i) for i in range(self.count())]:
            self.setEditText(text)
        else:
            self.setEditText('')

class Columns(QtGui.QComboBox):
    def __init__(self, gtask, codeDict, flagList, codeDictChanger, codeStringChanger):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(Columns,self).__init__()

        self.setEditable(True)

        self.gtask = gtask
        self.codeDict=codeDict

        if gtask['default']:
            self.setEditText(gtask['default'])

        self.textChanged.connect(lambda: self.changeCommand(gtask, flagList, self, codeDictChanger, codeStringChanger))

    def getLayer(self):

        try:
            layer = int(self.codeDict['layer'])
            return layer
        except:
            return self.codeDict['layer']

    def getColumns(self,layers,layer):

        for item in script.db_describe(table = layers[layer]["table"],
                                      driver = layers[layer]["driver"],
                                      database = layers[layer]["database"])['cols']:
            self.addItem(item[0])

    def setValues(self):

        self.clear()

        try:
            layers=script.vector_db(map=self.codeDict['input'])
            layer=self.getLayer()

            if layer==-1:
                for layer in layers.keys():
                    self.getColumns(layers,layer)
            else:self.getColumns(layers,layer)
        except:self.addItem('')

    def showPopup(self):

        text=self.currentText()
        self.setValues()
        super(Columns,self).showPopup()
        if text in [self.itemText(i) for i in range(self.count())]:
            self.setEditText(text)
        else:
            self.setEditText('')

class Colors(QtGui.QWidget):

    def __init__(self, gtask, codeDict, flagList, codeDictChanger, codeStringChanger):
        super(Colors, self).__init__()

        layout = QtGui.QHBoxLayout()
        self.colorBtn = QtGui.QPushButton()

        self.btnStyle = 'border-style: double; border-width: 3px; border-color: beige; min-width: 8em; padding: 6px'

        if gtask['default']=='none':
            self.colorBtn.setStyleSheet("QPushButton {background-color: grey; %s}" % self.btnStyle)
            self.colorBtn.setText('Select color')
            layout.addWidget(self.colorBtn)
            transparent = QtGui.QCheckBox('Transparent')
            transparent.stateChanged.connect(lambda: self.parseText(gtask, flagList, layout, codeDictChanger, codeStringChanger))
            layout.addWidget(transparent)
        else:
            if QtGui.QColor(gtask['default']).red() + QtGui.QColor(gtask['default']).blue() + QtGui.QColor(gtask['default']).green() < 387:
                textColor = 'white'
            else:
                textColor = 'black'
            self.colorBtn.setStyleSheet("QPushButton {background-color: %s; color: %s; %s}" % (gtask['default'], textColor, self.btnStyle))
            self.colorBtn.setText(gtask['default'])
            layout.addWidget(self.colorBtn)

        layout.addStretch()
        self.setLayout(layout)
        self.defaultText = self.colorBtn.text()

        self.colorBtn.clicked.connect(lambda: self.color_picker())
        self.colorBtn.clicked.connect(lambda: self.parseText(gtask, flagList, layout, codeDictChanger, codeStringChanger))

    def color_picker(self):
        color = QtGui.QColorDialog.getColor(initial=QtGui.QColor(self.colorBtn.palette().color(QtGui.QPalette.Background)))
        if color.isValid():
            if color.red() + color.green() + color.blue() < 387:
                textColor = 'white'
            else:textColor = 'black'
            self.colorBtn.setStyleSheet("QPushButton { background-color: %s; color: %s; %s}" % (color.name(), textColor, self.btnStyle))
            self.colorBtn.setText('%s:%s:%s' % (color.red(), color.green(), color.blue()))

    def parseText(self, gtask, flagList, layout, codeDictChanger, codeStringChanger):
        if self.colorBtn.text()!=self.defaultText:
            self.changeCommand(gtask, flagList, layout, codeDictChanger, codeStringChanger)

class DbTable(QtGui.QComboBox):
    def __init__(self, gtask, codeDict, flagList, codeDictChanger, codeStringChanger):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(DbTable,self).__init__()
        self.codeDict = codeDict

        self.setEditable(True)

        if gtask['default']:
            self.setEditText(gtask['default'])

        self.textChanged.connect(lambda: self.changeCommand(gtask, flagList, self, codeDictChanger, codeStringChanger))

    def getDbInfo(self):
        try:
            driver = self.codeDict['driver']
            try:
                database = self.codeDict['database']
            except:
                connect = script.db_connection()
                database = connect['database']
        except:
            connect = script.db_connection()
            try:
                database = self.codeDict['database']
                driver = connect['driver']
            except:
                database = connect['database']
                driver = connect['driver']

        return driver, database

    def getTables(self):

        driver, database = self.getDbInfo()

        tables = script.start_command('db.tables',
                         flags = 'p',
                         driver = driver,
                         database = database,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

        return tables.communicate()[0]

    def showPopup(self):

        text = self.currentText()
        tables = self.getTables()

        self.clear()
        if tables:
            for table in tables.splitlines():
                self.addItem(table)
        else:self.addItem('')

        super(DbTable,self).showPopup()
        if text in [self.itemText(i) for i in range(self.count())]:
            self.setEditText(text)
        else:
            self.setEditText('')




