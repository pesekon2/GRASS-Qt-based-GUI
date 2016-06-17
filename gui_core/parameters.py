

from PyQt4 import QtGui
from types import TypeType
from PyQt4.QtCore import QObject
#from PyQt4.QtCore import pyqtSlot

class Factory():
    """
    Factory to decide which widget class should be used
    """
    @staticmethod
    def newWidget(gtask,code):
        """
        deciding which widget class should be used
        :param gtask: task for this widget
        :param code: runable and copyable code string
        :return:
        """
        classes = [j for (i,j) in globals().iteritems() if hasattr(j, 'canHandle')] #isinstance(j, TypeType)
        for oneClass in classes:
            if oneClass.canHandle(gtask['type'],gtask['multiple'],gtask['key_desc'],gtask['prompt'],gtask['values']):
                return oneClass(gtask,code)
        else:
            widget=QtGui.QLineEdit('TODO - Nobody expects the Spanish Inquisition')
            palette=QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.Base,QtGui.QColor('red'))
            widget.setPalette(palette)
            widget.textChanged.connect(lambda: CodeChanger(gtask,code,widget))
            return widget


# firstly, I define the widgets layout, then the widgets
class Parameters():
    def __init__(self, gtask, code):#, parent=None):
        #super(Parameters).__init__(parent)

        boxComplete=self.getLayout(gtask)

        try:
            self.widget = Factory().newWidget(gtask,code)
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
    def __init__(self, gtask, code):#,parent=QtGui.QLineEdit):
        """
        :param gtask: task for this widget
        :param code: runable and copyable code string
        """

        super(SqlQuery,self).__init__()
        self.textChanged.connect(lambda: CodeChanger(gtask,code,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return key_desc==['sql_query']

class Values(QtGui.QComboBox):
    def __init__(self, gtask, code):
        """
        :param gtask: task for this widget
        :param code: runable and copyable code string
        """

        super(Values,self).__init__()
        self.setEditable(True)
        self.addItems(gtask['values'])
        self.textChanged.connect(lambda: CodeChanger(gtask,code,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return (type=='string') and values and key_desc!=['sql_query'] # I think it should be done better in some next version





# now float types
class MultipleFloat(QtGui.QLineEdit):
    def __init__(self, gtask, code):
        """
        for float: multiple, coords
        :param gtask: task for this widget
        :param code: runable and copyable code string
        """

        super(MultipleFloat,self).__init__()
        self.textChanged.connect(lambda: CodeChanger(gtask,code,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='float' and (multiple==True or prompt=='coords')

class SimpleFloat(QtGui.QDoubleSpinBox):
    def __init__(self, gtask, code):
        """
        :param gtask: task for this widget
        :param code: runable and copyable code string
        """

        super(SimpleFloat,self).__init__()
        self.valueChanged.connect(lambda: CodeChanger(gtask,code,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='float' and multiple==False





# now integer types
class MultipleInteger(QtGui.QLineEdit):
    def __init__(self, gtask, code):
        """
        :param gtask: task for this widget
        :param code: runable and copyable code string
        """

        super(MultipleInteger,self).__init__()
        self.textChanged.connect(lambda: CodeChanger(gtask,code,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='integer' and multiple==True

class SimpleInteger(QtGui.QSpinBox):
    def __init__(self, gtask, code):
        """
        :param gtask: task for this widget
        :param code: runable and copyable code string
        """

        super(SimpleInteger,self).__init__()
        self.valueChanged.connect(lambda: CodeChanger(gtask,code,self))

    @staticmethod
    def canHandle(type,multiple,key_desc,prompt,values):
        return type=='integer' and multiple==False




class CodeChanger():
        """
        creates slots and signals into the code on below
        :param gtask:task for this widget
        :param code:code in string that user see on below
        :param widget:widget which should be edited
        """

        def __init__(self,gtask,code,widget):

            if type(widget) in [QtGui.QLineEdit,SqlQuery,MultipleFloat,MultipleInteger]:
                self.line_edit(gtask,code,widget)
            elif type(widget) in [SimpleFloat]:
                self.double_spin_box(gtask,code,widget)
            elif type(widget) in [Values]:
                self.combo_box(gtask,code,widget)
            elif type(widget) in [SimpleInteger]:
                self.spin_box(gtask,code,widget)

        def line_edit(self,gtask,code,widget):
            if widget.text():
                newCode=gtask['name']+'='+widget.text()
                code.setText(newCode)
            else:
                code.setText('')

        def double_spin_box(self,gtask,code,widget):
            if widget.text(): # should it write also 0,00?
                newCode=gtask['name']+'='+widget.text()
                code.setText(newCode)
            else:
                code.setText('')

        def spin_box(self,gtask,code,widget):
            if widget.text(): # should it write also 0,00?
                newCode=gtask['name']+'='+widget.text()
                code.setText(newCode)
            else:
                code.setText('')

        def combo_box(self,gtask,code,widget):
            if widget.currentText():
                newCode=gtask['name']+'='+widget.currentText()
                code.setText(newCode)
            else:
                code.setText('')



# to next versions: recreate CodeChanger (maybe dynamical reading by inheriting)



