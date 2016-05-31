

from PyQt4 import QtGui


# firstly, I define the widgets
class Parameters(QtGui.QWidget):
    def __init__(self, gtask, parent=None):
        super(Parameters, self).__init__(parent)

        boxComplete=self.getLayout(gtask)

        try:
            if gtask['type'] in ('float', 'range', 'sql_query'):
                self.widget = para_float(gtask).get()
            else:
                self.widget=QtGui.QLabel('TODO')
            boxComplete.addWidget(self.widget)

        except:
            self.widget=QtGui.QCheckBox(gtask['description'])
            boxComplete.addWidget(self.widget)
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
            description=QtGui.QLabel(gtask['description'])
            boxHeader.addWidget(description)
            boxHeader.addWidget(QtGui.QLabel('(%s=%s)' % (gtask['name'],gtask['type'])))
            description.setWordWrap(True)

            header=QtGui.QWidget()
            header.setLayout(boxHeader)

            layoutComplete=QtGui.QVBoxLayout()
            layoutComplete.addWidget(header)
            layoutComplete.setSpacing(0)
            layoutComplete.setMargin(0)
        except:layoutComplete=QtGui.QHBoxLayout() # flag

        return layoutComplete

class para_float(QtGui.QLineEdit):
    def __init__(self,gtask):
        """
        :param gtask: task for this widget
        """

    def get(self):
        """

        :return:QLineEdit
        """
# get multiple
        box=QtGui.QLineEdit()
        return box





