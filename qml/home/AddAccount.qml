import QtQuick
import com.binancetrader.AccountMdl 1.0
import com.binancetrader.Enums.AccountTypes 1.0

AddAccountForm {
    id:root




    tf_accountName.text         : addAccountMdl.accountName
    tf_accountName.onTextChanged: addAccountMdl.accountName = tf_accountName.text

    tf_apiKey.text              : addAccountMdl.apiKey
    tf_apiKey.onTextChanged     : addAccountMdl.apiKey = tf_apiKey.text

    tf_apiSecret.text           : addAccountMdl.apiSecret
    tf_apiSecret.onTextChanged  : addAccountMdl.apiSecret = tf_apiSecret.text

    tf_testResult.text          : addAccountMdl.testResult
    

    onPr_accountPassChanged     : addAccountMdl.accountPass = pr_accountPass

    cb_rememberAccountPass.onCheckedChanged : addAccountMdl.rememberAccountPass = cb_rememberAccountPass.checked


    bg_accountGroup.onCheckedButtonChanged: {
        if (bg_accountGroup.checkedButton === cb_realAccount) {
            addAccountMdl.realAccount = true;
        } else {
            addAccountMdl.realAccount = false;
        }
    }

    bg_typeGroup.onCheckedButtonChanged: {
        addAccountMdl.accountType = AccountTypes.from_string( bg_typeGroup.checkedButton.text )
    }



    Connections {
        target: root_cl
        function onCompleted(){
            if (addAccountMdl.realAccount) {
                bg_accountGroup.checkedButton = cb_realAccount;
            } else {
                bg_accountGroup.checkedButton = cb_mockAccount;
            }
        }
    }

    Connections {
        target:root_cl
        function onCompleted(){
            root.bg_typeGroup.checkedButton = root.cb_binance
        }
    }


    btn_test_key_and_secret.onClicked: () => {
        addAccountMdl.test_account();
    }

    btn_save.onClicked: () => {
        addAccountMdl.save_account();
    }

    btn_cancel.onClicked: () => {
        root.visible = false;
    }
}
