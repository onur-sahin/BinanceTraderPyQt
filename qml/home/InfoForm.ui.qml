import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Imagine

Item{

    id:root_infoForm

    property alias columnLayout : columnLayout
    property alias root_infoForm : root_infoForm

    ScrollView {
        anchors.fill:parent
        anchors.rightMargin:10

        id: scroll_info
        ScrollBar.vertical.policy:ScrollBar.AlwaysOn
        ScrollBar.horizontal.policy: ScrollBar.AlwaysOn
        ScrollBar.vertical.width:15
        ScrollBar.horizontal.height:15



        ColumnLayout {
            id:columnLayout
            spacing:30

            Item{
                Layout.preferredHeight:20
                Layout.preferredWidth:20
            }


     

        }

    }


}