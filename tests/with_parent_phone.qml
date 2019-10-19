import QtQuick 2.10
import QtQuick.Controls 2.3

ApplicationWindow {
    visible: true
    width: 400
    height: 400

    Component.onCompleted: {console.log('love')}

    footer: Rectangle {
        width: 400
        height: 200
        color: "dodgerblue"
    }

}
