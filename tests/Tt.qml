import QtQuick 2.10
import QtQuick.Controls 2.10
import QtQuick.Layouts 1.10


Rectangle {
    width: 200
    height: 200
    color: "red"

    Component.onCompleted: {
        console.log('Hello')
    }

}
