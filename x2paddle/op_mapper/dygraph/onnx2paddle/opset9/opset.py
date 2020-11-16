# Copyright (c) 2019  PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from x2paddle.decoder.onnx_decoder import ONNXGraph, ONNXGraphNode, ONNXGraphDataNode
from x2paddle.core.graph import GraphNode
from x2paddle.core.fluid_code import Layer
from x2paddle.core.fluid_code import FluidCode
from x2paddle.core.util import *
from functools import reduce
import numpy as np
import onnx
import onnx.numpy_helper as numpy_helper
from onnx.mapping import TENSOR_TYPE_TO_NP_TYPE
import logging as _logging
from collections import OrderedDict
import math
import os
import copy
import sys
import shutil

_logger = _logging.getLogger(__name__)


def _const_weight_or_none(node, necessary=False):
    if 'Constant' in node.layer_type:
        return node.value
    if isinstance(node, ONNXGraphDataNode):
        return node.weight
    if necessary:
        assert '{} should be an initializer or Constant operator.'.format(
            node.layer_name)
    return None


def _is_static_shape(shape):
    negtive_dims = 0
    error_dims = 0
    for dim in shape:
        if dim < 0:
            negtive_dims += 1
        if dim < -1:
            error_dims += 1
    if negtive_dims > 1:
        return False
    if error_dims > 0:
        return False
    return True


def _get_same_padding(in_size, kernel_size, stride):
    new_size = int(math.ceil(in_size * 1.0 / stride))
    pad_size = (new_size - 1) * stride + kernel_size - in_size
    pad0 = int(pad_size / 2)
    pad1 = pad_size - pad0
    return [pad0, pad1]


def print_mapping_info(func):
    def run_mapping(*args, **kwargs):
        node = args[1]
        try:
            res = func(*args, **kwargs)
        except:
            print("convert failed node:{}, op_type is {}".format(
                node.layer_name[9:], node.layer_type))
            raise
        else:
            return res

    return run_mapping


class OpSet9():
    elementwise_ops = {
        'Add': 'paddle.add',
        'Div': 'paddle.divide',
        'Sub': 'fluid.layers.elementwise_sub',
        'Mul': 'paddle.multiply',
        'Pow': 'paddle.pow',
    }

    default_op_mapping_field_values = OrderedDict()
    default_op_mapping_field_values['PADDLE_OP'] = ''
    default_op_mapping_field_values['PADDLE_INPUT_ARGS'] = None
    default_op_mapping_field_values['ATTR_MAPPING'] = dict()
    default_op_mapping_field_values['DEFAULTS'] = dict()

    default_op_mapping = {
        'Shape': ['paddle.shape', ['input']],
        'Ceil': ['paddle.ceil', ['x']],
        'ReduceMean': [
            'paddle.mean', ['x'], dict(
                axes='axis', keepdims='keepdim'), dict(keepdim=1)
        ],
        'ReduceSum': [
            'paddle.sum', ['x'], dict(
                axes='axis', keepdims='keepdim'), dict(keepdim=1)
        ],
        'ReduceMin': [
            'paddle.min', ['x'], dict(
                axes='axis', keepdims='keepdim'), dict(keepdim=1)
        ],
        'ReduceMax': [
            'paddle.max', ['x'], dict(
                axes='axis', keepdims='keepdim'), dict(keepdim=1)
        ],
        #active function
        'Relu': ['paddle.nn.ReLU', ['x']],
        'LeakyRelu': ['paddle.nn.LeakyReLU', ['x'], dict(alpha='negative_slope'), 
                      dict(negative_slope=.01)],
        'Elu': ['paddle.nn.functional.elu', ['x'], dict(), dict(alpha=1.)],
        'ThresholdedRelu': [
            'paddle.nn.functional.thresholded_relu', ['x'], dict(alpha='threshold'),
            dict(alpha=1.)
        ],
        'Tanh': ['paddle.nn.Tanh', ['x']],
        'Sigmoid': ['paddle.nn.Sigmoid', ['x']],
        'Softsign': ['paddle.nn.Softsign', ['x']],
        'Softplus': ['paddle.nn.Softplus', ['x'], dict(), dict(threshold=float(sys.maxsize))],
        'Exp': ['paddle.exp', ['x']],
        'Softmax': ['paddle.nn.Softmax', ['x'], dict(), dict(axis=1)],
        'Sqrt': ['paddle.sqrt', ['x']],
        'Floor': ['paddle.floor', ['x']],
        'Abs': ['paddle.abs', ['x']],
        'Erf': ['paddle.erf', ['x']],
    }

    def __init__(self, decoder, paddle_graph):
        super(OpSet9, self).__init__()
        self.graph = decoder.graph
        self.paddle_graph = paddle_graph
        self.input_index = 0
        self.inputs_info = dict()
        self.weights = dict()
        self.nn_name2id = dict()
        
    def get_node_name(self, node):
        if hasattr(node, "index"):
            return "{}_{}".format(node.layer_name, node.index)
        else:
            return node.layer_name

    @print_mapping_info
    def directly_map(self, node, *args, **kwargs):
        inputs = node.layer.input
        op_type = node.layer_type
        attrs = node.attr_map
        info = self.default_op_mapping[op_type]
        info.extend(
            list(self.default_op_mapping_field_values.values())[len(info):])
        (paddle_op,
        paddle_input_args,
        attr_mapping,
        default_attrs) = info
        mapped_attrs = {
            attr_mapping.get(key, key): value
            for key, value in attrs.items()
        }
        if '' in mapped_attrs:
            mapped_attrs.pop('')
        if '_' in mapped_attrs:
            mapped_attrs.pop('_')
        layer_attrs = default_attrs.copy()
        layer_attrs.update(mapped_attrs)
        assert len(inputs) == 1, 'directly_map error with multi inputs'
        input = self.graph.get_input_node(node, idx=0, copy=True)
        if paddle_op.startswith("paddle.nn"):
            op_name = paddle_op[10:].lower()
            op_name = name_generator(op_name, self.nn_name2id)
            output_name = node.layer_name
            layer_outputs = [op_name, output_name]
            self.paddle_graph.add_layer(
                kernel=paddle_op,
                inputs={paddle_input_args[0]: self.get_node_name(input)},
                outputs=layer_outputs,
                **layer_attrs)
        else:
            self.paddle_graph.add_layer(
                kernel=paddle_op,
                inputs={paddle_input_args[0]: self.get_node_name(input)},
                outputs=[node.layer_name],
                **layer_attrs)        
        if paddle_op == 'paddle.shape':
            self.paddle_graph.add_layer(
                'paddle.cast',
                inputs={"x": node.layer_name},
                outputs=[node.layer_name],
                dtype=string('int64'))
            
    @print_mapping_info
    def elementwise_map(self, node):
        assert node.layer_type in self.elementwise_ops
        op_type = self.elementwise_ops[node.layer_type]
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        val_y = self.graph.get_input_node(node, idx=1, copy=True)
        inputs_dict = {'x': self.get_node_name(val_x), 
                       'y': self.get_node_name(val_y)}
        self.paddle_graph.add_layer(
            op_type, 
            inputs=inputs_dict, 
            outputs=[node.layer_name])

    @print_mapping_info
    def place_holder(self, node):
        shape = node.out_shapes[0]
        for i, dim_shape in enumerate(shape):
            if dim_shape == 0 and i == 0:
                shape[i] = 1
            if dim_shape == 0 and i != 0:
                assert 'shape of input is not assigned'
        self.paddle_graph.add_layer(
            kernel="paddle.to_tensor",
            inputs={},
            outputs=[node.layer_name],
            data="x{}".format(self.input_index))
        self.inputs_info["x{}".format(self.input_index)] = [shape, node.dtype]
        self.input_index += 1

    @print_mapping_info
    def create_parameter(self, node, parameter=None):
        if parameter is not None:
            node = parameter
        dtype = node.dtype
        shape = node.out_shapes[0]
        if len(node.weight.shape) == 0:
            self.paddle_graph.add_layer(
                "paddle.full", 
                inputs={}, 
                outputs=[node.layer_name],
                dtype=string(dtype),
                shape=[1],
                fill_value=node.weight)
        else:
            self.weights[node.layer_name] = node.weight
            self.paddle_graph.add_layer(
                "self.create_parameter",
                inputs={},
                outputs=[node.layer_name],
                shape=shape,
                attr=string(node.layer_name),
                dtype=string(dtype),
                default_initializer="paddle.nn.initializer.Constant(value=0.0)")
        

    def _pad_if_asymmetric(self, node, pads, val_name):  # pads: SSEE
        assert len(pads) & 1 == 0
        symmetric = True
        ndims = len(pads) // 2
        for idx_dim in range(ndims):
            if pads[idx_dim] != pads[ndims + idx_dim]:
                symmetric = False
                break
        if symmetric:
            return pads[:ndims], val_name
        val_padded = self.Pad(node, op_independent=False)
        return [0] * ndims, val_padded

    def _interpolate(self, node):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        inputs = {'x': self.get_node_name(val_x)}
        if node.layer_type == 'Resize':
            if len(node.layer.input) == 2:
                # opset 10
                val_scales = self.graph.get_input_node(node, idx=1, copy=True)
                inputs['scale_factor'] = self.get_node_name(val_scales)
            elif len(node.layer.input) == 3:
                # opset 11
                val_scales = self.graph.get_input_node(node, idx=2, copy=True)
                inputs['scale_factor'] = self.get_node_name(val_scales)
            elif len(node.layer.input) == 4:
                # opset 11
                val_sizes = self.graph.get_input_node(node, idx=3, copy=True)
                var_nc, var_hw = val_sizes.layer_name + '_nc', val_sizes.layer_name + '_hw'
                self.paddle_graph.add_layer(
                    'paddle.split',
                    inputs={"x": self.get_node_name(val_sizes)},
                    outputs=[var_nc, var_hw],
                    num_or_sections=[2, 2],
                    axis=0)
                self.paddle_graph.add_layer(
                    "paddle.cast",
                    inputs={"x": var_hw},
                    outputs=[var_hw],
                    dtype=string('int32'))
                inputs['size'] = var_hw
        elif node.layer_type == 'Upsample':
            val_scales = self.graph.get_input_node(node, idx=1, copy=True)
            inputs['scale'] = val_scales

        mode = node.get_attr('mode', 'nearest')
        attrs = {"align_corners": False,
                 "mode": string(mode),
                 "align_mode": 1}
        self.paddle_graph.add_layer(
            kernel="paddle.nn.functional.interpolate",
            inputs=inputs,
            outputs=[node.layer_name],
            **attrs)
        
    @print_mapping_info
    def HardSigmoid(self, node):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        alpha = node.get_attr('alpha', 0.2)
        beta = node.get_attr('beta', 0.5)
        self.paddle_graph.add_layer(
            kernel="paddle.scale",
            inputs={"x": self.get_node_name(val_x)},
            outputs=[node.layer_name + "_val"],
            scale=alpha,
            bias=beta)
        self.paddle_graph.add_layer(
            kernel="paddle.clip",
            inputs={"x": node.layer_name + "_val"},
            outputs=[node.layer_name],
            min=0.0,
            max=1.0)        

    @print_mapping_info
    def RoiAlign(self, node):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        val_rois = self.graph.get_input_node(node, idx=1, copy=True)

        pooled_height = node.get_attr('output_height')
        pooled_width = node.get_attr('output_width')
        spatial_scale = node.get_attr('spatial_scale')
        sampling_ratio = node.get_attr('sampling_ratio')
        layer_attrs = {
            'pooled_height': pooled_height,
            'pooled_width': pooled_width,
            'spatial_scale': spatial_scale,
            'sampling_ratio': sampling_ratio,
        }
        self.paddle_graph.add_layer(
            'fluid.layers.roi_align',
            inputs={'input': self.get_node_name(val_x),
                    'rois': self.get_node_name(val_rois)},
            outputs=[node.layer_name],
            **layer_attrs)
                       

    @print_mapping_info
    def MaxRoiPool(self, node):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        val_rois = self.graph.get_input_node(node, idx=1, copy=True)

        spatial_scale = node.get_attr('spatial_scale')
        pooled_height, pooled_width = node.get_attr('pooled_shape')
        layer_attrs = {
            'pooled_height': pooled_height,
            'pooled_width': pooled_width,
            'spatial_scale': spatial_scale,
        }
        self.paddle_graph.add_layer(
            'fluid.layers.roi_pool',
            inputs={'input': self.get_node_name(val_x),
                    'rois': self.get_node_name(val_rois)},
            outputs=[node.layer_name],
            **layer_attrs)

    @print_mapping_info
    def Pad(self, node, op_independent=True):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        pads = node.get_attr('pads')
        mode = node.get_attr('mode', 'constant')
        value = node.get_attr('value', 0.)
        data_shape = val_x.out_shapes[0]
        output_shape = node.out_shapes[0]
        assume_pad2d = False
        layer_attrs = {}
        layer_attrs['mode'] = string(mode)
        paddings = []
        if len(pads) == 4:
            assume_pad2d |= mode != 'constant'
            if data_shape:
                assume_pad2d |= data_shape and len(data_shape) == 4  # NCHW
            if output_shape:
                assume_pad2d |= output_shape and len(output_shape) == 4  # NCHW
        if assume_pad2d:
            paddle_op = 'paddle.nn.Pad2D'
            layer_attrs['data_format'] = string('NCHW')
            layer_attrs['value'] = value
        else:
            paddle_op = 'fluid.layers.pad'
            layer_attrs["pad_value"] = value
        if len(pads) == 4:
            paddings = np.array(pads).reshape(
                (-1, 2)).transpose().flatten().tolist()  # SSEE -> SESE
        elif len(pads) == 8:
            paddings = np.array(pads).reshape(
                (-1, 4)).transpose().flatten().tolist()  # SSEE -> SESE
            if sum(paddings[:4]) == 0:
                paddle_op = 'paddle.nn.Pad2D'
                paddings = paddings[4:]
                layer_attrs['value'] = value
                if 'pad_value' in layer_attrs:
                    layer_attrs.pop('pad_value')
        tmp_paddings = copy.deepcopy(paddings)
        paddings[0] = tmp_paddings[2]
        paddings[1] = tmp_paddings[3]
        paddings[2] = tmp_paddings[0]
        paddings[3] = tmp_paddings[1]
        if paddle_op == 'paddle.nn.Pad2D':
            layer_attrs['padding'] = paddings
            nn_op_name = name_generator("pad2d", self.nn_name2id)
        else:
            layer_attrs['paddings'] = paddings
        if op_independent:
            self.paddle_graph.add_layer(
                paddle_op, 
                inputs={'x': self.get_node_name(val_x)}, 
                outputs=[nn_op_name, node.layer_name] if paddle_op == 'paddle.nn.Pad2D' else [node.layer_name], 
                **layer_attrs)
        else:
            self.paddle_graph.add_layer(
                paddle_op,
                inputs={'x': self.get_node_name(val_x)},
                outputs=[nn_op_name, node.layer_name + '_paded'] if paddle_op == 'paddle.nn.Pad2D' \
                    else [node.layer_name + '_paded'],
                **layer_attrs)
            return node.layer_name + '_paded'

    @print_mapping_info
    def Unsqueeze(self, node):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        axes = node.get_attr('axes')
        layer_attrs = {'axis': axes}
        if len(val_x.out_shapes[0]) == 0:
            if node.layer_name:
                self.paddle_graph.add_layer(
                    'paddle.reshape',
                    inputs={"x": self.get_node_name(val_x)},
                    outputs=[node.layer_name],
                    shape=[1])
        else:
            if str(val_x.dtype) == 'bool':
                val_x_cast = val_x.layer_name + '_cast'
                self.paddle_graph.add_layer(
                    'paddle.cast',
                    inputs={"x": self.get_node_name(val_x)},
                    outputs=[val_x_cast],
                    dtype=string('int64'))
                self.paddle_graph.add_layer(
                    'paddle.unsqueeze',
                    inputs={"x": val_x_cast},
                    outputs=[node.layer_name],
                    **layer_attrs)
            else:
                self.paddle_graph.add_layer(
                    'paddle.unsqueeze', 
                    inputs={"x": self.get_node_name(val_x)}, 
                    outputs=[node.layer_name],
                    **layer_attrs)

    @print_mapping_info
    def Shrink(self, node):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        bias = node.get_attr('bias')
        lambd = node.get_attr('lambd')
        assert bias == 0.0, 'not support bias!=0'
        self.paddle_graph.add_layer(
            'paddle.nn.functional.hardshrink', 
            inputs={"x": self.get_node_name(val_x)}, 
            outputs=[node.layer_name], 
            threshold=lambd)

    @print_mapping_info
    def Constant(self, node):
        val_output = self.graph.get_node(node.layer.output[0], copy=True)

        value = node.get_attr('value')
        dtype = np.dtype(value.dtype)
        output_dtype = val_output.dtype
        if output_dtype:
            assert dtype == output_dtype, 'tensor dtype unmatches storage dtype'

        shape = node.get_attr('shape', None)

        if shape is None:
            shape = val_output.out_shapes[0]
        if shape is None:
            shape = list(value.shape)
            _logger.warning('in (Constant -> %s): '
                            'attribute "shape" of %s not inferred, '
                            'using value as 1-D tensor may lead to fails',
                            val_output.layer_name, val_output.layer_name)
        if len(value) == 1:
            value = value.tolist()
            value = value[0]
            self.paddle_graph.add_layer(
                "paddle.full", 
                inputs={}, 
                outputs=[node.layer_name],
                dtype=string(dtype),
                shape=[1],
                fill_value=value)
        else:
            value = np.reshape(value, shape)
            self.weights[node.layer_name] = value
            self.paddle_graph.add_layer(
                "self.create_parameter",
                inputs={},
                outputs=[node.layer_name],
                shape=shape,
                attr=string(node.layer_name),
                dtype=string(dtype),
                default_initializer="paddle.nn.initializer.Constant(value=0.0)")

    @print_mapping_info
    def Resize(self, node):
        self._interpolate(node)

    @print_mapping_info
    def Upsample(self, node):
        self._interpolate(node)

    @print_mapping_info
    def InstanceNormalization(self, node):
        op_name = name_generator("instanse_norm", self.nn_name2id)
        output_name = node.layer_name
        layer_outputs = [op_name, output_name]
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        val_scale = self.graph.get_input_node(node, idx=1, copy=True)
        val_b = self.graph.get_input_node(node, idx=2, copy=True)
        epsilon = node.get_attr('epsilon', 1e-5)
        layer_attrs = {
            'num_features': node.out_shapes[0][1],
            'epsilon': epsilon,
            'weight_attr': string(self.get_node_name(val_scale)),
            'bias_attr': string(self.get_node_name(val_b))
        }
        dim = len(val_x.out_shapes[0])
        if dim == 2 or dim == 3:
            paddle_op = "paddle.nn.InstanceNorm1D"
        elif dim == 4:
            paddle_op = "paddle.nn.InstanceNorm2D"
        elif dim == 5:
            paddle_op = "paddle.nn.InstanceNorm3D"
        else:
            raise Exception("The paddle only support 2D, 3D, 4D or 5D input in InstanceNormalization.")
        self.paddle_graph.add_layer(
            paddle_op, 
            inputs={"x": self.get_node_name(val_x)}, 
            outputs=layer_outputs, 
            **layer_attrs)

    @print_mapping_info
    def Expand(self, node):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        val_shape = self.graph.get_input_node(node, idx=1, copy=True)
        val_x_dtype = val_x.dtype
        name_ones = node.layer_name + '_ones'
        attr_ones = {
            'shape': val_shape.layer_name,
            'dtype': string(val_x_dtype),
            'fill_value': 1
        }
        self.paddle_graph.add_layer(
            'paddle.full',
            inputs={},
            outputs=[name_ones],
            **attr_ones)
        inputs_dict = {'x': name_ones, 
                       'y': self.get_node_name(val_x)}
        self.paddle_graph.add_layer(
            'paddle.multiply',
            inputs=inputs_dict,
            outputs=[node.layer_name])

    @print_mapping_info
    def Gather(self, node):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        indices = self.graph.get_input_node(node, idx=1, copy=True)
        indices_shape = indices.out_shapes[0]
        axis = node.get_attr('axis', 0)
        #assert len(
        #    indices_shape) <= 2, "Gather op don't support dim of indice >2 "
        if axis == 0 and len(indices_shape) <= 1:
            if len(val_x.out_shapes[0]) <= 1:
                self.paddle_graph.add_layer(
                    'paddle.gather',
                    inputs={'x': self.get_node_name(val_x),
                            'index': self.get_node_name(indices)},
                    outputs=[node.layer_name])
            elif len(val_x.out_shapes[0]) > 1:
                if len(indices_shape) == 0:
                    gather_ = node.layer_name + '_1'
                    self.paddle_graph.add_layer(
                        'paddle.gather',
                        inputs={'x': self.get_node_name(val_x),
                                'index': self.get_node_name(indices)},
                        outputs=[gather_])
                    self.paddle_graph.add_layer(
                        'paddle.squeeze',
                        inputs={'x': gather_},
                        outputs=[node.layer_name],
                        axis=[0])
                else:
                    self.paddle_graph.add_layer(
                        'paddle.gather',
                        inputs={'x': self.get_node_name(val_x),
                                'index': self.get_node_name(indices)},
                        outputs=[node.layer_name])
        elif axis > 0 and len(indices_shape) <= 1:
            perm = list(range(len(val_x.out_shapes[0])))
            perm = [axis] + perm[:axis] + perm[axis + 1:]
            name_trans = val_x.layer_name + '_trans'
            self.paddle_graph.add_layer(
                'paddle.transpose',
                inputs={"x": self.get_node_name(val_x)},
                outputs=[name_trans],
                perm=perm)
            self.paddle_graph.add_layer(
                'paddle.gather',
                inputs={'x': name_trans,
                        'index': self.get_node_name(indices)},
                outputs=[node.layer_name])
            self.paddle_graph.add_layer(
                'paddle.transpose', 
                inputs={"x": node.layer_name}, 
                outputs=[node.layer_name], 
                perm=perm)
            if len(indices_shape) < 1:
                self.paddle_graph.add_layer(
                    'paddle.squeeze',
                    inputs={'x': node.layer_name},
                    outputs=[node.layer_name],
                    axis=[axis])
        elif axis == 0 and len(indices_shape) > 1:
            if val_x.out_shapes[0] is not None and isinstance(
                    val_x, ONNXGraphDataNode):
                indices_cast = indices.layer_name + '_cast'
                self.paddle_graph.add_layer(
                    'paddle.cast',
                    inputs={"x": self.get_node_name(indices)},
                    outputs=indices_cast,
                    dtype=string('int64'))
                op_name = name_generator("embedding", self.nn_name2id)
                output_name = node.layer_name
                layer_outputs = [op_name, output_name]
                self.paddle_graph.add_layer(
                    'paddle.nn.Embedding',
                    inputs={"x": indices_cast},
                    outputs=layer_outputs,
                    param_attr=string(val_x.layer_name),
                    size=val_x.out_shapes[0])
            else:
                from functools import reduce
                reshape_shape = reduce(lambda x, y: x * y, indices_shape)
                indices_reshape = indices.layer_name + '_shape'
                self.paddle_graph.add_layer(
                    'paddle.reshape',
                    inputs={"x": self.get_node_name(indices)},
                    outputs=[indices_reshape],
                    shape=[reshape_shape, ])

                perm = list(range(len(val_x.out_shapes[0])))
                self.paddle_graph.add_layer(
                    'paddle.gather',
                    inputs={'x': self.get_node_name(val_x),
                            'index': indices_reshape},
                    outputs=[node.layer_name])
                val_x_shape = val_x.out_shapes[0]
                reshaped_shape = []
                for i in perm:
                    reshaped_shape.append(indices_shape[i])
                for i in val_x_shape[:axis] + val_x_shape[axis + 1:]:
                    reshaped_shape.append(i)
                self.paddle_graph.add_layer(
                    'paddle.reshape',
                    inputs={"x": node.layer_name},
                    outputs=[node.layer_name],
                    shape=reshaped_shape)
        elif axis > 0 and len(indices_shape) > 1:
            from functools import reduce
            reshape_shape = reduce(lambda x, y: x * y, indices_shape)
            indices_reshape = indices.layer_name + '_shape'
            self.paddle_graph.add_layer(
                'paddle.reshape',
                inputs={"x": self.get_node_name(indices)},
                outputs=[indices_reshape],
                shape=[reshape_shape, ])

            perm = list(range(len(val_x.out_shapes[0])))
            perm = [axis] + perm[:axis] + perm[axis + 1:]
            name_trans = val_x.layer_name + '_transpose'
            self.paddle_graph.add_layer(
                'paddle.transpose',
                inputs={"x": self.get_node_name(val_x)},
                outputs=[name_trans],
                perm=perm)
            self.paddle_graph.add_layer(
                'paddle.gather',
                inputs={'x': name_trans,
                        'index': indices_reshape},
                outputs=[node.layer_name])
            input_transpose = node.layer_name + '_transpose'
            self.paddle_graph.add_layer(
                'paddle.transpose',
                inputs={"x": node.layer_name},
                outputs=[input_transpose],
                perm=perm)
            val_x_shape = val_x.out_shapes[0]
            reshaped_shape = []
            for i in perm:
                reshaped_shape.append(indices_shape[i])
            for i in val_x_shape[:axis] + val_x_shape[axis + 1:]:
                reshaped_shape.append(i)
            self.paddle_graph.add_layer(
                'paddle.reshape',
                inputs={"x": input_transpose},
                outputs=[node.layer_name],
                shape=reshaped_shape)

    @print_mapping_info
    def ScatterND(self, node):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        indices = self.graph.get_input_node(node, idx=1, copy=True)
        updates = self.graph.get_input_node(node, idx=2, copy=True)
        if len(indices.out_shapes[0]) == 1:
            self.paddle_graph.add_layer(
                'paddle.scatter',
                inputs={'x': self.get_node_name(val_x),
                        'index': self.get_node_name(indices),
                        'updates': self.get_node_name(updates)},
                outputs=[node.layer_name])
        else:
            input_inner_indices = node.layer_name + '_input_inner_indices'
            shape = val_x.out_shapes[0]
            self.paddle_graph.add_layer(
                'paddle.reshape',
                inputs={"x": self.get_node_name(indices)},
                outputs=[self.get_node_name(indices)],
                shape=indices.out_shapes[0])

            zeros_like_val_x = val_x.layer_name + '_zeros'
            self.paddle_graph.add_layer(
                'paddle.zeros_like',
                inputs={"x": self.get_node_name(val_x)},
                outputs=[zeros_like_val_x])
            self.paddle_graph.add_layer(
                'paddle.scatter_nd_add',
                inputs={
                    'x': zeros_like_val_x,
                    'index': self.get_node_name(indices),
                    'updates': self.get_node_name(updates)
                },
                outputs=[input_inner_indices])
            indices_mask = node.layer_name + '_indices_mask'
            constant_minus_one = node.layer_name + '_constant_minus_one'
            # full_like support create tensor shape like input tensor
            self.paddle_graph.add_layer(
                'paddle.full_like',
                inputs={"x": self.get_node_name(updates)},
                outputs=[constant_minus_one],
                dtype=string(updates.dtype),
                fill_value=-1)
            self.paddle_graph.add_layer(
                'paddle.scatter_nd_add',
                inputs={
                    'x': zeros_like_val_x,
                    'index': self.get_node_name(indices),
                    'updates': constant_minus_one
                },
                outputs=[indices_mask])
            constant_one = node.layer_name + '_constant_1'
            # full_like support create tensor shape like input tensor
            self.paddle_graph.add_layer(
                'paddle.full_like',
                inputs={"x": self.get_node_name(val_x)},
                outputs=[constant_one],
                dtype=string(val_x.dtype),
                fill_value=1)
            input_out_indices_mask = node.layer_name + '_input_out_indices_mask'
            self.paddle_graph.add_layer(
                "paddle.add",
                inputs={"x": indices_mask,
                        "y": constant_one},
                outputs=[input_out_indices_mask])

            input_out_indices = node.layer_name + '_input_out_indices'
            self.paddle_graph.add_layer(
                "paddle.multiply",
                inputs={"x": self.get_node_name(val_x),
                        "y": input_out_indices_mask},
                outputs=[input_out_indices])

            self.paddle_graph.add_layer(
                "paddle.add",
                inputs={"x": input_inner_indices,
                        "y": input_out_indices},
                outputs=[node.layer_name])

    @print_mapping_info
    def Range(self, node):
        val_start = self.graph.get_input_node(node, idx=0, copy=True)
        val_limit = self.graph.get_input_node(node, idx=1, copy=True)
        val_delta = self.graph.get_input_node(node, idx=2, copy=True)
        dtype = val_start.dtype
        inputs = {'start': self.get_node_name(val_start), 
                  'end': self.get_node_name(val_limit), 
                  'step': self.get_node_name(val_delta)}
        self.paddle_graph.add_layer(
            'paddle.arange',
            inputs=inputs,
            outputs=[node.layer_name],
            dtype=string(dtype))

    @print_mapping_info
    def Slice(self, node):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        starts, ends, axes, steps = None, None, None, None
        layer_attrs = {}
        if len(node.inputs) > 1:
            starts = self.graph.get_input_node(node, idx=1, copy=True)
            ends = self.graph.get_input_node(node, idx=2, copy=True)
            starts_value = _const_weight_or_none(starts)
            ends_value = _const_weight_or_none(ends)

            if len(node.inputs) > 3:
                axes = self.graph.get_input_node(node, idx=3, copy=True)
                axes = _const_weight_or_none(axes, necessary=True)
            if len(node.inputs) > 4:
                steps = self.graph.get_input_node(node, idx=4, copy=True)
                steps = _const_weight_or_none(steps)
            layer_attrs = {
                "axes": axes,
                "starts": starts.layer_name,
                "ends": ends.layer_name
            }
            if starts_value is not None and ends_value is not None:
                starts_value = starts_value.copy()
                ends_value = ends_value.copy()
                #for idx in range(len(ends_value)):
                #    if ends_value[idx] > 2**31 - 1:
                #        ends_value[idx] = 2**31 - 1
                #print(val_x.out_shapes)
                for idx in range(len(ends_value)):
                    if starts_value[idx] >= val_x.out_shapes[0][axes[idx]]:
                        starts_value[idx] = val_x.out_shapes[0][axes[idx]] - 1
                        ends_value[idx] = val_x.out_shapes[0][axes[idx]]
                        starts_value[idx] = val_x.out_shapes[0][axes[idx]] - 1
                    elif ends_value[idx] > 2**31 - 1:
                        ends_value[idx] = 2**31 - 1
                layer_attrs = {
                    "axes": axes,
                    "starts": starts_value,
                    "ends": ends_value
                }
            else:
                if starts.dtype != 'int32':
                    starts_cast = starts.layer_name + '_cast'
                    self.paddle_graph.add_layer(
                        'paddle.cast',
                        inputs={"x": self.get_node_name(starts)},
                        outputs=[starts_cast],
                        dtype=string('int32'))
                    layer_attrs['starts'] = starts_cast
                if ends.dtype != 'int32':
                    ends_cast = ends.layer_name + '_cast'
                self.paddle_graph.add_layer(
                    'paddle.cast',
                    inputs={"x": self.get_node_name(ends)},
                    outputs=[ends_cast],
                    dtype=string('int32'))
                layer_attrs['ends'] = ends_cast
        else:
            starts = node.get_attr('starts')
            ends = node.get_attr('ends')
            axes = node.get_attr('axes')
            for idx in range(len(ends)):
                if ends[idx] > 2**31 - 1:
                    ends[idx] = 2**31 - 1
            layer_attrs = {"axes": axes, "starts": starts, "ends": ends}

        if steps is not None:
            layer_attrs['strides'] = steps
            self.paddle_graph.add_layer(
                'paddle.strided_slice', 
                inputs={"x": self.get_node_name(val_x)}, 
                outputs=[node.layer_name], 
                **layer_attrs)
        else:
            self.paddle_graph.add_layer(
                'paddle.slice', 
                inputs={"input": self.get_node_name(val_x)}, 
                outputs=[node.layer_name],  
                **layer_attrs)

    @print_mapping_info
    def ConstantOfShape(self, node):
        val_shape = self.graph.get_input_node(node, idx=0, copy=True)
        val_y = self.graph.get_node(node.layer.output[0], copy=True)

        value = node.get_attr('value')
        dtype = value.dtype
        value = value.tolist()
        assert len(value) == 1, ('given value not Scalar, shape of value > 1, '
                                 'this is not supported')
        if len(value) == 1:
            value = value[0]
            layer_attrs = {
                'shape': val_shape.layer_name,
                'dtype': string(dtype),
                'fill_value': value
            }
            self.paddle_graph.add_layer(
                "paddle.full", 
                inputs={}, 
                outputs=[node.layer_name],
                **layer_attrs)

    @print_mapping_info
    def Clip(self, node):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        val_y = self.graph.get_node(node.layer.output[0], copy=True)
        max_value, min_value = None, None
        if len(node.inputs) == 1:
            max_value = node.get_attr('max')
            min_value = node.get_attr('min')
            layer_attrs = {
                'max': max_value,
                'min': min_value,
            }
            self.paddle_graph.add_layer(
                'paddle.clip', 
                inputs={"x": self.get_node_name(val_x)}, 
                outputs=[node.layer_name], 
                **layer_attrs)
        else:
            max_ipt = self.graph.get_input_node(node, idx=1, copy=True)
            min_ipt = self.graph.get_input_node(node, idx=2, copy=True)
            max_value = _const_weight_or_none(max_ipt)
            min_value = _const_weight_or_none(min_ipt)
            if max_value.shape == (1, ):
                max_value = max_value[0]
            if min_value.shape == (1, ):
                min_value = min_value[0]
        if max_value is not None and min_value is not None:
            layer_attrs = {'max': max_value, 'min': min_value}
            self.paddle_graph.add_layer(
                'paddle.clip', 
                inputs={"x": self.get_node_name(val_x)}, 
                outputs=[node.layer_name], 
                **layer_attrs)
        else:
            raise

    @print_mapping_info
    def Split(self, node):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)

        paddle_op = 'split'
        split = node.get_attr('split')
        axis = node.get_attr('axis', 0)
        layer_attrs = {
            'num_or_sections': split,
            'axis': axis,
        }
        outputs_list = list()
        if isinstance(split, list) or isinstance(split, tuple):
            for i, s in enumerate(split):
                outputs_list.append("{}_{}".format(node.layer_name, i))
        else:
            outputs_list.append(node.layer_name)

        self.paddle_graph.add_layer(
            'paddle.split', 
            inputs={"x": self.get_node_name(val_x)}, 
            outputs=outputs_list, 
            **layer_attrs)

    @print_mapping_info
    def Reshape(self, node):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        val_shape = self.graph.get_input_node(node, idx=1, copy=True)
        val_reshaped = self.graph.get_node(node.layer.output[0], copy=True)
        shape_value = _const_weight_or_none(val_shape)
        shape_dims = len(val_shape.out_shapes[0])

        if shape_value is not None:
            self.paddle_graph.add_layer(
                'paddle.reshape',
                inputs={'x': self.get_node_name(val_x)},
                outputs=[node.layer_name],
                shape=shape_value.tolist())
        elif len(node.out_shapes[0]) > 0 and _is_static_shape(node.out_shapes[
                0]):
            self.paddle_graph.add_layer(
                'paddle.reshape',
                inputs={'x': self.get_node_name(val_x)},
                outputs=[node.layer_name],
                shape=node.out_shapes[0])
        elif val_shape.dtype == 'int64':
            val_shape_cast = val_shape.layer_name + '_cast'
            self.paddle_graph.add_layer(
                'paddle.cast',
                inputs={'x': self.get_node_name(val_shape)},
                outputs=[val_shape_cast],
                dtype=string('int32'))
            # shape may be [], come form Gather by scalar indices
            if len(val_shape.out_shapes[0]) > 0:
                self.paddle_graph.add_layer(
                    'paddle.reshape',
                    inputs={'x': self.get_node_name(val_shape_cast)},
                    outputs=[val_shape_cast],
                    shape=val_shape.out_shapes[0])
            self.paddle_graph.add_layer(
                'paddle.reshape',
                inputs={'x': elf.get_node_name(val_x),
                        'shape': val_shape_cast},
                outputs=[node.layer_name])
        else:
            # shape may be [], come form Gather by scalar indices
            if len(val_shape.out_shapes[0]) > 0:
                self.paddle_graph.add_layer(
                    'paddle.reshape',
                    inputs={'x': self.get_node_name(val_shape)},
                    outputs=[self.get_node_name(val_shape)],
                    shape=val_shape.out_shapes[0])
            self.paddle_graph.add_layer(
                'paddle.reshape',
                inputs={'x': self.get_node_name(val_x),
                        'shape': self.get_node_name(val_shape)},
                outputs=node)

    @print_mapping_info
    def Cast(self, node):
        val_input = self.graph.get_input_node(node, idx=0, copy=True)
        val_output = self.graph.get_node(node.layer.output[0], copy=True)

        dtype = node.get_attr('to')
        if not isinstance(dtype, np.dtype):
            dtype = TENSOR_TYPE_TO_NP_TYPE[dtype]

        output_dtype = val_output.dtype
        if output_dtype:
            assert dtype == output_dtype, 'dtype of to unmatches output'
        self.paddle_graph.add_layer(
            'paddle.cast', 
            inputs={'x': self.get_node_name(val_input)}, 
            outputs=[node.layer_name], 
            dtype=string(dtype))

    @print_mapping_info
    def Not(self, node):
        val_input = self.graph.get_input_node(node, idx=0, copy=True)
        self.paddle_graph.add_layer('paddle.logical_not', 
                                    inputs={'x': self.get_node_name(val_input)}, 
                                    outputs=[node.layer_name])

    @print_mapping_info
    def AveragePool(self, node):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)

        auto_pad = node.get_attr('auto_pad', 'NOTSET')
        kernel_shape = node.get_attr("kernel_shape")
        poolnd = len(kernel_shape)
        strides = node.get_attr("strides")
        pad_mode = node.get_attr("pads")
        ceil_mode = bool(node.get_attr('ceil_mode', 0))
        pads = node.get_attr('pads', [0] * (poolnd * 2))

        paddings, val_x = self._pad_if_asymmetric(node, pads, val_x)

        if auto_pad == "SAME_UPPER" or auto_pad == "SAME_LOWER":
            input_shape = val_x.out_shapes[0]
            pad_h = _get_same_padding(input_shape[2], kernel_shape[0],
                                      strides[0])
            pad_w = _get_same_padding(input_shape[3], kernel_shape[1],
                                      strides[1])
            paddings = pad_h + pad_w

        paddle_op = 'fluid.layers.pool{}d'.format(poolnd)
        assert 2 <= poolnd <= 3, 'only pool2d and pool3d are supported'
        layer_attrs = {
            "pool_size": kernel_shape,
            "pool_type": string('avg'),
            "pool_stride": strides,
            "pool_padding": paddings,
            "ceil_mode": ceil_mode,
            "exclusive": 'True',
            "name": string(node.layer_name)
        }
        self.paddle_graph.add_layer(
            paddle_op, 
            inputs={'input': val_x if isinstance(val_x, str) else self.get_node_name(val_x)}, 
            outputs=[node.layer_name], 
            **layer_attrs)
        # TODO(syf): op has diff
#         op_name = name_generator("pool", self.nn_name2id)
#         output_name = node.layer_name
#         layer_outputs = [op_name, output_name]
#         paddle_op = 'paddle.nn.Pool{}D'.format(poolnd)
#         assert 1 <= poolnd <= 3, 'only Pool1D, Pool2D and Pool3D are supported'
#         layer_attrs = {
#             "kernel_size": kernel_shape,
#             "stride": strides,
#             "padding": paddings,
#             "ceil_mode": ceil_mode,
#             "exclusive": 'True',
#         }
#         self.paddle_graph.add_layer(
#             paddle_op, 
#             inputs={'x': self.get_node_name(val_x)}, 
#             outputs=layer_outputs, 
#             **layer_attrs)

    @print_mapping_info
    def Concat(self, node):
        inputs_list = []
        dtypes = set()
        for i in range(len(node.layer.input)):
            ipt = self.graph.get_input_node(node, idx=i, copy=True)
            inputs_list.append(self.get_node_name(ipt))
            dtypes.add(ipt.dtype)
        if len(dtypes) > 1:
            assert 'Unspported situation happened, please create issue on https://github.com/PaddlePaddle/X2Paddle/issues.'
        axis = node.get_attr('axis')
        self.paddle_graph.add_layer(
            'paddle.concat', 
            inputs={"x": inputs_list}, 
            outputs=[node.layer_name], 
            axis=axis)

    @print_mapping_info
    def Flatten(self, node):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        output_shape = node.out_shapes[0]
        axis = node.get_attr('axis', 1)
        shape_list = [1, 1]
        if axis == 0:
            for s in output_shape:
                shape_list[1] *= s
        else:
            for s in output_shape[:axis]:
                shape_list[0] *= s
            for s in output_shape[axis:]:
                shape_list[1] *= s
        self.paddle_graph.add_layer(
            'paddle.reshape', 
            inputs={"x": self.get_node_name(val_x)}, 
            outputs=[node.layer_name],
            shape=shape_list)

    @print_mapping_info
    def Gemm(self, node):
        val_a = self.graph.get_input_node(node, idx=0, copy=True)
        val_b = self.graph.get_input_node(node, idx=1, copy=True)
        val_c = self.graph.get_input_node(node, idx=2, copy=True)

        alpha = node.get_attr('alpha', 1.)  # optional
        beta = node.get_attr('beta', 1.)  # optional
        trans_a = bool(node.get_attr('transA', 0))  # optional
        trans_b = bool(node.get_attr('transB', 0))  # optional
        val_mm = node.layer_name + '_mm'
        matmul_inputs = {"x": self.get_node_name(val_a), 
                         "y": self.get_node_name(val_b)}
        attr_matmul = {
            "transpose_x": trans_a,
            "transpose_y": trans_b,
        }
        self.paddle_graph.add_layer(
            'paddle.matmul',
            inputs=matmul_inputs,
            outputs=[val_mm],
            **attr_matmul)
        self.paddle_graph.add_layer(
            "paddle.scale", 
            inputs={"x": val_mm}, 
            outputs=[val_mm],
            scale=alpha)

        if beta != 0:
            if beta == 1.:
                add_inputs = {"x": val_mm, 
                              "y": self.get_node_name(val_c)}
                self.paddle_graph.add_layer(
                    "paddle.add",
                    inputs=add_inputs,
                    outputs=[node.layer_name])
            else:
                var_beta = node.layer_name + '_beta'
                self.paddle_graph.add_layer(
                    "paddle.scale",
                    inputs={"x": self.get_node_name(val_c)},
                    outputs=[var_beta],
                    scale=beta)
                add_inputs = {"x": val_mm, "y": var_beta}
                self.paddle_graph.add_layer(
                    "paddle.addd",
                    inputs=add_inputs,
                    outputs=[node.layer_name])

    @print_mapping_info
    def Sum(self, node):
        val_inps = node.layer.input
        inputs_dict = {
            "x": self.get_node_name(
                self.graph.get_input_node(
                node, idx=0, copy=True)),
            "y": self.get_node_name(
                self.graph.get_input_node(
                node, idx=1, copy=True)),
        }
        self.paddle_graph.add_layer("paddle.add", 
                                    inputs=inputs_dict, 
                                    outputs=[node.layer_name])

        for idx, ipt in enumerate(val_inps[2:]):
            y = self.graph.get_input_node(node, idx=idx, copy=True)
            inputs_dict = {
                "x": node.layer_name,
                "y": self.get_node_name(y),
            }
            self.paddle_graph.add_layer(
                "paddle.add", 
                inputs=inputs_dict, 
                outputs=[node.layer_name])

    @print_mapping_info
    def MatMul(self, node):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        val_y = self.graph.get_input_node(node, idx=1, copy=True)
        x_shape = val_x.out_shapes[0]
        y_shape = val_y.out_shapes[0]
        inputs_dict = {"x": self.get_node_name(val_x), 
                       "y": self.get_node_name(val_y)}
        if y_shape[0] == 1 and x_shape[-1] != 1 and x_shape[0] != 1:
            y_squeeze = val_y.layer_name + '_squeeze'
            self.paddle_graph.add_layer(
                "paddle.squeeze",
                inputs={"x": self.get_node_name(val_y)},
                outputs=[y_squeeze],
                axis=[0])
            inputs_dict['y'] = y_squeeze
            self.paddle_graph.add_layer(
                "paddle.matmul", 
                inputs=inputs_dict, 
                outputs=[node.layer_name])
        else:
            self.paddle_graph.add_layer(
                "paddle.matmul", 
                inputs=inputs_dict, 
                outputs=[node.layer_name])

    @print_mapping_info
    def BatchNormalization(self, node):
        op_name = name_generator("batchnorm", self.nn_name2id)
        output_name = node.layer_name
        layer_outputs = [op_name, output_name]
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        val_scale = self.graph.get_input_node(node, idx=1, copy=True)
        val_b = self.graph.get_input_node(node, idx=2, copy=True)
        val_mean = self.graph.get_input_node(node, idx=3, copy=True)
        val_var = self.graph.get_input_node(node, idx=4, copy=True)

        momentum = node.get_attr('momentum', .9)
        epsilon = node.get_attr('epsilon', 1e-5)
        c = val_x.out_shapes[0][1]

        # Attribute: spatial is used in BatchNormalization-1,6,7
        spatial = bool(node.get_attr('spatial'))
        layer_attrs = {
            "num_channels": c,
            "momentum": momentum,
            "epsilon": epsilon,
            "is_test": True,
            "param_attr": string(self.get_node_name(val_scale)),
            "bias_attr": string(self.get_node_name(val_b)),
            "moving_mean_name": string(self.get_node_name(val_mean)),
            "moving_variance_name": string(self.get_node_name(val_var)),
            "use_global_stats": False,
        }
        self.paddle_graph.add_layer(
            "paddle.nn.BatchNorm", 
            inputs={"x": self.get_node_name(val_x)}, 
            outputs=layer_outputs, 
            **layer_attrs)

    @print_mapping_info
    def Transpose(self, node):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        perm = node.get_attr('perm')
        self.paddle_graph.add_layer(
            "paddle.transpose", 
            inputs={"x": self.get_node_name(val_x)},
            outputs=[node.layer_name], 
            perm=perm)

    @print_mapping_info
    def PRelu(self, node):
        op_name = name_generator("prelu", self.nn_name2id)
        output_name = node.layer_name
        layer_outputs = [op_name, output_name]
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        val_slope = self.graph.get_input_node(node, idx=1, copy=True)

        mode = 'channel'
        shape_slope = val_slope.out_shapes[0]
        if shape_slope == [1]:
            mode = 'all'
        elif len(shape_slope) > 2:
            mode = 'element'

        if mode == 'channel' and len(shape_slope) == 1:
            # paddle params shape need be [1, channel]
            slope_data = _const_weight_or_none(val_slope)
            slope_data = np.reshape(slope_data, [1] + shape_slope)
            self.weights[val_slope.layer_name] = slope_data

        layer_attrs = {
            "param_attr": string(val_slope.layer_name),
            'mode': string(mode),
            "channel": val_x.out_shapes[0][1] if mode == "channel" else None,
            "input_shape": val_x.out_shapes[0] if mode == "element" else None,
        }
        self.paddle_graph.add_layer(
            "paddle.nn.PReLU", 
            inputs={"x": self.get_node_name(val_x)}, 
            outputs=layer_outputs, 
            **layer_attrs)

    @print_mapping_info
    def Squeeze(self, node):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        axes = node.get_attr('axes')
        if len(val_x.out_shapes[0]) == 1:
            self.paddle_graph.add_layer(
                "paddle.cast",
                inputs={"x": self.get_node_name(val_x)},
                outputs=[node.layer_name],
                dtype=string(val_x.dtype))
        else:
            self.paddle_graph.add_layer(
                "paddle.squeeze", 
                inputs={"x": self.get_node_name(val_x)}, 
                outputs=[node.layer_name], 
                axis=axes)

    @print_mapping_info
    def Equal(self, node):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        val_y = self.graph.get_input_node(node, idx=1, copy=True)
        self.paddle_graph.add_layer(
            "paddle.equal",
            inputs={'x': self.get_node_name(val_x),
                    'y': self.get_node_name(val_y)},
            outputs=[node.layer_name])

    @print_mapping_info
    def Greater(self, node):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        val_y = self.graph.get_input_node(node, idx=1, copy=True)
        self.paddle_graph.add_layer(
            "paddle.greater_than",
            inputs={'x': self.get_node_name(val_x),
                    'y': self.get_node_name(val_y)},
            outputs=node,
            param_attr=None)

    @print_mapping_info
    def Where(self, node):
        condition = self.graph.get_input_node(node, idx=0, copy=True)
        val_x = self.graph.get_input_node(node, idx=1, copy=True)
        val_y = self.graph.get_input_node(node, idx=2, copy=True)

        not_condition = condition.layer_name + '_not'
        self.paddle_graph.add_layer(
            "paddle.logical_not",
            inputs={"x": self.get_node_name(condition)},
            outputs=[not_condition])
        cast_not_condition = not_condition + '_cast'
        self.paddle_graph.add_layer(
            "paddle.cast",
            inputs={"x": not_condition},
            outputs=[cast_not_condition],
            dtype=string(val_x.dtype))
        cast_condition = condition.layer_name + '_cast'
        self.paddle_graph.add_layer(
            "paddle.cast",
            inputs={"x": self.get_node_name(condition)},
            outputs=[cast_condition],
            dtype=string(val_x.dtype))
        mul_val_x = val_x.layer_name + '_mul'
        self.paddle_graph.add_layer(
            "paddle.multiply",
            inputs={'x': self.get_node_name(val_x),
                    'y': cast_condition},
            outputs=[mul_val_x])
        mul_val_y = val_y.layer_name + '_mul'
        self.paddle_graph.add_layer(
            "paddle.multiply",
            inputs={'x': self.get_node_name(val_y),
                    'y': cast_not_condition},
            outputs=[mul_val_y])

        self.paddle_graph.add_layer(
            "paddle.add",
            inputs={'x': mul_val_x,
                    'y': mul_val_y},
            outputs=[node.layer_name])

    @print_mapping_info
    def NonZero(self, node):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        val_x_dim = len(val_x.out_shapes[0])
        if val_x_dim == 1:
            self.paddle_graph.add_layer(
                "paddle.nonzero", 
                inputs={"x": self.get_node_name(val_x)}, 
                outputs=[self.get_node_name(val_x)])
            self.paddle_graph.add_layer(
                "paddle.transpose",
                inputs={"x": self.get_node_name(val_x)},
                outputs=[node.layer_naem],
                perm=[1, 0])
        if val_x_dim > 1:
            self.paddle_graph.add_layer(
                "paddle.nonzero", 
                inputs={"x": self.get_node_name(val_x)}, 
                outputs=[self.get_node_name(val_x)])
            self.paddle_graph.add_layer(
                "paddle.split",
                inputs={"x": self.get_node_name(val_x)}, 
                outputs=[self.get_node_name(val_x)],
                num_or_sections=1,
                axis=val_x_dim)
            self.paddle_graph.add_layer(
                "paddle.concat", 
                inputs={"x": self.get_node_name(val_x)}, 
                outputs=[node.layer_name])

    @print_mapping_info
    def Identity(self, node):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        self.paddle_graph.add_layer(
            "paddle.assign", 
            inputs={"x": self.get_node_name(val_x)}, 
            outputs=[node.layer_name])

    @print_mapping_info
    def Tile(self, node):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        val_repeats = self.graph.get_input_node(node, idx=1, copy=True)
        repeats = _const_weight_or_none(val_repeats)

        if repeats is None:
            repeats = val_repeats.layer_name
            if val_repeats.dtype != 'int32':
                self.paddle_graph.add_layer(
                    "paddle.cast",
                    inputs={"x": repeats},
                    outputs=["{}.tmp".format(repeats)],
                    dtype=string("int32"))
                repeats = "{}.tmp".format(repeats)

        elif isinstance(repeats, int):
            repeats = [repeats]

        attr = {
            'expand_times': repeats,
            "name": string(node.layer_name),
        }
        self.paddle_graph.add_layer(
            "paddle.tile", 
            inputs={"x": self.get_node_name(val_x)}, 
                    outputs=[node.layer_name], 
                    repeat_times=repeats)

    @print_mapping_info
    def MaxPool(self, node):
        op_name = name_generator("pool", self.nn_name2id)
        output_name = node.layer_name
        layer_outputs = [op_name, output_name]
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        auto_pad = node.get_attr('auto_pad', 'NOTSET')
        assert node.get_attr(
            "dilations") is None, 'only dilations = 0 is supported'  # optional

        kernel_shape = node.get_attr("kernel_shape")
        poolnd = len(kernel_shape)
        strides = node.get_attr("strides")
        pad_mode = node.get_attr("pads")
        ceil_mode = bool(node.get_attr('ceil_mode', 0))  # optional
        pads = node.get_attr('pads', [0] * (poolnd * 2))  # optional
        paddle_op = 'paddle.nn.MaxPool{}D'.format(poolnd)
        assert 1 <= poolnd <= 3, 'only Pool1D, Pool2D and Pool3D are supported'

        paddings, val_x = self._pad_if_asymmetric(node, pads, val_x)

        if auto_pad == "SAME_UPPER" or auto_pad == "SAME_LOWER":
            input_shape = val_x.out_shapes[0]
            pad_h = _get_same_padding(input_shape[2], kernel_shape[0],
                                      strides[0])
            pad_w = _get_same_padding(input_shape[3], kernel_shape[1],
                                      strides[1])
            paddings = pad_h + pad_w
            
        layer_attrs = {
            "kernel_size": kernel_shape,
            "stride": strides,
            "padding": paddings,
            "ceil_mode": ceil_mode,
        }
        self.paddle_graph.add_layer(
            paddle_op, 
            inputs={'x': val_x if isinstance(val_x, str) else self.get_node_name(val_x)}, 
            outputs=layer_outputs, 
            **layer_attrs)

    @print_mapping_info
    def GlobalMaxPool(self, node):
        op_name = name_generator("pool", self.nn_name2id)
        output_name = node.layer_name
        layer_outputs = [op_name, output_name]
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        input_shape = val_x.out_shapes[0]
        if len(input_shape) == 4:
            poolnd = 2
        elif len(input_shape) == 5:
            poolnd = 3
        elif len(input_shape) == 3:
            poolnd = 1
        paddle_op = 'paddle.nn.AdaptiveMaxPool{}D'.format(poolnd)
        assert 1 <= poolnd <= 3, 'only Pool1D, Pool2D and Pool3D are supported'
        output_shape = node.out_shapes[0]
        self.paddle_graph.add_layer(
            paddle_op, 
            inputs={'x': self.get_node_name(val_x)}, 
            outputs=layer_outputs, 
            output_size=output_shape[2:])

    @print_mapping_info
    def GlobalAveragePool(self, node):
        op_name = name_generator("pool", self.nn_name2id)
        output_name = node.layer_name
        layer_outputs = [op_name, output_name]
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        input_shape = val_x.out_shapes[0]
        if len(input_shape) == 4:
            poolnd = 2
        elif len(input_shape) == 5:
            poolnd = 3
        elif len(input_shape) == 3:
            poolnd = 1
        paddle_op = 'paddle.nn.AdaptiveAvgPool{}D'.format(poolnd)
        assert 1 <= poolnd <= 3, 'only Pool1D, Pool2D and Pool3D are supported'
        output_shape = node.out_shapes[0]
        self.paddle_graph.add_layer(
            paddle_op, 
            inputs={'x': self.get_node_name(val_x)}, 
            outputs=layer_outputs, 
            output_size=output_shape[2:])

    @print_mapping_info
    def Conv(self, node):
        op_name = name_generator("conv", self.nn_name2id)
        output_name = node.layer_name
        layer_outputs = [op_name, output_name]
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        val_w = self.graph.get_input_node(node, idx=1, copy=True)
        val_y = self.graph.get_node(node.layer.output[0], copy=True)
        has_bias = len(node.layer.input) == 3
        if has_bias:
            val_b = self.graph.get_input_node(node, idx=2, copy=True)
        auto_pad = node.get_attr('auto_pad', 'NOTSET')

        kernel_shape = node.get_attr('kernel_shape')
        convnd = len(kernel_shape)
        assert 2 <= convnd <= 3, 'only Conv2D and Conv3D is supported'
        num_out_channels = val_w.out_shapes[0][0]
        num_in_channels = val_w.out_shapes[0][1]
        paddle_op = 'paddle.nn.Conv{}D'.format(convnd)

        num_groups = node.get_attr('group', 1)
        strides = node.get_attr('strides', [1] * convnd)
        dilations = node.get_attr('dilations', [1] * convnd)
        pads = node.get_attr('pads', [0] * (convnd * 2))

        input_shape = val_x.out_shapes[0]
        paddings, val_x = self._pad_if_asymmetric(node, pads, val_x)

        if auto_pad == "SAME_UPPER" or auto_pad == "SAME_LOWER":
            pad_h = _get_same_padding(input_shape[2], kernel_shape[0],
                                      strides[0])
            pad_w = _get_same_padding(input_shape[3], kernel_shape[1],
                                      strides[1])
            paddings = pad_h + pad_w

        layer_attrs = {
            "in_channels": num_in_channels * num_groups,
            "out_channels": num_out_channels,
            "kernel_size": kernel_shape,
            "stride": strides,
            "padding": paddings,
            "dilation": dilations,
            "groups": num_groups,
            'weight_attr': string(val_w.layer_name),
        }
        if has_bias:
            layer_attrs["bias_attr"] = string(val_b.layer_name)
        else:
            layer_attrs["bias_attr"] = False
        self.paddle_graph.add_layer(
            paddle_op, 
            inputs={'x': val_x if isinstance(val_x, str) else self.get_node_name(val_x)}, 
            outputs=layer_outputs, 
            **layer_attrs)

    @print_mapping_info
    def ConvTranspose(self, node):
        val_x = self.graph.get_input_node(node, idx=0, copy=True)
        val_w = self.graph.get_input_node(node, idx=1, copy=True)
        val_b = None
        if len(node.layer.input) > 2:
            val_b = self.graph.get_input_node(node, idx=2, copy=True)
        auto_pad = node.get_attr('auto_pad', 'NOTSET')
        out_padding = node.get_attr('output_padding', [0, 0])
        kernel_shape = node.get_attr('kernel_shape')
        assert kernel_shape, 'kernel_shape not inferred'
        convnd = len(kernel_shape)
        assert 2 <= convnd <= 3, 'only Conv2DTranspose and Conv3DTranspose supported'
        num_in_channels = val_w.out_shapes[0][0]
        num_out_channels = val_w.out_shapes[0][1]
        paddle_op = 'paddle.nn.functional.conv{}d_transpose'.format(convnd)

        num_groups = node.get_attr('group', 1)
        strides = node.get_attr('strides', [1] * convnd)
        dilations = node.get_attr('dilations', [1] * convnd)
        output_size = node.get_attr('output_shape', [])
        pads = node.get_attr('pads', [0] * (convnd * 2))

        paddings, var_x = self._pad_if_asymmetric(node, pads, val_x)

        output_size = [0, 0]

        output_size[0] = (val_x.out_shapes[0][2] - 1
                          ) * strides[0] - 2 * paddings[0] + dilations[0] * (
                              kernel_shape[0] - 1) + 1 + out_padding[0]
        output_size[1] = (val_x.out_shapes[0][3] - 1
                          ) * strides[1] - 2 * paddings[1] + dilations[1] * (
                              kernel_shape[1] - 1) + 1 + out_padding[1]
#         layer_attrs = {
#             'in_channels': num_in_channels,
#             'out_channels': num_out_channels,
#             'output_size': output_size or None,
#             'kernel_size': kernel_shape,
#             'padding': paddings,
#             'stride': strides,
#             'dilation': dilations,
#             'groups': num_groups,
#             'weight_attr': string(val_w.layer_name),
#             'bias_attr': None if val_b is None else string(val_b.layer_name),
#         }
#         self.paddle_graph.add_layer(
#             paddle_op, 
#             inputs={"x": self.get_node_name(val_x)}, 
#             outputs=layer_outputs, 
#             **layer_attrs)
        inputs_dict = {'x': val_x if isinstance(val_x, str) else self.get_node_name(val_x),
                       "weight": val_w.layer_name}
        layer_attrs = {
            "stride": strides,
            "dilation": dilations,
            "padding": paddings,
            "groups": num_groups,
            "output_size": node.out_shapes[0][2:]}
        if val_b is not None:
            inputs_dict["bias"] = val_b.layer_name
        else:
            layer_attrs["bias"] = None
        self.paddle_graph.add_layer(
            kernel="paddle.nn.functional.conv2d_transpose",
            inputs=inputs_dict,
            outputs=[node.layer_name],
            **layer_attrs)
