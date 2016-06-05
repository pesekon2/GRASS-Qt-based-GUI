

from PyQt4 import QtGui


# firstly, I define the widgets
class Parameters(QtGui.QWidget):
    def __init__(self, gtask, parent=None):
        super(Parameters, self).__init__(parent)

        boxComplete=self.getLayout(gtask)

        try:
            if gtask['type'] in ('float'):
                self.widget = para_float(gtask).get()
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
    def __init__(self,gtask):
        """
        :param gtask: task for this widget
        """

        self.gtask = gtask

    def get(self):
        """

        :return:QLineEdit
        """

        if self.gtask['multiple']==True:
            box=QtGui.QLineEdit()
        else:
            box=QtGui.QDoubleSpinBox()

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
        print self.gtask
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

# get multiple



