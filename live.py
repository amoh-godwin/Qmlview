"""
Module for Live Reloading
"""
from PyQt5.QtCore import QFile, QResource, QIODevice
QResource.registerResource("_qmlview_resource_.rcc")


class Live():


    """
    """


    def __init__(self, engine, ward):
        self.engine = engine
        self._start_parent()

    def _start_parent(self):
        self.engine.load('live.qml')
