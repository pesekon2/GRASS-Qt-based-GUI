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
from grass.script import run_command
from grass.pygrass.modules.interface import module


class NewGUI(QtGui.QMainWindow):
    def __init__(self, function, parent=None):
        app = QtGui.QApplication([])
        super(NewGUI, self).__init__(parent)

        self.setWindowTitle(self.get_title(function))
        self.create_gui(function)

        self.show()
        sys.exit(app.exec_())

    def create_gui(self,function):
        """
        :param function: called function
        :return: completed gui
        """

        tabs,codeString=self.get_tabs(function)

        box=QtGui.QVBoxLayout()
        box.addWidget(self.get_description(function))
        box.addWidget(tabs)
        box.addWidget(self.basic_buttons(function))
        box.addWidget(self.horizontal_line())
        box.addWidget(codeString)
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

        self.codeDict={}
        self.flagList=[]
        codeString=QtGui.QTextEdit(function)
        codeString.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        codeString.setReadOnly(True)
        codeString.setFixedHeight(QtGui.QLineEdit().sizeHint().height()*2)

        # tabs for params
        for task in gtask.command_info(function)['params']:

            widget=newWidget(task,function,self.codeDict,self.flagList,codeString).newWidget()
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

            widget=newWidget(task,function,self.codeDict,self.flagList,codeString).newWidget()
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
                if not task['name'] == 'help': # we don't have to see help everywhere
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

        return tabs,codeString

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

    def basic_buttons(self,function):
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

        helpButton.clicked.connect(lambda: run_command(function,'help'))
        runButton.clicked.connect(lambda: self.run_command(function))

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

    def run_command(self,function):
        """
        runs the command
        """

        flags=''
        longFlags={}
        for i in self.flagList:
            if len(i)==1: flags = flags + i
            else: longFlags.update({i:True})

        if longFlags:
            paramsLongFlags={}
            paramsLongFlags.update(longFlags)
            paramsLongFlags.update(self.codeDict)
            run_command(function, *flags, **paramsLongFlags)
        else:
            run_command(function, *flags, **self.codeDict)

opt,arg=getopt.getopt(sys.argv,'second parameter')

mainform = NewGUI(arg[1])

# some cheats with 'string' widgets, help and output tabs