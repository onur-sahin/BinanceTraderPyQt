import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Fusion

ColumnLayout{
    property alias btn_addModel : btn_addModel
    property alias btn_delModel : btn_delModel

    Item{
        Layout.fillWidth:true
        Layout.fillHeight:true

        ScrollView {
            anchors.fill:parent
            anchors.rightMargin:10

            id: scroll_modelSelect
            ScrollBar.vertical.policy:ScrollBar.AlwaysOn
            ScrollBar.horizontal.policy: ScrollBar.AlwaysOn
            ScrollBar.vertical.width:15
            ScrollBar.horizontal.height:15

            ColumnLayout {
                id:columnLayout
                // anchors.margins:10
                anchors.centerIn: parent
                
                MyListViewModel{
                    Layout.minimumWidth: 100
                    Layout.minimumHeight: 100
                    Layout.preferredWidth: scroll_modelSelect.width*0.9
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.leftMargin:20
                    Layout.topMargin:20

                }

            
            }

        }

        Rectangle {
            width:parent.width
            height:parent.height
            color:"transparent"
            border.width:3
            border.color:"darkRed"
        }
    }


    RowLayout{
        Button{
            id:btn_addModel
            text:"Add Model"
            Layout.fillWidth:true
        }

        Button{
            id:btn_delModel
            text:"Delete Model"
            Layout.fillWidth:true
        }
    }



}
