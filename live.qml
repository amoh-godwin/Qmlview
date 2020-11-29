import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "resources/qml/others" as Other

ApplicationWindow {
    id: __main_win_dow__
    visible: true
    width: 480
    height: 600
    flags: Qt.WindowSystemMenuHint | Qt.Window | Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowMinMaxButtonsHint | Qt.WindowStaysOnTopHint

    property QtObject __qmlview__live_o_bject
    property string filename: ""


    FontLoader { id: __main__font__; source: "file:///H:/GitHub/Qmlview/resources/fonts/fa.otf"}


    ApplicationWindow {
        visible: true
        width: 128
        height: 32
        x: __main_win_dow__.x + 176
        y: __main_win_dow__.y - 72
        flags: Qt.Popup | Qt.WindowSystemMenuHint
        color: "white"

        RowLayout {
            anchors.fill: parent

            Other.CustomButton {
                text: "\uf850"
            }

            Other.CustomButton {
                text: "\uf84c"
            }

        }

    }


    Connections {
        target: __qmlview__live_o_bject

        function onUpdated(code) {
            var qml_obj = Qt.createQmlObject(code, __main_win_dow__, filename)
        }
    }


}
