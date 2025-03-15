import QtQuick
import com.binancetrader.PullDataMdl



PullDataProgressBarForm{
    id:root

    PullDataMdl {
        id        :pullDataMdl
        objectName:"pullDataMdl"
    }

    ColorAnimation {
        id: ca_infoRect
        target:root.rec_progbarBorder
        property:"border.color"
        duration: 1500
        to : "darkRed"
        from:  "red"
        loops: Animation.Infinite
        easing.type:Easing.InOutQuad
        running:false

    }

    
    pb_pulldata.to         : pullDataMdl.p_maxValue
    pb_pulldata.value      : pullDataMdl.p_value
    pb_pulldata2.to        : pullDataMdl.p_maxValue2
    pb_pulldata2.value     : pullDataMdl.p_value2
    tx_infoProgressBar.text: "pair: " + pullDataMdl.p_pair + "  interval: " + pullDataMdl.p_interval + " \n "
                             + pullDataMdl.p_startDt + "   -   " + pullDataMdl.p_endDt;
    

    btn_close.onClicked: { parent.destroy(); }

    btn_cancel.onClicked: { pullDataMdl.set_cancel_flag(); }

    Connections {
        target: pullDataMdl

        function onFinished(){
            btn_close.enabled=true;
            btn_cancel.enabled=false
        }
   }

   Connections {
        target: pullDataMdl

        function onErrorOccurred(){
            ca_infoRect.running=true
            btn_close.enabled=true
            btn_cancel.enabled=false
        }
   }



    Connections {
        target: root.ma_progbarBorder

        function onClicked(){
            ca_infoRect.running=false
            root.rec_progbarBorder.border.color = "red"
        }
   }


}