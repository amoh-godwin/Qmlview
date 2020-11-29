"""
Module for Live Reloading
"""
import threading
from time import sleep

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QFile, QResource, QIODevice

from misc import Split

QResource.registerResource("_qmlview_resource_.rcc")


class Live(QObject):


    """
    """


    def __init__(self, watch_file):
        QObject.__init__(self)
        self.watch_file = watch_file

        self.old_code = ''

        self._initialiase()

    updated = pyqtSignal(str, arguments=['updater'])

    def updater(self, code):
        self.updated.emit(code)

    def _initialiase(self):
        self._call_auto_reload()

    def _call_auto_reload(self):
        a_thread = threading.Thread(target=self._auto_reload)
        a_thread.daemon = True
        a_thread.start()

    def _auto_reload(self):
        while True:
            code = self._read_file(self.watch_file)
            if code != self.old_code:
                self.updater(code)
                self.old_code = code
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
