import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


InfoForm{



    function addPullDataProgressBar(){ // this function is triggred from inside Management.qml

        var loader = Qt.createQmlObject(
            'import QtQuick; Loader {source:"../PullDataProgressBar.qml"}',
            columnLayout
            );



            // loader.Layout.preferredWidth = root_infoForm.width * 0.8
            // loader.Layout.preferredHeight= 400
            // loader.Layout.minimumWidth   = 200
            // loader.Layout.minimumHeight  = 300
            loader.Layout.leftMargin     = 25
            // loader.Layout.bottomMargin   = 35
            

            // if( columnLayout.children[columnLayout.children.length > 0 )
        // loader.anchors.top = columnLayout.children[columnLayout.children.length-1].bottom;

        return loader;
    }




}