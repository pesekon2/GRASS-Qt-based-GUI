

from PyQt4 import QtGui
#from PyQt4.QtCore import pyqtSlot


# firstly, I define the widgets
class Parameters(QtGui.QWidget):
    def __init__(self, gtask, code, parent=None):
        super(Parameters, self).__init__(parent)

        boxComplete=self.getLayout(gtask)

        try:
            if gtask['type'] in ('float'):
                self.widget = para_float(gtask,code).get()
                #self.widget.textChanged.connect(lambda: self.change_code(gtask,code))
            elif gtask['type'] in ('string', 'name'):
                self.widget = para_string(gtask).get()
            elif gtask['type'] in ('integer'):
                self.widget = para_integer(gtask).get()
            else:
                self.widget=QtGui.QLabel('TODO')
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

class para_float(QtGui.QLineEdit):
    def __init__(self,gtask,code):
        """
        :param gtask: task for this widget
        """

        self.gtask = gtask
        self.code = code

    def get(self):
        """

        :return:QLineEdit
        """

        if self.gtask['multiple']==True:
            box=QtGui.QLineEdit()
            box.textChanged.connect(lambda: change_code(self.gtask,self.code,box))
        else:
            box=QtGui.QDoubleSpinBox()
            box.valueChanged.connect(lambda: change_code(self.gtask,self.code,box))

        return box

class para_string(QtGui.QComboBox):
    def __init__(self,gtask):
        """
        :param gtask: task for this widget
        """

        self.gtask = gtask

    def get(self):
        """

        :return:QLineEdit
        """

        if self.gtask['key_desc']==['sql_query']:
            box=QtGui.QLineEdit()
        else:
            box=QtGui.QComboBox()

        return box

class para_integer(QtGui.QSpinBox):
    def __init__(self,gtask):
        """
        :param gtask: task for this widget
        """

    def get(self):
        """

        :return:QLineEdit
        """

        box=QtGui.QSpinBox()
        return box

class change_code():
        """
        creates slots and signals into the code on below
        :param gtask:task for this widget
        :param code:code in string that user see on below
        :param widget:widget which should be edited
        """

        def __init__(self,gtask,code,widget):

            if type(widget)==QtGui.QLineEdit:
                self.line_edit(gtask,code,widget)
            elif type(widget)==QtGui.QDoubleSpinBox:
                self.double_spin_box(gtask,code,widget)

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