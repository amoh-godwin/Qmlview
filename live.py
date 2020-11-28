"""
Module for Live Reloading
"""
import threading

from PyQt5.QtCore import QObject, QFile, QResource, QIODevice


QResource.registerResource("_qmlview_resource_.rcc")


class Live(QObject):


    """
    """


    def __init__(self, engine, ward):
        QObject.__init__(self)
        self.engine = engine
        self._initialiase()

    def _initialiase(self):
        self._call_auto_reload()

    def _call_auto_reload(self):
        a_thread = threading.Thread(target=self._auto_reload)
        a_thread.daemon = True
        a_thread.start()

    def _auto_reload(self):
        pass
