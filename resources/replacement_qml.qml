import QtQuick.Controls 2.0

ApplicationWindow {
    visible: true

    property int foundWidth
    property int foundHeight

    width: foundWidth
    height: foundHeight

    Component.onCompleted: {
        foundWidth = this.contentData[0].width
        foundHeight = this.contentData[0].height
        var mainw = (x*2+160 - foundWidth) / 2
        var mainh = (y*2+160 - foundHeight) / 2

        x = mainw
        y = mainh

    }
