import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "others" as Other

ApplicationWindow {
    id: __main_win_dow__
    visible: true
    width: 480
    height: 600
    flags: Qt.WindowSystemMenuHint | Qt.Window | Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowMinMaxButtonsHint | Qt.WindowStaysOnTopHint

    property QtObject __qmlview__live_o_bject
    property string filename: ""

    property int d_width: 480
    property int d_height: 600

    signal handleShowProps()

    onHandleShowProps: {
        var show = __main_pop_up__window__.showProps
        __qmlview__live_o_bject.show_props(!show)
        __main_pop_up__window__.showProps = !show
        if(!show) {
            __qmlview__live_o_bject.oldProps = [width, height]
            __qmlview__live_o_bject.show_props(!show)
        } else {
            // set width and height
            __qmlview__live_o_bject.show_props(!show)
            __main_win_dow__.setWidth(d_width)
            __main_win_dow__.setHeight(d_height)
        }
    }

    FontLoader { id: __main__live_font__; source: "../fonts/fa.otf"}


    ApplicationWindow {
        id: __main_pop_up__window__
        visible: true
        width: 128
        height: 32
        x: __main_win_dow__.x + ((__main_win_dow__.width - width) / 2)
        y: __main_win_dow__.y - 72
        flags: Qt.Popup | Qt.WindowSystemMenuHint
        color: "white"

        property bool showProps: false

        RowLayout {
            anchors.fill: parent

            Other.CustomLiveButton {
                text: "\uf46a"
                enabled: false
            }

            Other.CustomLiveButton {
                text: __main_pop_up__window__.showProps ? "\uf850" : "\uf84c"

                onClicked: {
                    handleShowProps()
                }
            }

        }

    }




    Connections {
        target: __qmlview__live_o_bject

        function onUpdated(code) {
            var qml_obj = Qt.createQmlObject(code, __main_win_dow__, filename)
        }

        function onPropsUpdated(props, code) {
            var width = props[0]
            var height = props[1]

            // set width and height
            __main_win_dow__.setWidth(width)
            __main_win_dow__.setHeight(height)

        }
    }


}
