

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
        classes = [j for (i,j) in globals().iteritems() if hasattr(j, 'canHandle')] #isinstance(j, TypeType)
        for oneClass in classes:
            if oneClass.canHandle(gtask['type'],gtask['multiple'],gtask['key_desc'],gtask['prompt'],gtask['values']):
                return oneClass(gtask,function,codeDict,flagList,codeString)
        else:
            widget=QtGui.QLineEdit()
            widget.setText('TODO - Nobody expects the Spanish Inquisition') # just highlighting what should be done better
            palette=QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.Base,QtGui.QColor('red'))
            widget.setPalette(palette)
            widget.textChanged.connect(lambda: getCommandLine(gtask,function,codeDict,flagList,codeString,widget))

            def getCommandLine(gtask, function, codeDict, flagList, codeString,widget):
                if widget.text():
                    try:
                        codeDict[gtask['name']]=str(widget.text())
                    except: # it means that there is no item for this widget in dict
                        codeDict.update({gtask['name']:''})
                        codeDict[gtask['name']]=str(widget.text())
                else:
                    try:del codeDict[gtask['name']] # because we don't want to have not necessary items in dict
                    except:pass
                CodeChanger(gtask,function,codeDict,flagList,codeString,widget)

            return widget


# firstly, I define the widgets layout, then the widgets
class Parameters():
    def __init__(self, gtask, function, codeDict, flagList, codeString):#, parent=None):
        #super(Parameters).__init__(parent)

        boxComplete=self.getLayout(gtask)

        try:
            self.widget = Factory().newWidget(gtask, function, codeDict, flagList, codeString)
            if gtask['label'] and gtask['description']: # title is in label so we can use description as help/tooltip
                self.widget.setToolTip(gtask['description'])

            boxComplete.addWidget(self.widget)

        except:
            self.widget=QtGui.QCheckBox(gtask['description'])
            self.widget.stateChanged.connect(lambda: getCommandLine(gtask,function,codeDict,flagList,codeString,self.widget))
            boxComplete.addWidget(self.widget)
            boxComplete.addStretch()
            boxComplete.addWidget(QtGui.QLabel('(%s)' % gtask['name']))

            def getCommandLine(gtask, function, codeDict, flagList, codeString,widget):
                if widget.isChecked():
                    if gtask['name'] not in flagList: # it means that there is no item for this widget in dict
                        flagList.append(gtask['name'])
                else:
                    flagList.remove(gtask['name']) # because we don't want to have not necessary items in dict
                CodeChanger(gtask,function,codeDict,flagList,codeString,widget)

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
            #description.setWordWrap(True) #--------------------- DO I REALLY WANT TO WRAP IT? ---------------

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
        self.textChanged.connect(lambda: self.getCommandLine(gtask,function,codeDict,flagList,codeString,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return key_desc==['sql_query']

    def getCommandLine(self,gtask, function, codeDict, flagList, codeString,widget):
        if widget.text():
            try:
                codeDict[gtask['name']]=str(widget.text())
            except: # it means that there is no item for this widget in dict
                codeDict.update({gtask['name']:''})
                codeDict[gtask['name']]=str(widget.text())
        else:
            try:del codeDict[gtask['name']] # because we don't want to have not necessary items in dict
            except:pass
        CodeChanger(gtask,function,codeDict,flagList,codeString,widget)

class Cats(QtGui.QLineEdit): # maybe in future implement special widget when called from gui
    def __init__(self, gtask, function, codeDict, flagList, codeString):#,parent=QtGui.QLineEdit):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(Cats,self).__init__()
        self.textChanged.connect(lambda: self.getCommandLine(gtask,function,codeDict,flagList,codeString,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return prompt=='cats'

    def getCommandLine(self,gtask, function, codeDict, flagList, codeString,widget):
        if widget.text():
            try:
                codeDict[gtask['name']]=str(widget.text())
            except: # it means that there is no item for this widget in dict
                codeDict.update({gtask['name']:''})
                codeDict[gtask['name']]=str(widget.text())
        else:
            try:del codeDict[gtask['name']] # because we don't want to have not necessary items in dict
            except:pass
        CodeChanger(gtask,function,codeDict,flagList,codeString,widget)

class SimpleValues(QtGui.QComboBox):
    def __init__(self, gtask, function, codeDict, flagList, codeString):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(SimpleValues,self).__init__()
        self.setEditable(True)
        self.addItems(gtask['values'])
        self.textChanged.connect(lambda: self.getCommandLine(gtask,function,codeDict,flagList,codeString,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return (type=='string') and multiple==False and values

    def getCommandLine(self,gtask, function, codeDict, flagList, codeString,widget):
        if widget.currentText():
            try:
                codeDict[gtask['name']]=str(widget.currentText())
            except: # it means that there is no item for this widget in dict
                codeDict.update({gtask['name']:''})
                codeDict[gtask['name']]=str(widget.currentText())
        else:
            try:del codeDict[gtask['name']] # because we don't want to have not necessary items in dict
            except:pass
        CodeChanger(gtask,function,codeDict,flagList,codeString,widget)

class TreeComboBox(gselect.TreeComboBox):
    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='string' and key_desc!=['sql_query'] and (prompt=='raster' or prompt=='vector')

class BrowseFile(gselect.BrowseFile):
    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='string' and key_desc!=['sql_query'] and (prompt=='file')

class MultipleValues(gselect.MultipleValues):
    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return (type=='string') and multiple==True and values





# now float types
class MultipleFloat(QtGui.QLineEdit):
    def __init__(self, gtask, function, codeDict, flagList, codeString):
        """
        for float: multiple, coords
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(MultipleFloat,self).__init__()
        self.textChanged.connect(lambda: self.getCommandLine(gtask,function,codeDict,flagList,codeString,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='float' and (multiple==True or prompt=='coords')

    def getCommandLine(self,gtask, function, codeDict, flagList, codeString,widget):
        if widget.text():
            try:
                codeDict[gtask['name']]=str(widget.text())
            except: # it means that there is no item for this widget in dict
                codeDict.update({gtask['name']:''})
                codeDict[gtask['name']]=str(widget.text())
        else:
            try:del codeDict[gtask['name']] # because we don't want to have not necessary items in dict
            except:pass
        CodeChanger(gtask,function,codeDict,flagList,codeString,widget)

class SimpleFloat(QtGui.QDoubleSpinBox):
    def __init__(self, gtask, function, codeDict, flagList, codeString):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(SimpleFloat,self).__init__()
        self.valueChanged.connect(lambda: self.getCommandLine(gtask,function,codeDict,flagList,codeString,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='float' and multiple==False

    def getCommandLine(self,gtask, function, codeDict, flagList, codeString,widget):
        if widget.text():
            try:
                codeDict[gtask['name']]=str(widget.text())
            except: # it means that there is no item for this widget in dict
                codeDict.update({gtask['name']:''})
                codeDict[gtask['name']]=str(widget.text())
        else:
            try:del codeDict[gtask['name']] # because we don't want to have not necessary items in dict
            except:pass
        CodeChanger(gtask,function,codeDict,flagList,codeString,widget)





# now integer types
class MultipleInteger(QtGui.QLineEdit):
    def __init__(self, gtask, function, codeDict, flagList, codeString):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(MultipleInteger,self).__init__()
        self.textChanged.connect(lambda: self.getCommandLine(gtask,function,codeDict,flagList,codeString,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='integer' and multiple==True

    def getCommandLine(self,gtask, function, codeDict, flagList, codeString,widget):
        if widget.text():
            try:
                codeDict[gtask['name']]=str(widget.text())
            except: # it means that there is no item for this widget in dict
                codeDict.update({gtask['name']:''})
                codeDict[gtask['name']]=str(widget.text())
        else:
            try:del codeDict[gtask['name']] # because we don't want to have not necessary items in dict
            except:pass
        CodeChanger(gtask,function,codeDict,flagList,codeString,widget)

class SimpleInteger(QtGui.QSpinBox):
    def __init__(self, gtask, function, codeDict, flagList, codeString):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(SimpleInteger,self).__init__()
        self.valueChanged.connect(lambda: self.getCommandLine(gtask,function,codeDict,flagList,codeString,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='integer' and multiple==False

    def getCommandLine(self,gtask, function, codeDict, flagList, codeString,widget):
        if widget.text():
            try:
                codeDict[gtask['name']]=str(widget.text())
            except: # it means that there is no item for this widget in dict
                codeDict.update({gtask['name']:''})
                codeDict[gtask['name']]=str(widget.text())
        else:
            try:del codeDict[gtask['name']] # because we don't want to have not necessary items in dict
            except:pass
        CodeChanger(gtask,function,codeDict,flagList,codeString,widget)




class CodeChanger():
        """
        creates slots and signals into the qlabel on below
        :param gtask:task for this widget
        :param function: name of module
        :param codeDict: Dictionary with values for every widget
        :param codeString: the string that user see on below
        :param widget:widget which should be edited

        """

        def __init__(self,gtask, function, codeDict, flagList, codeString,widget):

            flags=''
            for i in flagList:
                if len(i)==1: flags = flags + ' -' + i
                else: flags = flags + ' --' + i
            codeString.setText(function+flags+' '
                               +' '.join('{}={}'.format(key, val) for key, val in codeDict.items()))



















