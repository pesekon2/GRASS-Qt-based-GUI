

from PyQt4 import QtGui


# firstly, I define the widgets
class Parameters(QtGui.QWidget):
    def __init__(self, gtask, parent=None):
        super(Parameters, self).__init__(parent)
        try:
            if gtask['type'] in ('float', 'range', 'sql_query'):
                self.widget = para_float(gtask).get()
            else:
                self.widget=QtGui.QLabel('TODO')
        except:
            self.widget=QtGui.QCheckBox(gtask['description'])

    def newWidget(self):
        """

        :return:The widget
        """

        return self.widget

class para_float(QtGui.QLineEdit):
    def __init__(self,gtask):
        """
        :param gtask: task for this widget
        """
        print gtask

    def get(self):
        """

        :return:QLineEdit
        """

        box=QtGui.QLineEdit()
        return box





