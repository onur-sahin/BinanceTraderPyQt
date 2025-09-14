import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Fusion

Page {
    id: homePage
    
    property alias info       : info
    // property alias modelSelect: modelSelect
    property alias management : management
    // property alias log        : log

    Rectangle {
            anchors.fill:scroll_homePage
            anchors.margins:-5
            color: "transparent"
            border.width: 3
            border.color: "gold"
    }

    ScrollView {
        id: scroll_homePage
        anchors.fill:parent
        anchors.margins:10
 
        // contentWidth: gl_homePage.implicitContentWidth
        // contentHeight: gl_homePage.implicitContentHeight

        spacing: 5
        
        // ScrollBar'ları her zaman göster
        ScrollBar.vertical.policy: ScrollBar.AlwaysOn
        ScrollBar.horizontal.policy: ScrollBar.AlwaysOn

 


        GridLayout {
            id: gl_homePage
            columns: 3
            rows: 10

            rowSpacing: 10
            columnSpacing: 10
            anchors.centerIn: parent
            anchors.fill: parent

            // anchors.margins:10
            // anchors.bottomMargin: 50

            Layout.minimumHeight:400
            Layout.minimumWidth:600
            // Layout.fillWidth:true
            // Layout.fillHeight:true


            Info {
                id:info
                // Layout.minimumWidth: homePage.width*0.33
                // Layout.minimumHeight: homePage.height*0.8
                Layout.preferredWidth: scroll_homePage.width*0.3
                Layout.preferredHeight: scroll_homePage.height*0.7
                Layout.minimumHeight:300
                Layout.minimumWidth:200
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.row:0
                Layout.column:0
                Layout.columnSpan: 1
                Layout.rowSpan: 8
                Layout.margins: 20
                // Layout.alignment :Qt.AlignTop

            }

            AccountSelect {
                id:accountSelect
                // Layout.minimumWidth: homePage.width*0.33
                // Layout.minimumHeight: homePage.height*0.8
                Layout.preferredWidth: scroll_homePage.width*0.3
                Layout.preferredHeight: scroll_homePage.height*0.2
                Layout.minimumHeight:100
                Layout.minimumWidth:300
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.row:0
                Layout.column:1
                Layout.columnSpan: 1
                Layout.rowSpan: 3
                Layout.margins: 20
                Layout.alignment :Qt.AlignTop

            }

            ModelSelect {
                id:modelSelect
                // Layout.minimumWidth: homePage.width*0.33
                // Layout.minimumHeight: homePage.height*0.8
                Layout.preferredWidth: scroll_homePage.width*0.3
                Layout.preferredHeight: scroll_homePage.height*0.4
                Layout.minimumHeight:100
                Layout.minimumWidth:300
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.row:3
                Layout.column:1
                Layout.columnSpan: 1
                Layout.rowSpan: 5
                Layout.margins: 20
                Layout.alignment :Qt.AlignTop

            }

            Management {
                id:management
                // Layout.minimumWidth: homePage.width*0.33
                // Layout.minimumHeight: homePage.height*0.8
                Layout.preferredWidth: scroll_homePage.width*0.3
                Layout.preferredHeight: scroll_homePage.height*0.7
                Layout.minimumHeight:400
                Layout.minimumWidth:200
                // Layout.maximumWidth: homePage.width*0.33
                // Layout.maximumHeight: homePage.height*0.8
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.row:0
                Layout.column:2
                Layout.columnSpan: 1
                Layout.rowSpan: 8
                // Layout.margins:10
                Layout.alignment :Qt.AlignCenter

            }


            Log {
                id:log
                // Layout.minimumWidth: scroll_homePage.width*0.99
                // Layout.minimumHeight: scroll_homePage.height*0.2
                Layout.preferredWidth: scroll_homePage.width*0.9
                Layout.preferredHeight: scroll_homePage.height*0.2
                Layout.minimumHeight:150
                Layout.minimumWidth:900
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.row:8
                Layout.column:0
                Layout.columnSpan: 3
                Layout.rowSpan: 2
                Layout.margins: 10
                Layout.bottomMargin:25
                Layout.alignment :Qt.AlignTop



            }


        }
    }
}
