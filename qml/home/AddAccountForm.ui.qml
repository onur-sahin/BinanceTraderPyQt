import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import com.binancetrader.AccountMdl 1.0
import com.binancetrader.Enums.AccountTypes 1.0


Window {
    id: root
    width: Screen.width * 0.3
    height: Screen.height * 0.5
    x: 100
    y: 100
    color:"grey"


    property alias btn_test_key_and_secret   : btn_test_key_and_secret
    property alias btn_save                  : btn_save
    property alias btn_cancel                : btn_cancel
    property alias tf_accountName            : tf_accountName
    property alias tf_apiKey                 : tf_apiKey
    property alias tf_apiSecret              : tf_apiSecret
    property alias cb_realAccount            : cb_realAccount
    property alias cb_mockAccount            : cb_mockAccount
    property alias cb_binance                : cb_binance    
    property alias cb_cm_future              : cb_cm_future  
    property alias cb_um_future              : cb_um_future  
    property alias bg_accountGroup           : bg_accountGroup
    property alias bg_typeGroup              : bg_typeGroup
    property alias pr_accountPass            : cl_accountPassword.pr_accountPass
    property alias cb_rememberAccountPass    : cb_rememberAccountPass
    property alias tf_testResult             : tf_testResult
    property alias root_cl                   : root_cl
    

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
                text: "Account Name"
            }
            TextField {
                id: tf_accountName
                Layout.fillWidth: true
                placeholderText: "Account name"
                
            }
        }
        RowLayout {
            Layout.rightMargin: 20
            Layout.leftMargin: 20
            Label {

                Layout.preferredWidth: root.width * 0.3
                text: "Api Key"
            }
            TextField {
                id: tf_apiKey
                Layout.fillWidth: true
                placeholderText: "Api Key"
            }
        }
        RowLayout {
            Layout.rightMargin: 20
            Layout.leftMargin: 20
            Label {
                Layout.preferredWidth: root.width * 0.3
                text: "Api Secret"
            }
            TextField {
                id: tf_apiSecret
                Layout.fillWidth: true
                placeholderText: "Api Secret"
            }
        }
        RowLayout {
            Layout.rightMargin: 20
            Layout.leftMargin: 20

            ButtonGroup {
                id: bg_accountGroup
                exclusive: true
                
            }

            Label {
                Layout.preferredWidth: root.width * 0.3
                text: "Account Real or Mock"
            }
            RowLayout {
                Layout.rightMargin: 20
                Layout.leftMargin: 20
                CheckBox {
                    id: cb_realAccount
                    Layout.fillWidth: true
                    text: "Real Account"
                    ButtonGroup.group: bg_accountGroup
                }
                CheckBox {
                    id: cb_mockAccount
                    Layout.fillWidth: true
                    text: "Mock Account"
                    ButtonGroup.group: bg_accountGroup
                }
            }
            
        }


        RowLayout {
            Layout.rightMargin: 20
            Layout.leftMargin: 20

            ButtonGroup {
                id: bg_typeGroup
                exclusive: true
                
            }

            Label {
                Layout.preferredWidth: root.width * 0.2
                text: "Account Type"
            }
            RowLayout {
                Layout.rightMargin: 20
                Layout.leftMargin: 20
                CheckBox {
                    id: cb_binance
                    Layout.fillWidth: true
                    text: AccountTypes.to_string(0)  // enum değerleri aslında int olduğundan bu ifade 0 numaralı enumun stringini döndürür
                    ButtonGroup.group: bg_typeGroup
                }
                CheckBox {
                    id: cb_cm_future
                    Layout.fillWidth: true
                    text: AccountTypes.to_string(1)
                    ButtonGroup.group: bg_typeGroup
                }
                CheckBox {
                    id: cb_um_future
                    text: AccountTypes.to_string(2)
                    ButtonGroup.group: bg_typeGroup
                }
            }
            
        }




        RowLayout {
            Layout.rightMargin: 20
            Layout.leftMargin: 20
            Button {
                id: btn_test_key_and_secret
                Layout.preferredWidth: root.width * 0.3
                text: "Test Key and Secret"
            }
            TextField {
                id:tf_testResult
                Layout.fillWidth: true
                text: "Not Tested"
                readOnly: true
            }
        }

        ColumnLayout{
            id: cl_accountPassword
            Layout.rightMargin: 20
            Layout.leftMargin: 20
            property bool    passwordsMatch: false // Şifrelerin eşit olup olmadığını kontrol eden flag
            property string pr_accountPass : passwordsMatch ? passwordField1.text : ""

            Text {
                Layout.fillWidth: true
                wrapMode: Text.Wrap
                color:"white"
                text: "Please enter a password to encrypt your Binance Account API Key and Secret Key, or your account information may be exposed to others."
            }
            // Birinci şifre TextField
            TextField {
                id: passwordField1
                Layout.fillWidth:true
                placeholderText: "Enter password"
                echoMode: TextInput.Password

                // Şifreler eşleşmiyorsa kenarlık rengi kırmızı olur
                
                onTextChanged:{ cl_accountPassword.passwordsMatch = passwordField1.text === passwordField2.text ? true : false}
                Rectangle{
                    anchors.fill:parent
                    color:"transparent"
                    border.width:2
                    border.color: cl_accountPassword.passwordsMatch ? "green" : "red"
                }
            
            }

            // İkinci şifre TextField
            TextField {
                id: passwordField2
                Layout.fillWidth:true
                placeholderText: "Confirm password"
                echoMode: TextInput.Password
                onTextChanged:{ cl_accountPassword.passwordsMatch = passwordField1.text === passwordField2.text ? true : false}

                Rectangle{
                    anchors.fill:parent
                    color:"transparent"
                    border.width:2
                    border.color: cl_accountPassword.passwordsMatch ? "green" : "red"
                }
            }

            CheckBox {
                id:cb_rememberAccountPass
                text:"Remember Password"
                tristate:false

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
}
