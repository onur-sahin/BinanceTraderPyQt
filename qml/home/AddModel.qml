import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// import com.binancetrader.ModelMdl 1.0

AddModelForm{

    tf_modelName.text           : addModelMdl.modelName
    tf_defaultPair.text         : addModelMdl.defaultPair
    tf_windowSize.text          : addModelMdl.windowSize
    tf_defaultInterval.text     : addModelMdl.defaultInterval
    cb_modelType.model          : addModelMdl.listOfModelTypes
    cb_modelType.onModelChanged : cb_modelType.model.count>0 ? 0 : -1

    tf_modelName      .onTextChanged:addModelMdl.modelName       = tf_modelName      .text 
    tf_defaultPair    .onTextChanged:addModelMdl.defaultPair     = tf_defaultPair    .text 
    tf_windowSize     .onTextChanged:addModelMdl.windowSize      = tf_windowSize     .text 
    tf_defaultInterval.onTextChanged:addModelMdl.defaultInterval = tf_defaultInterval.text 
   
    cb_modelType      .onCurrentIndexChanged: {
        Qt.callLater(()=> {
            addModelMdl.modelType = cb_modelType.currentText;
            console.log("cb_modelType.currentText: " + cb_modelType.currentText)

        });
    }

    onVisibleChanged:()=>{
        if( this.visible ){
            addModelMdl.update_model_types();
        }
    }

    btn_save.onClicked: () => {

        addModelMdl.printModel();


        
        let result = addModelMdl.save_model();

        messageDialog.title = "Model Save Status";

        if (result == "") {
            messageDialog.messageText = "✅ " + "\'" + addModelMdl.modelName + "\'" + " model is successfully saved.";

        } else {
            messageDialog.messageText = "⛔ " + "\'" + addModelMdl.modelName + "\'" + " model couldn't saved, Failed!";
        }

        messageDialog.open();


    }


    btn_cancel.onClicked: () => {
        this.visible=false
    }

    Component{
        id:gl_component
        GridLayout{
            property alias gridLayout : gridLayout
            id:gridLayout
        }
    }

    Component{
        id:cellComponent

        Rectangle{
            id: cell_rec
            objectName:"cell_rec"
            width: 75 < textElement.width ? textElement.width + 7 : 75
            height: 40
            color:"transparent"
            border.width:2
            border.color:"grey"
            // Layout.preferredWidth:120
            // Layout.preferredHeight:70
            property alias cell_rec : cell_rec
            property alias textElement :textElement

            property real rx : 0.1;
            property real ry : 0.1;
            property string row_name;

            Item{
                id:rowName
                objectName:"rowName"
                property string rowName : cell_rec.row_name
            }

            Text{
                id:textElement
                objectName:"textElement"
                x: cell_rec.rx+5
                y: cell_rec.ry
            }


            Text{
                id: i_txt
                x: cell_rec.rx + 5
                y: cell_rec.ry + textElement.height
                text:"I"
            }
            CheckBox{
                id:cb_i
                objectName:"cb_i"
                x: i_txt.x + i_txt.width-9
                y: i_txt.y-7
            }


            CheckBox{
                id:cb_c
                objectName:"cb_c"
                x:cb_i.x + cb_i.width-15
                y:cb_i.y
            }
            Text{
                id: c_txt
                x: cb_c.x + cb_c.width-9
                y: cell_rec.ry + textElement.height
                text:"C"
            }
                
            
        }
    }


    Component{
        id:c_rowName
        Text{
            property alias txt_rowName : txt_rowName
            id:txt_rowName
        }
    }

    btn_save_network.onClicked: ()=>{
        let a = findChildrenRecursive(cl_network);
        let result = []

        for( let b of a){
            if (b instanceof Rectangle && b.objectName === "cell_rec"){
                let c = findChildrenRecursive(b)
                let r_name;
                let c_name;
                let i_state;
                let c_state;
                for( let d of c){
                    if(d.objectName==="rowName"){
                        r_name = d.rowName
                    }else if(d.objectName=="textElement"){
                        c_name = d.text
                    }else if (d.objectName=="cb_i"){
                        i_state = d.checked
                    }else if ( d.objectName=="cb_c"){
                        c_state = d.checked
                    }else{
                        ;
                    }

                }

                // console.log(r_name + " - " + c_name + " - " + i_state + " - " + c_state)
                result.push([r_name, c_name, i_state, c_state])
            }
        }

        addModelMdl.setNetworksStatus(result);

    }

    btn_cancel_network.onClicked:()=>{
        networkWin.visible = false
    }


    btn_networks.onClicked: () =>{

        if (cl_network.created && cl_network.modelType === addModelMdl.modelType ){
            networkWin.visible = true;
            return;
        }

        if (cl_network.created && cl_network.modelType !== addModelMdl.modelType ){
            for( let c of cl_network.children ){
                c.destroy();
            }
        }

        cl_network.created=true;
        cl_network.modelType=addModelMdl.modelType;
        console.log("created model type: " + addModelMdl.modelType);

        let networkNames = addModelMdl.getNetworkNames();

        let row_n = 0;
        let col_n = 0;

        let cmpnt = gl_component.createObject(cl_network);
        cmpnt.gridLayout.rows    = networkNames.length
        cmpnt.gridLayout.columns = networkNames.length+1

        for(let name_r of networkNames){
            let rowName =  c_rowName.createObject()
            rowName.GridLayout.row        = row_n
            rowName.GridLayout.column     = 0;
            rowName.GridLayout.rowSpan    = 1;
            rowName.GridLayout.columnSpan = 1;
            rowName.txt_rowName.text      = name_r;

            cmpnt.gridLayout.children.push(rowName)

            for(let name_c of networkNames){
                let cell = cellComponent.createObject()
                cell.textElement.text          = name_c;
                cell.cell_rec.GridLayout.row    = row_n;
                cell.cell_rec.GridLayout.column = col_n + 1;
                rowName.GridLayout.rowSpan     = 1;
                rowName.GridLayout.colSpan     = 1;

                cmpnt.gridLayout.children.push(cell);
                cell.cell_rec.rx       = cell.cell_rec.x
                cell.cell_rec.ry       = cell.cell_rec.y
                cell.cell_rec.row_name = name_r;
                
                col_n++;

            }
            col_n = 0;
            row_n++;

        }

        networkWin.visible = true
    }

    function findChildrenRecursive(item) {
        // Bu öğe ve alt öğelerinin çocuklarını bul
        var childrenList = [];
        
        // Çocukları ekle
        for (var i = 0; i < item.children.length; i++) {
            childrenList.push(item.children[i]);  // Çocuğu listeye ekle

            // Çocuğun alt öğelerini recursive olarak ara
            childrenList = childrenList.concat(findChildrenRecursive(item.children[i]));
        }

        return childrenList;
    }

}