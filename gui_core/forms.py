#!/usr/bin/env python

import sys
import os
import getopt
import re
from parameters import Parameters as newWidget
from PyQt4 import QtGui
from PyQt4.QtCore import *
from grass.script import task as gtask
from grass.script import run_command


GUIDIR   = os.path.join(os.getenv("GISBASE"), "gui")
ICONDIR  = os.path.join(GUIDIR, "icons")
IMGDIR   = os.path.join(GUIDIR, "images")


class NewGUI(QtGui.QMainWindow):
    def __init__(self, module, parent=None):
        app = QtGui.QApplication([])
        super(NewGUI, self).__init__(parent)

        self.setWindowTitle(self.get_title(module))
        icon = QtGui.QIcon(os.path.join(ICONDIR,'grass-48x48.png'))
        #icon.
        self.setWindowIcon(icon)
        self.create_gui(module)

        self.show()
        sys.exit(app.exec_())

    def create_gui(self, module):
        """
        :param module: called module
        :return: completed gui
        """

        tabs, code_string = self.get_tabs(module)

        box = QtGui.QVBoxLayout()
        box.addWidget(self.get_description(module))
        box.addWidget(tabs)
        box.addWidget(self.basic_buttons(module))
        box.addWidget(self.horizontal_line())
        box.addWidget(code_string)
        box.setSpacing(10)
        complete_gui = QtGui.QWidget()
        complete_gui.setLayout(box)
        # print complete_gui.size()
        # self.resize(self.minimumSize())

        self.setCentralWidget(complete_gui)

        print self.width(), self.height()
        # self.setFixedHeight(300)
        # print complete_gui.size()

    def get_tabs(self, module):
        """
        :param module: called module
        :return: tabs
        """

        tabs = QtGui.QTabWidget()

        page_required = QtGui.QWidget()
        box_required = QtGui.QVBoxLayout()
        boxs = {}

        page_optional = QtGui.QWidget()
        box_optional = QtGui.QVBoxLayout()
        pages = {}

        page_section = {}
        boxs_section = {}

        self.codeDict = {}
        self.flagList = []
        code_string = QtGui.QTextEdit(module)
        code_string.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        code_string.setReadOnly(True)
        code_string.setFixedHeight(QtGui.QLineEdit().sizeHint().height()*2)

        # tabs for params
        for task in gtask.command_info(module)['params']:

            widget = newWidget(task, module, self.codeDict, self.flagList,
                               code_string).new_widget()

            if task['guisection']:
                try:
                    page_section[task['guisection']]
                except:
                    page = QtGui.QWidget()
                    #page.setFrameShape(QtGui.QFrame.NoFrame)
                    #page.setAutoFillBackground(True)
                    #page.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                    box = QtGui.QVBoxLayout()
                    page_section.update({task['guisection']: page})
                    boxs_section.update({task['guisection']: box})
                    pages.update({task['guisection']:
                                 page_section[task['guisection']]})
                    boxs.update({task['guisection']:
                                boxs_section[task['guisection']]})
                boxs[task['guisection']].addWidget(widget)

            elif task['required'] is True:
                try:
                    pages.update({'Required': page_required})
                    boxs.update({'Required': box_required})
                except:
                    pass
                boxs['Required'].addWidget(widget)

            else:
                try:
                    pages.update({'Optional': page_optional})
                    boxs.update({'Optional': box_optional})
                except:
                    pass
                boxs['Optional'].addWidget(widget)

        #tabs for flags
        for task in gtask.command_info(module)['flags']:

            widget = newWidget(task, module, self.codeDict, self.flagList,
                               code_string).new_widget()
            if task['guisection']:
                try:
                    page_section[task['guisection']]
                except:
                    page = QtGui.QWidget()
                    # page.setFrameShape(QtGui.QFrame.NoFrame)
                    # page.setAutoFillBackground(True)
                    # page.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                    box = QtGui.QVBoxLayout()
                    page_section.update({task['guisection']: page})
                    boxs_section.update({task['guisection']: box})
                    pages.update({task['guisection']:
                                 page_section[task['guisection']]})
                    boxs.update({task['guisection']:
                                boxs_section[task['guisection']]})
                boxs[task['guisection']].addWidget(widget)

            else:
                try:
                    pages.update({'Optional': page_optional})
                    boxs.update({'Optional': box_optional})
                except:
                    pass
                if not task['name'] == 'help':
                    boxs['Optional'].addWidget(widget)
                    # we don't have to see help everywhere

        for i in pages:
            boxs[i].addStretch()
            layout = boxs[i]
            layout.setSpacing(0)
            #layout.setContentsMargins(0,0,0,0)
            widget = QtGui.QWidget()
            widget.setLayout(layout)
            #pages[i].setLayout(layout)
            bla = QtGui.QLineEdit()
            #print bla.rgb()
            #QtGui.QColor.setCm
            print pages[i].palette().color(widget.backgroundRole()).red()
            print pages[i].palette().color(widget.backgroundRole()).green()
            print pages[i].palette().color(pages[i].backgroundRole()).blue()
            print pages[i].palette().color(pages[i].backgroundRole()).red()
            print pages[i].palette().color(widget.backgroundRole()).getCmyk()
            print pages[i].palette().color(widget.backgroundRole()).rgb()
            print ''
            #b = widget.styleSheet()
            #widget.setStyleSheet(page_required.styleSheet())
            #widget.setPalette(QtGui.QLineEdit().palette())
            #print QtGui.QLineEdit().palette()
            #widget.setAutoFillBackground(True)
            #print widget.autoFillBackground()
            a = QtGui.QScrollArea()
            palette = a.palette()
            print tabs.palette().color(tabs.backgroundRole()).getRgb()
            print tabs.palette().color(tabs.backgroundRole()).rgb()
            palette.setColor(
                a.backgroundRole(),
                QtGui.QLineEdit().palette().color(QtGui.QLineEdit().
                                                  backgroundRole()))
            a.setPalette(palette)
            aha = widget.palette()
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
            new_layout = QtGui.QVBoxLayout()
            new_layout.addWidget(a)
            new_layout.setContentsMargins(1, 1, 1, 1)

            #x = QtGui.QWidget()
            #x.setLayout(my2Ly)
            #newnew_layout = QtGui.QVBoxLayout()
            #newnew_layout.addWidget(x)
            #x.setAutoFillBackground(True)
            #newnew_layout.setContentsMargins(0,0,0,0)
            #a.setLayout(layout)
            #a.addScrollBarWidget(widget)

            pages[i].setLayout(new_layout)
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

        tabs.addTab(page_required, 'Required')
        for i in page_section:
            tabs.addTab(pages[i], i)
        tabs.addTab(page_optional, 'Optional')
        #tabs.setPalette(QtGui.QApplication.palette())
        #tabs.tab
        #print tabs.tabBar().color(tabs.backgroundRole()).getRgb()
        #tabs.widget(1).palette().color(tabs.backgroundRole()).getRgb()
        print QtGui.QLineEdit().palette().color(QtGui.QLineEdit().
                                                backgroundRole()).getRgb()

        return tabs, code_string

    def get_title(self, module):
        """
        :param module: called module
        :return: new title of the window with parameters
        """

        self.title = [p for p in gtask.command_info(module)['keywords']]
        self.title = re.sub("'", "", module + " " + str(self.title))
        return self.title

    def get_description(self, module):
        """
        :param module: called module
        :return: label with module description
        """

        logo = QtGui.QLabel()
        logo.setPixmap(QtGui.QPixmap(os.path.join(IMGDIR,'grass_form.png')))
        logo.setFixedWidth(logo.sizeHint().width())
        text = QtGui.QLabel(gtask.command_info(module)['description'])
        text.setWordWrap(True)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(logo)
        layout.addWidget(text)
        layout.setContentsMargins(0, 0, 0, 0)

        description = QtGui.QWidget()
        description.setLayout(layout)
        description.setFixedHeight(description.sizeHint().height())

        return description

    def basic_buttons(self, module):
        """
        :parameter: no
        :return: 4 basic buttons at the bottom of GUI
        """

        close_button = QtGui.QPushButton('Close')
        run_button = QtGui.QPushButton('Run')
        run_button.setStyleSheet('QPushButton {color: green;}')
        copy_button = QtGui.QPushButton('Copy')
        help_button = QtGui.QPushButton('Help')

        layout = QtGui.QHBoxLayout()
        layout.addWidget(close_button)
        layout.addWidget(run_button)
        layout.addWidget(copy_button)
        layout.addWidget(help_button)
        buttons = QtGui.QWidget()
        buttons.setLayout(layout)

        close_button.clicked.connect(lambda: self.close())
        help_button.clicked.connect(lambda: run_command(module, 'help'))
        run_button.clicked.connect(lambda: self.run_command(module))

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

    def run_command(self, module):
        """
        runs the command
        """

        flags = ''
        long_flags = {}
        for i in self.flagList:
            if len(i) == 1:
                flags = flags + i
            else:
                long_flags.update({i: True})

        if long_flags:
            params_long_flags = {}
            params_long_flags.update(long_flags)
            params_long_flags.update(self.codeDict)
            run_command(module, flags=flags, **params_long_flags)
        else:
            run_command(module, flags=flags, **self.codeDict)

opt, arg = getopt.getopt(sys.argv, 'second parameter')

mainform = NewGUI(arg[1])

# help and output tabs
