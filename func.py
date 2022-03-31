import os
import re
from PyQt6.QtCore import QFile, QIODevice, QResource
QResource.registerResource("_qmlview_resource_.rcc")


class Check():


    def __init__(self, filename):
        self.filename = filename
        self.search_keywords = ("ApplicationWindow" or "Window")

    def check_for_parent(self):
        
        # find parent
        with open(self.filename, 'r') as orig_file:
            lines = orig_file.readlines()
            checked = [n.split(" ", 1)[0] for n in lines if n != "\n"]

        # find if it has a window parent
        if self.search_keywords in checked:
            return True
        else:
            return False

    def check_for_qtcharts(self):
        # find parent
        with open(self.filename, 'r') as orig_file:
            lines = orig_file.readlines()
            checked = [n.split(" ")[1] for n in lines if 'import ' in n]

        # find if it has a QtCharts import
        if "QtCharts" in checked:
            return True
        else:
            return False

    def check_style(self):
        
        with open(self.filename, 'r') as o_file:
            data = o_file.read(1024)
            info = re.findall(r'\n\s*import QtQuick.Controls.[A-Za-z]+ ', data)

        # take it and remove the space after it
        if info:
            stat = info[0][:-1]
            style_name = stat.split('.')[-1]
            return style_name.lower()
        else:
            return ''


class FixQml():


    def __init__(self, filename):
        self.original_file = filename
        self.replacement_qml = ":/qml/replacement_qml.qml"
        self.found_entry = ""

    def put_in_parent(self):

        # put in a parent
        with open(self.original_file, 'r') as orig_file:
            lines = orig_file.readlines()
        
        # Put in the Controls import statement if not in there
        # remove the last space before the version nos.

        # find the lines that start with import and split to get the stats only
        imp_stats = [n.split(" ", 2)[1] for n in lines \
                   if n.startswith('import') and n != "\n"]

        if "QtQuick.Controls" in imp_stats:
            pass
        else:
            lines.insert(1, 'import QtQuick.Controls 2.0\n')

        a = [n for n in lines if n.startswith('import')]
        last_index = lines.index(a[-1])
        if lines[last_index + 1] == '\n':
            # insert code at lane two
            insert_index = last_index + 2
        else:
            # insert code at lane one
            insert_index = last_index + 1

        # Open with QFile
        replace_file = QFile(self.replacement_qml)
        replace_file.open(QIODevice.ReadOnly)
        rep_data = replace_file.readAll()
        replace_data = str(rep_data, 'utf-8')
        
        # insert replacement code here
        lines.insert(insert_index, replace_data + "\n")
        # append closing bracket
        lines.append("}")

        final_data = ""
        # convert list to string
        for line in lines:
            final_data += line

        return final_data
