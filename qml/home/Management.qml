import QtQuick

import "../js/datetimeValidators.js" as DatetimeValidators




ManagementForm{

    signal addPullDataProgressBar()  //this signal is capture by home.qml

    // cb_pairs.currentIndex: cb_pairs.find(mainVM.pair)


    // tf_trainStart_date .text : mainVM.trainStartDate
    // tf_trainStart_time .text : mainVM.trainStartTime
    // tf_trainEnd_date   .text : mainVM.trainEndDate
    // tf_trainEnd_time   .text : mainVM.trainEndTime
    // tf_interval        .text : mainVM.interval
    // tf_epoch           .text : mainVM.epoch
    // tf_test_speed      .text : mainVM.testSpeed
    // tf_max_chart_Count .text : mainVM.maxChartCount
    // tf_testStart_date  .text : mainVM.testStartDate
    // tf_testStart_time  .text : mainVM.testStartTime
    // tf_testEnd_date    .text : mainVM.testEndDate
    // tf_testEnd_time    .text : mainVM.testEndTime

    cb_pairs           .onCurrentIndexChanged: {
        Qt.callLater(()=>{
            mainVM.pair = cb_pairs.currentText
        });

    }
       

    tf_trainStart_date .onTextChanged:{
        if(DatetimeValidators.onDateTextChanged(tf_trainStart_date)){
            mainVM.trainStartDate   = tf_trainStart_date.text
        }
    }
    tf_trainStart_time .onTextChanged:{
        if(DatetimeValidators.onTimeTextChanged(tf_trainStart_time)){
            mainVM.trainStartTime = tf_trainStart_time.text
        }
    }
    tf_trainEnd_date   .onTextChanged:{
        if(DatetimeValidators.onDateTextChanged(tf_trainEnd_date  )){
            mainVM.trainEndDate   = tf_trainEnd_date  .text
        }
    }
    tf_trainEnd_time   .onTextChanged:{
        if(DatetimeValidators.onTimeTextChanged(tf_trainEnd_time  )){
            mainVM.trainEndTime          = tf_trainEnd_time  .text
        }
    }
    tf_testStart_date  .onTextChanged:{
        if(DatetimeValidators.onDateTextChanged(tf_testStart_date )){
            mainVM.testStartDate  = tf_testStart_date .text
        }
    }
    tf_testStart_time  .onTextChanged:{
        if(DatetimeValidators.onTimeTextChanged(tf_testStart_time )){
            mainVM.testStartTime    = tf_testStart_time .text
        }
    }
    tf_testEnd_date    .onTextChanged:{
        if(DatetimeValidators.onDateTextChanged(tf_testEnd_date   )){
            mainVM.testEndDate  = tf_testEnd_date   .text
        }
    }
    tf_testEnd_time    .onTextChanged:{
        if(DatetimeValidators.onTimeTextChanged(tf_testEnd_time   )){
            mainVM.testEndTime    = tf_testEnd_time   .text
        }
    }

    tf_interval        .onTextChanged:mainVM.interval       = tf_interval       .text
    tf_epoch           .onTextChanged:mainVM.epoch          = tf_epoch          .text
    tf_test_speed      .onTextChanged:mainVM.testSpeed      = tf_test_speed     .text
    tf_max_chart_Count .onTextChanged:mainVM.maxChartCount  = tf_max_chart_Count.text

    btn_pull_data.onClicked : {
        addPullDataProgressBar();  // this signal is capture by home.qml
    }

    btn_start_train.onClicked :{
        mainVM.startTrain();
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