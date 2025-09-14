from PyQt6.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot, QThread, QMutex
from PyQt6.QtCore import Qt, qCritical, QVariant
import importlib.util
import os, io
from psycopg2 import Binary
import torch
from returns.result import Failure
import subprocess

from DBManager import DBManager
from Queries import Queries, Q



class ModelMdl(QObject):

    modelNameChanged            = pyqtSignal()
    defaultPairChanged          = pyqtSignal()
    windowSizeChanged           = pyqtSignal()
    defaultIntervalChanged      = pyqtSignal()
    modelTypeChanged            = pyqtSignal()
    notesChanged                = pyqtSignal()
    listOfModelTypesChanged     = pyqtSignal()
    dictOfNeurolNetworksChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._modelName        = ""
        self._defaultPair      = ""
        self._windowSize       = 0
        self._defaultInterval  = ""
        self._modelType        = ""
        self._notes            = ""
        self._listOfModelTypes = []

        self._listOfModels     = []
        self._listOfModels.append(self)

        self._dictOfNeurolNetworks = {}

        self._process          = None
        self._thrd             = None

        self._networksStatus   = None


        self.modelName        = "default"
        self.defaultPair      = "BTCUSDT"
        self.windowSize       = 11
        self.defaultInterval  = "5m"
        self.notes            = ""

    # Properties with getter and setter methods

    @pyqtProperty(str, notify=modelNameChanged)
    def modelName(self):
        return self._modelName

    @modelName.setter
    def modelName(self, new_model_name):
        if self._modelName != new_model_name:
            self._modelName = new_model_name
            self.modelNameChanged.emit()

    @pyqtProperty(str, notify=defaultPairChanged)
    def defaultPair(self):
        return self._defaultPair

    @defaultPair.setter
    def defaultPair(self, new_default_pair):
        if self._defaultPair != new_default_pair:
            self._defaultPair = new_default_pair
            self.defaultPairChanged.emit()

    @pyqtProperty(int, notify=windowSizeChanged)
    def windowSize(self):
        return self._windowSize

    @windowSize.setter
    def windowSize(self, new_window_size):
        if self._windowSize != new_window_size:
            self._windowSize = new_window_size
            self.windowSizeChanged.emit()

    @pyqtProperty(str, notify=defaultIntervalChanged)
    def defaultInterval(self):
        return self._defaultInterval

    @defaultInterval.setter
    def defaultInterval(self, new_default_interval):
        if self._defaultInterval != new_default_interval:
            self._defaultInterval = new_default_interval
            self.defaultIntervalChanged.emit()

    @pyqtProperty(str, notify=modelTypeChanged)
    def modelType(self):
        return self._modelType

    @modelType.setter
    def modelType(self, new_model_type):
        if self._modelType != new_model_type:
            self._modelType = new_model_type
            self.modelTypeChanged.emit()

    @pyqtProperty(str, notify=notesChanged)
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, new_notes):
        if self._notes != new_notes:
            self._notes = new_notes
            self.notesChanged.emit()

    @pyqtProperty(list, notify=listOfModelTypesChanged)
    def listOfModelTypes(self):
        return self._listOfModelTypes

    @listOfModelTypes.setter
    def listOfModelTypes(self, list_of_model_types):
        self._listOfModelTypes = list_of_model_types
        self.listOfModelTypesChanged.emit()


    @pyqtProperty(QVariant, notify=dictOfNeurolNetworksChanged)
    def dictOfNeurolNetworks(self):
        return self._dictOfNeurolNetworks

    # Methods

    @pyqtSlot(str)
    def update_model_notes(self, notes:str):

        db = DBManager.get_instance()

        query = Queries.get(Q.UPDATE_MODEL_NOTES)

        result = db.execute(query, {"notes":notes, "model_name":self.modelName})

        if isinstance(result, Failure):
            qCritical(f"Failere in update_model_notes(): {str( result.failure() )}")


    def networkNames_from_networksStatus(self)->list:
        networkNames = []
        for l in self.networksStatus:
            if l[0] not in networkNames:
                networkNames.append( l[0] )

        return networkNames
    
    def get_inputSize(self, networkName:str)->int:
        
        inputSize = 0

        for l in self.networksStatus:
            if l[0] == networkName:
                if l[2] == True:
                    inputSize += 1

        return inputSize


    @pyqtSlot(result=str)
    def save_model(self)->str:
        
        networkNames = self.networkNames_from_networksStatus()
        base_path = "neurolNetworks/" + self.modelType

        db         = DBManager.get_instance()
        conn       = db.get_connection()


        for networkName in networkNames:
            module_path = os.path.join(base_path, f"{networkName}.py")
            module_name = f"{self.modelType}.{networkName}"


            try:
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                if spec is None:
                   raise ImportError(f"Cannot load spec for module: {module_name}")

                module = importlib.util.module_from_spec(spec)

                spec.loader.exec_module(module)

                cls = getattr(module, networkName)

                inputSize = self.get_inputSize(networkName)
                
                if inputSize == 0:
                    continue

                modelInstance   = cls(
                    input_size  = inputSize, # how many feature will be use price_p, volum_p... etc.
                    hidden_size = 32, # must be greater than input size (32-128)
                    num_layers  = 2,
                    seq_length  = self.windowSize,
                    model_name  = self.modelName
                )

            except FileNotFoundError as e:
                msg = f"Error: File not found: {module_path} : {str(e)}"
                qCritical(msg)
                return msg
            except SyntaxError as e:
                msg = f"Syntax error in {module_path}: {str(e)}"
                qCritical(msg)
                return msg
            except ImportError as e:
                msg = f"Import error: {str(e)}"
                qCritical(msg)
                return msg
            except AttributeError as e:
                msg = f"Attribute error: {str(e)}"
                qCritical(msg)
                return msg
            except TypeError as e:
                msg = f"Constructor error: {str(e)}"
                qCritical(msg)
                return msg
            except Exception as e:
                msg = f"Unexpected error: {str(e)}"
                qCritical(msg)
                return msg

            self.dictOfNeurolNetworks[networkName] = modelInstance
            self.dictOfNeurolNetworksChanged.emit()



        
        bindValues = {}
        bindValues["model_name"      ] = self.modelName
        bindValues["model_type"      ] = self.modelType
        bindValues["default_pair"    ] = self.defaultPair
        bindValues["default_interval"] = self.defaultInterval
        bindValues["window_size"     ] = self.windowSize
        bindValues["notes"           ] = self.notes

        result = db.execute(Queries.get(Q.INSERT_MODEL), bindValues, conn=conn, commit=False)

        if isinstance(result, Failure):
            qCritical(str(result.failure()))
            return str(result.failure())

        for networkName, model in self.dictOfNeurolNetworks.items():
            buffer     = io.BytesIO()
            torch.save(model.state_dict(), buffer)

            bindValues["network_name"] = networkName
            bindValues["bytea_object"] = Binary(buffer.getvalue())

            result = db.execute(Queries.get(Q.INSERT_NEUROL_MODEL), bindValues, conn=conn, commit=False)

            if isinstance(result, Failure):
                qCritical(db.format_error(result.failure()))
                db.conn.rollback()
                return db.format_error(result.failure())

        result = db.commit_connection(conn)

        if result != "":
            qCritical(result)
            db.cleanup()
            return result

        return ""

    def processModelsParallel(self):
        map(self.update_model_types, self._listOfModels)

    @pyqtSlot()
    def update_model_types(self):

        folder_path = os.path.join(os.getcwd(), "neurolNetworks")

        if not os.path.exists(folder_path):
            print(f"Neural network folder not exists. Path: {folder_path}")
            return

        # sadece klasörleri result'a atar
        result = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]

        if "__pycache__" in result :  result.remove("__pycache__")

        self.listOfModelTypes = result

    @pyqtSlot(result=list)
    def getNetworkNames(self):
        networks_path = os.path.join(os.getcwd(), "neurolNetworks/" + self.modelType)
        network_names = [f for f in os.listdir(networks_path) if f.endswith(".py")]

        if "__init__.py" in network_names : network_names.remove("__init__.py")

        # Removing file extensions
        return [name[:-3] for name in network_names]

    @pyqtSlot(list)
    def setNetworksStatus(self, network_list):
        self.networksStatus = network_list
        print(self.networksStatus)

    def getNetworksStatus(self):
        return self.networksStatus

    def check_model_name(self):
        pass

    def onDestroyed(self, obj):
        if obj in self._listOfModels:
            self._listOfModels.remove(obj)

    def processModelsParallel(self):
        map(self.update_model_types, self._listOfModels)

    @staticmethod
    def create_modelMdl_from_data(vm:dict)->'ModelMdl':

        model = ModelMdl()
        model.modelName            = vm.get("model_name"          , "default")
        model.defaultPair          = vm.get("default_pair"        , "BTCUSDT")
        model.windowSize           = vm.get("window_size"         , 11)
        model.defaultInterval      = vm.get("default_interval"    , "5m")
        model.modelType            = vm.get("model_type"          , "")
        model.notes                = vm.get("notes"               , "")

        return model

    @pyqtSlot()
    def printModel(self):
        msg = f"""
        model.modelName       : {self.modelName       }
        model.defaultPair     : {self.defaultPair     }
        model.windowSize      : {self.windowSize      }
        model.defaultInterval : {self.defaultInterval }
        model.modelType       : {self.modelType       }
        model.notes           : {self.notes           }
        model.listOfModelTypes: {self.listOfModelTypes}
        """

        print(msg)


# Simulating a simple usage example
if __name__ == "__main__":
    model = ModelMdl()

    model.modelName       = "Test Model"
    model.defaultPair     = "Pair A"
    model.windowSize      = 15
    model.defaultInterval = "5s"
    model.modelType       = "Type1"
    model.notes           = "Some notes"

    print(model.modelName)
    print(model.defaultPair)
    print(model.windowSize)
    print(model.defaultInterval)
    print(model.modelType)
    print(model.notes)
    print(model.listOfModelTypes)
