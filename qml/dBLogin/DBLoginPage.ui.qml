import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Fusion

Page {
    // Imagine.theme:"dark"
    // Material.theme: Material.Dark
    // Material.theme: Material.Light
    // Material.accent: Material.Light
    // Material.foreground: Material.Green
    // Material.background: Material.Teal
    id: loginAppPage

    // width: 400
    // height: 850
    property alias le_database: le_database
    property alias le_user: le_user
    property alias le_host: le_host
    property alias le_port: le_port
    property alias le_password: le_password
    property alias cb_remember_pass: cb_remember_pass
    property alias btn_test_connection: btn_test_connection
    property alias btn_login: btn_login
    property alias btn_cancel: btn_cancel

    property alias ta_connection_test_result: ta_connection_test_result

    ScrollView {

        width: parent.width - 10
        height: parent.height - 10
        // anchors.fill:parent
        anchors.centerIn: parent

        // ScrollBar.vertical.policy: ScrollBar.AlwaysOn
        ScrollBar.vertical.width: 15
        // ScrollBar.horizontal.policy: ScrollBar.AlwaysOn
        ScrollBar.horizontal.height: 15

        Column {
            id: column
            width: loginAppPage.width
            spacing: 20 // Öğeler arasında boşluk

            Label {
                id: label
                text: qsTr("Before using this Binance Trade program, you need to install the PostgreSQL database management program on your computer!")
                wrapMode: Text.Wrap
                width: parent.width - 25

                horizontalAlignment: Text.AlignJustify
            }

            ToolSeparator {
                id: toolSeparator
                width: parent.width - 25
            }

            Label {
                id: label1
                text: qsTr(
                          "Insert your PostgreSQL database connection settings")
                wrapMode: Text.Wrap
                width: parent.width
                horizontalAlignment: Text.AlignJustify
            }

            Row {
                id: row
                width: parent.width - 25

                // spacing: 10 // Satır içi boşluk
                Label {
                    id: label2
                    text: qsTr("Database:")
                    width: parent.width * 0.3 // Sol bileşenin genişliği
                    horizontalAlignment: Text.AlignLeft
                }

                TextField {
                    id: le_database
                    width: parent.width * 0.7 // Sağ bileşenin genişliği
                    text: qsTr("binancedb")
                    color: label2.color
                }
            }

            Label {
                id: databaseInfo
                wrapMode: Text.Wrap
                width: parent.width * 1
                anchors.right: parent.right
                anchors.rightMargin: 25
                text: qsTr("The database name cannot be 'postgres'. You must create a new database specifically for storing Binance data and program-related data using the PostgreSQL terminal or a PostgreSQL graphical user interface. For example, you can create a database named binancedb and enter the connection settings into this window. You must manually create the PostgreSQL database that the program will use.")
                horizontalAlignment: Text.AlignJustify
                font.pointSize:8
            }

            ToolSeparator {
                id: toolSeparator1
                width: parent.width - 25
            }

            GridLayout {
                width: parent.width - 25
                columns: 2

                Label {
                    id: label3
                    Layout.preferredWidth: parent.width * 0.3
                    text: qsTr("user")
                }

                TextField {
                    id: le_user
                    Layout.preferredWidth: parent.width * 0.7
                    text: qsTr("postgres")
                    color: label3.color
                }

                Label {
                    id: label4
                    Layout.preferredWidth: parent.width * 0.3
                    text: qsTr("host")
                }

                TextField {
                    id: le_host
                    Layout.preferredWidth: parent.width * 0.7
                    text: qsTr("localhost")
                    color: label4.color
                }

                Label {
                    id: label5
                    Layout.preferredWidth: parent.width * 0.3
                    text: qsTr("port")
                }

                TextField {
                    id: le_port
                    Layout.preferredWidth: parent.width * 0.7
                    text: qsTr("5432")
                    color: label5.color
                }

                Label {
                    id: label6
                    Layout.preferredWidth: parent.width * 0.3
                    text: qsTr("password")
                }

                TextField {
                    id: le_password
                    echoMode: TextInput.Password
                    Layout.preferredWidth: parent.width * 0.7
                    text: qsTr("")
                    passwordCharacter: "*"
                    color: label6.color
                }
            }

            Row {
                width: parent.width * 0.7 - 25
                anchors.right: parent.right
                anchors.rightMargin: 25

                CheckBox {
                    id: cb_remember_pass
                    text: qsTr("remember password")
                    tristate: false
                    width: parent.width * 0.5
                }

                Button {
                    id: btn_test_connection

                    text: qsTr("Test Connection")
                    width: parent.width * 0.5
                }
            }
            ScrollView {
                width: parent.width - 25
                height: Screen.height * 0.07
                ScrollBar.vertical.policy: ScrollBar.AlwaysOn
                ScrollBar.vertical.width: Screen.width * 0.01
                ScrollBar.horizontal.policy: ScrollBar.AlwaysOn
                ScrollBar.horizontal.height: Screen.width * 0.01

                // ScrollBar.vertical.shape:
                TextArea {
                    id: ta_connection_test_result
                    width: parent.width
                    text: qsTr("Connection test result: None")
                    readOnly: true
                }
            }
            Row {
                width: parent.width * 0.7 - 25
                anchors.right: parent.right
                anchors.rightMargin: 25
                spacing: 20
                Button {
                    id: btn_login
                    text: qsTr("Login")
                    width: parent.width * 0.5 - 10
                }

                Button {
                    id: btn_cancel
                    text: qsTr("Cancel")
                    width: parent.width * 0.5 - 10
                }
            }
        }
    }
}
