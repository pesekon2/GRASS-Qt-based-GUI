

from PyQt4 import QtGui


# firstly, I define the widgets
class Parameters(QtGui.QWidget):
    def __init__(self, gtask, parent=None):

        super(Parameters, self).__init__(parent)
        if gtask['type'] in ('float', 'range', 'sql_query'):
            self.widget=self.float(gtask)
        else:
            self.widget=QtGui.QLabel('TODO')

    def newWidget(self):
        """

        :return:The widget
        """

        return self.widget

    def float(self,gtask):
        """
        :param gtask: task for this widget
        :return: QLineEdit
        """

        box=QtGui.QLineEdit()
        return box
