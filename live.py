"""
Module for Live Reloading
"""
import threading
from time import sleep

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QFile, QResource, QIODevice, pyqtProperty

from misc import Split

QResource.registerResource("_qmlview_resource_.rcc")


class Live(QObject):


    """
    """


    def __init__(self, watch_file):
        QObject.__init__(self)
        self.watch_file = watch_file

        self.show_props = False

        self.old_code = ''
        self.old_props = ''

        self.not_closed = True

        self._initialiase()

    updated = pyqtSignal(str, arguments=['updater'])
    propsUpdated = pyqtSignal(list, str, arguments=['props_updater'])

    def props_updater(self, props, code):
        try:
            self.propsUpdated.emit(props, code)
        except RuntimeError:
            # possibly user exited out
            pass

    def updater(self, code):
        try:
            self.updated.emit(code)
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
        self._call_auto_reload()

    def _call_auto_reload(self):
        a_thread = threading.Thread(target=self._auto_reload)
        a_thread.daemon = True
        a_thread.start()

    def _auto_reload(self):
        while self.not_closed:
            if not self.show_props:
                code = self._read_file(self.watch_file)
                if code != self.old_code:
                    self.updater(code)
                    self.old_code = code
            else:
                props, code = self._read_all_file(self.watch_file)
                if props != self.old_props:
                    self.props_updater(props, code)
                    self.old_props = props
                elif code == self.old_code:
                    self.old_code = code
                    self.updater(code)
            sleep(0.1)

    def _read_file(self, filename):
        code = ""

        splitter = Split(filename)
        imps = splitter.orig_imp_stats
        bottom_code = splitter.orig_bottom_lines
        imps_text = ''.join(imps)
        btm_code_text = ''.join(bottom_code)
        code = imps_text + btm_code_text

        return code

    def _read_all_file(self, filename):

        splitter = Split(filename)
        imps = splitter.orig_imp_stats
        bottom_code = splitter.orig_bottom_lines
        props = splitter.wind_user_props
        prop = [props['width'].split(':')[-1].strip(), props['height'].split(':')[-1].strip()]
        imps_text = ''.join(imps)
        btm_code_text = ''.join(bottom_code)
        code = imps_text + btm_code_text

        return prop, code
