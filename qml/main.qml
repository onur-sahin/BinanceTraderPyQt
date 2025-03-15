import QtQuick
import QtQuick.Controls
import dBLogin
import home


ApplicationWindow {
    id     : applicationWindow
    property double p: 1.5
    width  : Screen.width * 0.8 * p
    height : Screen.height * 0.8 * p
    visible: true
    title  : qsTr("Hello World")
    // style:"Fusion"

    // Material.theme: Material.Dark
    // Material.density:0.5


    Item{

        id: root
        anchors.fill:parent
        state: "dBLoginState"
        // state: "homeState"


        DBLogin{
            id: dBLoginPage
            anchors.fill:parent
        }

        Item{
            id: appPage
            anchors.fill: parent

            TabBar {

                id: tabBar_main
                anchors.top: parent.top
                width: parent.width
                // spacing:10
                height: 50
                currentIndex: swipeview_main.currentIndex

                TabButton {
                    anchors.top: parent.top
                    height: 50
                    text: "Home"
            
                }

                TabButton {
                    anchors.top: parent.top
                    height: 50
                    text: "Trains"
                }

                TabButton {
                    anchors.top: parent.top
                    height: 50
                    text: "Trades"
                }
            }

            SwipeView {
                id: swipeview_main
                anchors.top   : tabBar_main.bottom
                anchors.bottom: parent.bottom
                width         : parent.width
                height        : parent.height
                currentIndex  : tabBar_main.currentIndex
            

                Home {

                }

                Train {
                    msg: "Trains Page"
                }

                Trade {
                    msg: "Trades Page"
                }
            }
        }

        Connections{
            target: dBLoginPage
            function onChangeStateToHome(){
                root.state = "homeState"
            }
        }
        


        states: [
            State {
                name: "dBLoginState"

                PropertyChanges { dBLoginPage.visible: true}
                PropertyChanges { appPage   .visible: false}


                onCompleted: {applicationWindow.width= Math.round(Screen.width * 0.5* applicationWindow.p);
                              applicationWindow.height= Math.round(Screen.height *0.9 *applicationWindow.p);
                }

            },
            State {
                name: "homeState"
                
                PropertyChanges { appPage   .visible: true}
                PropertyChanges { dBLoginPage.visible: false}

                onCompleted: {applicationWindow.width= Math.round(Screen.width * 0.8*applicationWindow.p);
                              applicationWindow.height= Math.round(Screen.height * 0.8*applicationWindow.p);
                }
            }


        ]
    }


}

// ApplicationWindow {
//     visible: true
//     width: 640
//     height: 480
//     title: "Model-View Example"

//     Material.theme:Material.Dark


//     ListView {
//         anchors.fill: parent
//         model: itemModel
//         delegate: Item {
//             width: parent.width
//             height: 50
//             Text {
//                 anchors.centerIn: parent
//                 text: modelData
//             }
//         }
//     }
// }
