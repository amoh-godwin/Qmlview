import QtQuick 2.10
import QtQuick.Controls 2.10
import QtQuick.Layouts 1.10

ApplicationWindow {
    id: m
    visible: true
    width: 400
    height: 400
    title: "Love is Good"

    Rectangle {
        anchors.fill: parent
        color: "dodgerblue"

        Text {
            anchors.centerIn: parent
            text: "I really wanted this all"
            color: "white"
        }

        Rectangle {
            width: parent.width
            height: 42
            color: "gold"
        }
    }

    Tt {}

}
