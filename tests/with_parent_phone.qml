import QtQuick 2.10
import QtQuick.Controls 2.3

ApplicationWindow {
    visible: true
    width: 400
    height: 400

    Component.onCompleted: {console.log('love')}

    menuBar: Rectangle {
        width: 400
        height: 200
        color: "dodgerblue"
    }

    header: Rectangle {
        width: 400
        height: 200
        color: "dodgerblue"
    }


    Rectangle {
        width: 400
        height: 400
        color: "gold"
    }

    footer: Rectangle {
        width: 400
        height: 200
        color: "dodgerblue"
    }

}
