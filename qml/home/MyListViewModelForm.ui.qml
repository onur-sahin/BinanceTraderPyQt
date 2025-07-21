import QtQuick
import QtQuick.Controls


   

ListView {
    id: listView
    width: 400
    height: 800

    signal clicked_mouseArea_first(int index)
    signal clicked_mouseArea_second(int index)
    signal clicked_mouseArea_third(int index)
    property alias listView : listView

    model: modelListModelMdl

    delegate: Rectangle {
        width: ListView.view.width
        height: 40
        color: ListView.view.currentIndex === index ? "lightBlue" : "lightGrey" // Seçili satır rengi

        Row {
            anchors.centerIn:parent
            width: parent.width -20
            height: parent.height -20
            spacing: 0

            Rectangle {

                width: parent.width/3
                height: parent.height

                color: "transparent"

                TextField {
                    id: firstField
                    anchors.centerIn:parent
                    width: parent.width
                    text: modelObj.modelName
                    readOnly: true
                    focus: true  // Çift tıklanınca odak alması için
                }

                MouseArea {
                    id:mouseArea_first
                    anchors.fill: parent
                    acceptedButtons: Qt.LeftButton
                    propagateComposedEvents: true  // Olayları üst bileşenlere de ilet
                    onDoubleClicked: clicked_mouseArea_first(index)
                }
            }

            Rectangle {
                width: parent.width / 3
                height: parent.height
                color: "transparent"

                TextField {
                    id: secondField
                    anchors.centerIn:parent
                    width: parent.width
                    text: modelObj.notes
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

            // Rectangle {
            //     width: parent.width / 3
            //     height: parent.height
            //     color: "transparent"

            //     TextField {
            //         id: thirdField
            //         anchors.centerIn:parent
            //         width: parent.width
            //         text: model.third
            //         readOnly: true
            //         focus: true
            //     }

            //     MouseArea {
            //         id: mouseArea_third
            //         anchors.fill: parent
            //         acceptedButtons: Qt.LeftButton
            //         propagateComposedEvents: true
            //         onDoubleClicked: clicked_mouseArea_third(index)
            //     }
            // }
        }

        MouseArea {
            id:mouseArea_rectangle
            anchors.fill: parent
            acceptedButtons: Qt.LeftButton
            propagateComposedEvents: true  // Olayları ilet
            onClicked: listView.currentIndex = index // Satırı seçili yap
        }
    }
}
