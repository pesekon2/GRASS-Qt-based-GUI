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


class NewGUI(QtGui.QMainWindow):
    def __init__(self, module, parent=None):
        app = QtGui.QApplication([])
        super(NewGUI, self).__init__(parent)

        self.setWindowTitle(self.get_title(module))
        self.create_gui(module)

        self.show()
        sys.exit(app.exec_())

    def create_gui(self,module):
        """
        :param module: called module
        :return: completed gui
        """

        tabs,codeString=self.get_tabs(module)

        box=QtGui.QVBoxLayout()
        box.addWidget(self.get_description(module))
        box.addWidget(tabs)
        box.addWidget(self.basic_buttons(module))
        box.addWidget(self.horizontal_line())
        box.addWidget(codeString)
        box.setSpacing(10)
        completeGui=QtGui.QWidget()
        completeGui.setLayout(box)
        #print completeGui.size()
        #self.resize(self.minimumSize())

        self.setCentralWidget(completeGui)

        print self.width(),self.height()
        #self.setFixedHeight(300)
        #print completeGui.size()

    def get_tabs(self,module):
        """
        :param module: called module
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
        codeString=QtGui.QTextEdit(module)
        codeString.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        codeString.setReadOnly(True)
        codeString.setFixedHeight(QtGui.QLineEdit().sizeHint().height()*2)

        # tabs for params
        for task in gtask.command_info(module)['params']:

            widget=newWidget(task,module,self.codeDict,self.flagList,codeString).newWidget()

            if task['guisection']:
                try:
                    pageSection[task['guisection']]
                except:
                    page=QtGui.QWidget()
                    #page.setFrameShape(QtGui.QFrame.NoFrame)
                    #page.setAutoFillBackground(True)
                    #page.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                    box=QtGui.QVBoxLayout()
                    pageSection.update({task['guisection']:page})
                    boxsSection.update({task['guisection']:box})
                    pages.update({task['guisection']:pageSection[task['guisection']]})
                    boxs.update({task['guisection']:boxsSection[task['guisection']]})
                boxs[task['guisection']].addWidget(widget)

            elif task['required']==True:
                try:
                    pages.update({'Required':pageRequired})
                    boxs.update({'Required':boxRequired})
                except:pass
                boxs['Required'].addWidget(widget)

            else:
                try:
                    pages.update({'Optional':pageOptional})
                    boxs.update({'Optional':boxOptional})
                except:pass
                boxs['Optional'].addWidget(widget)



        #tabs for flags
        for task in gtask.command_info(module)['flags']:

            widget=newWidget(task,module,self.codeDict,self.flagList,codeString).newWidget()
            if task['guisection']:
                try:
                    pageSection[task['guisection']]
                except:
                    page=QtGui.QWidget()
                    #page.setFrameShape(QtGui.QFrame.NoFrame)
                    #page.setAutoFillBackground(True)
                    #page.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
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

        for i in pages:
            boxs[i].addStretch()
            layout=boxs[i]
            layout.setSpacing(0)
            #layout.setContentsMargins(0,0,0,0)
            widget=QtGui.QWidget()
            widget.setLayout(layout)
            #pages[i].setLayout(layout)
            bla=QtGui.QLineEdit()
            #print bla.rgb()
            #QtGui.QColor.setCm
            print pages[i].palette().color(widget.backgroundRole()).red(),pages[i].palette().color(widget.backgroundRole()).green()
            print pages[i].palette().color(pages[i].backgroundRole()).blue()
            print pages[i].palette().color(pages[i].backgroundRole()).red()
            print pages[i].palette().color(widget.backgroundRole()).getCmyk()
            print pages[i].palette().color(widget.backgroundRole()).rgb()
            print ''
            #b = widget.styleSheet()
            #widget.setStyleSheet(pageRequired.styleSheet())
            #widget.setPalette(QtGui.QLineEdit().palette())
            #print QtGui.QLineEdit().palette()
            #widget.setAutoFillBackground(True)
            #print widget.autoFillBackground()
            a = QtGui.QScrollArea()
            palette=a.palette()
            print tabs.palette().color(tabs.backgroundRole()).getRgb()
            print tabs.palette().color(tabs.backgroundRole()).rgb()
            palette.setColor(a.backgroundRole(), self.palette().color(pages[i].backgroundRole()))
            a.setPalette(palette)
            aha=widget.palette()
            #print pages[i].palette().color(widget.backgroundRole()).rgb()
            #print a.palette().color(widget.backgroundRole()).rgb()
            #a.bac
            a.setWidget(widget)
            a.setWidgetResizable(True)
            a.setFrameShape(QtGui.QFrame.NoFrame)
            a.setAutoFillBackground(True)
            a.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            a.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            #a.setPalette(QtGui.QLineEdit().palette())
            #a.setAutoFillBackground(True)
            #widget.setAttribute(Qt.WA_TranslucentBackground)
            #widget.setStyleSheet(b)
            #a.setStyleSheet("background-color:transparent;")
            #a.setAttribute(Qt.WA_TranslucentBackground)
            #print widget.color.red()
            #a.setStyleSheet("color:white")
            #print a.numColors()
            #myLayout=QtGui.QHBoxLayout()
            #myLayout.addWidget(widget)
            #myLayout.addWidget(QtGui.QScrollBar())
            #bla=QtGui.QWidget()
            #bla.setLayout(myLayout)
            #my2Ly=QtGui.QHBoxLayout()
            #my2Ly.addWidget(bla)
            #my2Ly.addWidget(QtGui.QScrollBar())
            #a.setStyleSheet("background-color:transparent")
            #a.widget().setStyleSheet("background-color:green")
            #a.setPalette(QtGui.QPalette.Normal)
            #print tabs.numColors()
            #a.
            #print a.autoFillBackground()
            #widget.setAutoFillBackground(False)
            #a.setBackgroundRole(tabs.backgroundRole())
            #a.setEnabled(True)
            #a.setStyleSheet("background-color:%s" % str(tabs.numColors()))
            #a.setBackgroundRole(QtGui.QPalette.NoRole)
            newLayout = QtGui.QVBoxLayout()
            newLayout.addWidget(a)
            newLayout.setContentsMargins(1,1,1,1)

            #x = QtGui.QWidget()
            #x.setLayout(my2Ly)
            #newnewLayout = QtGui.QVBoxLayout()
            #newnewLayout.addWidget(x)
            #x.setAutoFillBackground(True)
            #newnewLayout.setContentsMargins(0,0,0,0)
            #a.setLayout(layout)
            #a.addScrollBarWidget(widget)

            pages[i].setLayout(newLayout)
            #pages[i].setAutoFillBackground(True)
            #print pages[i].autoFillBackground()
            #print layout.height()
            #print widget.height()
            #if widget.height()>300:
            #    scrollLayout = QtGui.QHBoxLayout()
            #    scrollLayout.addWidget(widget)
            #    scrollLayout.addWidget(QtGui.QScrollBar())
            #    pages[i].setLayout(scrollLayout)
            #else:
            #    pages[i].setLayout(layout)

        #self.setFixedHeight(500)
        #self.setFixedWidth(650)


        tabs.addTab(pageRequired,'Required')
        for i in pageSection:
            tabs.addTab(pages[i],i)
        tabs.addTab(pageOptional,'Optional')
        #tabs.setPalette(QtGui.QApplication.palette())
        #tabs.tab
        #print tabs.tabBar().color(tabs.backgroundRole()).getRgb()
        #tabs.widget(1).palette().color(tabs.backgroundRole()).getRgb()

        return tabs,codeString

    def get_title(self,module):
        """
        :param module: called module
        :return: new title of the window with parameters
        """

        self.title=[p for p in gtask.command_info(module)['keywords']]
        self.title=re.sub("'","",module + " " + str(self.title))
        return self.title


    def get_description(self,module):
        """
        :param module: called module
        :return: label with module description
        """

        text = gtask.command_info(module)['description']
        description = QtGui.QLabel(text)
        description.setWordWrap(True)
        return description

    def basic_buttons(self,module):
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

        closeButton.clicked.connect(lambda: self.close())
        helpButton.clicked.connect(lambda: run_command(module,'help'))
        runButton.clicked.connect(lambda: self.run_command(module))

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

    def run_command(self,module):
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
            run_command(module, flags=flags, **paramsLongFlags)
        else:
            run_command(module, flags=flags, **self.codeDict)

opt,arg=getopt.getopt(sys.argv,'second parameter')

mainform = NewGUI(arg[1])

# help and output tabs