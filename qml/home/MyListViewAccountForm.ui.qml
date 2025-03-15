import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


   

ListView {
    id: root
    // anchors.fill:parent


    signal clicked_mouseArea_first(int index)
    signal clicked_mouseArea_second(int index)
    signal clicked_mouseArea_third(int index)

    signal doubleClicked_mouseArea_lock(int index)

    model: accountListModelMdl

    delegate: Rectangle {
        width: root.width
        height: 40
        color: root.currentIndex === index ? "red" : "lightGrey" // Seçili satır rengi

        Row {
            anchors.centerIn:parent
            width: parent.width -20
            height: parent.height -20
            spacing: 0

            Rectangle {
                width: 30
                height:parent.height
            
                Text{
                    id:txt
                    text: model.isLocked ? "🔐" : "🔓"
                    font.pixelSize: 30
                    anchors.centerIn:parent
                    width:parent.width
  
                }
                color:"transparent"

                MouseArea {
                    id:ma_lock
                    anchors.fill:parent
                    onDoubleClicked:root.doubleClicked_mouseArea_lock(index)
                }
            }

            Rectangle {

                width: parent.width/3
                height: parent.height

                color: "transparent"

                TextField {
                    id: firstField
                    anchors.centerIn:parent
                    width: parent.width
                    text: model.accountName
                    readOnly: true
                    focus: true  // Çift tıklanınca odak alması için
                }

                MouseArea {
                    id:mouseArea_first
                    anchors.fill: parent
                    acceptedButtons: Qt.LeftButton
                    propagateComposedEvents: true  // Olayları üst bileşenlere de ilet
                    onDoubleClicked: root.clicked_mouseArea_first(index)
                }
            }

            Rectangle {
                width: parent.width /3
                height: parent.height
                color: "transparent"

                TextField {
                    id: secondField
                    anchors.centerIn:parent
                    width: parent.width
                    text: model.accountNotes
                    readOnly: true
                    focus: true
                }

                MouseArea {
                    id: mouseArea_second
                    anchors.fill: parent
                    acceptedButtons: Qt.LeftButton
                    propagateComposedEvents: true
                    onDoubleClicked: clicked_mouseArea_second(index)
                }
            }

            Rectangle {
                width: parent.width /3 -30
                height: parent.height
                color: "transparent"

                TextField {
                    id: thirdField
                    anchors.centerIn:parent
                    width: parent.width
                    text: "empty"
                    readOnly: true
                    focus: true
                }

                MouseArea {
                    id: mouseArea_third
                    anchors.fill: parent
                    acceptedButtons: Qt.LeftButton
                    propagateComposedEvents: true
                    onDoubleClicked: clicked_mouseArea_third(index)
                }
            }
        }

        MouseArea {
            id:mouseArea_rectangle
            anchors.fill: parent
            acceptedButtons: Qt.LeftButton
            propagateComposedEvents: true  // Olayları ilet
            onClicked: root.currentIndex = index // Satırı seçili yap
        }
    }
}
