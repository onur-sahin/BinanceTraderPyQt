import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Fusion

Item{

    // ScrollView {
    //     anchors.fill:parent

    //     id: scroll_log
    //     ScrollBar.vertical.policy:ScrollBar.AlwaysOn
    //     ScrollBar.horizontal.policy: ScrollBar.AlwaysOn
    //     ScrollBar.vertical.width:15
    //     ScrollBar.horizontal.height:15


    //     TextArea {
    //         id:textArea
    //         text:"eaiuaae"

    //         anchors.rightMargin:25
    //         anchors.leftMargin:10
    //         anchors.bottomMargin:50

    //     }


    // }


    ListView{
        id: lv_log
        anchors.fill:parent

        model: logModel
        clip:true

        
        onCountChanged: {
        Qt.callLater(() => {
            onCountChanged: lv_log.positionViewAtEnd()
            // lv_log.contentY = lv_log.contentHeight - lv_log.height;
        });
    }

        delegate:   Item {
                        width:lv_log.width
                        // height:30

                        height:txt.implicitHeight+10

                        

                            TextEdit {
                                id:txt
            
                                width:parent.width
                                anchors.left          : parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                text: logText !== undefined ? logText : "No Log Data"
                                readOnly:true
                                wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
                                selectByMouse: true
                        
                        
                                z:2
                                
                                // Component.onCompleted: console.log(model);
                                
                            }

                            Rectangle{
                                width:lv_log.width
                                height:txt.implicitHeight+10
                                // height:40
                                color: index%2 ? "lightblue" : "#9ce3ca"
                                border.color:"black"
                                z:1
                            }
                    }
    }



    Rectangle {
        width:parent.width
        height:parent.height
        color:"transparent"
        border.width:3
        // border.color:"darkRed"
        border.color: "transparent"
        
    }



}