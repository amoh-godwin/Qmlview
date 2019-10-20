import QtQuick 2.10
import QtQuick.Controls 2.3

ApplicationWindow {
    visible: true
    width: 400
    height: 640
    color: "black"

    Component.onCompleted: { console.log('love')}

    property string the_love: "JESUS"

    signal this_is_it()

    onThis_is_it: {
        console.log('dance')
    }

    menuBar: Rectangle {
        width: 400
        height: 48
        color: "dodgerblue"
    }

    header: Rectangle {
        width: 400
        height: 48
        color: "dodgerblue"
    }


    Rectangle {
        width: parent.width
        height: parent.height
        color: "gold"
    }

    footer: Rectangle {
        width: 400
        height: 48
        color: "dodgerblue"
    }

}
