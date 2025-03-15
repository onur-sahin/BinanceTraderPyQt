import QtQuick
import QtQuick.Controls


ToolSeparator{
    width:100
    height:50
    
    Rectangle {

        anchors.fill:parent
        // radius: 1
        height: parent.height
        width: parent.width
        z:10
        gradient: Gradient {
        GradientStop { position: 1.0; color: "darkGray" }
        GradientStop { position: 0.0; color: "dimGray" }
    }

    }
    
}