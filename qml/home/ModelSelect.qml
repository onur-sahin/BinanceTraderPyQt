import QtQuick


ModelSelectForm{



    btn_addModel.onClicked:{
        addModel.visible = true
    }

    btn_delModel.onClicked:{

    }

    Item{

        AddModel{
            id:addModel
            visible:false
        }

    }
    
}