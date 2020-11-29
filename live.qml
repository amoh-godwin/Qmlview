import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    id: __main_win_dow__
    visible: true
    width: 480
    height: 600
    flags: Qt.WindowSystemMenuHint | Qt.Window | Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowMinMaxButtonsHint | Qt.WindowStaysOnTopHint

    property QtObject __qmlview__live_o_bject
    property string filename: ""


    Connections {
        target: __qmlview__live_o_bject

        function onUpdated(code) {
            var qml_obj = Qt.createQmlObject(code, __main_win_dow__, filename)
        }
    }


}
