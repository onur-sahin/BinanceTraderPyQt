import QtQuick

import "../js/datetimeValidators.js" as DatetimeValidators




ManagementForm{

    signal addPullDataProgressBar()  //this signal is capture by home.qml


    cb_pairs.currentIndex    : managementMdl.pairIndex

    Component.onCompleted : {
        Qt.callLater(()=>{

        managementMdl.pairIndex     = cb_pairs.find("BTCUSDT")
        managementMdl.interval      = "5m"
        managementMdl.epoch         = "1"
        managementMdl.testSpeed     = 1
        managementMdl.maxChartCount = 300

           });
    }
   



    tf_trainStart_date .text : managementMdl.trainStartDate
    tf_trainStart_time .text : managementMdl.trainStartTime
    tf_trainEnd_date   .text : managementMdl.trainEndDate
    tf_trainEnd_time   .text : managementMdl.trainEndTime
    tf_interval        .text : managementMdl.interval
    tf_epoch           .text : managementMdl.epoch
    tf_test_speed      .text : managementMdl.testSpeed
    tf_max_chart_Count .text : managementMdl.maxChartCount
    tf_testStart_date  .text : managementMdl.testStartDate
    tf_testStart_time  .text : managementMdl.testStartTime
    tf_testEnd_date    .text : managementMdl.testEndDate
    tf_testEnd_time    .text : managementMdl.testEndTime

    cb_pairs           .onCurrentIndexChanged: {
        Qt.callLater(()=>{
            // console.log(cb_pairs.currentIndex)
            // console.log(cb_pairs.currentText)
            // console.log(managementMdl.pairIndex)
            // console.log(managementMdl.pair)
           
            managementMdl.pairIndex = cb_pairs.currentIndex
            managementMdl.pair      = cb_pairs.currentText

            // console.log(cb_pairs.currentIndex)
            // console.log(cb_pairs.currentText)
            // console.log(managementMdl.pairIndex)
            // console.log(managementMdl.pair)

        });
    }


    tf_trainStart_date .onTextChanged:{
        if(DatetimeValidators.onDateTextChanged(tf_trainStart_date)){
            console.log(tf_trainStart_date.text)
            managementMdl.trainStartDate   = tf_trainStart_date.text
        }
    }
    tf_trainStart_time .onTextChanged:{
        if(DatetimeValidators.onTimeTextChanged(tf_trainStart_time)){
            console.log(tf_trainStart_time.text)
            managementMdl.trainStartTime = tf_trainStart_time.text
        }
    }
    tf_trainEnd_date   .onTextChanged:{
        if(DatetimeValidators.onDateTextChanged(tf_trainEnd_date  )){
            managementMdl.trainEndDate   = tf_trainEnd_date  .text
        }
    }
    tf_trainEnd_time   .onTextChanged:{
        if(DatetimeValidators.onTimeTextChanged(tf_trainEnd_time  )){
            managementMdl.trainEndTime          = tf_trainEnd_time  .text
        }
    }
    tf_testStart_date  .onTextChanged:{
        if(DatetimeValidators.onDateTextChanged(tf_testStart_date )){
            managementMdl.testStartDate  = tf_testStart_date .text
        }
    }
    tf_testStart_time  .onTextChanged:{
        if(DatetimeValidators.onTimeTextChanged(tf_testStart_time )){
            managementMdl.testStartTime    = tf_testStart_time .text
        }
    }
    tf_testEnd_date    .onTextChanged:{
        if(DatetimeValidators.onDateTextChanged(tf_testEnd_date   )){
            managementMdl.testEndDate  = tf_testEnd_date   .text
        }
    }
    tf_testEnd_time    .onTextChanged:{
        if(DatetimeValidators.onTimeTextChanged(tf_testEnd_time   )){
            managementMdl.testEndTime    = tf_testEnd_time   .text
        }
    }

    tf_interval        .onTextChanged:managementMdl.interval       = tf_interval       .text
    tf_epoch           .onTextChanged:managementMdl.epoch          = tf_epoch          .text
    tf_test_speed      .onTextChanged:managementMdl.testSpeed      = tf_test_speed     .text
    tf_max_chart_Count .onTextChanged:managementMdl.maxChartCount  = tf_max_chart_Count.text

    btn_pull_data.onClicked : {
        // addPullDataProgressBar();  // this signal is capture by home.qml
        infoMdl.emit_addPullDataProgressBar(); // this function emit a signal and it is capture by info.qml
    }

    btn_start_train.onClicked :{
        managementMdl.startTrain();
    }

    
    function get_date(dateString){

        var dateParts = dateString.split("/");

        if (dateParts.length === 3) {
            var day = parseInt(dateParts[0]);
            var month = parseInt(dateParts[1]);
            var year = parseInt(dateParts[2]);

            // Tarih nesnesi oluşturuluyor
            var userDate = new Date(year, month - 1, day); // Month 0-11 arası olduğu için 1 çıkarıyoruz

            // Tarihi istediğiniz formatta yazdırma
            var formattedDate = userDate.getDate() + "/" + (userDate.getMonth() + 1) + "/" + userDate.getFullYear();
            console.log("Formatted Date: " + formattedDate);
                console.log("Invalid date format");
            }

        }

}