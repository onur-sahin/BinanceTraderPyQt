
import QtQuick
import QtQuick.Controls 2.1
import QtQuick.Layouts
import QtQuick.Dialogs
// import QtQuick.Controls.Material


MyListViewAccountForm{
    id:listView

    Connections{
        target:listView
    
        function onClicked_mouseArea_first(index){
            // console.log("First Field Double Clicked: " + index)
            var obj = listView.itemAtIndex(index).children[0].children[1].children[0] 
            obj.readOnly = false
            obj.forceActiveFocus() // Kullanıcı düzenleme yapabilsin
        }

    }


    Connections{
        target:listView

        function onClicked_mouseArea_second(index){
            var obj = listView.itemAtIndex(index).children[0].children[2].children[0] 
            obj.readOnly = false
            obj.forceActiveFocus() // Kullanıcı düzenleme yapabilsin
        }
    }

    Connections{
        target:listView

        function onNotes_editing_finished(index){
            var obj = listView.itemAtIndex(index).children[0].children[2].children[0]
            listView.model.getItem(index).update_account_notes(obj.text)
            obj.focus = false
            
        }
    }

    Connections{
        target:listView

        function onClicked_mouseArea_third(index){
            var obj = listView.itemAtIndex(index).children[0].children[3].children[0] 
            obj.readOnly = false
            obj.forceActiveFocus() // Kullanıcı düzenleme yapabilsin
        }
    }


    Connections {
        target: listView
        function onDoubleClicked_mouseArea_lock(index){
            dlg_keyInput.currentIndex        = index
            tf_apiKey   .pr_cryptedApiKey    = listView.model.getItem(index).cryptedApiKey
            tf_apiSecret.pr_cryptedApiSecret = listView.model.getItem(index).cryptedApiSecret

           
            tf_apiKey      .text       = listView.model.getItem(index).apiKey
            tf_apiSecret   .text       = listView.model.getItem(index).apiSecret
            tf_accountPass .text       = listView.model.getItem(index).accountPass
            ma_decrypteKeys.locked     = listView.model.getItem(index).isLocked

            dlg_keyInput.open();
        }
    }

    







    Dialog {
        id: dlg_keyInput
        width:700
        height:400
        title: "Enter Your Account Password and Decrypte"

        property int currentIndex : -1

        ColumnLayout{
            anchors.fill:parent
        

            ColumnLayout {
                spacing: 10
                Text {
                    
                    text: qsTr("Crypted Api Key: %1").arg(tf_apiKey.pr_cryptedApiKey)
                    Layout.fillWidth:true
                    color:"white"
                }

                TextField {
                    id: tf_apiKey
                    property string pr_cryptedApiKey
                    readOnly:true
                    text: ""
                    Layout.fillWidth:true
                    background: Rectangle {
                            implicitWidth : 200
                            implicitHeight: 40
                            color         : tf_apiKey.focus ? "transparent" : "#353637"
                            border.color  : tf_apiKey.focus ? "#21be2b"   : "transparent"

                    }

                }

            }


            ColumnLayout {
                spacing: 10
                Text {
                    text: qsTr("Crypted Api Secret: %1").arg(tf_apiSecret.pr_cryptedApiSecret)
                    Layout.fillWidth:true
                    color:"white"
                }

                TextField {
                    id: tf_apiSecret
                    property string pr_cryptedApiSecret
                    text:""
                    readOnly:true
                    Layout.fillWidth:true
                    background: Rectangle {
                            implicitWidth : 200
                            implicitHeight: 40
                            color         : tf_apiSecret.focus ? "transparent" : "#353637"
                            border.color  : tf_apiSecret.focus ? "#21be2b"   : "transparent"
                    }
                }
            }

            ColumnLayout {
                spacing: 10
                
                Text {
                    text: "Please enter your Account Pass and click key buttton on the left:"
                    Layout.fillWidth:true
                    color:"white"
                }

                RowLayout{
                    Item{
                        Layout.preferredHeight:parent.height
                        Layout.preferredWidth:20
                        Layout.fillWidth:true
                        Layout.alignment:Qt.AlignCenter
                        Text{
                            anchors.fill:parent
                            anchors.centerIn:parent
                            text:  ma_decrypteKeys.locked ? "   🔐" : "   🔓"
                            font.pixelSize:30
                            z:3
                        }

                        Rectangle {
                            anchors.fill:parent
                            color: ma_decrypteKeys.locked ? "black" : "green"
                            border.color:"white"
                            z:1
                        }

                        MouseArea {
                                id:ma_decrypteKeys
                                property bool locked : true
                                anchors.fill:parent
                                z:5
                        }

                    }

                    TextField {
                        id: tf_accountPass
                        readOnly:false
                        Layout.fillWidth:true
                        background: Rectangle {
                                implicitWidth: 200
                                implicitHeight: 40
                                color: tf_apiSecret.focus ? "transparent" : "#353637"
                                border.color: tf_apiSecret.focus ? "#21be2b" : "transparent"
                
                        }
                    }
                }

                CheckBox{
                    id:cb_rememberPass
                    text:"Remember Account Pass (Hashed text of your password will be saved your local file system!)"
                    checked: true
                    tristate:false
                }
            }

            ColumnLayout{
                Text {
                    id: txt_lock_testResult
                    Layout.preferredHeight:40
                    Layout.alignment:Qt.AlignCenter
                    font.pixelSize:20
                    color:"white"
                    Layout.fillWidth:true
                    text:"Test Result: None"

                    Rectangle{
                        anchors.fill:parent
                        color:"transparent"
                        border.width:1
                        border.color: "#f02c2c"
                    }
                }
            }

            RowLayout{
                Button{
                    id:btn_lock_save
                    Layout.fillWidth:true
                    text:"Save"
                }
                Button{
                    id:btn_lock_test
                    Layout.fillWidth:true
                    text:"test"
                    onClicked:{

                    }
                }
                Button{
                    id:btn_lock_cancel
                    Layout.fillWidth:true
                    text:"cancel"
                }
            }
        }
    }




    Connections {
        target:ma_decrypteKeys
        function onClicked() {
            var index = dlg_keyInput.currentIndex

            listView.model.getItem(index).decryptKeys(tf_accountPass.text)

            tf_apiKey      .text   = listView.model.getItem(index).apiKey
            tf_apiSecret   .text   = listView.model.getItem(index).apiSecret
            ma_decrypteKeys.locked = listView.model.getItem(index).isLocked
            var obj = listView.itemAtIndex(index).children[0].children[3].children[0] 

            listView.forceLayout()

        }
    }

    Connections {
        target: btn_lock_save

        function onClicked(){

            var index = dlg_keyInput.currentIndex
            listView.model.getItem(index).decryptKeys(tf_accountPass.text)
            listView.model.getItem(index).save_decryptedKeys(tf_accountPass.text, true)

            listView.forceLayout()
        }
    }

    Connections {
        target: btn_lock_cancel

        function onClicked(){
            dlg_keyInput.close();
        }
    }

    Connections {
        
        target: btn_lock_test

        function onClicked(){
            txt_lock_testResult.text = listView.model.testAccount(tf_apiKey.text, tf_apiSecret.text);
        }
    }

}