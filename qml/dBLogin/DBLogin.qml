import QtQuick

DBLoginPage {

    signal changeStateToHome();

    le_database.onTextChanged:{ dBLoginMdl.database = le_database.text }
    le_database { text: dBLoginMdl.database }

    le_user.onTextChanged:{ dBLoginMdl.user = le_user.text }
    le_user { text: dBLoginMdl.user }

    le_host.onTextChanged:{ dBLoginMdl.host = le_host.text }
    le_host { text: dBLoginMdl.host }

    le_port.onTextChanged:{ dBLoginMdl.port = le_port.text }
    le_port { text: dBLoginMdl.port }

    le_password.onTextChanged:{ dBLoginMdl.password = le_password.text }
    le_password { text: dBLoginMdl.password }

    cb_remember_pass.onCheckedChanged:{ dBLoginMdl.rememberPassword = cb_remember_pass.checked }
    cb_remember_pass { checked: dBLoginMdl.rememberPassword }


    btn_test_connection.onClicked:{ dBLoginMdl.test_database_connection() }
    
    btn_login.onClicked:{
        if (dBLoginMdl.test_database_connection()){

            dBLoginMdl.initialize_database()
            changeStateToHome()
            
        }
    }

    ta_connection_test_result { text: dBLoginMdl.connectionTestResult }


}
