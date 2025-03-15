from PyQt6.QtCore import QObject, pyqtSignal, pyqtProperty, QThread, QVariantList, QMutex
from PyQt6.QtCore import Qt
from PyQt6.QtConcurrent import map
import os
import subprocess


class ModelMdl(QObject):

    modelNameChanged        = pyqtSignal()
    defaultPairChanged      = pyqtSignal()
    windowSizeChanged       = pyqtSignal()
    defaultIntervalChanged  = pyqtSignal()
    modelTypeChanged        = pyqtSignal()
    notesChanged            = pyqtSignal()
    listOfModelTypesChanged = pyqtSignal()

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

        self._process = None
        self._thrd = None

        self.networksStatus = QVariantList()

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

    # Methods

    def save_model(self):
        # This would typically interact with a DB or other resources
        pass

    def processModelsParallel(self):
        map(self.update_model_types, self._listOfModels)

    def update_model_types(self):
        folder_path = os.path.join(os.getcwd(), "../pythonModules/neurolNetworks")
        if not os.path.exists(folder_path):
            print(f"Neural network folder not exists. Path: {folder_path}")
            return

        result = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]
        self.listOfModelTypes = result

    def getNetworkNames(self):
        networks_path = os.path.join(os.getcwd(), "../pythonModules/neurolNetworks/nn_models")
        network_names = [f for f in os.listdir(networks_path) if f.endswith(".py")]

        # Removing file extensions
        return [name[:-3] for name in network_names]

    def setNetworksStatus(self, network_list):
        self.networksStatus = QVariantList(network_list)

    def getNetworksStatus(self):
        return self.networksStatus

    def check_model_name(self):
        pass

    def onDestroyed(self, obj):
        if obj in self._listOfModels:
            self._listOfModels.remove(obj)

    def processModelsParallel(self):
        map(self.update_model_types, self._listOfModels)


# Simulating a simple usage example
if __name__ == "__main__":
    model = ModelMdl()

    model.modelName = "Test Model"
    model.defaultPair = "Pair A"
    model.windowSize = 15
    model.defaultInterval = "5s"
    model.modelType = "Type1"
    model.notes = "Some notes"

    print(model.modelName)
    print(model.defaultPair)
    print(model.windowSize)
    print(model.defaultInterval)
    print(model.modelType)
    print(model.notes)
    print(model.listOfModelTypes)
