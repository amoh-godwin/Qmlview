import QtQuick 2.10
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3

ApplicationWindow {
    id: main__window
    visible: true
    width: 360
    height: 640
    title: qsTr("Window")
    color: "black"
    flags: Qt.Window | Qt.FramelessWindowHint

    Component.onCompleted: {
        bg.width = width + 24
    }

    background: Rectangle {
        id: bg
        anchors.fill: parent
        color: "transparent"

        Image {
            width: parent.width
            height: parent.height
            source: "qrc:///images/phone-bg.png"
        }

    }

    Rectangle {
        id: ff__
        anchors.fill: parent
        anchors.topMargin: 36
        anchors.bottomMargin: 36
        anchors.leftMargin: 24
        anchors.rightMargin: 24
        color: "black"

        ColumnLayout {
            anchors.fill: parent
            spacing: 0

            Rectangle {// menubar
                id: _hidd_me_nu_bar
                Layout.fillWidth: true
                Layout.preferredHeight: (children.length > 0) ? children[0].height : 48
                visible: (children.length > 0)
                color: "black"

            }

            Rectangle {// header
                id: _hidd_he_ad_er
                Layout.fillWidth: true
                Layout.preferredHeight: (children.length > 0) ? children[0].height : 48
                visible: (children.length > 0)
            }

            Rectangle {// contentItem
                id: _hidd_co_nt_entItem
                Layout.fillWidth: true
                Layout.maximumWidth: ff__.width
                Layout.fillHeight: true
                Layout.maximumHeight: ff__.height
                visible: (children.length > 0)
                clip: true
                objectName: "ContentItem"


            }

            Rectangle {// footer
                id: _hidd_fo_ot_er
                Layout.fillWidth: true
                Layout.preferredHeight: (children.length > 0) ? children[0].height : 48
                visible: (children.length > 0)
            }

        }
    }

}
