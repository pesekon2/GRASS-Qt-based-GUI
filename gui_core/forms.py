#!/usr/bin/env python

import xml
import os
import sys
import re
from PyQt4 import QtGui, uic
from PyQt4.QtXml import *
from PyQt4.QtCore import *
from PyQt4.QtGui import QAction, QIcon, QDialog, QDialogButtonBox, QFileDialog, QListWidgetItem, QMessageBox
from grass.script import task as gtask

#print gtask.command_info('r.buffer')
#print [p[0] for p in gtask.command_info('r.buffer')['keywords']]

class NewQuery(QtGui.QWidget):
    def __init__(self, function, parent=None):
        super(NewQuery, self).__init__(parent)
        self.setWindowTitle(self.get_title(function))
        grid = QtGui.QGridLayout()
        label = QtGui.QLabel('Here should be some widgets')
        grid.addWidget(label)
        grid.addWidget(QtGui.QLineEdit('hi Vaclav'))
        self.setLayout(grid)
        #self.resize(300,200)

    def get_title(self,function):
        self.title=[p for p in gtask.command_info(function)['keywords']]
        self.title=re.sub("'","",str(self.title))
        return self.title

command='v.buffer'
tasked=gtask.command_info('r.buffer')

app = QtGui.QApplication([])
mainform = NewQuery(command)
mainform.show()
#newchildform = NewQuery(command)
#newchildform.show()
app.exec_()
