from dataclasses import dataclass
from typing import (
    Dict, List, Any, Optional, Union
)
from collections import OrderedDict

from NodeGraphQt import BaseNode
from NodeGraphQt.constants import NodeEnum, LayoutDirectionEnum, NodePropWidgetEnum

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.color import (
    COLOR_BG,
    COLOR_FONT,
    COLOR_GRID,
    INPUT_NODE_COLOR,
    OUTPUT_NODE_COLOR,
    NODE_BORDER_COLOR,
    get_node_color,
)
from utils.widgets import set_font, GRAPH_FONT_SIZE
from widgets.custom_node_item import CustomNodeItem


@dataclass
class OnnxNodeIO:
    name: str
    dtype: str
    shape: List[int]
    values: List


class ONNXNode(BaseNode):
    # unique node identifier.
    __identifier__ = 'nodes.node'
    # initial default node name.
    NODE_NAME = 'onnxnode'

    def __init__(self):
        super(ONNXNode, self).__init__(qgraphics_item=CustomNodeItem)
        self.set_layout_direction(LayoutDirectionEnum.VERTICAL.value)
        self.attrs = OrderedDict()
        self.node_name = ""
        self.op = ""
        self.onnx_inputs = []
        self.onnx_outputs = []

        # create node inputs.
        self.input_port = self.add_input('multi in', multi_input=True, display_name=False)
        # create node outputs.
        self.output_port = self.add_output('multi out', multi_output=True, display_name=False)
        self.set_font()

    def set_attrs(self, attrs:OrderedDict, push_undo=False):
        self.attrs = attrs
        for key, val in self.attrs.items():
            if self.has_property(key + "_"):
                self.set_property(key + "_", val, push_undo=push_undo)
            else:
                if key == "dtype":
                    self.create_property(key + "_", val, widget_type=NodePropWidgetEnum.QLABEL)
                else:
                    self.create_property(key + "_", val, widget_type=NodePropWidgetEnum.QLINE_EDIT)

    def get_attrs(self)->OrderedDict:
        d = [(key, self.get_property(key + "_")) for key in self.attrs.keys()]
        return OrderedDict(d)

    def set_node_name(self, node_name:str, push_undo=False):
        self.node_name = node_name
        if not self.has_property("node_name"):
            self.create_property("node_name", self.node_name, widget_type=NodePropWidgetEnum.QLINE_EDIT)
        else:
            self.set_property("node_name", self.node_name, push_undo=push_undo)

    def get_node_name(self):
        self.node_name = self.get_property("node_name")
        return self.node_name

    def set_op(self, op:str, push_undo=False):
        self.op = op
        self._view.name = op
        if not self.has_property("op"):
            self.create_property("op", self.op, widget_type=NodePropWidgetEnum.QLABEL)
        else:
            self.set_property("op", self.op, push_undo=push_undo)

    def set_onnx_inputs(self, onnx_inputs:List[OnnxNodeIO], push_undo=False):
        self.onnx_inputs = onnx_inputs
        value = [[inp.name, inp.dtype, inp.shape, inp.values] for inp in self.onnx_inputs]
        if not self.has_property("inputs_"):
            self.create_property("inputs_", value, widget_type=NodePropWidgetEnum.QLINE_EDIT)
        else:
            self.set_property("inputs_", value, push_undo=push_undo)

    def set_onnx_outputs(self, onnx_outputs:List[OnnxNodeIO], push_undo=False):
        self.onnx_outputs = onnx_outputs
        value = [[out.name, out.dtype, out.shape, out.values] for out in self.onnx_outputs]
        if not self.has_property("outputs_"):
            self.create_property("outputs_",  value, widget_type=NodePropWidgetEnum.QLINE_EDIT)
        else:
            self.set_property("outputs_", value, push_undo=push_undo)

    def set_color(self, push_undo=False):
        self.view.text_color = COLOR_FONT + [255]
        color = get_node_color(self.op)
        self.set_property('border_color', NODE_BORDER_COLOR + [255], push_undo)
        self.set_property('color', color + [255], push_undo)

    def set_font(self, font_size=GRAPH_FONT_SIZE, bold=False):
        set_font(self.view.text_item, font_size=font_size, bold=bold)


class ONNXInput(BaseNode):
    # unique node identifier.
    __identifier__ = 'nodes.node'
    # initial default node name.
    NODE_NAME = 'input'
    def __init__(self):
        super(ONNXInput, self).__init__(qgraphics_item=CustomNodeItem)
        self.set_layout_direction(LayoutDirectionEnum.VERTICAL.value)
        self.node_name = ""
        self.shape = []
        self.dtype = ""
        self.output_names = []
        self.create_property("node_name", self.node_name, widget_type=NodePropWidgetEnum.QLINE_EDIT)
        self.create_property("shape", self.shape, widget_type=NodePropWidgetEnum.QLINE_EDIT)
        self.create_property("dtype", self.dtype, widget_type=NodePropWidgetEnum.QLINE_EDIT)
        self.create_property("output_names", self.output_names, widget_type=NodePropWidgetEnum.QTEXT_EDIT)
        # create node outputs.
        self.output_port = self.add_output('multi out', multi_output=True, display_name=False)
        self.set_color()
        self.set_font()
        self._view.name = "input"

    def get_node_name(self):
        self.node_name = self.get_property("node_name")
        return self.node_name

    def set_node_name(self, node_name:str, push_undo=False):
        self.node_name = node_name
        self.set_property("node_name", self.node_name, push_undo=push_undo)

    def get_shape(self):
        self.shape = self.get_property("shape")
        return self.shape

    def set_shape(self, shape, push_undo=False):
        self.shape = shape
        self.set_property("shape", self.shape, push_undo=push_undo)

    def get_dtype(self):
        self.dtype = self.get_property("dtype")
        return self.dtype

    def set_dtype(self, dtype, push_undo=False):
        self.dtype = str(dtype)
        self.set_property("dtype", self.dtype, push_undo=push_undo)

    def get_output_names(self)->List[str]:
        self.output_names = self.get_property("output_names")
        return self.output_names

    def set_output_names(self, output_names, push_undo=False):
        self.output_names = output_names
        self.set_property("output_names", self.output_names, push_undo=push_undo)

    def set_color(self, push_undo=False):
        self.view.text_color = COLOR_FONT + [255]
        self.set_property('border_color', NODE_BORDER_COLOR + [255], push_undo)
        self.set_property('color', INPUT_NODE_COLOR + [255], push_undo)

    def set_font(self, font_size=GRAPH_FONT_SIZE, bold=False):
        set_font(self.view.text_item, font_size=font_size, bold=bold)


class ONNXOutput(BaseNode):
    # unique node identifier.
    __identifier__ = 'nodes.node'
    # initial default node name.
    NODE_NAME = 'output'
    def __init__(self):
        super(ONNXOutput, self).__init__(qgraphics_item=CustomNodeItem)
        self.set_layout_direction(LayoutDirectionEnum.VERTICAL.value)
        self.node_name = ""
        self.shape = []
        self.dtype:str = ""
        self.input_names = []
        self.create_property("node_name", self.node_name, widget_type=NodePropWidgetEnum.QLINE_EDIT)
        self.create_property("shape", self.shape, widget_type=NodePropWidgetEnum.QLINE_EDIT)
        self.create_property("dtype", self.dtype, widget_type=NodePropWidgetEnum.QLINE_EDIT)
        self.create_property("input_names", self.input_names, widget_type=NodePropWidgetEnum.QTEXT_EDIT)
        # create node inputs.
        self.input_port = self.add_input('multi in', multi_input=True, display_name=False)
        self.set_color()
        self.set_font()
        self._view.name = "output"

    def get_node_name(self):
        self.node_name = self.get_property("node_name")
        return self.node_name

    def set_node_name(self, node_name:str, push_undo=False):
        self.node_name = node_name
        self.set_property("node_name", self.node_name, push_undo=push_undo)

    def get_shape(self):
        self.shape = self.get_property("shape")
        return self.shape

    def set_shape(self, shape, push_undo=False):
        self.shape = shape
        self.set_property("shape", self.shape, push_undo)

    def get_dtype(self):
        self.dtype = self.get_property("dtype")
        return self.dtype

    def set_dtype(self, dtype, push_undo=False):
        self.dtype = str(dtype)
        self.set_property("dtype", self.dtype, push_undo)

    def get_input_names(self):
        self.input_names = self.get_property("input_names")
        return self.input_names

    def set_input_names(self, input_names, push_undo=False):
        self.input_names = input_names
        self.set_property("input_names", self.input_names, push_undo)

    def set_color(self, push_undo=False):
        self.view.text_color = COLOR_FONT + [255]
        self.set_property('border_color', NODE_BORDER_COLOR + [255], push_undo)
        self.set_property('color', INPUT_NODE_COLOR + [255], push_undo)

    def set_font(self, font_size=GRAPH_FONT_SIZE, bold=False):
        set_font(self.view.text_item, font_size=font_size, bold=bold)
