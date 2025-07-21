import QtQuick

MyListViewModelForm{

     id:listView


    Connections{
        target:listView
    
        function onClicked_mouseArea_first(index){
            // console.log("First Field Double Clicked: " + index)
            var obj = listView.itemAtIndex(index).children[0].children[0].children[0] 
            obj.readOnly = false
            obj.forceActiveFocus() // Kullanıcı düzenleme yapabilsin
        }

    }


    Connections{
        target:listView

        function onClicked_mouseArea_second(index){
            var obj = listView.itemAtIndex(index).children[0].children[1].children[0] 
            obj.readOnly = false
            obj.forceActiveFocus() // Kullanıcı düzenleme yapabilsin
        }
    }

    Connections{
        target:listView

        function onClicked_mouseArea_third(index){
            var obj = listView.itemAtIndex(index).children[0].children[2].children[0] 
            obj.readOnly = false
            obj.forceActiveFocus() // Kullanıcı düzenleme yapabilsin
        }
    }

}