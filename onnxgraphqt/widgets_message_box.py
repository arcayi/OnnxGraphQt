from PySide2 import QtCore, QtWidgets, QtGui
from typing import Union, List

class MessageBox(QtWidgets.QMessageBox):
    def __init__(self,
                 text:Union[str, List[str]],
                 title:str,
                 default_button=QtWidgets.QMessageBox.Ok,
                 icon=QtWidgets.QMessageBox.Icon.Information,
                 parent=None) -> int:
        super().__init__(parent)
        if isinstance(text, list):
            self.setText('\n'.join(text))
        else:
            self.setText(text)
        self.setWindowTitle(title)
        self.setDefaultButton(default_button)
        self.setIcon(icon)
        self.exec_()
        return

    @classmethod
    def info(cls,
             text:Union[str, List[str]],
             title:str,
             default_button=QtWidgets.QMessageBox.Ok,
             parent=None):
        return MessageBox(text, title, default_button, icon=MessageBox.Icon.Information, parent=parent)

    @classmethod
    def warn(cls,
             text:Union[str, List[str]],
             title:str,
             default_button=QtWidgets.QMessageBox.Ok,
             parent=None):
        return MessageBox(text, title, default_button, icon=MessageBox.Icon.Warning, parent=parent)

    @classmethod
    def error(cls,
              text:Union[str, List[str]],
              title:str,
              default_button=QtWidgets.QMessageBox.Ok,
              parent=None):
        return MessageBox(text, title, default_button, icon=MessageBox.Icon.Critical, parent=parent)
