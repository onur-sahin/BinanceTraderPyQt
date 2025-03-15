import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Fusion

ColumnLayout{
    property alias btn_addAccount   : btn_addAccount
    property alias btn_delAccount   : btn_delAccount
    property alias btn_pullAccounts : btn_pullAccounts
    property alias myListViewAccount: myListViewAccount

    Item{
        Layout.fillWidth:true
        Layout.fillHeight:true

        ScrollView {
            anchors.fill:parent
            anchors.rightMargin:10

            id: scroll_accountSelect
            ScrollBar.vertical.policy:ScrollBar.AlwaysOn
            ScrollBar.horizontal.policy: ScrollBar.AlwaysOn
            ScrollBar.vertical.width:15
            ScrollBar.horizontal.height:15

            ColumnLayout {
                id:columnLayout
                // anchors.margins:10
                anchors.centerIn: parent
                
                MyListViewAccount{
                    id:myListViewAccount
                    Layout.minimumWidth: 100
                    Layout.minimumHeight: 100
                    Layout.preferredWidth: scroll_accountSelect.width*0.9
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
            id:btn_pullAccounts
            text:"Pull Accounts"
            Layout.fillWidth:true
        }

        Button{
            id:btn_addAccount
            text:"Add Account"
            Layout.fillWidth:true
        }

        Button{
            id:btn_delAccount
            text:"Delete Account"
            Layout.fillWidth:true
        }
    }



}


    

   

