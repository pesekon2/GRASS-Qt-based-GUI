

from PyQt4 import QtGui
import gselect


class Factory():
    """
    Factory to decide which widget class should be used
    """

    @staticmethod
    def new_widget(gtask, code_dict, flag_list, code_dict_changer,
                   code_string_changer):
        """
        deciding which widget class should be used
        :param gtask: task for this widget
        :param : runable and copyable  string
        :return:
        """
        classes = [j for (i, j) in globals().iteritems()
                   if hasattr(j, 'can_handle')]
        for oneClass in classes:
            if oneClass.can_handle(gtask['type'], gtask['multiple'],
                                   gtask['key_desc'], gtask['prompt'],
                                   gtask['values']):
                return oneClass(gtask, code_dict, flag_list,
                                code_dict_changer, code_string_changer)
        else:
            return DefaultWidget(gtask, code_dict, flag_list,
                                 code_dict_changer,  code_string_changer)


# firstly, I define the widgets layout, then the widgets
class Parameters():
    def __init__(self, gtask, module, code_dict, flag_list, code_string):
        #super(Parameters).__init__(parent)

        self.module = module
        self.code_dict = code_dict
        self.flag_list = flag_list
        self.code_string = code_string
        self.gtask = gtask

        box_complete = self.get_layout()

        try:
            widget = Factory().new_widget(gtask, code_dict, flag_list,
                                          self.code_dict_changer,
                                          self.code_string_changer)
            box_complete.addWidget(widget)

        except:
            if gtask['name'] not in ['quiet', 'verbose']:
                widget = Flags(
                    gtask, code_dict, flag_list, self.code_dict_changer,
                    self.code_string_changer)
                box_complete.addWidget(widget)
                box_complete.addStretch()
                box_complete.addWidget(QtGui.QLabel('(%s)' % gtask['name']))
            elif gtask['name'] == 'quiet':
                widget = Quiet(
                    gtask, code_dict, flag_list, self.code_dict_changer,
                    self.code_string_changer)
                box_complete.addWidget(widget)


        if gtask['label'] and gtask['description']:
            # title is in label so we can use description as help/tooltip
            widget.setToolTip(gtask['description'])

        self.completeWidget = QtGui.QWidget()
        self.completeWidget.setLayout(box_complete)

    def new_widget(self):
        """
        :return:The widget
        """

        return self.completeWidget

    def get_layout(self):
        """
        create layout/box for the widget
        :param gtask: task for this widget
        :return: layout
        """

        try:
            box_header = QtGui.QHBoxLayout()

            if self.gtask['multiple'] is True:
                box_header.addWidget(QtGui.QLabel('[multiple]'))
            if self.gtask['label']:
                description = QtGui.QLabel(self.gtask['label'] + ':')
            else:
                description = QtGui.QLabel(self.gtask['description'] + ':')

            # description.setWordWrap(True)
            box_header.addWidget(description)

            if self.gtask['required'] is True:
                star = QtGui.QLabel('*')
                star.setStyleSheet('color: red')
                box_header.addWidget(star)

            box_header.addStretch()
            if self.gtask['key_desc']:
                box_header.addWidget(QtGui.QLabel('(%s=%s)' % (
                    self.gtask['name'], self.gtask['key_desc'][0])))
            else:
                box_header.addWidget(QtGui.QLabel('(%s=%s)' % (
                    self.gtask['name'], self.gtask['type'])))

            header = QtGui.QWidget()
            header.setLayout(box_header)

            layout_complete = QtGui.QVBoxLayout()
            layout_complete.addWidget(header)

        except:
            layout_complete = QtGui.QHBoxLayout()  # flag

        layout_complete.setSpacing(0)
        layout_complete.setMargin(0)

        return layout_complete

    def code_string_changer(self):
        flags = ''
        for i in self.flag_list:
            if len(i) == 1:
                flags = flags + ' -' + i
            else:
                flags = flags + ' --' + i
        self.code_string.setText(self.module + flags+' '+' '.join(
            '{}={}'.format(key, val) for key, val in self.code_dict.items()))

    def code_dict_changer(self, text):
        if text and (text != self.gtask['default'] or
                     self.gtask['name'] == 'layer'):
            try:
                self.code_dict[self.gtask['name']] = text
            except:  # it means that there is no item for this widget in dict
                self.code_dict.update({self.gtask['name']: text})
        else:
            try:
                del self.code_dict[self.gtask['name']]
                # because we don't want to have not necessary items in dict
            except:
                pass

        self.code_string_changer()


# now string types
class SqlQuery(QtGui.QLineEdit):
    def __init__(self, gtask, code_dict, flag_list, code_dict_changer,
                 code_string_changer):
        """
        :param gtask: task for this widget
        :param : runable and copyable string
        """

        super(SqlQuery, self).__init__()

        if gtask['default']:
            self.setText(gtask['default'])

        self.textChanged.connect(lambda: self.change_command(
            gtask, flag_list, self, code_dict_changer, code_string_changer))

    @staticmethod
    def can_handle(type, multiple, key_desc, prompt, values):
        return key_desc == ['sql_query']

    def change_command(self, gtask, flag_list, widget, code_dict_changer,
                       code_string_changer):
        code_dict_changer(str(widget.text()))


# maybe in future implement special widget when called from gui
class Cats(QtGui.QLineEdit):
    def __init__(self, gtask, code_dict, flag_list, code_dict_changer,
                 code_string_changer):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(Cats, self).__init__()

        if gtask['default']:
            self.setText(gtask['default'])

        self.textChanged.connect(lambda: self.change_command(
            gtask, flag_list, self, code_dict_changer, code_string_changer))

    @staticmethod
    def can_handle(type, multiple, key_desc, prompt, values):
        return prompt == 'cats'

    def change_command(self, gtask, flag_list, widget, code_dict_changer,
                       code_string_changer):
        code_dict_changer(str(widget.text()))


class SimpleValues(QtGui.QComboBox):
    def __init__(self, gtask, code_dict, flag_list, code_dict_changer,
                 code_string_changer):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(SimpleValues, self).__init__()

        self.setEditable(True)
        self.addItems(gtask['values'])

        if gtask['default']:
            self.setEditText(gtask['default'])

        self.textChanged.connect(lambda: self.change_command(
            gtask, flag_list, self, code_dict_changer, code_string_changer))

    @staticmethod
    def can_handle(type, multiple, key_desc, prompt, values):
        return (type == 'string') and (multiple is False) and values

    def change_command(self, gtask, flag_list, widget, code_dict_changer,
                       code_string_changer):
        code_dict_changer(str(widget.currentText()))


class Separator(QtGui.QComboBox):
    def __init__(self, gtask, code_dict, flag_list, code_dict_changer,
                 code_string_changer):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(Separator, self).__init__()

        self.setEditable(True)
        self.addItems(self.get_items(gtask))

        if gtask['default']:
            self.setEditText(gtask['default'])

        self.textChanged.connect(lambda: self.change_command(
            gtask, flag_list, self, code_dict_changer, code_string_changer))

    def get_items(self, gtask):
        items_string = gtask['description'].split('Special characters: ')[1]
        return items_string.split(', ')

    @staticmethod
    def can_handle(type, multiple, key_desc, prompt, values):
        return (type == 'string') and prompt == 'separator'

    def change_command(self, gtask, flag_list, widget, code_dict_changer,
                       code_string_changer):
        code_dict_changer(str(widget.currentText()))


# inherited from gselect.py
class TreeComboBox(gselect.TreeComboBox):
    @staticmethod
    def can_handle(type, multiple, key_desc, prompt, values):
        return type == 'string' and key_desc != ['sql_query'] \
               and prompt in ['raster', 'vector', 'raster_3d', 'group']

    def change_command(self, gtask, flag_list, widget, code_dict_changer,
                       code_string_changer):
        code_dict_changer(str(widget.currentText()))


class BrowseFile(gselect.BrowseFile):
    @staticmethod
    def can_handle(type, multiple, key_desc, prompt, values):
        return type == 'string' and key_desc != ['sql_query'] \
               and (prompt == 'file')

    def change_command(self, gtask, flag_list, widget, code_dict_changer,
                       code_string_changer):
        code_dict_changer(str(widget.text()))


class MultipleValues(gselect.MultipleValues):
    @staticmethod
    def can_handle(type, multiple, key_desc, prompt, values):
        return (type == 'string') and (multiple is True) and values

    def change_command(self, gtask, flag_list, widget, code_dict_changer,
                       code_string_changer):
        value = ''
        items = (widget.itemAt(i).widget() for i in range(widget.count()-1))

        for item in items:
            if item.isChecked():
                if value:
                    value = ','.join((value, str(item.objectName())))
                else:
                    value = str(item.objectName())

        code_dict_changer(str(value))


class Layers(gselect.Layers):
    @staticmethod
    def can_handle(type, multiple, key_desc, prompt, values):
        return (type == 'string') and prompt == 'layer'

    def change_command(self, gtask, flag_list, widget, code_dict_changer,
                       code_string_changer):
        code_dict_changer(str(widget.currentText()))


class Columns(gselect.Columns):
    @staticmethod
    def can_handle(type, multiple, key_desc, prompt, values):
        return (type == 'string') and prompt == 'dbcolumn'

    def change_command(self, gtask, flag_list, widget, code_dict_changer,
                       code_string_changer):
        code_dict_changer(str(widget.currentText()))


class Colors(gselect.Colors):
    @staticmethod
    def can_handle(type, multiple, key_desc, prompt, values):
        return (type == 'string') and prompt == 'color'

    def change_command(self, gtask, flag_list, widget, code_dict_changer,
                       code_string_changer):
        items = list((widget.itemAt(i).widget()
                      for i in range(widget.count()-1)))

        if len(items) > 1:
            if items[1].isChecked() is False:
                code_dict_changer(str(items[0].text()))
            else:
                code_dict_changer('')
        else:
            code_dict_changer(str(items[0].text()))


class DbTable(gselect.DbTable):
    @staticmethod
    def can_handle(type, multiple, key_desc, prompt, values):
        return prompt == 'dbtable'

    def change_command(self, gtask, flag_list, widget, code_dict_changer,
                       code_string_changer):
        code_dict_changer(str(widget.currentText()))



# now float types
class MultipleFloat(QtGui.QLineEdit):
    def __init__(self, gtask, code_dict, flag_list, code_dict_changer,
                 code_string_changer):
        """
        for float: multiple, coords
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(MultipleFloat, self).__init__()

        if gtask['default']:
            self.setText(gtask['default'])

        self.textChanged.connect(lambda: self.change_command(
            gtask, flag_list, self, code_dict_changer, code_string_changer))

    @staticmethod
    def can_handle(type, multiple, key_desc, prompt, values):
        return type=='float' and ((multiple is True) or prompt == 'coords')

    def change_command(self, gtask, flag_list, widget, code_dict_changer,
                       code_string_changer):
        code_dict_changer(str(widget.text()))


class SimpleFloat(QtGui.QDoubleSpinBox):
    def __init__(self, gtask, code_dict, flag_list, code_dict_changer,
                 code_string_changer):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(SimpleFloat, self).__init__()

        self.setRange(-10000000, 10000000)
        self.setDecimals(5)
        if gtask['default']:
            self.setValue(float(gtask['default']))

        self.valueChanged.connect(lambda: self.change_command(
            gtask, flag_list, self, code_dict_changer, code_string_changer))

    @staticmethod
    def can_handle(type, multiple, key_desc, prompt, values):
        return type == 'float' and multiple is False

    def change_command(self, gtask, flag_list, widget, code_dict_changer,
                       code_string_changer):
        code_dict_changer(str(widget.value()))





# now integer types
class MultipleInteger(QtGui.QLineEdit):
    def __init__(self, gtask, code_dict, flag_list, code_dict_changer,
                 code_string_changer):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(MultipleInteger, self).__init__()

        if gtask['default']:
            self.setText(gtask['default'])

        self.textChanged.connect(lambda: self.change_command(
            gtask, flag_list, self, code_dict_changer, code_string_changer))

    @staticmethod
    def can_handle(type, multiple, key_desc, prompt, values):
        return type == 'integer' and multiple is True

    def change_command(self, gtask, flag_list, widget, code_dict_changer,
                       code_string_changer):
        code_dict_changer(str(widget.text()))


class SimpleInteger(QtGui.QSpinBox):
    def __init__(self, gtask, code_dict, flag_list, code_dict_changer,
                 code_string_changer):
        """
        :param gtask: task for this widget
        :param : runable and copyable  string
        """

        super(SimpleInteger, self).__init__()

        self.setRange(-10000000, 10000000)

        if gtask['default']:
            self.setValue(int(gtask['default']))

        self.valueChanged.connect(lambda: self.change_command(
            gtask, flag_list, self, code_dict_changer, code_string_changer))

    @staticmethod
    def can_handle(type, multiple, key_desc, prompt, values):
        return type == 'integer' and multiple is False

    def change_command(self, gtask, flag_list, widget, code_dict_changer,
                       code_string_changer):
        code_dict_changer(str(widget.text()))




class Flags(QtGui.QCheckBox):
    def __init__(self, gtask, code_dict, flag_list, code_dict_changer,
                 code_string_changer):

        super(Flags, self).__init__(self.get_label(gtask))

        self.stateChanged.connect(lambda: self.change_command(
            gtask, flag_list, self, code_dict_changer, code_string_changer))

    def get_label(self, gtask):
        if gtask['label']:
            return gtask['label']
        else:
            return gtask['description']

    def change_command(self, gtask, flag_list, widget, code_dict_changer,
                       code_string_changer):
        if widget.isChecked():
            if gtask['name'] not in flag_list:
                # it means that there is no item for this widget in dict
                flag_list.append(gtask['name'])
        else:
            flag_list.remove(gtask['name'])
            # because we don't want to have not necessary items in dict

        code_string_changer()



class Quiet(gselect.Quiet):
    def change_command(self, gtask, flag_list, widget, code_dict_changer,
                       code_string_changer):
        if widget.text() == 'Normal module output':
            try:
                flag_list.remove('quiet')
            except:
                flag_list.remove('verbose')
        elif widget.text() == 'Quiet module output':
            flag_list.append('quiet')
        else:
            flag_list.append('verbose')

        code_string_changer()


# default widget
class DefaultWidget(QtGui.QLineEdit):
    def __init__(self, gtask, code_dict, flag_list, code_dict_changer,
                 code_string_changer):

        super(DefaultWidget, self).__init__()

        # just highlighting what should be done better
        self.setText('TODO - Nobody expects the Spanish Inquisition')
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Active,
                         QtGui.QPalette.Base, QtGui.QColor('red'))
        self.setPalette(palette)

        #if gtask['default']: # uncomment when not using highlighting
        #    self.setText(gtask['default'])

        self.textChanged.connect(lambda: self.change_command(
            gtask, flag_list, self, code_dict_changer, code_string_changer))

    def change_command(self, gtask, flag_list, widget, code_dict_changer,
                       code_string_changer):
        print gtask
        code_dict_changer(str(widget.text()))





# prompt=datasource (v.external), v.proj, d.vect (symbols, colors)
# datasource_layer (v.import), words for predefined colors
# column/layer also from map (v.db.join), wordwrap, size
# mapset select for existing path





















