import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


Window {
    id: root
    width : Screen.width  * 0.3
    height: Screen.height * 0.5
    x: 100
    y: 100

    property alias btn_save              : btn_save
    property alias tf_modelName          : tf_modelName
    property alias tf_defaultPair        : tf_defaultPair
    property alias tf_windowSize         : tf_windowSize
    property alias tf_defaultInterval    : tf_defaultInterval
    property alias cb_modelType          : cb_modelType
    property alias btn_cancel            : btn_cancel
    property alias messageDialog         : messageDialog
    property alias btn_networks          : btn_networks
    property alias networkWin            : networkWin
    property alias cl_network            : cl_network

    property alias btn_save_network      : btn_save_network


    ColumnLayout {
        id: root_cl
        spacing: 10
        anchors.fill: parent
        Layout.fillWidth: true
        signal completed()
        
        Component.onCompleted: completed()

        RowLayout {
            Layout.rightMargin: 20
            Layout.leftMargin: 20
            Label {
                Layout.preferredWidth: root.width * 0.3
                text: "Model Name"
            }
            TextField {
                id: tf_modelName
                Layout.fillWidth: true
                placeholderText: "model name"
            }
        }
        RowLayout {
            Layout.rightMargin: 20
            Layout.leftMargin: 20
            Label {

                Layout.preferredWidth: root.width * 0.3
                text: "Default Pair"
            }
            TextField {
                id: tf_defaultPair
                Layout.fillWidth: true
                placeholderText: "Default Pair"
            }
        }
        RowLayout {
            Layout.rightMargin: 20
            Layout.leftMargin: 20
            Label {
                Layout.preferredWidth: root.width * 0.3
                text: "Window Size"
            }
            TextField {
                id: tf_windowSize
                Layout.fillWidth: true
                validator: IntValidator { bottom: 1 }
            }
        }
        RowLayout {
            Layout.rightMargin: 20
            Layout.leftMargin: 20
            Label {
                Layout.preferredWidth: root.width * 0.3
                text: "Default Interval"
            }
            TextField {
                id: tf_defaultInterval
                Layout.fillWidth: true
                validator: IntValidator { bottom: 1 }
            }
       
        }
        RowLayout{
            Layout.rightMargin: 20
            Layout.leftMargin: 20
            TextField{
                Layout.preferredWidth: root.width * 0.9
                Layout.fillWidth: true
                text:"s=second m=minute h=hour\nW=weak  D =day        M=month"
                readOnly:true
            }
        }
        RowLayout {
            Layout.rightMargin: 20
            Layout.leftMargin: 20

            Label {
                Layout.preferredWidth: root.width * 0.3
                text: "Model Type"
            }

            ComboBox {
                id:cb_modelType
                Layout.fillWidth: true
            }
            Button{
                id: btn_networks
                Layout.preferredWidth: root.width * 0.2
                text: "Networks"
            }

        }


        RowLayout {

            Layout.rightMargin: 20
            Layout.leftMargin: 20
            Layout.fillWidth:true
            Button {
                id: btn_save
                Layout.preferredWidth:root.width*0.45
                text: "SAVE"
            }
            Button {
                id: btn_cancel
                Layout.preferredWidth:root.width*0.45
                text: "CANCEL"
            }
        }
    }


    Dialog{
        id:messageDialog
        width:500
        height:300
        property string messageText
        contentItem: Text {
                        id:text
                        text: messageDialog.messageText
                     }
        standardButtons: Dialog.Ok
    }

    Window{
        id: networkWin
        width:1300
        height:800
        ScrollView{

            width:parent.width-20
            height:parent.height-20

            ScrollBar.vertical: ScrollBar {
                width:15
                height:parent.height

                anchors.left: parent.right // Scrollbar'ı sağ tarafa yerleştiririz
                policy: ScrollBar.AlwaysOn
            }
            ScrollBar.horizontal: ScrollBar {
                height: 15
                width: parent.width
                anchors.top: parent.bottom // Scrollbar'ı alt tarafa yerleştiririz
                policy: ScrollBar.AlwaysOn
            }

        
            ColumnLayout{
                anchors.fill:parent
                
                ColumnLayout{
                    id:cl_network
                    property bool created: false
                    // Layout.fillWidth:true
                    // Layout.fillHeight:true
                }

                RowLayout{
                    id:cl_buttons
                    // Layout.fillWidth:true

                    Button{
                        id:btn_save_network
                        text:"SAVE"
                        Layout.fillWidth:true
                    }
                    Button{
                        text:"btn2"
                        Layout.fillWidth:true
                    }
                }



            }
        }


    }


}
