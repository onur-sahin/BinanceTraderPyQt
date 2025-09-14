import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


InfoForm {
    id:infoForm
  

    Connections {
        target: infoMdl
        function onAddPullDataProgressBar() {

            var loader = Qt.createQmlObject(`
                import QtQuick
                import QtQuick.Layouts

                    Loader {
                        id:loader
                        source: "../PullDataProgressBar.qml"
                        active: true

                        onStatusChanged: {
                            if (status === Loader.Ready && item) {
                                ;
                            }
                        }
                    }
                
            `, columnLayout);

            Qt.callLater(function(){
                var pullDataMdl = findChildRecursive(loader, "item_pullDataMdl").ref_pullDataMdl
                
                pullDataMdl.pair            = managementMdl.pair
                pullDataMdl.interval        = managementMdl.interval
                pullDataMdl.startTs         = managementMdl.ts_ms_trainStart
                pullDataMdl.endTs           = managementMdl.ts_ms_trainEnd

                var selectedAccountIndex    = accountListModelMdl.selectedIndex

                if (selectedAccountIndex == -1){
                    return
                }

                pullDataMdl.account         = accountListModelMdl.getItem(selectedAccountIndex)

                pullDataMdl.pull_data()


            });
            
    
        }
    }



    function rec(item){

        var result = [];

        if(!item){
            return result
        }

        for (var child of item.children) {

            result.push(child)
            var j = rec(child)

            result = result.concat(j)
        }

        return result
    }


    function findChildRecursive(item, objectName) {
        if (!item || !item.children) {
            return null
        }

        for (var i = 0; i < item.children.length; ++i) {
            var child = item.children[i]

            if (child.objectName === objectName) {
                return child
            }

            var result = findChildRecursive(child, objectName)

            if (result !== null) {
                return result
            }
        } 

        return null
    }



    function childrenRecursive(item) {
        var childrenList = [];

        if (!item || !item.children)
            return childrenList;

        for (var i = 0; i < item.children.length; i++) {
            var child = item.children[i];
            if (!child)
                continue;

            childrenList.push(child);
            childrenList = childrenList.concat(childrenRecursive(child));
        }

        return childrenList;
    }

}


// InfoForm{

//     function addPullDataProgressBar(){ // this function is triggred from inside Management.qml



//         var loader = Qt.createQmlObject(
//             'import QtQuick; Loader { source: "../PullDataProgressBar.qml" }',
//             columnLayout
//         );

//         loader.active = true

//         Qt.createQmlObject(`
//             import QtQuick;
//             Connections {
//                 target: loader
//                 onStatusChanged: {
                    
//                     if (loader.status === Loader.Ready && loader.item) {
//                         // Set Layout attached properties only if loader.item is an Item
//                         loader.item.Layout.leftMargin = 25;
//                         // loader.item.Layout.preferredWidth = root_infoForm.width * 0.8
//                         // loader.item.Layout.preferredHeight= 400
//                         // loader.item.Layout.minimumWidth   = 200
//                         // loader.item.Layout.minimumHeight  = 300
//                         // loader.item.Layout.bottomMargin   = 35
//                     }
//                 }
//             }
//         `, loader);





//             // if( columnLayout.children[columnLayout.children.length > 0 )
//         // loader.anchors.top = columnLayout.children[columnLayout.children.length-1].bottom;

//         return loader;
//     }




// }