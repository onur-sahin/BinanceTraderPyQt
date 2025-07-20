import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs
import QtQuick.Layouts

import com.binancetrader.AccountMdl

AccountSelectForm{

    Item{
        AddAccount{
            id:addAccount
            visible: false
        }
    }


    btn_addAccount.onClicked:{

        addAccount.visible = true

    }


    btn_pullAccounts.onClicked:{
        accountListModelMdl.loadFromDatabaseRequested();  //this is a signal capture inside AddAccountMdl::AddAccountMdl
    }

    btn_delAccount.onClicked:{
        var currentIndex = myListViewAccount.currentIndex;
        if(currentIndex === -1){
            return
            
        }

        // var selected = myListViewAccount.model.currentItem
        // var obj = selected;
        // var proto = obj;
        // var methods = [];

        // while (proto) {
        //     methods = methods.concat(Object.getOwnPropertyNames(proto).filter(function(property) {
        //         return typeof obj[property] === "function";
        //     }));
        //     proto = Object.getPrototypeOf(proto);
        // }
        // console.log("Methods of object:", methods);

        md_accountDelete.accountName = myListViewAccount.model.getItem(currentIndex).accountName
        md_accountDelete.index       = currentIndex
        md_accountDelete.open();
    }


    // Connections {
    //     target: addAccountMdl
    //     function onNewAccountCreated(account) {
    //         accountListModelMdl.addItem(account)

    //     }
    // }

    Dialog{

        id:md_accountDelete
        width:400
        height:200
        title:"☢️⚠️Account Delete Warning!⚠️☢️"
        
        property string accountName : "accountName";
        property int index       : -1;

        background: Rectangle{
                        anchors.fill:parent
                        anchors.centerIn:parent
                        border.width:2
                        border.color:"red"
                        color:"#6c0000"
                    }

        contentItem:

            Text {
                anchors.centerIn : parent
                anchors.leftMargin:30
                anchors.rightMargin:30
                color:"white"
                font.bold:true
                text: qsTr("Account:<b><font color='red'> %1 </font></b> will be deleted on program and in your database! <br><br>ARE YOU SURE?").arg(md_accountDelete.accountName);
                wrapMode: Text.WordWrap
            }
        

        footer : DialogButtonBox {
    
            Button{
                id:btn_yes
                text:"Yes"
                DialogButtonBox.buttonRole:DialogButtonBox.AcceptRole
            }

            Button{
                id:btn_cancel
                text:"Cancel"
                DialogButtonBox.buttonRole: DialogButtonBox.RejectRole
            }
            
        }

        onAccepted:{
            // index = myListViewAccou

            var obj = myListViewAccount.model.getItem(index)
            var result = obj.deleteAccount()

            if (result){
                var result2 = myListViewAccount.model.removeRow(index)
            }

        }


    }

    

}