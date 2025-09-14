
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Fusion



Item{
    id:root

    property alias cb_pairs           : cb_pairs
    property alias tf_trainStart_date : tf_trainStart_date
    property alias tf_trainStart_time : tf_trainStart_time
    property alias tf_trainEnd_date   : tf_trainEnd_date
    property alias tf_trainEnd_time   : tf_trainEnd_time
    property alias tf_interval        : tf_interval
    property alias tf_epoch           : tf_epoch
    property alias btn_start_train    : btn_start_train
    property alias btn_pull_data      : btn_pull_data
    property alias tf_test_speed      : tf_test_speed
    property alias tf_max_chart_Count : tf_max_chart_Count
    property alias tf_testStart_date  : tf_testStart_date
    property alias tf_testStart_time  : tf_testStart_time
    property alias tf_testEnd_date    : tf_testEnd_date
    property alias tf_testEnd_time    : tf_testEnd_time
    property alias btn_start_test     : btn_start_test
    property alias btn_start_trade    : btn_start_trade
    

    ScrollView {
        id:scroll_management
        // anchors.fill:parent
        anchors.centerIn:parent
        width:parent.width-10
        height:parent.height-10
        
        // anchors.rightMargin:20
        ScrollBar.vertical.policy:ScrollBar.AlwaysOn
        ScrollBar.horizontal.policy: ScrollBar.AlwaysOn
        ScrollBar.vertical.width:15
        ScrollBar.horizontal.height:15
        
        GridLayout {
            id:gl_management
            
            // Layout.preferredHeight: scroll_management.height * 0.8
            width:root.width*0.8
            height:root.height*0.9

            rowSpacing:10

            columns:20
            rows:20

            // Item{
            //     Layout.row:0
            //     Layout.column:20
            //     Layout.rowSpan:13
            //     Layout.columnSpan:21
            //     Layout.minimumWidth: 40
            //     Layout.minimumHeight:25
            // }
    


            Column {
                Layout.fillWidth:true
                Layout.leftMargin:15
                
                TextField {
                    id: searchField
                    Layout.rowSpan:1
                    Layout.columnSpan:20
                    Layout.fillWidth:true
    
                    placeholderText: "Ara..."
                    onTextChanged: cb_pairs.updateFilter(text)  // Filtreleme tetikleniyor

                }

                ComboBox {
                    id: cb_pairs
                    Layout.rowSpan:1
                    Layout.columnSpan:20
                    Layout.fillWidth:true
                    // currentIndex:0
                    model: filteredModel

                    function updateFilter(searchText) {
                        filteredModel.clear();
                        for (var i = 0; i < originalModel.count; i++) {
                            var item = originalModel.get(i);
                            if (item.text.toLowerCase().includes(searchText.toLowerCase())) {
                                filteredModel.append(item);
                            }
                        }
                    }
                }

                ListView {
                    id:lv_pairs
                    model:pairListMdl

                    delegate: Text {
                        text: model.text
                    }
                }

                ListModel {
                    id: originalModel
                    ListElement { text: "BTCUSDT"  }
                    ListElement { text: "LTCUSDT"    }
                    ListElement { text: "DOGEUSDT"      }
                }

                ListModel {
                    id: filteredModel
                }

                Component.onCompleted: cb_pairs.updateFilter("")
            }


            MySeperator{Layout.rowSpan:1; Layout.preferredHeight:15; Layout.columnSpan:20; Layout.fillWidth:true;}

            Label{
                id:lb_train_start
                text:"train start:"
                Layout.columnSpan:8
                Layout.rowSpan:1
                Layout.fillWidth: true
                Layout.leftMargin:15
            }

            TextField {
                id:tf_trainStart_date
                Layout.columnSpan:8
                Layout.rowSpan:1
                text:"01/01/2022"
                inputMask:"99/99/9999"
                validator: null
                Layout.fillWidth: true
                property color defaultColor : lb_train_start.color
                Component.onCompleted : defaultColor = defaultColor
                
            }
            TextField {
                id:tf_trainStart_time
                Layout.columnSpan:4
                Layout.rowSpan:1
                text:"12:00"
                inputMask:"99:99"
                validator: null
                Layout.fillWidth: true
                property color defaultColor :lb_train_start.color
                Component.onCompleted: defaultColor = defaultColor
                
            }

            Label{
                id: lb_train_end
                text:"train end:"
                Layout.columnSpan:8
                Layout.rowSpan:1
                Layout.fillWidth: true
                Layout.leftMargin:15
                
                
            }
            TextField {
                id:tf_trainEnd_date
                Layout.columnSpan:8
                Layout.rowSpan:1
                text:"01/01/2022"
                inputMask:"99/99/9999"
                validator: null
                Layout.fillWidth: true
                property color defaultColor : lb_train_end.color
                Component.onCompleted : defaultColor = defaultColor
                
            }
            TextField { 
                id:tf_trainEnd_time
                Layout.columnSpan:4
                Layout.rowSpan:1
                text:"15:00"
                inputMask:"99:99"
                validator: null
                Layout.fillWidth: true
                property color defaultColor :lb_train_end.color
                Component.onCompleted: defaultColor = defaultColor
                
            }

            Label{
                text:"interval:"
                Layout.rowSpan:1
                Layout.columnSpan:5
                Layout.fillWidth: true
                Layout.leftMargin:15
                
                
            }

            TextField  {
                id:tf_interval
                text:"5m"
                Layout.rowSpan:1
                Layout.columnSpan:5
                Layout.fillWidth: true
                
            }

            Label{
                text:"epoch:"
                Layout.rowSpan:1
                Layout.columnSpan:5
                Layout.fillWidth: true
                
            }

            TextField  {
                id:tf_epoch
                text:"2"
                inputMask:"9"
                Layout.rowSpan:1
                Layout.columnSpan:5
                Layout.fillWidth: true
                
                validator: IntValidator { bottom: 1 }
            }

            Button {
                id: btn_start_train
                text:"Start Train (pull data)"
                Layout.rowSpan:1
                Layout.columnSpan:10
                Layout.fillWidth: true
                Layout.leftMargin:15
                
                
            }
            Button {
                id: btn_pull_data
                text:"Pull data"
                Layout.rowSpan:1
                Layout.columnSpan:10
                Layout.fillWidth: true

                
            }

            MySeperator{Layout.rowSpan:1; Layout.preferredHeight:15; Layout.columnSpan:20; Layout.fillWidth:true;}

            Label{
                text:"test speed (candle/sn):"
                Layout.rowSpan:1
                Layout.columnSpan:10
                Layout.fillWidth: true
                Layout.leftMargin:15
                
                
            }
            TextField{
                id:tf_test_speed
                text:"1"
                Layout.rowSpan:1
                Layout.columnSpan:10
                Layout.fillWidth: true
                
            }
            Label{
                text:"Max Chart Count:"
                Layout.rowSpan:1
                Layout.columnSpan:10
                Layout.fillWidth: true
                Layout.leftMargin:15
                
                
            }
            TextField{
                id:tf_max_chart_Count
                text:"300"
                inputMask:"9[999]"
                Layout.rowSpan:1
                Layout.columnSpan:10
                Layout.fillWidth: true
                
            }
            
            Label{
                id: lb_test_start
                text:"test start:"
                Layout.columnSpan:8
                Layout.rowSpan:1
                Layout.fillWidth: true
                Layout.leftMargin:15
                
                
            }
            TextField {
                id:tf_testStart_date
                Layout.columnSpan:8
                Layout.rowSpan:1
                text:"01/01/2022"
                inputMask:"99/99/9999"
                validator: null
                Layout.fillWidth: true
                property color defaultColor : lb_test_start.color
                Component.onCompleted : defaultColor = defaultColor
                
            }
            TextField { 
                id:tf_testStart_time
                Layout.columnSpan:4
                Layout.rowSpan:1
                text:"12:00"
                inputMask:"99:99"
                validator: null
                Layout.fillWidth: true
                property color defaultColor :lb_test_start.color
                Component.onCompleted: defaultColor = defaultColor
                
            }

            Label{
                id: lb_test_end
                text:"test end:"
                Layout.columnSpan:8
                Layout.rowSpan:1
                Layout.fillWidth: true
                Layout.leftMargin:15
                
                
            }
            TextField {
                id:tf_testEnd_date
                Layout.columnSpan:8
                Layout.rowSpan:1
                text:"01/01/2022"
                inputMask:"99/99/9999"
                validator: null
                Layout.fillWidth: true
                property color defaultColor : lb_test_end.color
                Component.onCompleted : defaultColor = defaultColor
                
            }
            TextField { 
                id:tf_testEnd_time
                Layout.columnSpan:4
                Layout.rowSpan:1
                text:"15:00"
                inputMask:"99:99"
                validator: null
                Layout.fillWidth: true
                property color defaultColor :lb_test_end.color
                Component.onCompleted: defaultColor = defaultColor
                
            }

            Button{
                id:btn_start_test
                text:"Start Test"
                Layout.rowSpan:1
                Layout.columnSpan:20
                Layout.fillWidth: true
                Layout.leftMargin:15
                
                
            }


            MySeperator{Layout.rowSpan:1; Layout.preferredHeight:15; Layout.columnSpan:20; Layout.fillWidth:true;}

            Button{
                id:btn_start_trade
                text:"Start Trade"
                Layout.rowSpan:1
                Layout.columnSpan:20
                Layout.fillWidth:true
                Layout.leftMargin:15
                
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