import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts

Button {
    Layout.alignment: Layout.Center
    Layout.preferredWidth: 36
    Layout.preferredHeight: 28
    font.family: __main__live_font__.name
    font.pixelSize: 16

    background: Rectangle {
        implicitWidth: 36
        implicitHeight: 28
        color: parent.pressed ? "#c1c1c1" : parent.hovered ? "#e1e1e1" : "transparent"
    }

    contentItem: Text {
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
        text: parent.text
        font: parent.font
        opacity: enabled ? 1.0 : 0.5
    }

}
