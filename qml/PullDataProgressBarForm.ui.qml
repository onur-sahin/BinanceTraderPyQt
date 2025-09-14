import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Fusion

Rectangle {
    id: rec_progbarBorder
    color: "transparent"
    border.width: 4
    border.color: "blue"
    width: root_rec.implicitWidth + 40
    height: root_rec.implicitHeight + 40
    Layout.leftMargin: 40

    property alias root_rec           : root_rec
    property alias pb_pulldata        : pb_pulldata
    property alias pb_pulldata2       : pb_pulldata2
    property alias btn_cancel         : btn_cancel
    property alias btn_close          : btn_close
    property alias tx_infoProgressBar : tx_infoProgressBar
    property alias rec_progbarBorder  : rec_progbarBorder
    property alias ma_progbarBorder   : ma_progbarBorder


    MouseArea {
        id:ma_progbarBorder
        anchors.fill:parent
    }



    ColumnLayout {
        id: root_rec
        anchors.fill: parent
        spacing: 15
        // Layout.preferredHeight:400
        // Layout.preferredWidth: 600

        Text {
            id: tx_infoProgressBar
            color: "white"
            Layout.fillWidth: true
            Layout.leftMargin: 20
            Layout.rightMargin: 20
            Layout.topMargin: 15
        }

        ProgressBar {
            id: pb_pulldata
            objectName: "pb_pulldata"
            Layout.leftMargin: 20
            Layout.rightMargin: 20
            Layout.fillWidth: true
            // width:
            // height:35
            value: 0.0
            from: 0
            to: 100
            z: 3

            Behavior on value {
                NumberAnimation {
                    duration: 300
                }
            }

            Text {
                id: progressText
                text: qsTr("%1%   -   %2/%3").arg((pb_pulldata.value / pb_pulldata.to * 100).toFixed(0)).arg(pb_pulldata.value.toFixed(0)).arg(pb_pulldata.to.toFixed(0))
                anchors.centerIn: pb_pulldata
                // font.pointSize: 20
                color: "white"
                font.bold: true
                z: 9
            }
        }

        ProgressBar {
            id: pb_pulldata2
            objectName: "pb_pulldata2"
            Layout.fillWidth: true
            Layout.leftMargin: 20
            Layout.rightMargin: 20
            // width:root_rec.width
            // Layout.preferredHeight:35
            value: 0.0
            from: 0
            to: 100
            z: 3

            Behavior on value {
                NumberAnimation {
                    duration: 300
                }
            }

            Text {
                id: progressText2
                text: qsTr("%1%   -   %2/%3").arg((pb_pulldata2.value / pb_pulldata2.to * 100).toFixed(0)).arg(pb_pulldata2.value.toFixed(0)).arg(pb_pulldata2.to.toFixed(0))
                anchors.centerIn: pb_pulldata2
                // font.pointSize: 20
                color: "white"
                font.bold: true
                z: 9
            }
        }

        RowLayout {
            id: row_btn
            // width:pb_pulldata.width
            Layout.bottomMargin: 15

            Button {
                id: btn_cancel
                text: "Cancel"
                Layout.fillWidth: true
                Layout.leftMargin: 20
                Layout.rightMargin: 10
                // height:25
            }
            Button {
                id: btn_close
                Layout.fillWidth: true
                Layout.leftMargin: 10
                Layout.rightMargin: 20
                enabled: false

                text: "Close"
                // height:25
            }
        }
    }
}
