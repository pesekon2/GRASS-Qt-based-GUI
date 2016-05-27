#!/usr/bin/env python

import xml
import os
import sys,getopt
import re
from PyQt4 import QtGui, uic
from PyQt4.QtXml import *
from PyQt4.QtCore import *
from grass.script import task as gtask



class NewGUI(QtGui.QMainWindow):
    def __init__(self, function, parent=None):
        app = QtGui.QApplication([])
        super(NewGUI, self).__init__(parent)

        self.setWindowTitle(self.get_title(function))
        self.create_gui(function)

        #self.resize(300,200)

        self.show()
        sys.exit(app.exec_())

    def create_gui(self,function):
        """
        :param function: called function
        :return: completed gui
        """

        box=QtGui.QVBoxLayout()
        box.addWidget(self.get_description(function))
        box.addWidget(self.get_tabs(function))
        box.addWidget(self.basic_buttons())
        box.setSpacing(10)
        completeGui=QtGui.QWidget()
        completeGui.setLayout(box)

        self.setCentralWidget(completeGui)

    def get_tabs(self,function):
        """
        :param function: called function
        :return: tabs
        """

        tabs = QtGui.QTabWidget()

        pageRequired=QtGui.QWidget()
        boxRequired=QtGui.QVBoxLayout()
        #box1.addWidget(QtGui.QLineEdit())
        #page1.setLayout(box1)

        pageOptional=QtGui.QWidget()
        boxOptional=QtGui.QVBoxLayout()
        pages={}

        # tabs for params
        for task in gtask.command_info(function)['params']:

            if task['required']==True:
                try:
                    pages.update({'Required':pageRequired})
                except:pass
            elif task['guisection']:
                try:
                    pages[task['guisection']]
                except:
                    page=QtGui.QWidget()
                    pages.update({task['guisection']:page})
            else:
                try:
                    pages.update({'Optional':pageOptional})
                except:pass

        #tabs for flags
        for task in gtask.command_info(function)['flags']:

            if task['guisection']:
                try:
                    pages[task['guisection']]
                except:
                    page=QtGui.QWidget()
                    pages.update({task['guisection']:page})
            else:
                try:
                    pages.update({'Optional':pageOptional})
                except:pass

        for i in pages:
            tabs.addTab(pages[i],i)

        return tabs

    def get_title(self,function):
        """
        :param function: called function
        :return: new title of the window with parameters
        """

        self.title=[p for p in gtask.command_info(function)['keywords']]
        self.title=re.sub("'","",function + " " + str(self.title))
        return self.title


    def get_description(self,function):
        """
        :param function: called function
        :return: label with function description
        """

        text = gtask.command_info(function)['description']
        description = QtGui.QLabel(text)
        description.setWordWrap(True)
        return description

    def basic_buttons(self):
        """
        :parameter: no
        :return: 4 basic buttons at the bottom of GUI
        """

        closeButton=QtGui.QPushButton('Close')
        runButton=QtGui.QPushButton('Run')
        runButton.setStyleSheet('QPushButton {color: green;}')
        copyButton=QtGui.QPushButton('Copy')
        helpButton=QtGui.QPushButton('Help')

        layout=QtGui.QHBoxLayout()
        layout.addWidget(closeButton)
        layout.addWidget(runButton)
        layout.addWidget(copyButton)
        layout.addWidget(helpButton)
        buttons=QtGui.QWidget()
        buttons.setLayout(layout)

        return buttons

opt, arg=getopt.getopt(sys.argv,'second parameter')
mainform = NewGUI(arg[1])

# usage, need to update tabs