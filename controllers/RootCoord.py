from PyQt6.QtCore import QObject
from PyQt6.QtQml  import QQmlApplicationEngine, qmlRegisterType, qmlRegisterSingletonType
from item_model   import ItemModel
from AccountMdl   import AccountMdl
from LogManager   import LogManager
from DBLoginMdl   import DBLoginMdl
from ModelMdl     import ModelMdl

from AccountTypes import AccountTypes
from LogListMdl          import LogListModelMdl
from AccountListModelMdl import AccountListModelMdl
from ModelListModelMdl   import ModelListModelMdl


class RootCoord(QObject):
    def __init__(self, engine: QQmlApplicationEngine):
        super().__init__(parent=engine)
        self.engine              = engine
        self.model               = ItemModel(["Item 1", "Item 2", "Item 3"])

        self.dBLoginMdl          = DBLoginMdl(self)
        self.addModelMdl         = ModelMdl(self)
        self.addAccountMdl       = AccountMdl(self)

        self.accountListModelMdl = AccountListModelMdl(self)
        self.modelListModelMdl   = ModelListModelMdl(self)


    def load_qml(self):
        context = self.engine.rootContext()
        # context.setContextProperty("itemModel", self.model)

        # Log& log = Log::instance();
        # LogListModelMdl     *logModel           = new LogListModelMdl();
        # log.m_logModel = logModel;
        # engine->rootContext()->setContextProperty("logModel",    logModel);

        log = LogManager.instance()
        logModel = LogListModelMdl()
        log.set_log_model(logModel)
        context.setContextProperty("logModel", logModel)

        qmlRegisterSingletonType(AccountTypes, "com.binancetrader.Enums.AccountTypes", 1, 0, lambda engine, script:AccountTypes(), name="AccountTypes")


        qmlRegisterType( AccountMdl, "com.binancetrader.AccountMdl" , 1, 0, "AccountMdl" )
        qmlRegisterType( ModelMdl,   "com.binancetrader.ModelMdl"   , 1, 0, "ModelMdl"   )
        # qmlRegisterType<PullDataMdl>("com.binancetrader.PullDataMdl", 1, 0, "PullDataMdl");

        context.setContextProperty("dBLoginMdl"         , self.dBLoginMdl         )
        context.setContextProperty("addModelMdl"        , self.addModelMdl        )
        context.setContextProperty("addAccountMdl"      , self.addAccountMdl      )
        context.setContextProperty("modelListModelMdl"  , self.modelListModelMdl  )
        context.setContextProperty("accountListModelMdl", self.accountListModelMdl)



        self.engine.addImportPath("qml")
        self.engine.load('qml/main.qml')

















# if __name__ == "__main__":
#     app = QCoreApplication([])
#     engine = QQmlApplicationEngine()
    
#     controller = MainController(engine)
#     controller.load_qml()
    
#     app.exec()
