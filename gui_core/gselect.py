

from PyQt4.QtCore import QModelIndex, QEvent, Qt
from PyQt4 import QtGui
from grass import script
import subprocess


class TreeComboBox(QtGui.QComboBox):
    """
    widget for tree view models
    """
    def __init__(self, gtask, code_dict, flag_list, code_dict_changer,
                 code_string_changer, parent=None):
        """
        constructor
        :param gtask: part of gtask for this widget
        :param code_dict: dictionary of filled parameters
        :param flag_list: list of checked flags
        :param code_dict_changer: method for changing code_dict
        :param code_string_changer: method for changing string with code
        :return: created widget
        """

        super(TreeComboBox, self).__init__(parent)

        self.__skip_next_hide = False

        tree_view = QtGui.QTreeView(self)
        tree_view.setFrameShape(QtGui.QFrame.NoFrame)
        tree_view.setEditTriggers(tree_view.NoEditTriggers)
        tree_view.setAlternatingRowColors(True)
        tree_view.setSelectionBehavior(tree_view.SelectRows)
        # tree_view.setWordWrap(True)
        tree_view.setAllColumnsShowFocus(True)
        self.setView(tree_view)
        self.setEditable(True)
        self.setModel(self.get_model(gtask))
        self.textChanged.connect(lambda: self.change_command(
            gtask, flag_list, self, code_dict_changer,
            code_string_changer))  # see in parameters.py

        self.view().viewport().installEventFilter(self)

    def showPopup(self):
        self.setRootModelIndex(QModelIndex())
        super(TreeComboBox, self).showPopup()

    def hidePopup(self):
        self.setRootModelIndex(self.view().currentIndex().parent())
        # self.setCurrentIndex(self.view().currentIndex().row())
        if self.__skip_next_hide:
            self.__skip_next_hide = False
        else:
            super(TreeComboBox, self).hidePopup()

    def select_index(self, index):
        self.setRootModelIndex(index.parent())
        self.setCurrentIndex(index.row())

    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseButtonPress and object is \
                self.view().viewport():
            index = self.view().indexAt(event.pos())
            self.__skip_next_hide = not self.view().visualRect(index).\
                contains(event.pos())
        return False

    def get_model(self, gtask):
        """
        creates the core of a tree based model to input into widget
        :param gtask: part of gtask for this widget
        :return: tree model
        """
        mapsets = script.mapsets(search_path=True)
        model = QtGui.QStandardItemModel()
        # model.__init__(parent=None)
        model.setParent(self)
        for mapset in mapsets:
            parent_item = QtGui.QStandardItem('Mapset: '+mapset)
            parent_item.setSelectable(False)
            list = script.core.list_pairs(gtask['prompt'])
            for map in list:
                if mapset in map:
                    parent_item.appendRow(QtGui.QStandardItem
                                          ('%s@%s' % (map[0], map[1])))
            model.appendRow(parent_item)

        return model


class BrowseFile(QtGui.QWidget):
    """
    widget that allows user to choose path to file or directory
    """
    def __init__(self, gtask, code_dict, flag_list, code_dict_changer,
                 code_string_changer, parent=None):
        """
        constructor
        :param gtask: part of gtask for this widget
        :param code_dict: dictionary of filled parameters
        :param flag_list: list of checked flags
        :param code_dict_changer: method for changing code_dict
        :param code_string_changer: method for changing string with code
        :return: created widget
        """

        super(BrowseFile, self).__init__(parent)
        self.gtask = gtask

        layout = QtGui.QHBoxLayout()
        self.line = QtGui.QLineEdit()
        button = QtGui.QPushButton('Browse')
        button.clicked.connect(self.select_file)

        button.setMinimumSize(button.sizeHint())
        self.line.setMinimumSize(self.line.sizeHint())

        layout.addWidget(self.line)
        layout.addWidget(button)
        self.setLayout(layout)

        self.line.textChanged.connect(lambda: self.change_command(
            gtask, flag_list, self.line, code_dict_changer,
            code_string_changer))  # see in parameters.py

    def select_file(self):
        """
        raise dialog to choose file or directory
        """

        if self.gtask['prompt'] == 'file':
            file_path = QtGui.QFileDialog.getOpenFileName(self, 'Select file')
        else:
            file_path = QtGui.QFileDialog.getExistingDirectory(self, 'Select directory')
        if file_path:
            self.line.setText(file_path)
        else:
            return


class MultipleValues(QtGui.QGroupBox):
    """
    widget that allows user to choose predefined values (even more than one)
    """
    def __init__(self, gtask, code_dict, flag_list, code_dict_changer,
                 code_string_changer):
        """
        constructor
        :param gtask: part of gtask for this widget
        :param code_dict: dictionary of filled parameters
        :param flag_list: list of checked flags
        :param code_dict_changer: method for changing code_dict
        :param code_string_changer: method for changing string with code
        :return: created widget
        """

        super(MultipleValues, self).__init__()

        default_boxes = gtask['default'].split(',')

        i = 0
        if not gtask['values_desc']:
            layout = QtGui.QHBoxLayout()
            for item in gtask['values']:
                box = QtGui.QCheckBox(item)
                box.setObjectName(gtask['values'][i])
                if box.objectName() in default_boxes:
                    box.setChecked(True)
                layout.addWidget(box)
                box.stateChanged.connect(lambda: self.change_command(
                    gtask, flag_list, layout, code_dict_changer,
                    code_string_changer))  # see in parameters.py
                i = i+1
        else:
            layout = QtGui.QVBoxLayout()
            layout.setSpacing(0)
            for item in gtask['values_desc']:
                box = QtGui.QCheckBox(item)
                box.setObjectName(gtask['values'][i])
                if box.objectName() in default_boxes:
                    box.setChecked(True)
                layout.addWidget(box)
                box.stateChanged.connect(lambda: self.change_command(
                    gtask, flag_list, layout, code_dict_changer,
                    code_string_changer))  # see in parameters.py
                i = i+1

        layout.addStretch()
        self.setLayout(layout)


class Layers(QtGui.QComboBox):
    """
    widget that allows user to choose from layers in chosen map (input, map)
    """
    def __init__(self, gtask, code_dict, flag_list, code_dict_changer,
                 code_string_changer):
        """
        constructor
        :param gtask: part of gtask for this widget
        :param code_dict: dictionary of filled parameters
        :param flag_list: list of checked flags
        :param code_dict_changer: method for changing code_dict
        :param code_string_changer: method for changing string with code
        :return: created widget
        """

        super(Layers, self).__init__()

        self.setEditable(True)

        self.gtask = gtask
        self.code_dict = code_dict

        if gtask['default']:
            self.setEditText(gtask['default'])

        self.textChanged.connect(lambda: self.change_command(
            gtask, flag_list, self, code_dict_changer, code_string_changer))

    def get_layers(self):
        """
        load layers (based on map in input or map widget)
        """

        self.clear()

        if self.gtask['element'] == 'layer_all':
            self.addItem('-1')

        try:
            layers = script.vector_db(map=self.code_dict['input'])
            for layer in layers:
                self.addItem(str(layer))
        except:
            try:
                layers = script.vector_db(map=self.code_dict['map'])
                for layer in layers:
                    self.addItem(str(layer))
            except:
                if self.count() == 0:
                    self.addItem('')

    def showPopup(self):
        text = self.currentText()
        self.get_layers()
        super(Layers, self).showPopup()
        if text in [self.itemText(i) for i in range(self.count())]:
            self.setEditText(text)
        else:
            self.setEditText('')


class Columns(QtGui.QComboBox):
    """
    widget that allows user to choose from columns in chosen map and layer
    """
    def __init__(self, gtask, code_dict, flag_list, code_dict_changer,
                 code_string_changer):
        """
        constructor
        :param gtask: part of gtask for this widget
        :param code_dict: dictionary of filled parameters
        :param flag_list: list of checked flags
        :param code_dict_changer: method for changing code_dict
        :param code_string_changer: method for changing string with code
        :return: created widget
        """

        super(Columns, self).__init__()

        self.setEditable(True)

        # self.gtask = gtask
        self.code_dict = code_dict

        if gtask['default']:
            self.setEditText(gtask['default'])

        self.textChanged.connect(lambda: self.change_command(
            gtask, flag_list, self, code_dict_changer, code_string_changer))

    def get_layer(self):
        """
        transforming layer into int (if it is)
        :return: name of layer (int, string)
        """

        try:
            layer = int(self.code_dict['layer'])
            return layer
        except:
            return self.code_dict['layer']

    def get_columns(self, layers, layer):
        """
        load columns
        :param layers: dictionary of all layers in map
        :param layer: layer chosen in widget Layer
        """

        for item in script.db_describe(
                table=layers[layer]["table"],
                driver=layers[layer]["driver"],
                database=layers[layer]["database"])['cols']:
            self.addItem(item[0])

    def set_values(self):
        """
        setting columns into the widget
        """

        self.clear()

        try:
            layers = script.vector_db(map=self.code_dict['input'])
            layer = self.get_layer()

            if layer == -1:
                for layer in layers.keys():
                    self.get_columns(layers, layer)
            else:
                self.get_columns(layers, layer)
        except:
            try:
                layers = script.vector_db(map=self.code_dict['map'])
                layer = self.get_layer()

                if layer == -1:
                    for layer in layers.keys():
                        self.get_columns(layers, layer)
                else:
                    self.get_columns(layers, layer)
            except:
                self.addItem('')

    def showPopup(self):

        text = self.currentText()
        self.set_values()

        super(Columns, self).showPopup()
        if text in [self.itemText(i) for i in range(self.count())]:
            self.setEditText(text)
        else:
            self.setEditText('')


class Colors(QtGui.QWidget):
    """
    widget that allows user to choose color from color dialog
    """
    def __init__(self, gtask, code_dict, flag_list, code_dict_changer,
                 code_string_changer):
        """
        constructor
        :param gtask: part of gtask for this widget
        :param code_dict: dictionary of filled parameters
        :param flag_list: list of checked flags
        :param code_dict_changer: method for changing code_dict
        :param code_string_changer: method for changing string with code
        :return: created widget
        """

        super(Colors, self).__init__()

        layout = QtGui.QHBoxLayout()
        self.colorBtn = QtGui.QPushButton()

        self.btnStyle = 'border-style: double; border-width: 3px; ' \
                        'border-color: beige; min-width: 8em; padding: 6px'

        if gtask['default'] == 'none':
            self.colorBtn.setStyleSheet(
                "QPushButton {background-color: #c8c8c8;%s}" % self.btnStyle)
            self.colorBtn.setText('Select color')
            layout.addWidget(self.colorBtn)
            transparent = QtGui.QCheckBox('Transparent')
            transparent.stateChanged.connect(lambda: self.parse_text(
                gtask, flag_list, layout, code_dict_changer,
                code_string_changer))
            layout.addWidget(transparent)
        else:
            splitted_color = gtask['default'].split(':')
            if len(splitted_color)>1:
                color_name = '#%02x%02x%02x' % (
                    int(splitted_color[0]), int(splitted_color[1]),
                    int(splitted_color[2]))
            else:
                color_name = gtask['default']

            if QtGui.QColor(color_name).red() + \
                    QtGui.QColor(color_name).blue() + \
                    QtGui.QColor(color_name).green() < 387:
                text_color = 'white'
            else:
                text_color = 'black'

            self.colorBtn.setStyleSheet("QPushButton {background-color: %s;"
                                        "color: %s; %s}"
                                        % (color_name, text_color,
                                           self.btnStyle))
            self.colorBtn.setText(gtask['default'])
            layout.addWidget(self.colorBtn)

        layout.addStretch()

        self.setLayout(layout)
        self.defaultText = self.colorBtn.text()

        self.colorBtn.clicked.connect(lambda: self.color_picker())
        self.colorBtn.clicked.connect(lambda: self.parse_text(
            gtask, flag_list, layout, code_dict_changer, code_string_changer))

    def color_picker(self):
        color = QtGui.QColorDialog.getColor(
            initial=QtGui.QColor(self.colorBtn.palette().
                                 color(QtGui.QPalette.Background)))
        if color.isValid():
            if color.red() + color.green() + color.blue() < 387:
                text_color = 'white'
            else:
                text_color = 'black'
            self.colorBtn.setStyleSheet("QPushButton { background-color: %s;"
                                        "color: %s; %s}"
                                        % (color.name(), text_color,
                                           self.btnStyle))
            self.colorBtn.setText('%s:%s:%s' % (color.red(), color.green(),
                                                color.blue()))

    def parse_text(self, gtask, flag_list, layout, code_dict_changer,
                   code_string_changer):
        if self.colorBtn.text() != self.defaultText:
            self.change_command(gtask, flag_list, layout, code_dict_changer,
                                code_string_changer)


class DbTable(QtGui.QComboBox):
    """
    widget that allows user to choose db table
    """
    def __init__(self, gtask, code_dict, flag_list, code_dict_changer,
                 code_string_changer):
        """
        constructor
        :param gtask: part of gtask for this widget
        :param code_dict: dictionary of filled parameters
        :param flag_list: list of checked flags
        :param code_dict_changer: method for changing code_dict
        :param code_string_changer: method for changing string with code
        :return: created widget
        """

        super(DbTable, self).__init__()
        self.code_dict = code_dict

        self.setEditable(True)

        if gtask['default']:
            self.setEditText(gtask['default'])

        self.textChanged.connect(lambda: self.change_command(
            gtask, flag_list, self, code_dict_changer, code_string_changer))

    def get_db_info(self):
        """
        check if there is defined driver or database
        :return: driver and database (default or defined)
        """

        try:
            driver = self.code_dict['driver']
            try:
                database = self.code_dict['database']
            except:
                connect = script.db_connection()
                database = connect['database']
        except:
            connect = script.db_connection()
            try:
                database = self.code_dict['database']
                driver = connect['driver']
            except:
                database = connect['database']
                driver = connect['driver']

        return driver, database

    def get_tables(self):
        """
        get tables from user's database
        :return: tables in one string
        """

        driver, database = self.get_db_info()

        tables = script.start_command('db.tables',
                                      flags='p',
                                      driver=driver,
                                      database=database,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)

        return tables.communicate()[0]

    def showPopup(self):

        text = self.currentText()
        tables = self.get_tables()

        self.clear()
        if tables:
            for table in tables.splitlines():
                self.addItem(table)
        else:
            self.addItem('')

        super(DbTable, self).showPopup()
        if text in [self.itemText(i) for i in range(self.count())]:
            self.setEditText(text)
        else:
            self.setEditText('')





class Quiet(QtGui.QWidget):
    """
    special widget with which user can choose quiet, normal or verbose module output
    """
    def __init__(self, gtask, code_dict, flag_list, code_dict_changer,
                 code_string_changer):
        """
        constructor
        :param gtask: part of gtask for this widget
        :param code_dict: dictionary of filled parameters
        :param flag_list: list of checked flags
        :param code_dict_changer: method for changing code_dict
        :param code_string_changer: method for changing string with code
        :return: created widget
        """

        super(Quiet, self).__init__()
        self.setLayout(self.get_layout(gtask, flag_list, code_dict_changer,
                                       code_string_changer))

    def get_layout(self, gtask, flag_list, code_dict_changer,
                   code_string_changer):
        """
        create slider and wrap it into a layout
        :return: completed layout
        """

        label = QtGui.QLabel('Normal module output')
        slider = QtGui.QSlider(Qt.Horizontal)
        slider.setSingleStep(1)
        slider.setMinimum(0)
        slider.setMaximum(2)
        slider.setValue(1)
        slider.setFixedWidth(slider.sizeHint().width())

        slider.valueChanged.connect(lambda: self.slider_moved(slider, label))
        slider.valueChanged.connect(lambda: self.change_command(
            gtask, flag_list, label, code_dict_changer, code_string_changer))

        layout = QtGui.QHBoxLayout()
        layout.addWidget(label)
        layout.addStretch()
        layout.addWidget(slider)

        return layout

    def slider_moved(self, slider, label):
        """
        change label when slider moves
        :param slider: the main widget
        :param label: label telling user which output does he have chosen
        """
        if slider.value() == 1:
            label.setText('Normal module output')
        elif slider.value() == 0:
            label.setText('Quiet module output')
        else:
            label.setText('Verbose module output')




