#!/usr/bin/env python

import xml
import os
import sys,getopt
import re
from parameters import Parameters as newWidget
from PyQt4 import QtGui, uic
from PyQt4.QtXml import *
from PyQt4.QtCore import *
from grass.script import task as gtask
#import grass.script
from grass.script import start_command
from grass.pygrass.modules.interface import module
#from python\grass\pygrass\modules\interface


class NewGUI(QtGui.QMainWindow):
    def __init__(self, function, parent=None):
        app = QtGui.QApplication([])
        super(NewGUI, self).__init__(parent)

        self.setWindowTitle(self.get_title(function))
        self.create_gui(function)
        #print self.size()




        self.show()
        #print self.size()
        #print self.size()
        #self.resize(self.minimumSizeHint())
        #print self.size()
        sys.exit(app.exec_())

    def create_gui(self,function):
        """
        :param function: called function
        :return: completed gui
        """

        tabs,code=self.get_tabs(function)

        box=QtGui.QVBoxLayout()
        box.addWidget(self.get_description(function))
        box.addWidget(tabs)
        box.addWidget(self.basic_buttons())
        box.addWidget(self.horizontal_line())
        box.addWidget(code)
        box.setSpacing(10)
        completeGui=QtGui.QWidget()
        completeGui.setLayout(box)
        #print completeGui.size()
        #self.resize(self.minimumSize())

        self.setCentralWidget(completeGui)
        #print completeGui.size()

    def get_tabs(self,function):
        """
        :param function: called function
        :return: tabs
        """

        tabs = QtGui.QTabWidget()

        pageRequired=QtGui.QWidget()
        boxRequired=QtGui.QVBoxLayout()
        boxs={}

        pageOptional=QtGui.QWidget()
        boxOptional=QtGui.QVBoxLayout()
        pages={}

        pageSection={}
        boxsSection={}

        self.codeLayout=QtGui.QHBoxLayout()
        name = QtGui.QLabel(function)
        self.codeLayout.addWidget(name)
        codeWidget=QtGui.QWidget()

        # tabs for params
        for task in gtask.command_info(function)['params']:

            code=QtGui.QLabel()
            self.codeLayout.addWidget(code)
            widget=newWidget(task,code).newWidget()
            if task['required']==True:
                try:
                    pages.update({'Required':pageRequired})
                    boxs.update({'Required':boxRequired})
                except:pass
                boxs['Required'].addWidget(widget)

            elif task['guisection']:
                try:
                    pages[task['guisection']]
                except:
                    page=QtGui.QWidget()
                    box=QtGui.QVBoxLayout()
                    pageSection.update({task['guisection']:page})
                    boxsSection.update({task['guisection']:box})
                    pages.update({task['guisection']:pageSection[task['guisection']]})
                    boxs.update({task['guisection']:boxsSection[task['guisection']]})
                boxs[task['guisection']].addWidget(widget)

            else:
                try:
                    pages.update({'Optional':pageOptional})
                    boxs.update({'Optional':boxOptional})
                except:pass
                boxs['Optional'].addWidget(widget)

        #tabs for flags
        for task in gtask.command_info(function)['flags']:

            code=QtGui.QLabel()
            self.codeLayout.addWidget(code)
            widget=newWidget(task,code).newWidget()
            if task['guisection']:
                try:
                    pages[task['guisection']]
                except:
                    page=QtGui.QWidget()
                    box=QtGui.QVBoxLayout()
                    pageSection.update({task['guisection']:page})
                    boxsSection.update({task['guisection']:box})
                    pages.update({task['guisection']:pageSection[task['guisection']]})
                    boxs.update({task['guisection']:boxsSection[task['guisection']]})
                boxs[task['guisection']].addWidget(widget)

            else:
                try:
                    pages.update({'Optional':pageOptional})
                    boxs.update({'Optional':boxOptional})
                except:pass
                boxs['Optional'].addWidget(widget)

        #boxOptional.setContentsMargins(0,0,0,0)
        for i in pages:
            #print boxs[i].spacing() #*****************************
            #boxs[i].resize(boxs[i].minimumSizeHint())
            boxs[i].addStretch()
            layout=boxs[i]
            layout.setSpacing(0)
            pages[i].setLayout(layout)
            #pages[i].resize(pages[i].minimumSizeHint())
            tabs.addTab(pages[i],i)

        codeWidget.setLayout(self.codeLayout)

        return tabs,codeWidget

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

        runButton.clicked.connect(lambda: self.run_command())

        return buttons

    def horizontal_line(self):
        """
        creates a horizontal line
        :return: horizontal line
        """

        line = QtGui.QFrame()
        line.setFrameShape(QtGui.QFrame.HLine)
        line.setFrameShadow(QtGui.QFrame.Sunken)
        return line

    def get_command_one_string(self):
        """
        transforms widgets at the bottom of GUI into one executable string
        :return: command in one string
        """

        text = ''
        for i in range(self.codeLayout.count()-1):
            label = self.codeLayout.itemAt(i).widget().text() # getting again qlabel and the text
            if label:
                text = text + ' ' + label

        return text

    def run_command(self):

        print self.get_command_one_string()       # uncomment this to see the command
        #start_command(self.get_command_one_string())

opt,arg=getopt.getopt(sys.argv,'second parameter')

mainform = NewGUI(arg[1])
# hide 'help' checkbox, some cheats with 'string' widgets, help and output tabs, run_command change comment (after reading strings)