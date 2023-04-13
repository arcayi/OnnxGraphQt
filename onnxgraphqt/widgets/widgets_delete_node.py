from collections import namedtuple
from typing import List
import signal
from PySide2 import QtCore, QtWidgets, QtGui

from onnxgraphqt.graph.onnx_node_graph import OnnxGraph
from onnxgraphqt.widgets.widgets_message_box import MessageBox
from onnxgraphqt.utils.widgets import set_font, BASE_FONT_SIZE, LARGE_FONT_SIZE


DeleteNodeProperties = namedtuple("DeleteNodeProperties",
    [
        "remove_node_names",
    ])

class DeleteNodeWidgets(QtWidgets.QDialog):
    # _DEFAULT_WINDOW_WIDTH = 400
    _MAX_REMOVE_NODE_NAMES_COUNT = 5

    def __init__(self, graph: OnnxGraph=None, selected_nodes:List[str]=[], parent=None) -> None:
        super().__init__(parent)
        self.setModal(False)
        self.setWindowTitle("delete node")
        self.graph = graph
        self.selected_nodes = selected_nodes
        self.initUI()
        self.updateUI(self.graph, selected_nodes)

    def initUI(self):
        set_font(self, font_size=BASE_FONT_SIZE)

        base_layout = QtWidgets.QVBoxLayout()
        base_layout.setSizeConstraint(base_layout.SizeConstraint.SetFixedSize)

        # attributes
        self.layout = QtWidgets.QVBoxLayout()
        lbl = QtWidgets.QLabel("remove_node_names                                        ")
        set_font(lbl, font_size=LARGE_FONT_SIZE, bold=True)
        self.layout.addWidget(lbl)
        self.visible_remove_node_names_count = 1
        self.remove_node_names = {}
        for index in range(self._MAX_REMOVE_NODE_NAMES_COUNT):
            self.remove_node_names[index] = {}
            self.remove_node_names[index]["base"] = QtWidgets.QWidget()
            self.remove_node_names[index]["layout"] = QtWidgets.QHBoxLayout(self.remove_node_names[index]["base"])
            self.remove_node_names[index]["layout"].setContentsMargins(0, 0, 0, 0)
            self.remove_node_names[index]["name"] = QtWidgets.QComboBox()
            self.remove_node_names[index]["name"].setEditable(True)
            self.remove_node_names[index]["layout"].addWidget(self.remove_node_names[index]["name"])
            self.layout.addWidget(self.remove_node_names[index]["base"])
        self.btn_add = QtWidgets.QPushButton("+")
        self.btn_del = QtWidgets.QPushButton("-")
        self.btn_add.clicked.connect(self.btn_add_clicked)
        self.btn_del.clicked.connect(self.btn_del_clicked)
        self.set_visible()
        layout_btn = QtWidgets.QHBoxLayout()
        layout_btn.addWidget(self.btn_add)
        layout_btn.addWidget(self.btn_del)
        self.layout.addLayout(layout_btn)

        # add layout
        base_layout.addLayout(self.layout)

        # Dialog button
        btn = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok |
                                         QtWidgets.QDialogButtonBox.Cancel)
        btn.accepted.connect(self.accept)
        btn.rejected.connect(self.reject)
        # layout.addWidget(btn)
        base_layout.addWidget(btn)

        self.setLayout(base_layout)

    def updateUI(self, graph: OnnxGraph=None, selected_nodes:List[str]=[]):
        if graph:
            for index in range(self._MAX_REMOVE_NODE_NAMES_COUNT):
                self.remove_node_names[index]["name"].clear()
                for name, node in graph.nodes.items():
                    self.remove_node_names[index]["name"].addItem(name)
                self.remove_node_names[index]["name"].setCurrentIndex(-1)

            index = 0
            visible_count = 0
            for index in range(self._MAX_REMOVE_NODE_NAMES_COUNT):
                if len(selected_nodes) < visible_count + 1:
                    break
                node = selected_nodes[index]
                if node in graph.nodes.keys():
                    self.remove_node_names[visible_count]["name"].setCurrentText(node)
                    visible_count += 1
            self.visible_remove_node_names_count = min(visible_count + 1, self._MAX_REMOVE_NODE_NAMES_COUNT)
        self.set_visible()

    def set_visible(self):
        for key, widgets in self.remove_node_names.items():
            widgets["base"].setVisible(key < self.visible_remove_node_names_count)
        if self.visible_remove_node_names_count == 1:
            self.btn_add.setEnabled(True)
            self.btn_del.setEnabled(False)
        elif self.visible_remove_node_names_count >= self._MAX_REMOVE_NODE_NAMES_COUNT:
            self.btn_add.setEnabled(False)
            self.btn_del.setEnabled(True)
        else:
            self.btn_add.setEnabled(True)
            self.btn_del.setEnabled(True)

    def btn_add_clicked(self, e):
        self.visible_remove_node_names_count = min(max(0, self.visible_remove_node_names_count + 1), self._MAX_REMOVE_NODE_NAMES_COUNT)
        self.set_visible()

    def btn_del_clicked(self, e):
        self.visible_remove_node_names_count = min(max(0, self.visible_remove_node_names_count - 1), self._MAX_REMOVE_NODE_NAMES_COUNT)
        self.set_visible()


    def get_properties(self)->DeleteNodeProperties:

        remove_node_names = []
        for i in range(self.visible_remove_node_names_count):
            name = self.remove_node_names[i]["name"].currentText()
            if str.strip(name):
                remove_node_names.append(name)

        return DeleteNodeProperties(
            remove_node_names=remove_node_names
        )

    def accept(self) -> None:
        # value check
        invalid = False
        props = self.get_properties()
        print(props)
        err_msgs = []
        if len(props.remove_node_names) == 0:
            err_msgs.append("- remove_node_names is not set.")
            invalid = True

        if invalid:
            for m in err_msgs:
                print(m)
            MessageBox.error(err_msgs, "delete node", parent=self)
            return
        return super().accept()



if __name__ == "__main__":
    import signal
    import os
    # handle SIGINT to make the app terminate on CTRL+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QtWidgets.QApplication([])
    window = DeleteNodeWidgets()
    window.show()

    app.exec_()