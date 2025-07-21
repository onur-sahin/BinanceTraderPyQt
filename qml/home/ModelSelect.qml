import QtQuick


ModelSelectForm{



    btn_addModel.onClicked:{
        addModel.visible = true
    }

    btn_delModel.onClicked:{

    }

    btn_pullModels.onClicked:{
        modelListModelMdl.loadFromDatabaseRequested();
    }

    Item{

        AddModel{
            id:addModel
            visible:false
        }

    }
    
}