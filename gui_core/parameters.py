

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
    def newWidget(gtask, function, codeDict, flagList, codeString):
        """
        deciding which widget class should be used
        :param gtask: task for this widget
        :param : runable and copyable  string
        :return:
        """
        classes = [j for (i,j) in globals().iteritems() if hasattr(j, 'canHandle')]
        for oneClass in classes:
            if oneClass.canHandle(gtask['type'],gtask['multiple'],gtask['key_desc'],gtask['prompt'],gtask['values']):
                return oneClass(gtask,function,codeDict,flagList,codeString)
        else:
            return DefaultWidget(gtask,function,codeDict,flagList,codeString)


# firstly, I define the widgets layout, then the widgets
class Parameters():
    def __init__(self, gtask, function, codeDict, flagList, codeString):
        #super(Parameters).__init__(parent)

        boxComplete=self.getLayout(gtask)

        try:
            widget = Factory().newWidget(gtask, function, codeDict, flagList, codeString)
            if gtask['label'] and gtask['description']: # title is in label so we can use description as help/tooltip
                widget.setToolTip(gtask['description'])

            boxComplete.addWidget(widget)

        except:
            widget=Flags(gtask,function,codeDict,flagList,codeString)
            boxComplete.addWidget(widget)
            boxComplete.addStretch()
            boxComplete.addWidget(QtGui.QLabel('(%s)' % gtask['name']))

        self.completeWidget=QtGui.QWidget()
        self.completeWidget.setLayout(boxComplete)

    def newWidget(self):
        """
        :return:The widget
        """

        return self.completeWidget

    def getLayout(self,gtask):
        """
        create layout/box for the widget
        :param gtask: task for this widget
        :return: layout
        """

        try:
            boxHeader=QtGui.QHBoxLayout()

            if gtask['multiple']==True:
                boxHeader.addWidget(QtGui.QLabel('[multiple]'))
            if gtask['label']:
                description=QtGui.QLabel(gtask['label'])
            else:
                description=QtGui.QLabel(gtask['description'])
            boxHeader.addWidget(description)
            boxHeader.addStretch()
            boxHeader.addWidget(QtGui.QLabel('(%s=%s)' % (gtask['name'],gtask['type'])))

            header=QtGui.QWidget()
            header.setLayout(boxHeader)

            layoutComplete=QtGui.QVBoxLayout()
            layoutComplete.addWidget(header)

        except:layoutComplete=QtGui.QHBoxLayout() # flag

        layoutComplete.setSpacing(0)
        layoutComplete.setMargin(0)

        return layoutComplete




# now string types
class SqlQuery(QtGui.QLineEdit):
    def __init__(self, gtask, function, codeDict, flagList, codeString):#,parent=QtGui.QLineEdit):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(SqlQuery,self).__init__()
        self.textChanged.connect(lambda: self.setCommand(gtask,function,codeDict,flagList,codeString,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return key_desc==['sql_query']

    def setCommand(self,gtask, function, codeDict, flagList, codeString,widget):
        codeDictChanger(gtask,function,codeDict,flagList,codeString,str(widget.text()))

class Cats(QtGui.QLineEdit): # maybe in future implement special widget when called from gui
    def __init__(self, gtask, function, codeDict, flagList, codeString):#,parent=QtGui.QLineEdit):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(Cats,self).__init__()
        self.textChanged.connect(lambda: self.setCommand(gtask,function,codeDict,flagList,codeString,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return prompt=='cats'

    def setCommand(self,gtask, function, codeDict, flagList, codeString,widget):
        codeDictChanger(gtask,function,codeDict,flagList,codeString,str(widget.text()))

class SimpleValues(QtGui.QComboBox):
    def __init__(self, gtask, function, codeDict, flagList, codeString):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(SimpleValues,self).__init__()
        self.setEditable(True)
        self.addItems(gtask['values'])
        self.textChanged.connect(lambda: self.setCommand(gtask,function,codeDict,flagList,codeString,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return (type=='string') and multiple==False and values

    def setCommand(self,gtask, function, codeDict, flagList, codeString,widget):
        codeDictChanger(gtask,function,codeDict,flagList,codeString,str(widget.currentText()))

#inherited from gselect.py
class TreeComboBox(gselect.TreeComboBox):
    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='string' and key_desc!=['sql_query'] and (prompt=='raster' or prompt=='vector')

    def setCommand(self,gtask, function, codeDict, flagList, codeString,widget):
        codeDictChanger(gtask,function,codeDict,flagList,codeString,str(widget.currentText()))

class BrowseFile(gselect.BrowseFile):
    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='string' and key_desc!=['sql_query'] and (prompt=='file')

    def setCommand(self,gtask, function, codeDict, flagList, codeString,widget):
        codeDictChanger(gtask,function,codeDict,flagList,codeString,str(widget.text()))

class MultipleValues(gselect.MultipleValues):
    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return (type=='string') and multiple==True and values

    def setCommand(self,gtask, function, codeDict, flagList, codeString,widget):
        value=''
        items = (widget.itemAt(i).widget() for i in range(widget.count()-1))

        for item in items:
            if item.isChecked():
                if value:
                    value=','.join((value,str(item.text())))
                else:
                    value=str(item.text())

        codeDictChanger(gtask,function,codeDict,flagList,codeString,str(value))





# now float types
class MultipleFloat(QtGui.QLineEdit):
    def __init__(self, gtask, function, codeDict, flagList, codeString):
        """
        for float: multiple, coords
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(MultipleFloat,self).__init__()
        self.textChanged.connect(lambda: self.setCommand(gtask,function,codeDict,flagList,codeString,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='float' and (multiple==True or prompt=='coords')

    def setCommand(self,gtask, function, codeDict, flagList, codeString,widget):
        codeDictChanger(gtask,function,codeDict,flagList,codeString,str(widget.text()))

class SimpleFloat(QtGui.QDoubleSpinBox):
    def __init__(self, gtask, function, codeDict, flagList, codeString):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(SimpleFloat,self).__init__()
        self.valueChanged.connect(lambda: self.setCommand(gtask,function,codeDict,flagList,codeString,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='float' and multiple==False

    def setCommand(self,gtask, function, codeDict, flagList, codeString,widget):
        codeDictChanger(gtask,function,codeDict,flagList,codeString,str(widget.text()))





# now integer types
class MultipleInteger(QtGui.QLineEdit):
    def __init__(self, gtask, function, codeDict, flagList, codeString):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(MultipleInteger,self).__init__()
        self.textChanged.connect(lambda: self.setCommand(gtask,function,codeDict,flagList,codeString,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='integer' and multiple==True

    def setCommand(self,gtask, function, codeDict, flagList, codeString,widget):
        codeDictChanger(gtask,function,codeDict,flagList,codeString,str(widget.text()))

class SimpleInteger(QtGui.QSpinBox):
    def __init__(self, gtask, function, codeDict, flagList, codeString):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(SimpleInteger,self).__init__()
        self.valueChanged.connect(lambda: self.setCommand(gtask,function,codeDict,flagList,codeString,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='integer' and multiple==False

    def setCommand(self,gtask, function, codeDict, flagList, codeString,widget):
        codeDictChanger(gtask,function,codeDict,flagList,codeString,str(widget.text()))



class Flags(QtGui.QCheckBox):
    def __init__(self, gtask, function, codeDict, flagList, codeString):

        super(Flags,self).__init__(gtask['description'])
        self.stateChanged.connect(lambda: self.setCommand(gtask,function,codeDict,flagList,codeString,self))

    def setCommand(self,gtask, function, codeDict, flagList, codeString,widget):
        if widget.isChecked():
            if gtask['name'] not in flagList: # it means that there is no item for this widget in dict
                flagList.append(gtask['name'])
        else:
            flagList.remove(gtask['name']) # because we don't want to have not necessary items in dict
        codeStringChanger(function,codeDict,flagList,codeString)



# default widget
class DefaultWidget(QtGui.QLineEdit):
    def __init__(self, gtask, function, codeDict, flagList, codeString):

        super(DefaultWidget,self).__init__()
        self.setText('TODO - Nobody expects the Spanish Inquisition') # just highlighting what should be done better
        palette=QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.Base,QtGui.QColor('red'))
        self.setPalette(palette)

        self.textChanged.connect(lambda: self.setCommand(gtask,function,codeDict,flagList,codeString,self))

    def setCommand(self,gtask, function, codeDict, flagList, codeString,widget):
        codeDictChanger(gtask,function,codeDict,flagList,codeString,str(widget.text()))




# methods for updating command
def codeDictChanger(gtask, function, codeDict, flagList, codeString,text):
    if text:
        try:
            codeDict[gtask['name']]=text
        except: # it means that there is no item for this widget in dict
            codeDict.update({gtask['name']:text})
    else:
        try:del codeDict[gtask['name']] # because we don't want to have not necessary items in dict
        except:pass
    codeStringChanger(function,codeDict,flagList,codeString)


def codeStringChanger(function,codeDict,flagList,codeString):
    flags=''
    for i in flagList:
        if len(i)==1: flags = flags + ' -' + i
        else: flags = flags + ' --' + i
    codeString.setText(function+flags+' '
                       +' '.join('{}={}'.format(key, val) for key, val in codeDict.items()))



















