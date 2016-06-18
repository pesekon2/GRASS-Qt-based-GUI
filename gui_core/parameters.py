

from PyQt4 import QtGui
from types import TypeType
from PyQt4.QtCore import QModelIndex,QEvent,Qt,QObject
#from PyQt4.QtCore import pyqtSlot
from grass import script
import gselect

class Factory():
    """
    Factory to decide which widget class should be used
    """
    @staticmethod
    def newWidget(gtask,function,codeDict,codeString):
        """
        deciding which widget class should be used
        :param gtask: task for this widget
        :param : runable and copyable  string
        :return:
        """
        classes = [j for (i,j) in globals().iteritems() if hasattr(j, 'canHandle')] #isinstance(j, TypeType)
        for oneClass in classes:
            if oneClass.canHandle(gtask['type'],gtask['multiple'],gtask['key_desc'],gtask['prompt'],gtask['values']):
                return oneClass(gtask,function,codeDict,codeString)
        else:
            widget=QtGui.QLineEdit()
            widget.setText('TODO - Nobody expects the Spanish Inquisition')
            palette=QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.Base,QtGui.QColor('red'))
            widget.setPalette(palette)
            widget.textChanged.connect(lambda: CodeChanger(gtask,function,codeDict,codeString,widget))
            return widget


# firstly, I define the widgets layout, then the widgets
class Parameters():
    def __init__(self, gtask, function, codeDict,codeString):#, parent=None):
        #super(Parameters).__init__(parent)

        boxComplete=self.getLayout(gtask)

        try:
            self.widget = Factory().newWidget(gtask, function, codeDict,codeString)
            boxComplete.addWidget(self.widget)

        except:
            self.widget=QtGui.QCheckBox(gtask['description'])
            boxComplete.addWidget(self.widget)
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
    def __init__(self, gtask,function,codeDict,codeString):#,parent=QtGui.QLineEdit):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(SqlQuery,self).__init__()
        self.textChanged.connect(lambda: CodeChanger(gtask,function,codeDict,codeString,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return key_desc==['sql_query']

class Values(QtGui.QComboBox):
    def __init__(self, gtask, function, codeDict,codeString):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(Values,self).__init__()
        self.setEditable(True)
        self.addItems(gtask['values'])
        self.textChanged.connect(lambda: CodeChanger(gtask,function,codeDict,codeString,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return (type=='string') and values # I think it should be done better in some next version

class TreeComboBox(gselect.TreeComboBox):
    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='string' and key_desc!=['sql_query'] and (prompt=='raster' or prompt=='vector')





# now float types
class MultipleFloat(QtGui.QLineEdit):
    def __init__(self, gtask, function, codeDict,codeString):
        """
        for float: multiple, coords
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(MultipleFloat,self).__init__()
        self.textChanged.connect(lambda: CodeChanger(gtask,function,codeDict,codeString,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='float' and (multiple==True or prompt=='coords')

class SimpleFloat(QtGui.QDoubleSpinBox):
    def __init__(self, gtask, function, codeDict,codeString):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(SimpleFloat,self).__init__()
        self.valueChanged.connect(lambda: CodeChanger(gtask,function,codeDict,codeString,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='float' and multiple==False





# now integer types
class MultipleInteger(QtGui.QLineEdit):
    def __init__(self, gtask, function, codeDict,codeString):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(MultipleInteger,self).__init__()
        self.textChanged.connect(lambda: CodeChanger(gtask,function,codeDict,codeString,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='integer' and multiple==True

class SimpleInteger(QtGui.QSpinBox):
    def __init__(self, gtask, function, codeDict,codeString):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(SimpleInteger,self).__init__()
        self.valueChanged.connect(lambda: CodeChanger(gtask,function,codeDict,codeString,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='integer' and multiple==False




class CodeChanger():
        """
        creates slots and signals into the qlabel on below
        :param gtask:task for this widget
        :param function: name of module
        :param codeDict: Dictionary with values for every widget
        :param codeString: the string that user see on below
        :param widget:widget which should be edited

        """

        def __init__(self,gtask,function,codeDict,codeString,widget):

            if type(widget) in [QtGui.QLineEdit,SqlQuery,MultipleFloat,MultipleInteger]:
                self.line_edit(gtask,function,codeDict,codeString,widget)
            elif type(widget) in [SimpleFloat]:
                self.double_spin_box(gtask,function,codeDict,codeString,widget)
            elif type(widget) in [Values,TreeComboBox]:
                self.combo_box(gtask,function,codeDict,codeString,widget)
            elif type(widget) in [SimpleInteger]:
                self.spin_box(gtask,function,codeDict,codeString,widget)

        def line_edit(self,gtask,function,codeDict,codeString,widget):
            if widget.text():
                try:
                    codeDict[gtask['name']]=str(widget.text())
                    codeString.setText(function+' '+', '.join('{}={}'.format(key, val) for key, val in codeDict.items()))
                except: # it means that there is no item for this widget in dict
                    codeDict.update({gtask['name']:''})
                    codeDict[gtask['name']]=str(widget.text())
                    codeString.setText(function+' '+', '.join('{}={}'.format(key, val) for key, val in codeDict.items()))
            else:
                if codeDict[gtask['name']]:del codeDict[gtask['name']] # because we don't want to have not necessary items in dict
                codeString.setText(function+' '+', '.join('{}={}'.format(key, val) for key, val in codeDict.items()))

        def double_spin_box(self,gtask,function,codeDict,codeString,widget):
            if widget.text():
                try:
                    codeDict[gtask['name']]=str(widget.text())
                    codeString.setText(function+' '+', '.join('{}={}'.format(key, val) for key, val in codeDict.items()))
                except: # it means that there is no item for this widget in dict
                    codeDict.update({gtask['name']:''})
                    codeDict[gtask['name']]=str(widget.text())
                    codeString.setText(function+' '+', '.join('{}={}'.format(key, val) for key, val in codeDict.items()))
            else:
                if codeDict[gtask['name']]:del codeDict[gtask['name']] # because we don't want to have not necessary items in dict
                codeString.setText(function+' '+', '.join('{}={}'.format(key, val) for key, val in codeDict.items()))

        def spin_box(self,gtask,function,codeDict,codeString,widget):
            if widget.text():
                try:
                    codeDict[gtask['name']]=str(widget.text())
                    codeString.setText(function+' '+', '.join('{}={}'.format(key, val) for key, val in codeDict.items()))
                except: # it means that there is no item for this widget in dict
                    codeDict.update({gtask['name']:''})
                    codeDict[gtask['name']]=str(widget.text())
                    codeString.setText(function+' '+', '.join('{}={}'.format(key, val) for key, val in codeDict.items()))
            else:
                if codeDict[gtask['name']]:del codeDict[gtask['name']] # because we don't want to have too not necessary in dict
                codeString.setText(function+' '+', '.join('{}={}'.format(key, val) for key, val in codeDict.items()))

        def combo_box(self,gtask,function,codeDict,codeString,widget):
            if widget.currentText():
                try:
                    codeDict[gtask['name']]=str(widget.currentText())
                    codeString.setText(function+' '+', '.join('{}={}'.format(key, val) for key, val in codeDict.items()))
                except: # it means that there is no item for this widget in dict
                    codeDict.update({gtask['name']:''})
                    codeDict[gtask['name']]=str(widget.currentText())
                    codeString.setText(function+' '+', '.join('{}={}'.format(key, val) for key, val in codeDict.items()))
            else:
                if codeDict[gtask['name']]:del codeDict[gtask['name']] # because we don't want to have not necessary items in dict
                codeString.setText(function+' '+', '.join('{}={}'.format(key, val) for key, val in codeDict.items()))



# to next versions: recreate CodeChanger (maybe dynamical reading by inheriting), when there is no text in widget



