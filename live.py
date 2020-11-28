"""
Module for Live Reloading
"""
import threading
from time import sleep

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QFile, QResource, QIODevice


QResource.registerResource("_qmlview_resource_.rcc")


class Live(QObject):


    """
    """


    def __init__(self, watch_file):
        QObject.__init__(self)
        self.watch_file = watch_file
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
            self.updater(code)
            sleep(1)

    def _read_file(self, filename):
        code = ""

        with open(filename, mode='r') as fh:
            code = fh.read()

        return code
