import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Fusion
Page {
    id:tradePage
    // anchors.fill:parent olmaz

    property string msg : "Empty"

    Label{
        id:label
        anchors.centerIn:parent
        text:tradePage.msg
        font.pixelSize: 40
        font.bold:true

    }
}