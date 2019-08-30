import re
from PyQt5.QtCore import QFile, QIODevice, QResource
QResource.registerResource("./resource.rcc")

class CheckStyle():


    def __init__(self, filename):
        self.filename = filename

    def check_style(self):

        with open(self.filename, 'r') as o_file:
            data = o_file.read(1024)
            info = re.findall('\n\s*import QtQuick.Controls.[A-Za-z]+ ', data)

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
        self.search_keywords = ("ApplicationWindow", "Window")
        self.found_entry = ""


    def handle(self):

        # does the main
        if self.check_for_parent():
            return True, "0"
        else:
            data = self.put_in_parent()
            return False, data

    def check_for_parent(self):

        # find parent
        with open(self.original_file, 'r') as orig_file:
            data = orig_file.read(1024)
            info = re.findall('\n\s*[A-Z].*?.*?.*? {', data)

        splits = re.split("\n?\s+", info[0])
        clear_stat = splits[-2] + " " + splits[-1]
        self.found_entry = clear_stat
        # Just the word without the curly braces
        clean_pat = splits[-2]

        if clean_pat in self.search_keywords:
            return True
        else:
            return False

    def put_in_parent(self):

        # put in a parent
        with open(self.original_file, 'r') as orig_file:
            ori_data = orig_file.read()

            splits = ori_data.split(self.found_entry, 1)
            top_data = splits[0]
            bottom_data = self.found_entry + splits[1]

        # Open with QFile
        replace_file = QFile(self.replacement_qml)
        replace_file.open(QIODevice.ReadOnly)
        rep_data = replace_file.readAll()
        replace_data = str(rep_data, 'utf-8')

        final_data = top_data + replace_data + "\n" + bottom_data + "\n" + "}"

        return final_data
