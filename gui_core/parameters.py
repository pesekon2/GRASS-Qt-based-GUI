

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
    def newWidget(gtask, codeDict, flagList, codeStringChanger):
        """
        deciding which widget class should be used
        :param gtask: task for this widget
        :param : runable and copyable  string
        :return:
        """
        classes = [j for (i,j) in globals().iteritems() if hasattr(j, 'canHandle')]
        for oneClass in classes:
            if oneClass.canHandle(gtask['type'],gtask['multiple'],gtask['key_desc'],gtask['prompt'],gtask['values']):
                return oneClass(gtask, codeDict, flagList, codeStringChanger)
        else:
            return DefaultWidget(gtask, codeDict, flagList, codeStringChanger)


# firstly, I define the widgets layout, then the widgets
class Parameters():
    def __init__(self, gtask, function, codeDict, flagList, codeString):
        #super(Parameters).__init__(parent)

        boxComplete=self.getLayout(gtask)
        self.function=function
        self.codeDict=codeDict
        self.flagList=flagList
        self.codeString=codeString

        try:
            widget = Factory().newWidget(gtask, codeDict, flagList, self.codeStringChanger)
            if gtask['label'] and gtask['description']: # title is in label so we can use description as help/tooltip
                widget.setToolTip(gtask['description'])

            boxComplete.addWidget(widget)

        except:
            widget=Flags(gtask, codeDict, flagList, self.codeStringChanger)
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

    def codeStringChanger(self):
        #print getattr(Parameters,'__init__')
        flags=''
        for i in self.flagList:
            if len(i)==1: flags = flags + ' -' + i
            else: flags = flags + ' --' + i
        self.codeString.setText(self.function+flags+' '
                           +' '.join('{}={}'.format(key, val) for key, val in self.codeDict.items()))


# now string types
class SqlQuery(QtGui.QLineEdit):
    def __init__(self, gtask, codeDict, flagList, codeStringChanger):#,parent=QtGui.QLineEdit):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(SqlQuery,self).__init__()
        self.textChanged.connect(lambda: self.changeCommand(gtask, codeDict, flagList, self, codeStringChanger))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return key_desc==['sql_query']

    def changeCommand(self, gtask, codeDict, flagList, widget, codeStringChanger):
        codeDictChanger(gtask, codeDict, str(widget.text()), codeStringChanger)

class Cats(QtGui.QLineEdit): # maybe in future implement special widget when called from gui
    def __init__(self, gtask, codeDict, flagList, codeStringChanger):#,parent=QtGui.QLineEdit):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(Cats,self).__init__()
        self.textChanged.connect(lambda: self.changeCommand(gtask, codeDict, flagList, self, codeStringChanger))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return prompt=='cats'

    def changeCommand(self, gtask, codeDict, flagList, widget, codeStringChanger):
        codeDictChanger(gtask, codeDict, str(widget.text()), codeStringChanger)

class SimpleValues(QtGui.QComboBox):
    def __init__(self, gtask, codeDict, flagList, codeStringChanger):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(SimpleValues,self).__init__()
        self.setEditable(True)
        self.addItems(gtask['values'])
        self.textChanged.connect(lambda: self.changeCommand(gtask, codeDict, flagList, self, codeStringChanger))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return (type=='string') and multiple==False and values

    def changeCommand(self, gtask, codeDict, flagList, widget, codeStringChanger):
        codeDictChanger(gtask, codeDict, str(widget.currentText()), codeStringChanger)

#inherited from gselect.py
class TreeComboBox(gselect.TreeComboBox):
    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='string' and key_desc!=['sql_query'] and prompt in ['raster', 'vector', 'raster_3d']

    def changeCommand(self, gtask, codeDict, flagList, widget, codeStringChanger):
        codeDictChanger(gtask, codeDict, str(widget.currentText()), codeStringChanger)

class BrowseFile(gselect.BrowseFile):
    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='string' and key_desc!=['sql_query'] and (prompt=='file')

    def changeCommand(self, gtask, codeDict, flagList, widget, codeStringChanger):
        codeDictChanger(gtask, codeDict, str(widget.text()), codeStringChanger)

class MultipleValues(gselect.MultipleValues):
    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return (type=='string') and multiple==True and values

    def changeCommand(self, gtask, codeDict, flagList, widget, codeStringChanger):
        value=''
        items = (widget.itemAt(i).widget() for i in range(widget.count()-1))

        for item in items:
            if item.isChecked():
                if value:
                    value=','.join((value,str(item.text())))
                else:
                    value=str(item.text())

        codeDictChanger(gtask, codeDict, str(value), codeStringChanger)





# now float types
class MultipleFloat(QtGui.QLineEdit):
    def __init__(self, gtask, codeDict, flagList, codeStringChanger):
        """
        for float: multiple, coords
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(MultipleFloat,self).__init__()
        self.textChanged.connect(lambda: self.changeCommand(gtask, codeDict, flagList, self, codeStringChanger))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='float' and (multiple==True or prompt=='coords')

    def changeCommand(self, gtask, codeDict, flagList, widget, codeStringChanger):
        codeDictChanger(gtask, codeDict, str(widget.text()), codeStringChanger)

class SimpleFloat(QtGui.QDoubleSpinBox):
    def __init__(self, gtask, codeDict, flagList, codeStringChanger):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(SimpleFloat,self).__init__()
        self.valueChanged.connect(lambda: self.changeCommand(gtask, codeDict, flagList, self, codeStringChanger))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='float' and multiple==False

    def changeCommand(self, gtask, codeDict, flagList, widget, codeStringChanger):
        codeDictChanger(gtask, codeDict, str(widget.text()), codeStringChanger)





# now integer types
class MultipleInteger(QtGui.QLineEdit):
    def __init__(self, gtask, codeDict, flagList, codeStringChanger):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(MultipleInteger,self).__init__()
        self.textChanged.connect(lambda: self.changeCommand(gtask, codeDict, flagList, self, codeStringChanger))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='integer' and multiple==True

    def changeCommand(self, gtask, codeDict, flagList, widget, codeStringChanger):
        codeDictChanger(gtask, codeDict, str(widget.text()), codeStringChanger)

class SimpleInteger(QtGui.QSpinBox):
    def __init__(self, gtask, codeDict, flagList, codeStringChanger):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(SimpleInteger,self).__init__()
        self.valueChanged.connect(lambda: self.changeCommand(gtask, codeDict, flagList, self, codeStringChanger))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='integer' and multiple==False

    def changeCommand(self, gtask, codeDict, flagList, widget, codeStringChanger):
        codeDictChanger(gtask, codeDict, str(widget.text()), codeStringChanger)



class Flags(QtGui.QCheckBox):
    def __init__(self, gtask, codeDict, flagList, codeStringChanger):

        super(Flags,self).__init__(gtask['description'])
        self.stateChanged.connect(lambda: self.changeCommand(gtask, codeDict, flagList, self, codeStringChanger))

    def changeCommand(self, gtask, codeDict, flagList, widget, codeStringChanger):
        if widget.isChecked():
            if gtask['name'] not in flagList: # it means that there is no item for this widget in dict
                flagList.append(gtask['name'])
        else:
            flagList.remove(gtask['name']) # because we don't want to have not necessary items in dict
        codeStringChanger()



# default widget
class DefaultWidget(QtGui.QLineEdit):
    def __init__(self, gtask, codeDict, flagList, codeStringChanger):

        super(DefaultWidget,self).__init__()
        self.setText('TODO - Nobody expects the Spanish Inquisition') # just highlighting what should be done better
        palette=QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.Base,QtGui.QColor('red'))
        self.setPalette(palette)

        self.textChanged.connect(lambda: self.changeCommand(gtask, codeDict, flagList, self, codeStringChanger))

    def changeCommand(self,gtask, codeDict, flagList, widget, codeStringChanger):
        print gtask
        codeDictChanger(gtask, codeDict, str(widget.text()), codeStringChanger)




# methods for updating command

def codeDictChanger(gtask, codeDict, text, codeStringChanger):
    if text:
        try:
            codeDict[gtask['name']]=text
        except: # it means that there is no item for this widget in dict
            codeDict.update({gtask['name']:text})
    else:
        try:del codeDict[gtask['name']] # because we don't want to have not necessary items in dict
        except:pass
    codeStringChanger()



















