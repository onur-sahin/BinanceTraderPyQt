
# from typing import Any, Optional
# from lightning.pytorch.utilities.types import STEP_OUTPUT
# from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional
from PyQt6.QtCore import QObject, pyqtSignal as Signal
import torch.nn as nn
import torch
import lightning as L
from torch.optim import Adam
import sys




class price_p2(L.LightningModule):

    finished  = Signal()

    def __init__(self, input_size, hidden_size=3, num_layers=1, seq_length=11, lims=[-1, 1], model_name="default"):
        super().__init__()

        self.model_name  = model_name
        self.input_size  = input_size
        self.hidden_size = hidden_size
        self.num_layers  = num_layers
        self.seq_length  = seq_length
        self.lims        = lims
        self.lr          = 0.00001 
        self.tmp_acc     = 0.0

        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size,
                            num_layers=num_layers, batch_first=True, dropout=0.3, dtype=torch.float64)

        self.fcl_1= nn.Linear(hidden_size,          int(hidden_size/2), dtype=torch.float64)
        self.fcl_2= nn.Linear(int(hidden_size/2),   1,                  dtype=torch.float64)

        self.dropout1 = nn.Dropout(0.3)
        self.dropout2 = nn.Dropout(0.3)
        self.loss_fn  = nn.MSELoss()
        self.count    = 0

    def forward(self, inputs:torch.Tensor):
        self.count += 1

        if inputs.ndim == 4:
            inputs = inputs.squeeze()

        lstm_out, (hn, cn) = self.lstm(inputs)

        fcl_out =self.fcl_1(  self.dropout1(  lstm_out[:,-1]  )  )

        fcl_out2 = self.fcl_2(self.dropout2(fcl_out))

        return fcl_out2

    def configure_optimizers(self):
        return Adam(self.parameters(), lr = self.lr)

    def on_train_start(self, trainer, pl_module):
        pass

    def on_train_end(self, trainer, pl_module):
        pass


    def training_step(self, batch, batch_idx):

        x_inputs, y_labels = batch

        y_pred = self.forward( x_inputs )

        loss = self.loss_fn(y_pred, y_labels)
        acc  = self.acc_calculator(y_pred, y_labels)
        self.tmp_acc = acc

        self.log_dict({"train_loss":loss, "train_acc":acc})

        return loss

    def on_train_batch_end(self, outputs, batch: Any, batch_idx: int) -> None:

        if batch_idx % 100 == 0:
            pass
            # self.writer.add_scalar("train_acc",  self.tmp_acc,    batch_idx)
            # self.writer.add_scalar("train_loss", outputs["loss"], batch_idx)


        if batch_idx % 1000 == 0:
            print(outputs + f"train_acc: {self.tmp_acc}")

        if batch_idx % 1000 == 0:
            # self.writer.flush()
            pass


    @staticmethod
    def acc_calculator(x, y):
        return ( 1-abs(x-y)/2 ).mean().item()


    # def validation_step(self, batch, bacth_idx):
    #     x_inputs, y_labels = batch

    #     y_pred = self.forward(x_inputs)

    #     val_loss = self.loss_fn(y_pred, y_labels)

    #     # calculate acc
    #     val_acc = self.acc_calculator(y_pred, y_labels)

    #     # log the outputs!
    #     self.log_dict({'val_loss': val_loss, 'val_acc': val_acc})
    #     return


    def test_step(self, batch, batch_idx):

        x_inputs, y_labels = batch

        y_pred = self.forward( x_inputs )

        test_loss = self.loss_fn(y_pred, y_labels)
        test_acc  = self.acc_calculator(y_pred, y_labels)

        self.log_dict({"test_loss:":test_loss, "test_acc":test_acc})


    def on_train_epoch_end(self):
        pass
        # self.signals:Signals
        # self.signals.setProgbarValue.emit(self.model_name + '-!-' + str(self.current_epoch+1))
