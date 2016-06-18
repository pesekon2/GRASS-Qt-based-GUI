

from PyQt4.QtCore import QObject,QModelIndex,QEvent
from PyQt4 import QtGui
from grass import script
import parameters



class TreeComboBox(QtGui.QComboBox):
    def __init__(self, gtask, function, codeDict, codeString, parent=None):#, *args):
        super(TreeComboBox,self).__init__(parent)#*args)

        self.__skip_next_hide = False

        tree_view = QtGui.QTreeView(self)
        tree_view.setFrameShape(QtGui.QFrame.NoFrame)
        tree_view.setEditTriggers(tree_view.NoEditTriggers)
        tree_view.setAlternatingRowColors(True)
        tree_view.setSelectionBehavior(tree_view.SelectRows)
        #tree_view.setWordWrap(True)
        tree_view.setAllColumnsShowFocus(True)
        self.setView(tree_view)
        self.setEditable(True)
        self.setModel(self.getModel(gtask))
        self.textChanged.connect(lambda: parameters.CodeChanger(gtask, function, codeDict, codeString,self))

        self.view().viewport().installEventFilter(self)

    def showPopup(self):
        self.setRootModelIndex(QModelIndex())
        super(TreeComboBox,self).showPopup()

    def hidePopup(self):
        self.setRootModelIndex(self.view().currentIndex().parent())
        #self.setCurrentIndex(self.view().currentIndex().row())
        if self.__skip_next_hide:
            self.__skip_next_hide = False
        else:
            super(TreeComboBox,self).hidePopup()

    def selectIndex(self, index):
        self.setRootModelIndex(index.parent())
        self.setCurrentIndex(index.row())

    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseButtonPress and object is self.view().viewport():
            index = self.view().indexAt(event.pos())
            self.__skip_next_hide = not self.view().visualRect(index).contains(event.pos())
        return False

    def getModel(self,gtask):
        mapsets = script.mapsets(search_path = True)
        model = QtGui.QStandardItemModel()
        #model.__init__(parent=None)
        model.setParent(self)
        for mapset in mapsets:
            parent_item = QtGui.QStandardItem('Mapset: '+mapset)
            list = script.core.list_pairs(gtask['prompt'])
            for map in list:
                if mapset in map:
                    parent_item.appendRow(QtGui.QStandardItem('%s@%s' %(map[0],map[1])))
            model.appendRow(parent_item)

        return model

