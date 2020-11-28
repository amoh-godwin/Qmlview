import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    id: __main_win_dow__
    visible: true
    width: 500
    height: 400

    property QtObject __qmlview__live_o_bject


    Connections {
        target: __qmlview__live_o_bject

        function onUpdated(code) {
            console.log(code)
            var qml_obj = Qt.createQmlObject(code, __main_win_dow__, 'livetest.qml')
        }
    }


}
