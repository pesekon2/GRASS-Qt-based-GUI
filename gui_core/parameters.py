

from PyQt4 import QtGui
from types import TypeType
from PyQt4.QtCore import QModelIndex,QEvent,Qt,QObject
from grass import script
import gselect

class Factory():
    """
    Factory to decide which widget class should be used
    """
    @staticmethod
    def newWidget(gtask, codeDict, flagList, codeDictChanger, codeStringChanger):
        """
        deciding which widget class should be used
        :param gtask: task for this widget
        :param : runable and copyable  string
        :return:
        """
        classes = [j for (i,j) in globals().iteritems() if hasattr(j, 'canHandle')]
        for oneClass in classes:
            if oneClass.canHandle(gtask['type'],gtask['multiple'],gtask['key_desc'],gtask['prompt'],gtask['values']):
                return oneClass(gtask, codeDict, flagList, codeDictChanger, codeStringChanger)
        else:
            return DefaultWidget(gtask, codeDict, flagList, codeDictChanger,  codeStringChanger)


# firstly, I define the widgets layout, then the widgets
class Parameters():
    def __init__(self, gtask, module, codeDict, flagList, codeString):
        #super(Parameters).__init__(parent)

        boxComplete=self.getLayout()
        self.module=module
        self.codeDict=codeDict
        self.flagList=flagList
        self.codeString=codeString
        self.gtask=gtask

        try:
            widget = Factory().newWidget(gtask, codeDict, flagList, self.codeDictChanger, self.codeStringChanger)
            boxComplete.addWidget(widget)

        except:
            widget=Flags(gtask, codeDict, flagList, self.codeDictChanger, self.codeStringChanger)
            boxComplete.addWidget(widget)
            boxComplete.addStretch()
            boxComplete.addWidget(QtGui.QLabel('(%s)' % gtask['name']))

        if gtask['label'] and gtask['description']: # title is in label so we can use description as help/tooltip
            widget.setToolTip(gtask['description'])

        self.completeWidget=QtGui.QWidget()
        self.completeWidget.setLayout(boxComplete)

    def newWidget(self):
        """
        :return:The widget
        """

        return self.completeWidget

    def getLayout(self):
        """
        create layout/box for the widget
        :param gtask: task for this widget
        :return: layout
        """

        try:
            boxHeader=QtGui.QHBoxLayout()

            if self.gtask['multiple']==True:
                boxHeader.addWidget(QtGui.QLabel('[multiple]'))
            if self.gtask['label']:
                description=QtGui.QLabel(self.gtask['label'])
            else:
                description=QtGui.QLabel(self.gtask['description'])
            boxHeader.addWidget(description)
            boxHeader.addStretch()
            boxHeader.addWidget(QtGui.QLabel('(%s=%s)' % (self.gtask['name'],self.gtask['type'])))

            header=QtGui.QWidget()
            header.setLayout(boxHeader)

            layoutComplete=QtGui.QVBoxLayout()
            layoutComplete.addWidget(header)

        except:layoutComplete=QtGui.QHBoxLayout() # flag

        layoutComplete.setSpacing(0)
        layoutComplete.setMargin(0)

        return layoutComplete

    def codeStringChanger(self):
        flags=''
        for i in self.flagList:
            if len(i)==1: flags = flags + ' -' + i
            else: flags = flags + ' --' + i
        self.codeString.setText(self.module+flags+' '
                           +' '.join('{}={}'.format(key, val) for key, val in self.codeDict.items()))

    def codeDictChanger(self, text):
        if text and text!=self.gtask['default']:
            try:
                self.codeDict[self.gtask['name']]=text
            except: # it means that there is no item for this widget in dict
                self.codeDict.update({self.gtask['name']:text})
        else:
            try:del self.codeDict[self.gtask['name']] # because we don't want to have not necessary items in dict
            except:pass

        self.codeStringChanger()


# now string types
class SqlQuery(QtGui.QLineEdit):
    def __init__(self, gtask, codeDict, flagList, codeDictChanger, codeStringChanger):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(SqlQuery,self).__init__()

        if gtask['default']:
            self.setText(gtask['default'])

        self.textChanged.connect(lambda: self.changeCommand(gtask, flagList, self, codeDictChanger, codeStringChanger))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return key_desc==['sql_query']

    def changeCommand(self, gtask, flagList, widget, codeDictChanger, codeStringChanger):
        codeDictChanger(str(widget.text()))

class Cats(QtGui.QLineEdit): # maybe in future implement special widget when called from gui
    def __init__(self, gtask, codeDict, flagList, codeDictChanger, codeStringChanger):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(Cats,self).__init__()

        if gtask['default']:
            self.setText(gtask['default'])

        self.textChanged.connect(lambda: self.changeCommand(gtask, flagList, self, codeDictChanger, codeStringChanger))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return prompt=='cats'

    def changeCommand(self, gtask, flagList, widget, codeDictChanger, codeStringChanger):
        codeDictChanger(str(widget.text()))

class SimpleValues(QtGui.QComboBox):
    def __init__(self, gtask, codeDict, flagList, codeDictChanger, codeStringChanger):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(SimpleValues,self).__init__()

        self.setEditable(True)
        self.addItems(gtask['values'])

        if gtask['default']:
            self.setEditText(gtask['default'])

        self.textChanged.connect(lambda: self.changeCommand(gtask, flagList, self, codeDictChanger, codeStringChanger))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return (type=='string') and multiple==False and values

    def changeCommand(self, gtask, flagList, widget, codeDictChanger, codeStringChanger):
        codeDictChanger(str(widget.currentText()))

class Separator(QtGui.QComboBox):
    def __init__(self, gtask, codeDict, flagList, codeDictChanger, codeStringChanger):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(Separator,self).__init__()

        self.setEditable(True)
        self.addItems(self.getItems(gtask))

        if gtask['default']:
            self.setEditText(gtask['default'])

        self.textChanged.connect(lambda: self.changeCommand(gtask, flagList, self, codeDictChanger, codeStringChanger))

    def getItems(self, gtask):
        # in case that description is not same for all of them, type it manually here
        itemsString = gtask['description'].split('Special characters: ')[1]
        return itemsString.split(', ')

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return (type=='string') and prompt=='separator'

    def changeCommand(self, gtask, flagList, widget, codeDictChanger, codeStringChanger):
        codeDictChanger(str(widget.currentText()))

#inherited from gselect.py
class TreeComboBox(gselect.TreeComboBox):
    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='string' and key_desc!=['sql_query'] and prompt in ['raster', 'vector', 'raster_3d', 'group']

    def changeCommand(self, gtask, flagList, widget, codeDictChanger, codeStringChanger):
        codeDictChanger(str(widget.currentText()))

class BrowseFile(gselect.BrowseFile):
    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='string' and key_desc!=['sql_query'] and (prompt=='file')

    def changeCommand(self, gtask, flagList, widget, codeDictChanger, codeStringChanger):
        codeDictChanger(str(widget.text()))

class MultipleValues(gselect.MultipleValues):
    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return (type=='string') and multiple==True and values

    def changeCommand(self, gtask, flagList, widget, codeDictChanger, codeStringChanger):
        value=''
        items = (widget.itemAt(i).widget() for i in range(widget.count()-1))

        for item in items:
            if item.isChecked():
                if value:
                    value=','.join((value,str(item.objectName())))
                else:
                    value=str(item.objectName())

        codeDictChanger(str(value))

class Layers(gselect.Layers):
    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return (type=='string') and prompt=='layer'

    def changeCommand(self, gtask, flagList, widget, codeDictChanger, codeStringChanger):
        codeDictChanger(str(widget.currentText()))

class Columns(gselect.Columns):
    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return (type=='string') and prompt=='dbcolumn'

    def changeCommand(self, gtask, flagList, widget, codeDictChanger, codeStringChanger):
        codeDictChanger(str(widget.currentText()))

class Colors(gselect.Colors):
    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return (type=='string') and prompt=='color'

    def changeCommand(self, gtask, flagList, widget, codeDictChanger, codeStringChanger):
        items = list((widget.itemAt(i).widget() for i in range(widget.count()-1)))

        if len(items)>1:
            if items[1].isChecked()==False:
                codeDictChanger(str(items[0].text()))
            else:codeDictChanger('')
        else:
            codeDictChanger(str(items[0].text()))

class DbTable(gselect.DbTable):
    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return prompt=='dbtable'

    def changeCommand(self, gtask, flagList, widget, codeDictChanger, codeStringChanger):
        codeDictChanger(str(widget.currentText()))


# now float types
class MultipleFloat(QtGui.QLineEdit):
    def __init__(self, gtask, codeDict, flagList, codeDictChanger, codeStringChanger):
        """
        for float: multiple, coords
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(MultipleFloat,self).__init__()

        if gtask['default']:
            self.setText(gtask['default'])

        self.textChanged.connect(lambda: self.changeCommand(gtask, flagList, self, codeDictChanger, codeStringChanger))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='float' and (multiple==True or prompt=='coords')

    def changeCommand(self, gtask, flagList, widget, codeDictChanger, codeStringChanger):
        codeDictChanger(str(widget.text()))

class SimpleFloat(QtGui.QDoubleSpinBox):
    def __init__(self, gtask, codeDict, flagList, codeDictChanger, codeStringChanger):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(SimpleFloat,self).__init__()

        if gtask['default']:
            self.setValue(float(gtask['default']))

        self.valueChanged.connect(lambda: self.changeCommand(gtask, flagList, self, codeDictChanger, codeStringChanger))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='float' and multiple==False

    def changeCommand(self, gtask, flagList, widget, codeDictChanger, codeStringChanger):
        codeDictChanger(str(widget.value()))





# now integer types
class MultipleInteger(QtGui.QLineEdit):
    def __init__(self, gtask, codeDict, flagList, codeDictChanger, codeStringChanger):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(MultipleInteger,self).__init__()

        if gtask['default']:
            self.setText(gtask['default'])

        self.textChanged.connect(lambda: self.changeCommand(gtask, flagList, self, codeDictChanger, codeStringChanger))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='integer' and multiple==True

    def changeCommand(self, gtask, flagList, widget, codeDictChanger, codeStringChanger):
        codeDictChanger(str(widget.text()))

class SimpleInteger(QtGui.QSpinBox):
    def __init__(self, gtask, codeDict, flagList, codeDictChanger, codeStringChanger):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(SimpleInteger,self).__init__()

        if gtask['default']:
            self.setValue(int(gtask['default']))

        self.valueChanged.connect(lambda: self.changeCommand(gtask, flagList, self, codeDictChanger, codeStringChanger))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='integer' and multiple==False

    def changeCommand(self, gtask, flagList, widget, codeDictChanger, codeStringChanger):
        codeDictChanger(str(widget.text()))




class Flags(QtGui.QCheckBox):
    def __init__(self, gtask, codeDict, flagList, codeDictChanger, codeStringChanger):

        super(Flags,self).__init__(self.getLabel(gtask))

        self.stateChanged.connect(lambda: self.changeCommand(gtask, flagList, self, codeDictChanger, codeStringChanger))

    def getLabel(self, gtask):
        if gtask['label']:
            return gtask['label']
        else:
            return gtask['description']

    def changeCommand(self, gtask, flagList, widget, codeDictChanger, codeStringChanger):
        if widget.isChecked():
            if gtask['name'] not in flagList: # it means that there is no item for this widget in dict
                flagList.append(gtask['name'])
        else:
            flagList.remove(gtask['name']) # because we don't want to have not necessary items in dict
        codeStringChanger()




# default widget
class DefaultWidget(QtGui.QLineEdit):
    def __init__(self, gtask, codeDict, flagList, codeDictChanger, codeStringChanger):

        super(DefaultWidget,self).__init__()

        self.setText('TODO - Nobody expects the Spanish Inquisition') # just highlighting what should be done better
        palette=QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.Base,QtGui.QColor('red'))
        self.setPalette(palette)

        #if gtask['default']: # uncomment when not using highlighting
        #    self.setText(gtask['default'])

        self.textChanged.connect(lambda: self.changeCommand(gtask, flagList, self, codeDictChanger, codeStringChanger))

    def changeCommand(self, gtask, flagList, widget, codeDictChanger, codeStringChanger):
        print gtask
        codeDictChanger(str(widget.text()))




# column/layer also from map (v.db.join), d.vect, wordwrap, size
# key_desc, required after guisection, prompt=datasource (v.external),
# datasource_layer (v.import), words for predefined colors





















