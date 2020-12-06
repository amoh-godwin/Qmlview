"""
Module for Live Reloading
"""
import threading
from time import sleep
import os
import re
from random import randrange
from platform import system
from glob import glob

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QFile, QResource, QIODevice, pyqtProperty

from misc import Split

QResource.registerResource("_qmlview_resource_.rcc")


class Live(QObject):


    """
    """


    def __init__(self, watch_file):
        QObject.__init__(self)

        self.os_name = system().lower()
        self.watch_file = os.path.realpath(watch_file)
        self.folder = os.path.split(watch_file)[0]
        self.u_qmltypes = ()
        self.u_qmltypes_map = {}
        # add permission
        if self.os_name != 'windows':
            # add permissions
            os.system(f'chmod +rw {self.folder}')
        self.filename = os.path.join(self.folder, '00001000.qml')

        self.show_props = False

        self.old_code = ''
        self.old_props = ''
        self.old_qmltypes_codes = {}

        self.new_qmltypes_files = {}

        self.not_closed = True

        self._initialiase()

    updated = pyqtSignal(str, arguments=['updater'])
    propsUpdated = pyqtSignal(list, str, arguments=['props_updater'])

    def props_updater(self, props, filename):
        try:
            filename = 'file:///' + filename
            self.propsUpdated.emit(props, filename)
        except RuntimeError:
            # possibly user exited out
            pass

    def updater(self, filename):
        print('updater', filename)
        try:
            filename = 'file:///' + filename
            self.updated.emit(filename)
        except RuntimeError:
            # possibly user exited out
            pass

    @pyqtProperty(list)
    def oldProps(self):
        return self.old_props

    @oldProps.setter
    def oldProps(self, props):
        self.old_props = props

    @pyqtSlot(bool)
    def show_props(self, show):
        self.show_props = show

    def _initialiase(self):
        # Initialise everything
        print('init')
        with open(self.watch_file, 'r') as fh:
            code = fh.read()

        with open(self.filename, 'w') as fw:
            fw.write(code)

        # pick initial qmltypes
        self._find_qmltypes(self.folder)
        # replace all qmltypes in there
        # replace it in all of our qmltypes and the filename
        patt = os.path.join(self.folder, 'Live*_*.qml')
        items = glob(patt)
        print('items: ', items)
        items.append(self.filename)
        for item in items:
            self._init_replace_conts(item)

        self.monitor_qmltypes()

        self._call_auto_reload()

    def _call_auto_reload(self):
        a_thread = threading.Thread(target=self._auto_reload)
        a_thread.daemon = True
        a_thread.start()

    def _auto_reload(self):
        print('auto reload')
        while self.not_closed:
            if not self.show_props:
                code = self._read_file(self.watch_file)
                if code != self.old_code:
                    self._save_to_file(code)
                    self.updater(self.filename)
                    self.old_code = code
            else:
                props, code = self._read_all_file(self.watch_file)
                if props != self.old_props:
                    self._save_to_file(code)
                    self.props_updater(props, self.filename)
                    self.old_props = props
                elif code == self.old_code:
                    self.old_code = code
                    self.updater(code)
            sleep(0.1)

    def _find_qmltypes(self, folder):
        print('find_qmltypes')
        u_qmltypes = list(self.u_qmltypes)
        patt = os.path.join(folder, '*.qml')
        items = glob(patt)
        for x in items:
            name = os.path.split(x)[1]
            if name[0].istitle():
                with open(x, 'r') as fh:
                    code = fh.read()
                    print(x, len(code))
                type_name = name.rsplit('.')[0]
                new_t_name = f'Live{randrange(1,250)}_{type_name}'
                self.u_qmltypes_map[type_name] = new_t_name
                new_file = os.path.join(folder, new_t_name+'.qml')
                print(x, new_file)
                self.new_qmltypes_files[x] = new_file
                self.old_qmltypes_codes[x] = code
                self._save_qmltype_file(code, new_file)
                u_qmltypes.append(x)

        self.u_qmltypes = tuple(u_qmltypes)

    def _find_qmltypes_in_file(self, filename):
        print('find_qmltypes_in_file')
        # useless delete
        with open(filename, 'r') as fh:
            data = fh.read()

        all_types = re.findall(r'\s*[A-Z][A-Za-z0-9]+\s*{', data)

    def _is_in_file(self, needle, filename):
        print('_is_in_file')
        # check if a qml file contains type

        with open(filename, 'r') as fh:
            data = fh.read()

        entry = re.findall(needle, data)
        if entry:
            return True

    def _init_replace_conts(self, filename):
        print('init_replace_conts')
        # replace all occurences of a type with
        # the new one with a common space between the curly bracket
        with open(filename, 'r') as fh:
            data = fh.read()

        print('***************\n', data)
        print('\n', self.u_qmltypes_map, '\n')

        u_qml_map = self.u_qmltypes_map.copy()
        for x in u_qml_map:
            patt = x + r'\s*{'
            # no of types found in file
            founds = re.findall(r''+patt, data)
            y = self.u_qmltypes_map[x]
            yx = '\n' + y + ' {'
            self.u_qmltypes_map[y] = ''
            for y in founds:
                data = data.replace(y, yx)

        print('***************\n', 'suprising')
        print(data, '\n\n')

        # save to that file
        self._save_qmltype_file(data, filename)

    def monitor_qmltypes(self):
        m_thread = threading.Thread(target=self._monitor_qmltype)
        m_thread.daemon = True
        m_thread.start()

    def _monitor_qmltype(self):
        print('_monitor_qmltype')
        # Monitor qmltypes
        while self.not_closed:
            for file in self.u_qmltypes:
                code = self._read_qmltype_file(file)
                if code != self.old_qmltypes_codes[file]:
                    # re-arrange the code to the code we all know
                    # and deal with inside qml
                    new_code = self._load_with_qmltypes(code)
                    self._save_qmltype_file(new_code, file)
                    self._rename_all()
                    # updater
                    with open(self.filename, 'r') as fh:
                        data = fh.read()
                    new_data = self._load_with_qmltypes(data)
                    self._save_to_file(new_data)
                    self.updater(self.filename)
                    self.old_qmltypes_codes[file] = code
            sleep(1)

    def _load_with_qmltypes(self, code):
        print('_load_with_qmltypes: ', len(code))
        print('\n*****************\n\n')
        print('before\n', code)
        for x in self.u_qmltypes_map:
            xs = r'\s' + x + ' {'
            ys = '\n' +self.u_qmltypes_map[x] + ' {'
            print('loe: ', x, self.u_qmltypes_map[x], self.u_qmltypes_map)
            code = re.sub(xs, ys, code)
            print(len(code))

        print('after \n', code)
        print('*********************\n\n\n')
        return code

    def _read_file(self, filename):
        print('read_file', filename)
        code = ""

        splitter = Split(filename, pick_comp=True)
        imps = splitter.orig_imp_stats
        bottom_code = splitter.orig_bottom_lines
        imps_text = ''.join(imps)
        btm_code_text = ''.join(bottom_code)
        # Append Rectangle to bottom code
        cont = '\nRectangle {\n anchors.fill: parent\n'
        cont += 'color: "transparent"\n' + btm_code_text + '\n}'
        code = imps_text + cont

        return code

    def _read_qmltype_file(self, filename):
        print('_read_qmltype')
        with open(filename, 'r') as fh:
            data = fh.read()
        return data

    def _read_all_file(self, filename):

        print('read_all_file')
        splitter = Split(filename, pick_comp=True)
        imps = splitter.orig_imp_stats
        bottom_code = splitter.orig_bottom_lines
        props = splitter.wind_user_props
        prop = [props['width'].split(':')[-1].strip(), props['height'].split(':')[-1].strip()]
        imps_text = ''.join(imps)
        btm_code_text = ''.join(bottom_code)
        # Append Rectangle to bottom code
        cont = '\nRectangle {\n anchors.fill: parent\n'
        cont += 'color: "transparent"\n' + btm_code_text + '\n}'
        code = imps_text + cont

        return prop, code

    def _rename_all(self):
        print('rename_all')
        # reconstruct all
        # generate new names for a qml type
        # rename that file
        # rename all files containing that name
        all_types = self.new_qmltypes_files.copy()
        print('\nall types\n', all_types)
        for x in all_types:

            old_file = all_types[x]
            folder, base_name = tuple(os.path.split(x))
            old_t_name = base_name.rsplit('.')[0]
            main_name = old_t_name.split('_', 1)[-1]
            print(main_name, old_t_name, base_name)
            print('up')
            # new name
            new_name = f'Live{randrange(1,250)}_{main_name}'
            # rename
            new_file = os.path.join(folder, f'{new_name}.qml')
            os.rename(old_file, new_file)
            self.new_qmltypes_files[x] = new_file
            self.u_qmltypes_map[old_t_name] = new_name

            # rename all files with that name
            for y in self.new_qmltypes_files:
                old_obj = old_t_name + ' {'
                new_obj = new_name + ' {'
                if self._is_in_file(old_obj, y):
                    with open(y, 'r') as fh:
                        data = fh.read()

                    data = data.replace(old_obj, new_obj)

                    with open(y, 'w') as fw:
                        fw.write(data)

    def _save_to_file(self, code):

        print('_save_to_file')
        # remove old file
        if os.path.exists(self.filename):
            os.unlink(self.filename)

        # Make file hidden to user
        if self.os_name == 'windows':
            name = str(randrange(1, 100000))
        else:
            name = '.' + str(randrange(1, 100000))

        self.filename = os.path.join(self.folder, name + '.qml')

        # replace
        for x in self.u_qmltypes_map:
            rx = r'\s' + x +' {'
            yx = '\n' + self.u_qmltypes_map[x] +' {'
            code = re.sub(rx, yx, code)

        # save file
        with open(self.filename, 'w') as fh:
            fh.write(code)

        # Make file hidden on win
        if self.os_name == 'windows':
            dos = 'attrib +s +h ' + self.filename
            os.system(dos)

        return True

    def _save_qmltype_file(self, code, filename):

        print('_save_qmltype_file: ', filename)
        # delete the current filename used for the qmltype
        """
        if filename:
            os.unlink(filename)
        """

        #new_file = self.new_qmltypes_files[filename]
        with open(filename, 'w') as fh:
            fh.write(code)

        # Make file hidden on win
        """if self.os_name == 'windows':
            dos = 'attrib +s +h ' + new_file
            os.system(dos)"""
