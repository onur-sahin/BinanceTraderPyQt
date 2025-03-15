import QtQuick
import com.binancetrader.AccountMdl 1.0

AddAccountForm {
    id:root




    tf_accountName.text         : addAccountMdl.p_accountName
    tf_accountName.onTextChanged: addAccountMdl.p_accountName = tf_accountName.text

    tf_apiKey.text         : addAccountMdl.p_apiKey
    tf_apiKey.onTextChanged: addAccountMdl.p_apiKey = tf_apiKey.text

    tf_apiSecret.text         : addAccountMdl.p_apiSecret
    tf_apiSecret.onTextChanged: addAccountMdl.p_apiSecret = tf_apiSecret.text

    tf_testResult.text: addAccountMdl.p_testResult
    

    onPr_accountPassChanged: addAccountMdl.p_accountPass = pr_accountPass

    cb_rememberAccountPass.onCheckedChanged : addAccountMdl.p_rememberAccountPass = cb_rememberAccountPass.checked


    bg_accountGroup.onCheckedButtonChanged: {
        if (bg_accountGroup.checkedButton === cb_realAccount) {
            addAccountMdl.p_realAccount = true;
        } else {
            addAccountMdl.p_realAccount = false;
        }
    }

    Connections {
        target: root_cl
        function onCompleted(){
            if (addAccountMdl.p_realAccount) {
                bg_accountGroup.checkedButton = cb_realAccount;
            } else {
                bg_accountGroup.checkedButton = cb_mockAccount;
            }
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
