

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
            if oneClass.canHandle(gtask['type'],gtask):
                return oneClass(gtask,code).get()
        else:return QtGui.QLabel('TODO')


# firstly, I define the widgets
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

class SqlQuery(QtGui.QLineEdit):
    def __init__(self, gtask, code):#,parent=QtGui.QLineEdit):
        """
        :param gtask: task for this widget
        :param code: runable and copyable code string
        """

        super(SqlQuery,self).__init__()
        self.textChanged.connect(lambda: CodeChanger(gtask,code,self))

    @staticmethod
    def canHandle(type,gtask):
        return gtask['key_desc']==['sql_query']

    def get(self):
        """

        :return:QLineEdit
        """

        return self

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
    def canHandle(type,gtask):
        return gtask['type']=='string' and gtask['values']

    def get(self):
        """

        :return:QComboBox with values
        """

        return self

class OtherStrings(QtGui.QComboBox):
    def __init__(self, gtask, code):
        """
        :param gtask: task for this widget
        :param code: runable and copyable code string
        """

        super(OtherStrings,self).__init__()
        self.setEditable(True)
        palette=QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.Base,QtGui.QColor('red'))
        self.setPalette(palette)
        self.textChanged.connect(lambda: CodeChanger(gtask,code,self))

    @staticmethod
    def canHandle(type,gtask):
        return gtask['type']=='string' and not gtask['values']

    def get(self):
        """

        :return:QComboBox
        """

        return self

class ParaFloat():
    def __init__(self,gtask,code):
        """
        :param gtask: task for this widget
        :param code: runable and copyable code string
        """

        self.gtask = gtask
        self.code = code

    @staticmethod
    def canHandle(type,gtask):
        return type=='float'

    def get(self):
        """

        :return:QLineEdit
        """

        if self.gtask['multiple']==True:
            box=QtGui.QLineEdit()
            box.textChanged.connect(lambda: CodeChanger(self.gtask,self.code,box))
        else:
            if self.gtask['prompt']==None:
                box=QtGui.QDoubleSpinBox()
                box.valueChanged.connect(lambda: CodeChanger(self.gtask,self.code,box))
            elif self.gtask['prompt']=='coords':
                box=QtGui.QLineEdit()
                box.textChanged.connect(lambda: CodeChanger(self.gtask,self.code,box))
            else:
                box=QtGui.QLabel('TODO')

        return box

class ParaInteger():
    def __init__(self,gtask,code):
        """
        :param gtask: task for this widget
        :param code: runable and copyable code string
        """

        self.code = code

    @staticmethod
    def canHandle(type,gtask):
        return type == 'integer'

    def get(self):
        """

        :return:QLineEdit
        """

        box=QtGui.QSpinBox()
        return box

class CodeChanger():
        """
        creates slots and signals into the code on below
        :param gtask:task for this widget
        :param code:code in string that user see on below
        :param widget:widget which should be edited
        """

        def __init__(self,gtask,code,widget):

            if type(widget) in [QtGui.QLineEdit,SqlQuery]:
                self.line_edit(gtask,code,widget)
            elif type(widget)==QtGui.QDoubleSpinBox:
                self.double_spin_box(gtask,code,widget)
            elif type(widget) in [Values,OtherStrings]:
                self.combo_box(gtask,code,widget)

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

        def combo_box(self,gtask,code,widget):
            if widget.currentText():
                newCode=gtask['name']+'='+widget.currentText()
                code.setText(newCode)
            else:
                code.setText('')



# poslat gtask



