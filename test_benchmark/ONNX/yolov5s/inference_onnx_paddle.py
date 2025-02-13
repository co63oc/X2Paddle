#!/usr/bin/env python
# coding: utf-8

# In[6]:

import os
import onnx
import numpy as np

# In[1]:

from onnx import helper
from onnx import AttributeProto, TensorProto, GraphProto
import onnx.shape_inference as shape_inference


def make_variable_name(name):
    """
    make a valid code name for ParamAttr
    """

    if name == '':
        raise ValueError('name should not be empty')
    for s in ' .*?\\/-:':  #
        name = name.replace(s, '_')
    return 'x2paddle_' + name


def standardize_variable_name(graph):
    """
    standardize variable name for paddle's code
    """
    for initializer in graph.initializer:
        initializer.name = make_variable_name(initializer.name)
    for ipt in graph.input:
        ipt.name = make_variable_name(ipt.name)
    for output in graph.output:
        output.name = make_variable_name(output.name)
    for item in graph.value_info:
        item.name = make_variable_name(item.name)
    for node in graph.node:
        node.name = make_variable_name(node.output[0])
        for i in range(len(node.input)):
            node.input[i] = make_variable_name(node.input[i])
        for i in range(len(node.output)):
            node.output[i] = make_variable_name(node.output[i])


def get_results_of_inference(model, np_images):
    results_of_inference = {}
    nodes = []
    standardize_variable_name(model.graph)
    for node in model.graph.node:
        nd = helper.make_tensor_value_info(node.name,
                                           TensorProto.UNDEFINED,
                                           shape=None)
        nodes.append(nd)

    while len(nodes) > 0:
        tmp_nodes = nodes[:254]
        model.graph.ClearField('output')
        model.graph.output.MergeFrom(tmp_nodes)
        prepared_backend = prepare(model, device='CPU', no_check_UNSAFE=True)
        output = prepared_backend.run(inputs=np_images)

        for idx, info in enumerate(tmp_nodes):
            results_of_inference[info.name] = output[idx]
        nodes = nodes[254:]
    return results_of_inference


def get_results_of_inference_rt(model, input_data):
    import onnxruntime as rt
    results_of_inference = {}
    standardize_variable_name(model.graph)
    inputs = []

    model = shape_inference.infer_shapes(model)
    outputs = []
    for value_info in model.graph.value_info:
        outputs.append(value_info)

    model.graph.ClearField('output')
    model.graph.output.MergeFrom(outputs)
    onnx.save(model, './onnx_model_infer.onnx')

    sess = rt.InferenceSession('./onnx_model_infer.onnx')
    inputs_dict = {}
    for i, data in enumerate(input_data):
        inputs_dict[sess.get_inputs()[i].name] = data
    res = sess.run(None, input_feed=inputs_dict)

    for idx, info in enumerate(outputs):
        results_of_inference[info.name] = res[idx]
    return results_of_inference


# In[7]:

from paddle.fluid.initializer import Constant
from paddle.fluid.param_attr import ParamAttr
import paddle.fluid as fluid

# In[8]:

x2paddle_input = fluid.layers.data(dtype='float32',
                                   shape=[1, 3, 640, 640],
                                   name='x2paddle_input',
                                   append_batch_size=False)
x2paddle_1450 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1450',
                                              default_initializer=Constant(0.0))
x2paddle_1451 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1451',
                                              default_initializer=Constant(0.0))
x2paddle_1452 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1452',
                                              default_initializer=Constant(0.0))
x2paddle_1453 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1453',
                                              default_initializer=Constant(0.0))
x2paddle_1454 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1454',
                                              default_initializer=Constant(0.0))
x2paddle_1455 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1455',
                                              default_initializer=Constant(0.0))
x2paddle_1456 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1456',
                                              default_initializer=Constant(0.0))
x2paddle_1457 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1457',
                                              default_initializer=Constant(0.0))
x2paddle_1458 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1458',
                                              default_initializer=Constant(0.0))
x2paddle_1459 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1459',
                                              default_initializer=Constant(0.0))
x2paddle_1460 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1460',
                                              default_initializer=Constant(0.0))
x2paddle_1461 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1461',
                                              default_initializer=Constant(0.0))
x2paddle_model_0_conv_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[32],
    name='x2paddle_model_0_conv_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_0_conv_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[32],
    name='x2paddle_model_0_conv_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_0_conv_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[32],
    name='x2paddle_model_0_conv_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_0_conv_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[32],
    name='x2paddle_model_0_conv_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_0_conv_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[32, 12, 3, 3],
    name='x2paddle_model_0_conv_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_1_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_1_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_1_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_1_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_1_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_1_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_1_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_1_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_1_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64, 32, 3, 3],
    name='x2paddle_model_1_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_10_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512],
    name='x2paddle_model_10_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_10_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512],
    name='x2paddle_model_10_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_10_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512],
    name='x2paddle_model_10_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_10_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512],
    name='x2paddle_model_10_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_10_cv1_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_10_cv1_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_10_cv1_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_10_cv1_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_10_cv1_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_10_cv1_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_10_cv1_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_10_cv1_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_10_cv1_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256, 512, 1, 1],
    name='x2paddle_model_10_cv1_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_10_cv2_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256, 512, 1, 1],
    name='x2paddle_model_10_cv2_weight',
    default_initializer=Constant(0.0))
x2paddle_model_10_cv3_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256, 256, 1, 1],
    name='x2paddle_model_10_cv3_weight',
    default_initializer=Constant(0.0))
x2paddle_model_10_cv4_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512],
    name='x2paddle_model_10_cv4_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_10_cv4_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512],
    name='x2paddle_model_10_cv4_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_10_cv4_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512],
    name='x2paddle_model_10_cv4_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_10_cv4_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512],
    name='x2paddle_model_10_cv4_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_10_cv4_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512, 512, 1, 1],
    name='x2paddle_model_10_cv4_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_10_m_0_cv1_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_10_m_0_cv1_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_10_m_0_cv1_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_10_m_0_cv1_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_10_m_0_cv1_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_10_m_0_cv1_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_10_m_0_cv1_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_10_m_0_cv1_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_10_m_0_cv1_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256, 256, 1, 1],
    name='x2paddle_model_10_m_0_cv1_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_10_m_0_cv2_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_10_m_0_cv2_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_10_m_0_cv2_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_10_m_0_cv2_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_10_m_0_cv2_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_10_m_0_cv2_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_10_m_0_cv2_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_10_m_0_cv2_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_10_m_0_cv2_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256, 256, 3, 3],
    name='x2paddle_model_10_m_0_cv2_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_11_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[255],
    name='x2paddle_model_11_bias',
    default_initializer=Constant(0.0))
x2paddle_model_11_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[255, 512, 1, 1],
    name='x2paddle_model_11_weight',
    default_initializer=Constant(0.0))
x2paddle_model_14_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_14_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_14_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_14_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_14_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_14_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_14_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_14_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_14_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256, 768, 1, 1],
    name='x2paddle_model_14_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_15_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_15_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_15_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_15_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_15_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_15_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_15_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_15_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_15_cv1_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_15_cv1_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_15_cv1_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_15_cv1_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_15_cv1_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_15_cv1_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_15_cv1_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_15_cv1_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_15_cv1_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128, 256, 1, 1],
    name='x2paddle_model_15_cv1_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_15_cv2_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128, 256, 1, 1],
    name='x2paddle_model_15_cv2_weight',
    default_initializer=Constant(0.0))
x2paddle_model_15_cv3_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128, 128, 1, 1],
    name='x2paddle_model_15_cv3_weight',
    default_initializer=Constant(0.0))
x2paddle_model_15_cv4_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_15_cv4_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_15_cv4_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_15_cv4_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_15_cv4_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_15_cv4_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_15_cv4_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_15_cv4_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_15_cv4_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256, 256, 1, 1],
    name='x2paddle_model_15_cv4_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_15_m_0_cv1_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_15_m_0_cv1_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_15_m_0_cv1_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_15_m_0_cv1_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_15_m_0_cv1_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_15_m_0_cv1_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_15_m_0_cv1_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_15_m_0_cv1_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_15_m_0_cv1_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128, 128, 1, 1],
    name='x2paddle_model_15_m_0_cv1_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_15_m_0_cv2_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_15_m_0_cv2_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_15_m_0_cv2_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_15_m_0_cv2_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_15_m_0_cv2_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_15_m_0_cv2_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_15_m_0_cv2_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_15_m_0_cv2_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_15_m_0_cv2_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128, 128, 3, 3],
    name='x2paddle_model_15_m_0_cv2_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_16_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[255],
    name='x2paddle_model_16_bias',
    default_initializer=Constant(0.0))
x2paddle_model_16_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[255, 256, 1, 1],
    name='x2paddle_model_16_weight',
    default_initializer=Constant(0.0))
x2paddle_model_19_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_19_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_19_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_19_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_19_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_19_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_19_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_19_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_19_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128, 384, 1, 1],
    name='x2paddle_model_19_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_2_cv1_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[32],
    name='x2paddle_model_2_cv1_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_2_cv1_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[32],
    name='x2paddle_model_2_cv1_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_2_cv1_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[32],
    name='x2paddle_model_2_cv1_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_2_cv1_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[32],
    name='x2paddle_model_2_cv1_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_2_cv1_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[32, 64, 1, 1],
    name='x2paddle_model_2_cv1_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_2_cv2_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_2_cv2_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_2_cv2_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_2_cv2_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_2_cv2_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_2_cv2_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_2_cv2_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_2_cv2_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_2_cv2_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64, 32, 3, 3],
    name='x2paddle_model_2_cv2_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_20_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_20_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_20_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_20_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_20_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_20_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_20_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_20_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_20_cv1_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_20_cv1_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_20_cv1_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_20_cv1_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_20_cv1_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_20_cv1_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_20_cv1_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_20_cv1_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_20_cv1_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64, 128, 1, 1],
    name='x2paddle_model_20_cv1_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_20_cv2_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64, 128, 1, 1],
    name='x2paddle_model_20_cv2_weight',
    default_initializer=Constant(0.0))
x2paddle_model_20_cv3_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64, 64, 1, 1],
    name='x2paddle_model_20_cv3_weight',
    default_initializer=Constant(0.0))
x2paddle_model_20_cv4_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_20_cv4_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_20_cv4_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_20_cv4_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_20_cv4_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_20_cv4_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_20_cv4_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_20_cv4_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_20_cv4_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128, 128, 1, 1],
    name='x2paddle_model_20_cv4_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_20_m_0_cv1_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_20_m_0_cv1_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_20_m_0_cv1_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_20_m_0_cv1_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_20_m_0_cv1_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_20_m_0_cv1_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_20_m_0_cv1_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_20_m_0_cv1_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_20_m_0_cv1_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64, 64, 1, 1],
    name='x2paddle_model_20_m_0_cv1_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_20_m_0_cv2_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_20_m_0_cv2_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_20_m_0_cv2_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_20_m_0_cv2_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_20_m_0_cv2_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_20_m_0_cv2_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_20_m_0_cv2_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_20_m_0_cv2_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_20_m_0_cv2_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64, 64, 3, 3],
    name='x2paddle_model_20_m_0_cv2_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_21_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[255],
    name='x2paddle_model_21_bias',
    default_initializer=Constant(0.0))
x2paddle_model_21_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[255, 128, 1, 1],
    name='x2paddle_model_21_weight',
    default_initializer=Constant(0.0))
x2paddle_model_22_anchor_grid = fluid.layers.create_parameter(
    dtype='float32',
    shape=[3, 1, 3, 1, 1, 2],
    name='x2paddle_model_22_anchor_grid',
    default_initializer=Constant(0.0))
x2paddle_model_3_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_3_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_3_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_3_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_3_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_3_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_3_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_3_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_3_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128, 64, 3, 3],
    name='x2paddle_model_3_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_4_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_4_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_4_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_4_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_4_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_4_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_4_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_4_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_4_cv1_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_cv1_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_4_cv1_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_cv1_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_4_cv1_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_cv1_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_4_cv1_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_cv1_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_4_cv1_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64, 128, 1, 1],
    name='x2paddle_model_4_cv1_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_4_cv2_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64, 128, 1, 1],
    name='x2paddle_model_4_cv2_weight',
    default_initializer=Constant(0.0))
x2paddle_model_4_cv3_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64, 64, 1, 1],
    name='x2paddle_model_4_cv3_weight',
    default_initializer=Constant(0.0))
x2paddle_model_4_cv4_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_4_cv4_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_4_cv4_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_4_cv4_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_4_cv4_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_4_cv4_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_4_cv4_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_4_cv4_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_4_cv4_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128, 128, 1, 1],
    name='x2paddle_model_4_cv4_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_0_cv1_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_m_0_cv1_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_0_cv1_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_m_0_cv1_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_0_cv1_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_m_0_cv1_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_0_cv1_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_m_0_cv1_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_0_cv1_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64, 64, 1, 1],
    name='x2paddle_model_4_m_0_cv1_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_0_cv2_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_m_0_cv2_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_0_cv2_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_m_0_cv2_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_0_cv2_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_m_0_cv2_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_0_cv2_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_m_0_cv2_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_0_cv2_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64, 64, 3, 3],
    name='x2paddle_model_4_m_0_cv2_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_1_cv1_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_m_1_cv1_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_1_cv1_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_m_1_cv1_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_1_cv1_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_m_1_cv1_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_1_cv1_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_m_1_cv1_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_1_cv1_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64, 64, 1, 1],
    name='x2paddle_model_4_m_1_cv1_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_1_cv2_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_m_1_cv2_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_1_cv2_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_m_1_cv2_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_1_cv2_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_m_1_cv2_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_1_cv2_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_m_1_cv2_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_1_cv2_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64, 64, 3, 3],
    name='x2paddle_model_4_m_1_cv2_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_2_cv1_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_m_2_cv1_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_2_cv1_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_m_2_cv1_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_2_cv1_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_m_2_cv1_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_2_cv1_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_m_2_cv1_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_2_cv1_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64, 64, 1, 1],
    name='x2paddle_model_4_m_2_cv1_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_2_cv2_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_m_2_cv2_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_2_cv2_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_m_2_cv2_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_2_cv2_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_m_2_cv2_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_2_cv2_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64],
    name='x2paddle_model_4_m_2_cv2_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_4_m_2_cv2_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[64, 64, 3, 3],
    name='x2paddle_model_4_m_2_cv2_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_5_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_5_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_5_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_5_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_5_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_5_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_5_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_5_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_5_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256, 128, 3, 3],
    name='x2paddle_model_5_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_6_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_6_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_6_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_6_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_6_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_6_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_6_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_6_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_6_cv1_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_cv1_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_6_cv1_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_cv1_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_6_cv1_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_cv1_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_6_cv1_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_cv1_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_6_cv1_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128, 256, 1, 1],
    name='x2paddle_model_6_cv1_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_6_cv2_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128, 256, 1, 1],
    name='x2paddle_model_6_cv2_weight',
    default_initializer=Constant(0.0))
x2paddle_model_6_cv3_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128, 128, 1, 1],
    name='x2paddle_model_6_cv3_weight',
    default_initializer=Constant(0.0))
x2paddle_model_6_cv4_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_6_cv4_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_6_cv4_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_6_cv4_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_6_cv4_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_6_cv4_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_6_cv4_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_6_cv4_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_6_cv4_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256, 256, 1, 1],
    name='x2paddle_model_6_cv4_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_0_cv1_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_m_0_cv1_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_0_cv1_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_m_0_cv1_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_0_cv1_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_m_0_cv1_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_0_cv1_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_m_0_cv1_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_0_cv1_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128, 128, 1, 1],
    name='x2paddle_model_6_m_0_cv1_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_0_cv2_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_m_0_cv2_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_0_cv2_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_m_0_cv2_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_0_cv2_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_m_0_cv2_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_0_cv2_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_m_0_cv2_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_0_cv2_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128, 128, 3, 3],
    name='x2paddle_model_6_m_0_cv2_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_1_cv1_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_m_1_cv1_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_1_cv1_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_m_1_cv1_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_1_cv1_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_m_1_cv1_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_1_cv1_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_m_1_cv1_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_1_cv1_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128, 128, 1, 1],
    name='x2paddle_model_6_m_1_cv1_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_1_cv2_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_m_1_cv2_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_1_cv2_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_m_1_cv2_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_1_cv2_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_m_1_cv2_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_1_cv2_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_m_1_cv2_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_1_cv2_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128, 128, 3, 3],
    name='x2paddle_model_6_m_1_cv2_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_2_cv1_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_m_2_cv1_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_2_cv1_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_m_2_cv1_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_2_cv1_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_m_2_cv1_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_2_cv1_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_m_2_cv1_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_2_cv1_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128, 128, 1, 1],
    name='x2paddle_model_6_m_2_cv1_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_2_cv2_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_m_2_cv2_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_2_cv2_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_m_2_cv2_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_2_cv2_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_m_2_cv2_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_2_cv2_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128],
    name='x2paddle_model_6_m_2_cv2_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_6_m_2_cv2_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[128, 128, 3, 3],
    name='x2paddle_model_6_m_2_cv2_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_7_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512],
    name='x2paddle_model_7_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_7_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512],
    name='x2paddle_model_7_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_7_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512],
    name='x2paddle_model_7_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_7_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512],
    name='x2paddle_model_7_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_7_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512, 256, 3, 3],
    name='x2paddle_model_7_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_8_cv1_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_8_cv1_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_8_cv1_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_8_cv1_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_8_cv1_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_8_cv1_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_8_cv1_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_8_cv1_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_8_cv1_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256, 512, 1, 1],
    name='x2paddle_model_8_cv1_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_8_cv2_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512],
    name='x2paddle_model_8_cv2_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_8_cv2_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512],
    name='x2paddle_model_8_cv2_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_8_cv2_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512],
    name='x2paddle_model_8_cv2_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_8_cv2_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512],
    name='x2paddle_model_8_cv2_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_8_cv2_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512, 1024, 1, 1],
    name='x2paddle_model_8_cv2_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_9_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512],
    name='x2paddle_model_9_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_9_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512],
    name='x2paddle_model_9_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_9_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512],
    name='x2paddle_model_9_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_9_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512],
    name='x2paddle_model_9_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_9_cv1_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_9_cv1_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_9_cv1_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_9_cv1_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_9_cv1_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_9_cv1_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_9_cv1_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_9_cv1_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_9_cv1_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256, 512, 1, 1],
    name='x2paddle_model_9_cv1_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_9_cv2_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256, 512, 1, 1],
    name='x2paddle_model_9_cv2_weight',
    default_initializer=Constant(0.0))
x2paddle_model_9_cv3_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256, 256, 1, 1],
    name='x2paddle_model_9_cv3_weight',
    default_initializer=Constant(0.0))
x2paddle_model_9_cv4_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512],
    name='x2paddle_model_9_cv4_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_9_cv4_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512],
    name='x2paddle_model_9_cv4_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_9_cv4_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512],
    name='x2paddle_model_9_cv4_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_9_cv4_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512],
    name='x2paddle_model_9_cv4_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_9_cv4_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[512, 512, 1, 1],
    name='x2paddle_model_9_cv4_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_9_m_0_cv1_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_9_m_0_cv1_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_9_m_0_cv1_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_9_m_0_cv1_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_9_m_0_cv1_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_9_m_0_cv1_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_9_m_0_cv1_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_9_m_0_cv1_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_9_m_0_cv1_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256, 256, 1, 1],
    name='x2paddle_model_9_m_0_cv1_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_9_m_0_cv2_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_9_m_0_cv2_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_9_m_0_cv2_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_9_m_0_cv2_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_9_m_0_cv2_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_9_m_0_cv2_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_9_m_0_cv2_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_9_m_0_cv2_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_9_m_0_cv2_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256, 256, 3, 3],
    name='x2paddle_model_9_m_0_cv2_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_9_m_1_cv1_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_9_m_1_cv1_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_9_m_1_cv1_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_9_m_1_cv1_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_9_m_1_cv1_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_9_m_1_cv1_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_9_m_1_cv1_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_9_m_1_cv1_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_9_m_1_cv1_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256, 256, 1, 1],
    name='x2paddle_model_9_m_1_cv1_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_model_9_m_1_cv2_bn_bias = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_9_m_1_cv2_bn_bias',
    default_initializer=Constant(0.0))
x2paddle_model_9_m_1_cv2_bn_running_mean = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_9_m_1_cv2_bn_running_mean',
    default_initializer=Constant(0.0))
x2paddle_model_9_m_1_cv2_bn_running_var = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_9_m_1_cv2_bn_running_var',
    default_initializer=Constant(0.0))
x2paddle_model_9_m_1_cv2_bn_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256],
    name='x2paddle_model_9_m_1_cv2_bn_weight',
    default_initializer=Constant(0.0))
x2paddle_model_9_m_1_cv2_conv_weight = fluid.layers.create_parameter(
    dtype='float32',
    shape=[256, 256, 3, 3],
    name='x2paddle_model_9_m_1_cv2_conv_weight',
    default_initializer=Constant(0.0))
x2paddle_321 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_321',
                                             default_initializer=Constant(0.0))
x2paddle_322 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_322',
                                             default_initializer=Constant(0.0))
x2paddle_323 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_323',
                                             default_initializer=Constant(0.0))
x2paddle_324 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_324',
                                             default_initializer=Constant(0.0))
x2paddle_326 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_326',
                                             default_initializer=Constant(0.0))
x2paddle_327 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_327',
                                             default_initializer=Constant(0.0))
x2paddle_328 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_328',
                                             default_initializer=Constant(0.0))
x2paddle_329 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_329',
                                             default_initializer=Constant(0.0))
x2paddle_331 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_331',
                                             default_initializer=Constant(0.0))
x2paddle_332 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_332',
                                             default_initializer=Constant(0.0))
x2paddle_333 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_333',
                                             default_initializer=Constant(0.0))
x2paddle_334 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_334',
                                             default_initializer=Constant(0.0))
x2paddle_336 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_336',
                                             default_initializer=Constant(0.0))
x2paddle_337 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_337',
                                             default_initializer=Constant(0.0))
x2paddle_338 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_338',
                                             default_initializer=Constant(0.0))
x2paddle_339 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_339',
                                             default_initializer=Constant(0.0))
x2paddle_341 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_341',
                                             default_initializer=Constant(0.0))
x2paddle_342 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_342',
                                             default_initializer=Constant(0.0))
x2paddle_343 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_343',
                                             default_initializer=Constant(0.0))
x2paddle_344 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_344',
                                             default_initializer=Constant(0.0))
x2paddle_346 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_346',
                                             default_initializer=Constant(0.0))
x2paddle_347 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_347',
                                             default_initializer=Constant(0.0))
x2paddle_348 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_348',
                                             default_initializer=Constant(0.0))
x2paddle_349 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_349',
                                             default_initializer=Constant(0.0))
x2paddle_351 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_351',
                                             default_initializer=Constant(0.0))
x2paddle_352 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_352',
                                             default_initializer=Constant(0.0))
x2paddle_353 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_353',
                                             default_initializer=Constant(0.0))
x2paddle_354 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_354',
                                             default_initializer=Constant(0.0))
x2paddle_356 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_356',
                                             default_initializer=Constant(0.0))
x2paddle_357 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_357',
                                             default_initializer=Constant(0.0))
x2paddle_358 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_358',
                                             default_initializer=Constant(0.0))
x2paddle_359 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_359',
                                             default_initializer=Constant(0.0))
x2paddle_502 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_502',
                                             default_initializer=Constant(0.0))
x2paddle_505 = fluid.layers.create_parameter(dtype='float32',
                                             shape=[1],
                                             name='x2paddle_505',
                                             default_initializer=Constant(0.0))
x2paddle_510 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_510',
                                             default_initializer=Constant(0.0))
x2paddle_513 = fluid.layers.create_parameter(dtype='float32',
                                             shape=[1],
                                             name='x2paddle_513',
                                             default_initializer=Constant(0.0))
x2paddle_520 = fluid.layers.create_parameter(dtype='float32',
                                             shape=[0],
                                             name='x2paddle_520',
                                             default_initializer=Constant(0.0))
x2paddle_522 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_522',
                                             default_initializer=Constant(0.0))
x2paddle_523 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_523',
                                             default_initializer=Constant(0.0))
x2paddle_524 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_524',
                                             default_initializer=Constant(0.0))
x2paddle_528 = fluid.layers.create_parameter(dtype='float32',
                                             shape=[0],
                                             name='x2paddle_528',
                                             default_initializer=Constant(0.0))
x2paddle_553 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_553',
                                             default_initializer=Constant(0.0))
x2paddle_556 = fluid.layers.create_parameter(dtype='float32',
                                             shape=[1],
                                             name='x2paddle_556',
                                             default_initializer=Constant(0.0))
x2paddle_561 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_561',
                                             default_initializer=Constant(0.0))
x2paddle_564 = fluid.layers.create_parameter(dtype='float32',
                                             shape=[1],
                                             name='x2paddle_564',
                                             default_initializer=Constant(0.0))
x2paddle_571 = fluid.layers.create_parameter(dtype='float32',
                                             shape=[0],
                                             name='x2paddle_571',
                                             default_initializer=Constant(0.0))
x2paddle_573 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_573',
                                             default_initializer=Constant(0.0))
x2paddle_574 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_574',
                                             default_initializer=Constant(0.0))
x2paddle_575 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_575',
                                             default_initializer=Constant(0.0))
x2paddle_579 = fluid.layers.create_parameter(dtype='float32',
                                             shape=[0],
                                             name='x2paddle_579',
                                             default_initializer=Constant(0.0))
x2paddle_604 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_604',
                                             default_initializer=Constant(0.0))
x2paddle_607 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_607',
                                             default_initializer=Constant(0.0))
x2paddle_610 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_610',
                                             default_initializer=Constant(0.0))
x2paddle_623 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_623',
                                             default_initializer=Constant(0.0))
x2paddle_624 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_624',
                                             default_initializer=Constant(0.0))
x2paddle_625 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_625',
                                             default_initializer=Constant(0.0))
x2paddle_626 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_626',
                                             default_initializer=Constant(0.0))
x2paddle_628 = fluid.layers.create_parameter(dtype='float32',
                                             shape=[1],
                                             name='x2paddle_628',
                                             default_initializer=Constant(0.0))
x2paddle_630 = fluid.layers.create_parameter(dtype='float32',
                                             shape=[1],
                                             name='x2paddle_630',
                                             default_initializer=Constant(0.0))
x2paddle_632 = fluid.layers.create_parameter(dtype='float32',
                                             shape=[1, 1, 80, 80, 2],
                                             name='x2paddle_632',
                                             default_initializer=Constant(0.0))
x2paddle_634 = fluid.layers.create_parameter(dtype='float32',
                                             shape=[1],
                                             name='x2paddle_634',
                                             default_initializer=Constant(0.0))
x2paddle_636 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[4],
                                             name='x2paddle_636',
                                             default_initializer=Constant(0.0))
x2paddle_638 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[5],
                                             name='x2paddle_638',
                                             default_initializer=Constant(0.0))
x2paddle_641 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_641',
                                             default_initializer=Constant(0.0))
x2paddle_643 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[5],
                                             name='x2paddle_643',
                                             default_initializer=Constant(0.0))
x2paddle_648 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_648',
                                             default_initializer=Constant(0.0))
x2paddle_651 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_651',
                                             default_initializer=Constant(0.0))
x2paddle_652 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_652',
                                             default_initializer=Constant(0.0))
x2paddle_655 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_655',
                                             default_initializer=Constant(0.0))
x2paddle_658 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_658',
                                             default_initializer=Constant(0.0))
x2paddle_659 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_659',
                                             default_initializer=Constant(0.0))
x2paddle_662 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_662',
                                             default_initializer=Constant(0.0))
x2paddle_665 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_665',
                                             default_initializer=Constant(0.0))
x2paddle_666 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_666',
                                             default_initializer=Constant(0.0))
x2paddle_669 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_669',
                                             default_initializer=Constant(0.0))
x2paddle_672 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_672',
                                             default_initializer=Constant(0.0))
x2paddle_673 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_673',
                                             default_initializer=Constant(0.0))
x2paddle_676 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_676',
                                             default_initializer=Constant(0.0))
x2paddle_679 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_679',
                                             default_initializer=Constant(0.0))
x2paddle_680 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_680',
                                             default_initializer=Constant(0.0))
x2paddle_682 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_682',
                                             default_initializer=Constant(0.0))
x2paddle_683 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_683',
                                             default_initializer=Constant(0.0))
x2paddle_684 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_684',
                                             default_initializer=Constant(0.0))
x2paddle_685 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_685',
                                             default_initializer=Constant(0.0))
x2paddle_687 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[5],
                                             name='x2paddle_687',
                                             default_initializer=Constant(0.0))
x2paddle_689 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[4],
                                             name='x2paddle_689',
                                             default_initializer=Constant(0.0))
x2paddle_691 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[3],
                                             name='x2paddle_691',
                                             default_initializer=Constant(0.0))
x2paddle_693 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[2],
                                             name='x2paddle_693',
                                             default_initializer=Constant(0.0))
x2paddle_695 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_695',
                                             default_initializer=Constant(0.0))
x2paddle_704 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_704',
                                             default_initializer=Constant(0.0))
x2paddle_712 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_712',
                                             default_initializer=Constant(0.0))
x2paddle_720 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_720',
                                             default_initializer=Constant(0.0))
x2paddle_728 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_728',
                                             default_initializer=Constant(0.0))
x2paddle_736 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_736',
                                             default_initializer=Constant(0.0))
x2paddle_744 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_744',
                                             default_initializer=Constant(0.0))
x2paddle_745 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_745',
                                             default_initializer=Constant(0.0))
x2paddle_746 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_746',
                                             default_initializer=Constant(0.0))
x2paddle_751 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_751',
                                             default_initializer=Constant(0.0))
x2paddle_752 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_752',
                                             default_initializer=Constant(0.0))
x2paddle_753 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_753',
                                             default_initializer=Constant(0.0))
x2paddle_754 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_754',
                                             default_initializer=Constant(0.0))
x2paddle_756 = fluid.layers.create_parameter(dtype='float32',
                                             shape=[1],
                                             name='x2paddle_756',
                                             default_initializer=Constant(0.0))
x2paddle_758 = fluid.layers.create_parameter(dtype='float32',
                                             shape=[1],
                                             name='x2paddle_758',
                                             default_initializer=Constant(0.0))
x2paddle_760 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_760',
                                             default_initializer=Constant(0.0))
x2paddle_763 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[4],
                                             name='x2paddle_763',
                                             default_initializer=Constant(0.0))
x2paddle_765 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[5],
                                             name='x2paddle_765',
                                             default_initializer=Constant(0.0))
x2paddle_768 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_768',
                                             default_initializer=Constant(0.0))
x2paddle_770 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[5],
                                             name='x2paddle_770',
                                             default_initializer=Constant(0.0))
x2paddle_775 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_775',
                                             default_initializer=Constant(0.0))
x2paddle_778 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_778',
                                             default_initializer=Constant(0.0))
x2paddle_779 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_779',
                                             default_initializer=Constant(0.0))
x2paddle_782 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_782',
                                             default_initializer=Constant(0.0))
x2paddle_785 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_785',
                                             default_initializer=Constant(0.0))
x2paddle_786 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_786',
                                             default_initializer=Constant(0.0))
x2paddle_789 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_789',
                                             default_initializer=Constant(0.0))
x2paddle_792 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_792',
                                             default_initializer=Constant(0.0))
x2paddle_793 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_793',
                                             default_initializer=Constant(0.0))
x2paddle_796 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_796',
                                             default_initializer=Constant(0.0))
x2paddle_799 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_799',
                                             default_initializer=Constant(0.0))
x2paddle_800 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_800',
                                             default_initializer=Constant(0.0))
x2paddle_803 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_803',
                                             default_initializer=Constant(0.0))
x2paddle_806 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_806',
                                             default_initializer=Constant(0.0))
x2paddle_807 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_807',
                                             default_initializer=Constant(0.0))
x2paddle_809 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_809',
                                             default_initializer=Constant(0.0))
x2paddle_810 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_810',
                                             default_initializer=Constant(0.0))
x2paddle_811 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_811',
                                             default_initializer=Constant(0.0))
x2paddle_812 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_812',
                                             default_initializer=Constant(0.0))
x2paddle_814 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[5],
                                             name='x2paddle_814',
                                             default_initializer=Constant(0.0))
x2paddle_816 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[4],
                                             name='x2paddle_816',
                                             default_initializer=Constant(0.0))
x2paddle_818 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[3],
                                             name='x2paddle_818',
                                             default_initializer=Constant(0.0))
x2paddle_820 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[2],
                                             name='x2paddle_820',
                                             default_initializer=Constant(0.0))
x2paddle_822 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_822',
                                             default_initializer=Constant(0.0))
x2paddle_831 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_831',
                                             default_initializer=Constant(0.0))
x2paddle_839 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_839',
                                             default_initializer=Constant(0.0))
x2paddle_847 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_847',
                                             default_initializer=Constant(0.0))
x2paddle_855 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_855',
                                             default_initializer=Constant(0.0))
x2paddle_863 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_863',
                                             default_initializer=Constant(0.0))
x2paddle_871 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_871',
                                             default_initializer=Constant(0.0))
x2paddle_872 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_872',
                                             default_initializer=Constant(0.0))
x2paddle_873 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_873',
                                             default_initializer=Constant(0.0))
x2paddle_886 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_886',
                                             default_initializer=Constant(0.0))
x2paddle_889 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_889',
                                             default_initializer=Constant(0.0))
x2paddle_892 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_892',
                                             default_initializer=Constant(0.0))
x2paddle_905 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_905',
                                             default_initializer=Constant(0.0))
x2paddle_906 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_906',
                                             default_initializer=Constant(0.0))
x2paddle_907 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_907',
                                             default_initializer=Constant(0.0))
x2paddle_908 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_908',
                                             default_initializer=Constant(0.0))
x2paddle_910 = fluid.layers.create_parameter(dtype='float32',
                                             shape=[1],
                                             name='x2paddle_910',
                                             default_initializer=Constant(0.0))
x2paddle_912 = fluid.layers.create_parameter(dtype='float32',
                                             shape=[1],
                                             name='x2paddle_912',
                                             default_initializer=Constant(0.0))
x2paddle_914 = fluid.layers.create_parameter(dtype='float32',
                                             shape=[1, 1, 40, 40, 2],
                                             name='x2paddle_914',
                                             default_initializer=Constant(0.0))
x2paddle_916 = fluid.layers.create_parameter(dtype='float32',
                                             shape=[1],
                                             name='x2paddle_916',
                                             default_initializer=Constant(0.0))
x2paddle_918 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[4],
                                             name='x2paddle_918',
                                             default_initializer=Constant(0.0))
x2paddle_920 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[5],
                                             name='x2paddle_920',
                                             default_initializer=Constant(0.0))
x2paddle_923 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_923',
                                             default_initializer=Constant(0.0))
x2paddle_925 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[5],
                                             name='x2paddle_925',
                                             default_initializer=Constant(0.0))
x2paddle_930 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_930',
                                             default_initializer=Constant(0.0))
x2paddle_933 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_933',
                                             default_initializer=Constant(0.0))
x2paddle_934 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_934',
                                             default_initializer=Constant(0.0))
x2paddle_937 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_937',
                                             default_initializer=Constant(0.0))
x2paddle_940 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_940',
                                             default_initializer=Constant(0.0))
x2paddle_941 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_941',
                                             default_initializer=Constant(0.0))
x2paddle_944 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_944',
                                             default_initializer=Constant(0.0))
x2paddle_947 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_947',
                                             default_initializer=Constant(0.0))
x2paddle_948 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_948',
                                             default_initializer=Constant(0.0))
x2paddle_951 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_951',
                                             default_initializer=Constant(0.0))
x2paddle_954 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_954',
                                             default_initializer=Constant(0.0))
x2paddle_955 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_955',
                                             default_initializer=Constant(0.0))
x2paddle_958 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_958',
                                             default_initializer=Constant(0.0))
x2paddle_961 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_961',
                                             default_initializer=Constant(0.0))
x2paddle_962 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_962',
                                             default_initializer=Constant(0.0))
x2paddle_964 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_964',
                                             default_initializer=Constant(0.0))
x2paddle_965 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_965',
                                             default_initializer=Constant(0.0))
x2paddle_966 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_966',
                                             default_initializer=Constant(0.0))
x2paddle_967 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_967',
                                             default_initializer=Constant(0.0))
x2paddle_969 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[5],
                                             name='x2paddle_969',
                                             default_initializer=Constant(0.0))
x2paddle_971 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[4],
                                             name='x2paddle_971',
                                             default_initializer=Constant(0.0))
x2paddle_973 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[3],
                                             name='x2paddle_973',
                                             default_initializer=Constant(0.0))
x2paddle_975 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[2],
                                             name='x2paddle_975',
                                             default_initializer=Constant(0.0))
x2paddle_977 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_977',
                                             default_initializer=Constant(0.0))
x2paddle_986 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_986',
                                             default_initializer=Constant(0.0))
x2paddle_994 = fluid.layers.create_parameter(dtype='int64',
                                             shape=[1],
                                             name='x2paddle_994',
                                             default_initializer=Constant(0.0))
x2paddle_1002 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1002',
                                              default_initializer=Constant(0.0))
x2paddle_1010 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1010',
                                              default_initializer=Constant(0.0))
x2paddle_1018 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1018',
                                              default_initializer=Constant(0.0))
x2paddle_1026 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1026',
                                              default_initializer=Constant(0.0))
x2paddle_1027 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1027',
                                              default_initializer=Constant(0.0))
x2paddle_1028 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1028',
                                              default_initializer=Constant(0.0))
x2paddle_1033 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1033',
                                              default_initializer=Constant(0.0))
x2paddle_1034 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1034',
                                              default_initializer=Constant(0.0))
x2paddle_1035 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1035',
                                              default_initializer=Constant(0.0))
x2paddle_1036 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1036',
                                              default_initializer=Constant(0.0))
x2paddle_1038 = fluid.layers.create_parameter(dtype='float32',
                                              shape=[1],
                                              name='x2paddle_1038',
                                              default_initializer=Constant(0.0))
x2paddle_1040 = fluid.layers.create_parameter(dtype='float32',
                                              shape=[1],
                                              name='x2paddle_1040',
                                              default_initializer=Constant(0.0))
x2paddle_1042 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1042',
                                              default_initializer=Constant(0.0))
x2paddle_1045 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[4],
                                              name='x2paddle_1045',
                                              default_initializer=Constant(0.0))
x2paddle_1047 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[5],
                                              name='x2paddle_1047',
                                              default_initializer=Constant(0.0))
x2paddle_1050 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1050',
                                              default_initializer=Constant(0.0))
x2paddle_1052 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[5],
                                              name='x2paddle_1052',
                                              default_initializer=Constant(0.0))
x2paddle_1057 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1057',
                                              default_initializer=Constant(0.0))
x2paddle_1060 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1060',
                                              default_initializer=Constant(0.0))
x2paddle_1061 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1061',
                                              default_initializer=Constant(0.0))
x2paddle_1064 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1064',
                                              default_initializer=Constant(0.0))
x2paddle_1067 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1067',
                                              default_initializer=Constant(0.0))
x2paddle_1068 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1068',
                                              default_initializer=Constant(0.0))
x2paddle_1071 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1071',
                                              default_initializer=Constant(0.0))
x2paddle_1074 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1074',
                                              default_initializer=Constant(0.0))
x2paddle_1075 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1075',
                                              default_initializer=Constant(0.0))
x2paddle_1078 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1078',
                                              default_initializer=Constant(0.0))
x2paddle_1081 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1081',
                                              default_initializer=Constant(0.0))
x2paddle_1082 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1082',
                                              default_initializer=Constant(0.0))
x2paddle_1085 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1085',
                                              default_initializer=Constant(0.0))
x2paddle_1088 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1088',
                                              default_initializer=Constant(0.0))
x2paddle_1089 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1089',
                                              default_initializer=Constant(0.0))
x2paddle_1091 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1091',
                                              default_initializer=Constant(0.0))
x2paddle_1092 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1092',
                                              default_initializer=Constant(0.0))
x2paddle_1093 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1093',
                                              default_initializer=Constant(0.0))
x2paddle_1094 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1094',
                                              default_initializer=Constant(0.0))
x2paddle_1096 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[5],
                                              name='x2paddle_1096',
                                              default_initializer=Constant(0.0))
x2paddle_1098 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[4],
                                              name='x2paddle_1098',
                                              default_initializer=Constant(0.0))
x2paddle_1100 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[3],
                                              name='x2paddle_1100',
                                              default_initializer=Constant(0.0))
x2paddle_1102 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[2],
                                              name='x2paddle_1102',
                                              default_initializer=Constant(0.0))
x2paddle_1104 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1104',
                                              default_initializer=Constant(0.0))
x2paddle_1113 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1113',
                                              default_initializer=Constant(0.0))
x2paddle_1121 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1121',
                                              default_initializer=Constant(0.0))
x2paddle_1129 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1129',
                                              default_initializer=Constant(0.0))
x2paddle_1137 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1137',
                                              default_initializer=Constant(0.0))
x2paddle_1145 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1145',
                                              default_initializer=Constant(0.0))
x2paddle_1153 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1153',
                                              default_initializer=Constant(0.0))
x2paddle_1154 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1154',
                                              default_initializer=Constant(0.0))
x2paddle_1155 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1155',
                                              default_initializer=Constant(0.0))
x2paddle_1168 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1168',
                                              default_initializer=Constant(0.0))
x2paddle_1171 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1171',
                                              default_initializer=Constant(0.0))
x2paddle_1174 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1174',
                                              default_initializer=Constant(0.0))
x2paddle_1187 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1187',
                                              default_initializer=Constant(0.0))
x2paddle_1188 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1188',
                                              default_initializer=Constant(0.0))
x2paddle_1189 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1189',
                                              default_initializer=Constant(0.0))
x2paddle_1190 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1190',
                                              default_initializer=Constant(0.0))
x2paddle_1192 = fluid.layers.create_parameter(dtype='float32',
                                              shape=[1],
                                              name='x2paddle_1192',
                                              default_initializer=Constant(0.0))
x2paddle_1194 = fluid.layers.create_parameter(dtype='float32',
                                              shape=[1],
                                              name='x2paddle_1194',
                                              default_initializer=Constant(0.0))
x2paddle_1196 = fluid.layers.create_parameter(dtype='float32',
                                              shape=[1, 1, 20, 20, 2],
                                              name='x2paddle_1196',
                                              default_initializer=Constant(0.0))
x2paddle_1198 = fluid.layers.create_parameter(dtype='float32',
                                              shape=[1],
                                              name='x2paddle_1198',
                                              default_initializer=Constant(0.0))
x2paddle_1200 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[4],
                                              name='x2paddle_1200',
                                              default_initializer=Constant(0.0))
x2paddle_1202 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[5],
                                              name='x2paddle_1202',
                                              default_initializer=Constant(0.0))
x2paddle_1205 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1205',
                                              default_initializer=Constant(0.0))
x2paddle_1207 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[5],
                                              name='x2paddle_1207',
                                              default_initializer=Constant(0.0))
x2paddle_1212 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1212',
                                              default_initializer=Constant(0.0))
x2paddle_1215 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1215',
                                              default_initializer=Constant(0.0))
x2paddle_1216 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1216',
                                              default_initializer=Constant(0.0))
x2paddle_1219 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1219',
                                              default_initializer=Constant(0.0))
x2paddle_1222 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1222',
                                              default_initializer=Constant(0.0))
x2paddle_1223 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1223',
                                              default_initializer=Constant(0.0))
x2paddle_1226 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1226',
                                              default_initializer=Constant(0.0))
x2paddle_1229 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1229',
                                              default_initializer=Constant(0.0))
x2paddle_1230 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1230',
                                              default_initializer=Constant(0.0))
x2paddle_1233 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1233',
                                              default_initializer=Constant(0.0))
x2paddle_1236 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1236',
                                              default_initializer=Constant(0.0))
x2paddle_1237 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1237',
                                              default_initializer=Constant(0.0))
x2paddle_1240 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1240',
                                              default_initializer=Constant(0.0))
x2paddle_1243 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1243',
                                              default_initializer=Constant(0.0))
x2paddle_1244 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1244',
                                              default_initializer=Constant(0.0))
x2paddle_1246 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1246',
                                              default_initializer=Constant(0.0))
x2paddle_1247 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1247',
                                              default_initializer=Constant(0.0))
x2paddle_1248 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1248',
                                              default_initializer=Constant(0.0))
x2paddle_1249 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1249',
                                              default_initializer=Constant(0.0))
x2paddle_1251 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[5],
                                              name='x2paddle_1251',
                                              default_initializer=Constant(0.0))
x2paddle_1253 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[4],
                                              name='x2paddle_1253',
                                              default_initializer=Constant(0.0))
x2paddle_1255 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[3],
                                              name='x2paddle_1255',
                                              default_initializer=Constant(0.0))
x2paddle_1257 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[2],
                                              name='x2paddle_1257',
                                              default_initializer=Constant(0.0))
x2paddle_1259 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1259',
                                              default_initializer=Constant(0.0))
x2paddle_1268 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1268',
                                              default_initializer=Constant(0.0))
x2paddle_1276 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1276',
                                              default_initializer=Constant(0.0))
x2paddle_1284 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1284',
                                              default_initializer=Constant(0.0))
x2paddle_1292 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1292',
                                              default_initializer=Constant(0.0))
x2paddle_1300 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1300',
                                              default_initializer=Constant(0.0))
x2paddle_1308 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1308',
                                              default_initializer=Constant(0.0))
x2paddle_1309 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1309',
                                              default_initializer=Constant(0.0))
x2paddle_1310 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1310',
                                              default_initializer=Constant(0.0))
x2paddle_1315 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1315',
                                              default_initializer=Constant(0.0))
x2paddle_1316 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1316',
                                              default_initializer=Constant(0.0))
x2paddle_1317 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1317',
                                              default_initializer=Constant(0.0))
x2paddle_1318 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1318',
                                              default_initializer=Constant(0.0))
x2paddle_1320 = fluid.layers.create_parameter(dtype='float32',
                                              shape=[1],
                                              name='x2paddle_1320',
                                              default_initializer=Constant(0.0))
x2paddle_1322 = fluid.layers.create_parameter(dtype='float32',
                                              shape=[1],
                                              name='x2paddle_1322',
                                              default_initializer=Constant(0.0))
x2paddle_1324 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1324',
                                              default_initializer=Constant(0.0))
x2paddle_1327 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[4],
                                              name='x2paddle_1327',
                                              default_initializer=Constant(0.0))
x2paddle_1329 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[5],
                                              name='x2paddle_1329',
                                              default_initializer=Constant(0.0))
x2paddle_1332 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1332',
                                              default_initializer=Constant(0.0))
x2paddle_1334 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[5],
                                              name='x2paddle_1334',
                                              default_initializer=Constant(0.0))
x2paddle_1339 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1339',
                                              default_initializer=Constant(0.0))
x2paddle_1342 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1342',
                                              default_initializer=Constant(0.0))
x2paddle_1343 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1343',
                                              default_initializer=Constant(0.0))
x2paddle_1346 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1346',
                                              default_initializer=Constant(0.0))
x2paddle_1349 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1349',
                                              default_initializer=Constant(0.0))
x2paddle_1350 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1350',
                                              default_initializer=Constant(0.0))
x2paddle_1353 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1353',
                                              default_initializer=Constant(0.0))
x2paddle_1356 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1356',
                                              default_initializer=Constant(0.0))
x2paddle_1357 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1357',
                                              default_initializer=Constant(0.0))
x2paddle_1360 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1360',
                                              default_initializer=Constant(0.0))
x2paddle_1363 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1363',
                                              default_initializer=Constant(0.0))
x2paddle_1364 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1364',
                                              default_initializer=Constant(0.0))
x2paddle_1367 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1367',
                                              default_initializer=Constant(0.0))
x2paddle_1370 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1370',
                                              default_initializer=Constant(0.0))
x2paddle_1371 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1371',
                                              default_initializer=Constant(0.0))
x2paddle_1373 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1373',
                                              default_initializer=Constant(0.0))
x2paddle_1374 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1374',
                                              default_initializer=Constant(0.0))
x2paddle_1375 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1375',
                                              default_initializer=Constant(0.0))
x2paddle_1376 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1376',
                                              default_initializer=Constant(0.0))
x2paddle_1378 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[5],
                                              name='x2paddle_1378',
                                              default_initializer=Constant(0.0))
x2paddle_1380 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[4],
                                              name='x2paddle_1380',
                                              default_initializer=Constant(0.0))
x2paddle_1382 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[3],
                                              name='x2paddle_1382',
                                              default_initializer=Constant(0.0))
x2paddle_1384 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[2],
                                              name='x2paddle_1384',
                                              default_initializer=Constant(0.0))
x2paddle_1386 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1386',
                                              default_initializer=Constant(0.0))
x2paddle_1395 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1395',
                                              default_initializer=Constant(0.0))
x2paddle_1403 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1403',
                                              default_initializer=Constant(0.0))
x2paddle_1411 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1411',
                                              default_initializer=Constant(0.0))
x2paddle_1419 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1419',
                                              default_initializer=Constant(0.0))
x2paddle_1427 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1427',
                                              default_initializer=Constant(0.0))
x2paddle_1435 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1435',
                                              default_initializer=Constant(0.0))
x2paddle_1436 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1436',
                                              default_initializer=Constant(0.0))
x2paddle_1437 = fluid.layers.create_parameter(dtype='int64',
                                              shape=[1],
                                              name='x2paddle_1437',
                                              default_initializer=Constant(0.0))
x2paddle_325 = fluid.layers.strided_slice(x2paddle_input,
                                          axes=[2],
                                          starts=[0],
                                          ends=[2147483647],
                                          strides=[2])
x2paddle_335 = fluid.layers.strided_slice(x2paddle_input,
                                          axes=[2],
                                          starts=[1],
                                          ends=[2147483647],
                                          strides=[2])
x2paddle_345 = fluid.layers.strided_slice(x2paddle_input,
                                          axes=[2],
                                          starts=[0],
                                          ends=[2147483647],
                                          strides=[2])
x2paddle_355 = fluid.layers.strided_slice(x2paddle_input,
                                          axes=[2],
                                          starts=[1],
                                          ends=[2147483647],
                                          strides=[2])
x2paddle_639 = fluid.layers.shape(x2paddle_638)
x2paddle_639 = fluid.layers.cast(x2paddle_639, dtype='int64')
x2paddle_761_1 = fluid.layers.gather(input=x2paddle_model_22_anchor_grid,
                                     index=x2paddle_760)
x2paddle_761 = fluid.layers.squeeze(input=x2paddle_761_1, axes=[0])
x2paddle_766 = fluid.layers.shape(x2paddle_765)
x2paddle_766 = fluid.layers.cast(x2paddle_766, dtype='int64')
x2paddle_921 = fluid.layers.shape(x2paddle_920)
x2paddle_921 = fluid.layers.cast(x2paddle_921, dtype='int64')
x2paddle_1043_1 = fluid.layers.gather(input=x2paddle_model_22_anchor_grid,
                                      index=x2paddle_1042)
x2paddle_1043 = fluid.layers.squeeze(input=x2paddle_1043_1, axes=[0])
x2paddle_1048 = fluid.layers.shape(x2paddle_1047)
x2paddle_1048 = fluid.layers.cast(x2paddle_1048, dtype='int64')
x2paddle_1203 = fluid.layers.shape(x2paddle_1202)
x2paddle_1203 = fluid.layers.cast(x2paddle_1203, dtype='int64')
x2paddle_1325_1 = fluid.layers.gather(input=x2paddle_model_22_anchor_grid,
                                      index=x2paddle_1324)
x2paddle_1325 = fluid.layers.squeeze(input=x2paddle_1325_1, axes=[0])
x2paddle_1330 = fluid.layers.shape(x2paddle_1329)
x2paddle_1330 = fluid.layers.cast(x2paddle_1330, dtype='int64')
x2paddle_330 = fluid.layers.strided_slice(x2paddle_325,
                                          axes=[3],
                                          starts=[0],
                                          ends=[2147483647],
                                          strides=[2])
x2paddle_340 = fluid.layers.strided_slice(x2paddle_335,
                                          axes=[3],
                                          starts=[0],
                                          ends=[2147483647],
                                          strides=[2])
x2paddle_350 = fluid.layers.strided_slice(x2paddle_345,
                                          axes=[3],
                                          starts=[1],
                                          ends=[2147483647],
                                          strides=[2])
x2paddle_360 = fluid.layers.strided_slice(x2paddle_355,
                                          axes=[3],
                                          starts=[1],
                                          ends=[2147483647],
                                          strides=[2])
x2paddle_640 = fluid.layers.fill_constant(shape=x2paddle_639,
                                          dtype='int64',
                                          value=1)
x2paddle_767 = fluid.layers.fill_constant(shape=x2paddle_766,
                                          dtype='int64',
                                          value=1)
x2paddle_922 = fluid.layers.fill_constant(shape=x2paddle_921,
                                          dtype='int64',
                                          value=1)
x2paddle_1049 = fluid.layers.fill_constant(shape=x2paddle_1048,
                                           dtype='int64',
                                           value=1)
x2paddle_1204 = fluid.layers.fill_constant(shape=x2paddle_1203,
                                           dtype='int64',
                                           value=1)
x2paddle_1331 = fluid.layers.fill_constant(shape=x2paddle_1330,
                                           dtype='int64',
                                           value=1)
x2paddle_361 = fluid.layers.concat(
    [x2paddle_330, x2paddle_340, x2paddle_350, x2paddle_360], axis=1)
x2paddle_642 = fluid.layers.elementwise_mul(x=x2paddle_640, y=x2paddle_641)
x2paddle_769 = fluid.layers.elementwise_mul(x=x2paddle_767, y=x2paddle_768)
x2paddle_924 = fluid.layers.elementwise_mul(x=x2paddle_922, y=x2paddle_923)
x2paddle_1051 = fluid.layers.elementwise_mul(x=x2paddle_1049, y=x2paddle_1050)
x2paddle_1206 = fluid.layers.elementwise_mul(x=x2paddle_1204, y=x2paddle_1205)
x2paddle_1333 = fluid.layers.elementwise_mul(x=x2paddle_1331, y=x2paddle_1332)
x2paddle_362 = fluid.layers.conv2d(
    x2paddle_361,
    num_filters=32,
    filter_size=[3, 3],
    stride=[1, 1],
    padding=[1, 1],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_0_conv_conv_weight',
    name='x2paddle_362',
    bias_attr=False)
x2paddle_644 = fluid.layers.equal(x=x2paddle_643, y=x2paddle_642)
x2paddle_771 = fluid.layers.equal(x=x2paddle_770, y=x2paddle_769)
x2paddle_926 = fluid.layers.equal(x=x2paddle_925, y=x2paddle_924)
x2paddle_1053 = fluid.layers.equal(x=x2paddle_1052, y=x2paddle_1051)
x2paddle_1208 = fluid.layers.equal(x=x2paddle_1207, y=x2paddle_1206)
x2paddle_1335 = fluid.layers.equal(x=x2paddle_1334, y=x2paddle_1333)
x2paddle_363 = fluid.layers.batch_norm(
    x2paddle_362,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_0_conv_bn_weight',
    bias_attr='x2paddle_model_0_conv_bn_bias',
    moving_mean_name='x2paddle_model_0_conv_bn_running_mean',
    moving_variance_name='x2paddle_model_0_conv_bn_running_var',
    use_global_stats=False,
    name='x2paddle_363')
x2paddle_644_not = fluid.layers.logical_not(x2paddle_644)
x2paddle_644_not_cast = fluid.layers.cast(x2paddle_644_not, dtype='int64')
x2paddle_644_cast = fluid.layers.cast(x2paddle_644, dtype='int64')
x2paddle_640_mul = fluid.layers.elementwise_mul(x=x2paddle_640,
                                                y=x2paddle_644_cast)
x2paddle_638_mul = fluid.layers.elementwise_mul(x=x2paddle_638,
                                                y=x2paddle_644_not_cast)
x2paddle_645 = fluid.layers.elementwise_add(x=x2paddle_640_mul,
                                            y=x2paddle_638_mul)
x2paddle_771_not = fluid.layers.logical_not(x2paddle_771)
x2paddle_771_not_cast = fluid.layers.cast(x2paddle_771_not, dtype='int64')
x2paddle_771_cast = fluid.layers.cast(x2paddle_771, dtype='int64')
x2paddle_767_mul = fluid.layers.elementwise_mul(x=x2paddle_767,
                                                y=x2paddle_771_cast)
x2paddle_765_mul = fluid.layers.elementwise_mul(x=x2paddle_765,
                                                y=x2paddle_771_not_cast)
x2paddle_772 = fluid.layers.elementwise_add(x=x2paddle_767_mul,
                                            y=x2paddle_765_mul)
x2paddle_926_not = fluid.layers.logical_not(x2paddle_926)
x2paddle_926_not_cast = fluid.layers.cast(x2paddle_926_not, dtype='int64')
x2paddle_926_cast = fluid.layers.cast(x2paddle_926, dtype='int64')
x2paddle_922_mul = fluid.layers.elementwise_mul(x=x2paddle_922,
                                                y=x2paddle_926_cast)
x2paddle_920_mul = fluid.layers.elementwise_mul(x=x2paddle_920,
                                                y=x2paddle_926_not_cast)
x2paddle_927 = fluid.layers.elementwise_add(x=x2paddle_922_mul,
                                            y=x2paddle_920_mul)
x2paddle_1053_not = fluid.layers.logical_not(x2paddle_1053)
x2paddle_1053_not_cast = fluid.layers.cast(x2paddle_1053_not, dtype='int64')
x2paddle_1053_cast = fluid.layers.cast(x2paddle_1053, dtype='int64')
x2paddle_1049_mul = fluid.layers.elementwise_mul(x=x2paddle_1049,
                                                 y=x2paddle_1053_cast)
x2paddle_1047_mul = fluid.layers.elementwise_mul(x=x2paddle_1047,
                                                 y=x2paddle_1053_not_cast)
x2paddle_1054 = fluid.layers.elementwise_add(x=x2paddle_1049_mul,
                                             y=x2paddle_1047_mul)
x2paddle_1208_not = fluid.layers.logical_not(x2paddle_1208)
x2paddle_1208_not_cast = fluid.layers.cast(x2paddle_1208_not, dtype='int64')
x2paddle_1208_cast = fluid.layers.cast(x2paddle_1208, dtype='int64')
x2paddle_1204_mul = fluid.layers.elementwise_mul(x=x2paddle_1204,
                                                 y=x2paddle_1208_cast)
x2paddle_1202_mul = fluid.layers.elementwise_mul(x=x2paddle_1202,
                                                 y=x2paddle_1208_not_cast)
x2paddle_1209 = fluid.layers.elementwise_add(x=x2paddle_1204_mul,
                                             y=x2paddle_1202_mul)
x2paddle_1335_not = fluid.layers.logical_not(x2paddle_1335)
x2paddle_1335_not_cast = fluid.layers.cast(x2paddle_1335_not, dtype='int64')
x2paddle_1335_cast = fluid.layers.cast(x2paddle_1335, dtype='int64')
x2paddle_1331_mul = fluid.layers.elementwise_mul(x=x2paddle_1331,
                                                 y=x2paddle_1335_cast)
x2paddle_1329_mul = fluid.layers.elementwise_mul(x=x2paddle_1329,
                                                 y=x2paddle_1335_not_cast)
x2paddle_1336 = fluid.layers.elementwise_add(x=x2paddle_1331_mul,
                                             y=x2paddle_1329_mul)
x2paddle_364 = fluid.layers.leaky_relu(x2paddle_363,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_364')
x2paddle_365 = fluid.layers.conv2d(x2paddle_364,
                                   num_filters=64,
                                   filter_size=[3, 3],
                                   stride=[2, 2],
                                   padding=[1, 1],
                                   dilation=[1, 1],
                                   groups=1,
                                   param_attr='x2paddle_model_1_conv_weight',
                                   name='x2paddle_365',
                                   bias_attr=False)
x2paddle_366 = fluid.layers.batch_norm(
    x2paddle_365,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_1_bn_weight',
    bias_attr='x2paddle_model_1_bn_bias',
    moving_mean_name='x2paddle_model_1_bn_running_mean',
    moving_variance_name='x2paddle_model_1_bn_running_var',
    use_global_stats=False,
    name='x2paddle_366')
x2paddle_367 = fluid.layers.leaky_relu(x2paddle_366,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_367')
x2paddle_368 = fluid.layers.conv2d(
    x2paddle_367,
    num_filters=32,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_2_cv1_conv_weight',
    name='x2paddle_368',
    bias_attr=False)
x2paddle_369 = fluid.layers.batch_norm(
    x2paddle_368,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_2_cv1_bn_weight',
    bias_attr='x2paddle_model_2_cv1_bn_bias',
    moving_mean_name='x2paddle_model_2_cv1_bn_running_mean',
    moving_variance_name='x2paddle_model_2_cv1_bn_running_var',
    use_global_stats=False,
    name='x2paddle_369')
x2paddle_370 = fluid.layers.leaky_relu(x2paddle_369,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_370')
x2paddle_371 = fluid.layers.conv2d(
    x2paddle_370,
    num_filters=64,
    filter_size=[3, 3],
    stride=[1, 1],
    padding=[1, 1],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_2_cv2_conv_weight',
    name='x2paddle_371',
    bias_attr=False)
x2paddle_372 = fluid.layers.batch_norm(
    x2paddle_371,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_2_cv2_bn_weight',
    bias_attr='x2paddle_model_2_cv2_bn_bias',
    moving_mean_name='x2paddle_model_2_cv2_bn_running_mean',
    moving_variance_name='x2paddle_model_2_cv2_bn_running_var',
    use_global_stats=False,
    name='x2paddle_372')
x2paddle_373 = fluid.layers.leaky_relu(x2paddle_372,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_373')
x2paddle_374 = fluid.layers.elementwise_add(x=x2paddle_367, y=x2paddle_373)
x2paddle_375 = fluid.layers.conv2d(x2paddle_374,
                                   num_filters=128,
                                   filter_size=[3, 3],
                                   stride=[2, 2],
                                   padding=[1, 1],
                                   dilation=[1, 1],
                                   groups=1,
                                   param_attr='x2paddle_model_3_conv_weight',
                                   name='x2paddle_375',
                                   bias_attr=False)
x2paddle_376 = fluid.layers.batch_norm(
    x2paddle_375,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_3_bn_weight',
    bias_attr='x2paddle_model_3_bn_bias',
    moving_mean_name='x2paddle_model_3_bn_running_mean',
    moving_variance_name='x2paddle_model_3_bn_running_var',
    use_global_stats=False,
    name='x2paddle_376')
x2paddle_377 = fluid.layers.leaky_relu(x2paddle_376,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_377')
x2paddle_378 = fluid.layers.conv2d(
    x2paddle_377,
    num_filters=64,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_4_cv1_conv_weight',
    name='x2paddle_378',
    bias_attr=False)
x2paddle_403 = fluid.layers.conv2d(x2paddle_377,
                                   num_filters=64,
                                   filter_size=[1, 1],
                                   stride=[1, 1],
                                   padding=[0, 0],
                                   dilation=[1, 1],
                                   groups=1,
                                   param_attr='x2paddle_model_4_cv2_weight',
                                   name='x2paddle_403',
                                   bias_attr=False)
x2paddle_379 = fluid.layers.batch_norm(
    x2paddle_378,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_4_cv1_bn_weight',
    bias_attr='x2paddle_model_4_cv1_bn_bias',
    moving_mean_name='x2paddle_model_4_cv1_bn_running_mean',
    moving_variance_name='x2paddle_model_4_cv1_bn_running_var',
    use_global_stats=False,
    name='x2paddle_379')
x2paddle_380 = fluid.layers.leaky_relu(x2paddle_379,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_380')
x2paddle_381 = fluid.layers.conv2d(
    x2paddle_380,
    num_filters=64,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_4_m_0_cv1_conv_weight',
    name='x2paddle_381',
    bias_attr=False)
x2paddle_382 = fluid.layers.batch_norm(
    x2paddle_381,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_4_m_0_cv1_bn_weight',
    bias_attr='x2paddle_model_4_m_0_cv1_bn_bias',
    moving_mean_name='x2paddle_model_4_m_0_cv1_bn_running_mean',
    moving_variance_name='x2paddle_model_4_m_0_cv1_bn_running_var',
    use_global_stats=False,
    name='x2paddle_382')
x2paddle_383 = fluid.layers.leaky_relu(x2paddle_382,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_383')
x2paddle_384 = fluid.layers.conv2d(
    x2paddle_383,
    num_filters=64,
    filter_size=[3, 3],
    stride=[1, 1],
    padding=[1, 1],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_4_m_0_cv2_conv_weight',
    name='x2paddle_384',
    bias_attr=False)
x2paddle_385 = fluid.layers.batch_norm(
    x2paddle_384,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_4_m_0_cv2_bn_weight',
    bias_attr='x2paddle_model_4_m_0_cv2_bn_bias',
    moving_mean_name='x2paddle_model_4_m_0_cv2_bn_running_mean',
    moving_variance_name='x2paddle_model_4_m_0_cv2_bn_running_var',
    use_global_stats=False,
    name='x2paddle_385')
x2paddle_386 = fluid.layers.leaky_relu(x2paddle_385,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_386')
x2paddle_387 = fluid.layers.elementwise_add(x=x2paddle_380, y=x2paddle_386)
x2paddle_388 = fluid.layers.conv2d(
    x2paddle_387,
    num_filters=64,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_4_m_1_cv1_conv_weight',
    name='x2paddle_388',
    bias_attr=False)
x2paddle_389 = fluid.layers.batch_norm(
    x2paddle_388,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_4_m_1_cv1_bn_weight',
    bias_attr='x2paddle_model_4_m_1_cv1_bn_bias',
    moving_mean_name='x2paddle_model_4_m_1_cv1_bn_running_mean',
    moving_variance_name='x2paddle_model_4_m_1_cv1_bn_running_var',
    use_global_stats=False,
    name='x2paddle_389')
x2paddle_390 = fluid.layers.leaky_relu(x2paddle_389,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_390')
x2paddle_391 = fluid.layers.conv2d(
    x2paddle_390,
    num_filters=64,
    filter_size=[3, 3],
    stride=[1, 1],
    padding=[1, 1],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_4_m_1_cv2_conv_weight',
    name='x2paddle_391',
    bias_attr=False)
x2paddle_392 = fluid.layers.batch_norm(
    x2paddle_391,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_4_m_1_cv2_bn_weight',
    bias_attr='x2paddle_model_4_m_1_cv2_bn_bias',
    moving_mean_name='x2paddle_model_4_m_1_cv2_bn_running_mean',
    moving_variance_name='x2paddle_model_4_m_1_cv2_bn_running_var',
    use_global_stats=False,
    name='x2paddle_392')
x2paddle_393 = fluid.layers.leaky_relu(x2paddle_392,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_393')
x2paddle_394 = fluid.layers.elementwise_add(x=x2paddle_387, y=x2paddle_393)
x2paddle_395 = fluid.layers.conv2d(
    x2paddle_394,
    num_filters=64,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_4_m_2_cv1_conv_weight',
    name='x2paddle_395',
    bias_attr=False)
x2paddle_396 = fluid.layers.batch_norm(
    x2paddle_395,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_4_m_2_cv1_bn_weight',
    bias_attr='x2paddle_model_4_m_2_cv1_bn_bias',
    moving_mean_name='x2paddle_model_4_m_2_cv1_bn_running_mean',
    moving_variance_name='x2paddle_model_4_m_2_cv1_bn_running_var',
    use_global_stats=False,
    name='x2paddle_396')
x2paddle_397 = fluid.layers.leaky_relu(x2paddle_396,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_397')
x2paddle_398 = fluid.layers.conv2d(
    x2paddle_397,
    num_filters=64,
    filter_size=[3, 3],
    stride=[1, 1],
    padding=[1, 1],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_4_m_2_cv2_conv_weight',
    name='x2paddle_398',
    bias_attr=False)
x2paddle_399 = fluid.layers.batch_norm(
    x2paddle_398,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_4_m_2_cv2_bn_weight',
    bias_attr='x2paddle_model_4_m_2_cv2_bn_bias',
    moving_mean_name='x2paddle_model_4_m_2_cv2_bn_running_mean',
    moving_variance_name='x2paddle_model_4_m_2_cv2_bn_running_var',
    use_global_stats=False,
    name='x2paddle_399')
x2paddle_400 = fluid.layers.leaky_relu(x2paddle_399,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_400')
x2paddle_401 = fluid.layers.elementwise_add(x=x2paddle_394, y=x2paddle_400)
x2paddle_402 = fluid.layers.conv2d(x2paddle_401,
                                   num_filters=64,
                                   filter_size=[1, 1],
                                   stride=[1, 1],
                                   padding=[0, 0],
                                   dilation=[1, 1],
                                   groups=1,
                                   param_attr='x2paddle_model_4_cv3_weight',
                                   name='x2paddle_402',
                                   bias_attr=False)
x2paddle_404 = fluid.layers.concat([x2paddle_402, x2paddle_403], axis=1)
x2paddle_405 = fluid.layers.batch_norm(
    x2paddle_404,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_4_bn_weight',
    bias_attr='x2paddle_model_4_bn_bias',
    moving_mean_name='x2paddle_model_4_bn_running_mean',
    moving_variance_name='x2paddle_model_4_bn_running_var',
    use_global_stats=False,
    name='x2paddle_405')
x2paddle_406 = fluid.layers.leaky_relu(x2paddle_405,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_406')
x2paddle_407 = fluid.layers.conv2d(
    x2paddle_406,
    num_filters=128,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_4_cv4_conv_weight',
    name='x2paddle_407',
    bias_attr=False)
x2paddle_408 = fluid.layers.batch_norm(
    x2paddle_407,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_4_cv4_bn_weight',
    bias_attr='x2paddle_model_4_cv4_bn_bias',
    moving_mean_name='x2paddle_model_4_cv4_bn_running_mean',
    moving_variance_name='x2paddle_model_4_cv4_bn_running_var',
    use_global_stats=False,
    name='x2paddle_408')
x2paddle_409 = fluid.layers.leaky_relu(x2paddle_408,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_409')
x2paddle_410 = fluid.layers.conv2d(x2paddle_409,
                                   num_filters=256,
                                   filter_size=[3, 3],
                                   stride=[2, 2],
                                   padding=[1, 1],
                                   dilation=[1, 1],
                                   groups=1,
                                   param_attr='x2paddle_model_5_conv_weight',
                                   name='x2paddle_410',
                                   bias_attr=False)
x2paddle_411 = fluid.layers.batch_norm(
    x2paddle_410,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_5_bn_weight',
    bias_attr='x2paddle_model_5_bn_bias',
    moving_mean_name='x2paddle_model_5_bn_running_mean',
    moving_variance_name='x2paddle_model_5_bn_running_var',
    use_global_stats=False,
    name='x2paddle_411')
x2paddle_412 = fluid.layers.leaky_relu(x2paddle_411,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_412')
x2paddle_413 = fluid.layers.conv2d(
    x2paddle_412,
    num_filters=128,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_6_cv1_conv_weight',
    name='x2paddle_413',
    bias_attr=False)
x2paddle_438 = fluid.layers.conv2d(x2paddle_412,
                                   num_filters=128,
                                   filter_size=[1, 1],
                                   stride=[1, 1],
                                   padding=[0, 0],
                                   dilation=[1, 1],
                                   groups=1,
                                   param_attr='x2paddle_model_6_cv2_weight',
                                   name='x2paddle_438',
                                   bias_attr=False)
x2paddle_414 = fluid.layers.batch_norm(
    x2paddle_413,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_6_cv1_bn_weight',
    bias_attr='x2paddle_model_6_cv1_bn_bias',
    moving_mean_name='x2paddle_model_6_cv1_bn_running_mean',
    moving_variance_name='x2paddle_model_6_cv1_bn_running_var',
    use_global_stats=False,
    name='x2paddle_414')
x2paddle_415 = fluid.layers.leaky_relu(x2paddle_414,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_415')
x2paddle_416 = fluid.layers.conv2d(
    x2paddle_415,
    num_filters=128,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_6_m_0_cv1_conv_weight',
    name='x2paddle_416',
    bias_attr=False)
x2paddle_417 = fluid.layers.batch_norm(
    x2paddle_416,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_6_m_0_cv1_bn_weight',
    bias_attr='x2paddle_model_6_m_0_cv1_bn_bias',
    moving_mean_name='x2paddle_model_6_m_0_cv1_bn_running_mean',
    moving_variance_name='x2paddle_model_6_m_0_cv1_bn_running_var',
    use_global_stats=False,
    name='x2paddle_417')
x2paddle_418 = fluid.layers.leaky_relu(x2paddle_417,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_418')
x2paddle_419 = fluid.layers.conv2d(
    x2paddle_418,
    num_filters=128,
    filter_size=[3, 3],
    stride=[1, 1],
    padding=[1, 1],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_6_m_0_cv2_conv_weight',
    name='x2paddle_419',
    bias_attr=False)
x2paddle_420 = fluid.layers.batch_norm(
    x2paddle_419,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_6_m_0_cv2_bn_weight',
    bias_attr='x2paddle_model_6_m_0_cv2_bn_bias',
    moving_mean_name='x2paddle_model_6_m_0_cv2_bn_running_mean',
    moving_variance_name='x2paddle_model_6_m_0_cv2_bn_running_var',
    use_global_stats=False,
    name='x2paddle_420')
x2paddle_421 = fluid.layers.leaky_relu(x2paddle_420,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_421')
x2paddle_422 = fluid.layers.elementwise_add(x=x2paddle_415, y=x2paddle_421)
x2paddle_423 = fluid.layers.conv2d(
    x2paddle_422,
    num_filters=128,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_6_m_1_cv1_conv_weight',
    name='x2paddle_423',
    bias_attr=False)
x2paddle_424 = fluid.layers.batch_norm(
    x2paddle_423,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_6_m_1_cv1_bn_weight',
    bias_attr='x2paddle_model_6_m_1_cv1_bn_bias',
    moving_mean_name='x2paddle_model_6_m_1_cv1_bn_running_mean',
    moving_variance_name='x2paddle_model_6_m_1_cv1_bn_running_var',
    use_global_stats=False,
    name='x2paddle_424')
x2paddle_425 = fluid.layers.leaky_relu(x2paddle_424,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_425')
x2paddle_426 = fluid.layers.conv2d(
    x2paddle_425,
    num_filters=128,
    filter_size=[3, 3],
    stride=[1, 1],
    padding=[1, 1],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_6_m_1_cv2_conv_weight',
    name='x2paddle_426',
    bias_attr=False)
x2paddle_427 = fluid.layers.batch_norm(
    x2paddle_426,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_6_m_1_cv2_bn_weight',
    bias_attr='x2paddle_model_6_m_1_cv2_bn_bias',
    moving_mean_name='x2paddle_model_6_m_1_cv2_bn_running_mean',
    moving_variance_name='x2paddle_model_6_m_1_cv2_bn_running_var',
    use_global_stats=False,
    name='x2paddle_427')
x2paddle_428 = fluid.layers.leaky_relu(x2paddle_427,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_428')
x2paddle_429 = fluid.layers.elementwise_add(x=x2paddle_422, y=x2paddle_428)
x2paddle_430 = fluid.layers.conv2d(
    x2paddle_429,
    num_filters=128,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_6_m_2_cv1_conv_weight',
    name='x2paddle_430',
    bias_attr=False)
x2paddle_431 = fluid.layers.batch_norm(
    x2paddle_430,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_6_m_2_cv1_bn_weight',
    bias_attr='x2paddle_model_6_m_2_cv1_bn_bias',
    moving_mean_name='x2paddle_model_6_m_2_cv1_bn_running_mean',
    moving_variance_name='x2paddle_model_6_m_2_cv1_bn_running_var',
    use_global_stats=False,
    name='x2paddle_431')
x2paddle_432 = fluid.layers.leaky_relu(x2paddle_431,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_432')
x2paddle_433 = fluid.layers.conv2d(
    x2paddle_432,
    num_filters=128,
    filter_size=[3, 3],
    stride=[1, 1],
    padding=[1, 1],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_6_m_2_cv2_conv_weight',
    name='x2paddle_433',
    bias_attr=False)
x2paddle_434 = fluid.layers.batch_norm(
    x2paddle_433,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_6_m_2_cv2_bn_weight',
    bias_attr='x2paddle_model_6_m_2_cv2_bn_bias',
    moving_mean_name='x2paddle_model_6_m_2_cv2_bn_running_mean',
    moving_variance_name='x2paddle_model_6_m_2_cv2_bn_running_var',
    use_global_stats=False,
    name='x2paddle_434')
x2paddle_435 = fluid.layers.leaky_relu(x2paddle_434,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_435')
x2paddle_436 = fluid.layers.elementwise_add(x=x2paddle_429, y=x2paddle_435)
x2paddle_437 = fluid.layers.conv2d(x2paddle_436,
                                   num_filters=128,
                                   filter_size=[1, 1],
                                   stride=[1, 1],
                                   padding=[0, 0],
                                   dilation=[1, 1],
                                   groups=1,
                                   param_attr='x2paddle_model_6_cv3_weight',
                                   name='x2paddle_437',
                                   bias_attr=False)
x2paddle_439 = fluid.layers.concat([x2paddle_437, x2paddle_438], axis=1)
x2paddle_440 = fluid.layers.batch_norm(
    x2paddle_439,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_6_bn_weight',
    bias_attr='x2paddle_model_6_bn_bias',
    moving_mean_name='x2paddle_model_6_bn_running_mean',
    moving_variance_name='x2paddle_model_6_bn_running_var',
    use_global_stats=False,
    name='x2paddle_440')
x2paddle_441 = fluid.layers.leaky_relu(x2paddle_440,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_441')
x2paddle_442 = fluid.layers.conv2d(
    x2paddle_441,
    num_filters=256,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_6_cv4_conv_weight',
    name='x2paddle_442',
    bias_attr=False)
x2paddle_443 = fluid.layers.batch_norm(
    x2paddle_442,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_6_cv4_bn_weight',
    bias_attr='x2paddle_model_6_cv4_bn_bias',
    moving_mean_name='x2paddle_model_6_cv4_bn_running_mean',
    moving_variance_name='x2paddle_model_6_cv4_bn_running_var',
    use_global_stats=False,
    name='x2paddle_443')
x2paddle_444 = fluid.layers.leaky_relu(x2paddle_443,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_444')
x2paddle_445 = fluid.layers.conv2d(x2paddle_444,
                                   num_filters=512,
                                   filter_size=[3, 3],
                                   stride=[2, 2],
                                   padding=[1, 1],
                                   dilation=[1, 1],
                                   groups=1,
                                   param_attr='x2paddle_model_7_conv_weight',
                                   name='x2paddle_445',
                                   bias_attr=False)
x2paddle_446 = fluid.layers.batch_norm(
    x2paddle_445,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_7_bn_weight',
    bias_attr='x2paddle_model_7_bn_bias',
    moving_mean_name='x2paddle_model_7_bn_running_mean',
    moving_variance_name='x2paddle_model_7_bn_running_var',
    use_global_stats=False,
    name='x2paddle_446')
x2paddle_447 = fluid.layers.leaky_relu(x2paddle_446,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_447')
x2paddle_448 = fluid.layers.conv2d(
    x2paddle_447,
    num_filters=256,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_8_cv1_conv_weight',
    name='x2paddle_448',
    bias_attr=False)
x2paddle_449 = fluid.layers.batch_norm(
    x2paddle_448,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_8_cv1_bn_weight',
    bias_attr='x2paddle_model_8_cv1_bn_bias',
    moving_mean_name='x2paddle_model_8_cv1_bn_running_mean',
    moving_variance_name='x2paddle_model_8_cv1_bn_running_var',
    use_global_stats=False,
    name='x2paddle_449')
x2paddle_450 = fluid.layers.leaky_relu(x2paddle_449,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_450')
x2paddle_451 = fluid.layers.pool2d(x2paddle_450,
                                   pool_size=[5, 5],
                                   pool_type='max',
                                   pool_stride=[1, 1],
                                   pool_padding=[2, 2],
                                   ceil_mode=False,
                                   name='x2paddle_451',
                                   exclusive=False)
x2paddle_452 = fluid.layers.pool2d(x2paddle_450,
                                   pool_size=[9, 9],
                                   pool_type='max',
                                   pool_stride=[1, 1],
                                   pool_padding=[4, 4],
                                   ceil_mode=False,
                                   name='x2paddle_452',
                                   exclusive=False)
x2paddle_453 = fluid.layers.pool2d(x2paddle_450,
                                   pool_size=[13, 13],
                                   pool_type='max',
                                   pool_stride=[1, 1],
                                   pool_padding=[6, 6],
                                   ceil_mode=False,
                                   name='x2paddle_453',
                                   exclusive=False)
x2paddle_454 = fluid.layers.concat(
    [x2paddle_450, x2paddle_451, x2paddle_452, x2paddle_453], axis=1)
x2paddle_455 = fluid.layers.conv2d(
    x2paddle_454,
    num_filters=512,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_8_cv2_conv_weight',
    name='x2paddle_455',
    bias_attr=False)
x2paddle_456 = fluid.layers.batch_norm(
    x2paddle_455,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_8_cv2_bn_weight',
    bias_attr='x2paddle_model_8_cv2_bn_bias',
    moving_mean_name='x2paddle_model_8_cv2_bn_running_mean',
    moving_variance_name='x2paddle_model_8_cv2_bn_running_var',
    use_global_stats=False,
    name='x2paddle_456')
x2paddle_457 = fluid.layers.leaky_relu(x2paddle_456,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_457')
x2paddle_458 = fluid.layers.conv2d(
    x2paddle_457,
    num_filters=256,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_9_cv1_conv_weight',
    name='x2paddle_458',
    bias_attr=False)
x2paddle_476 = fluid.layers.conv2d(x2paddle_457,
                                   num_filters=256,
                                   filter_size=[1, 1],
                                   stride=[1, 1],
                                   padding=[0, 0],
                                   dilation=[1, 1],
                                   groups=1,
                                   param_attr='x2paddle_model_9_cv2_weight',
                                   name='x2paddle_476',
                                   bias_attr=False)
x2paddle_459 = fluid.layers.batch_norm(
    x2paddle_458,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_9_cv1_bn_weight',
    bias_attr='x2paddle_model_9_cv1_bn_bias',
    moving_mean_name='x2paddle_model_9_cv1_bn_running_mean',
    moving_variance_name='x2paddle_model_9_cv1_bn_running_var',
    use_global_stats=False,
    name='x2paddle_459')
x2paddle_460 = fluid.layers.leaky_relu(x2paddle_459,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_460')
x2paddle_461 = fluid.layers.conv2d(
    x2paddle_460,
    num_filters=256,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_9_m_0_cv1_conv_weight',
    name='x2paddle_461',
    bias_attr=False)
x2paddle_462 = fluid.layers.batch_norm(
    x2paddle_461,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_9_m_0_cv1_bn_weight',
    bias_attr='x2paddle_model_9_m_0_cv1_bn_bias',
    moving_mean_name='x2paddle_model_9_m_0_cv1_bn_running_mean',
    moving_variance_name='x2paddle_model_9_m_0_cv1_bn_running_var',
    use_global_stats=False,
    name='x2paddle_462')
x2paddle_463 = fluid.layers.leaky_relu(x2paddle_462,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_463')
x2paddle_464 = fluid.layers.conv2d(
    x2paddle_463,
    num_filters=256,
    filter_size=[3, 3],
    stride=[1, 1],
    padding=[1, 1],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_9_m_0_cv2_conv_weight',
    name='x2paddle_464',
    bias_attr=False)
x2paddle_465 = fluid.layers.batch_norm(
    x2paddle_464,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_9_m_0_cv2_bn_weight',
    bias_attr='x2paddle_model_9_m_0_cv2_bn_bias',
    moving_mean_name='x2paddle_model_9_m_0_cv2_bn_running_mean',
    moving_variance_name='x2paddle_model_9_m_0_cv2_bn_running_var',
    use_global_stats=False,
    name='x2paddle_465')
x2paddle_466 = fluid.layers.leaky_relu(x2paddle_465,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_466')
x2paddle_467 = fluid.layers.elementwise_add(x=x2paddle_460, y=x2paddle_466)
x2paddle_468 = fluid.layers.conv2d(
    x2paddle_467,
    num_filters=256,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_9_m_1_cv1_conv_weight',
    name='x2paddle_468',
    bias_attr=False)
x2paddle_469 = fluid.layers.batch_norm(
    x2paddle_468,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_9_m_1_cv1_bn_weight',
    bias_attr='x2paddle_model_9_m_1_cv1_bn_bias',
    moving_mean_name='x2paddle_model_9_m_1_cv1_bn_running_mean',
    moving_variance_name='x2paddle_model_9_m_1_cv1_bn_running_var',
    use_global_stats=False,
    name='x2paddle_469')
x2paddle_470 = fluid.layers.leaky_relu(x2paddle_469,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_470')
x2paddle_471 = fluid.layers.conv2d(
    x2paddle_470,
    num_filters=256,
    filter_size=[3, 3],
    stride=[1, 1],
    padding=[1, 1],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_9_m_1_cv2_conv_weight',
    name='x2paddle_471',
    bias_attr=False)
x2paddle_472 = fluid.layers.batch_norm(
    x2paddle_471,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_9_m_1_cv2_bn_weight',
    bias_attr='x2paddle_model_9_m_1_cv2_bn_bias',
    moving_mean_name='x2paddle_model_9_m_1_cv2_bn_running_mean',
    moving_variance_name='x2paddle_model_9_m_1_cv2_bn_running_var',
    use_global_stats=False,
    name='x2paddle_472')
x2paddle_473 = fluid.layers.leaky_relu(x2paddle_472,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_473')
x2paddle_474 = fluid.layers.elementwise_add(x=x2paddle_467, y=x2paddle_473)
x2paddle_475 = fluid.layers.conv2d(x2paddle_474,
                                   num_filters=256,
                                   filter_size=[1, 1],
                                   stride=[1, 1],
                                   padding=[0, 0],
                                   dilation=[1, 1],
                                   groups=1,
                                   param_attr='x2paddle_model_9_cv3_weight',
                                   name='x2paddle_475',
                                   bias_attr=False)
x2paddle_477 = fluid.layers.concat([x2paddle_475, x2paddle_476], axis=1)
x2paddle_478 = fluid.layers.batch_norm(
    x2paddle_477,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_9_bn_weight',
    bias_attr='x2paddle_model_9_bn_bias',
    moving_mean_name='x2paddle_model_9_bn_running_mean',
    moving_variance_name='x2paddle_model_9_bn_running_var',
    use_global_stats=False,
    name='x2paddle_478')
x2paddle_479 = fluid.layers.leaky_relu(x2paddle_478,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_479')
x2paddle_480 = fluid.layers.conv2d(
    x2paddle_479,
    num_filters=512,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_9_cv4_conv_weight',
    name='x2paddle_480',
    bias_attr=False)
x2paddle_481 = fluid.layers.batch_norm(
    x2paddle_480,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_9_cv4_bn_weight',
    bias_attr='x2paddle_model_9_cv4_bn_bias',
    moving_mean_name='x2paddle_model_9_cv4_bn_running_mean',
    moving_variance_name='x2paddle_model_9_cv4_bn_running_var',
    use_global_stats=False,
    name='x2paddle_481')
x2paddle_482 = fluid.layers.leaky_relu(x2paddle_481,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_482')
x2paddle_483 = fluid.layers.conv2d(
    x2paddle_482,
    num_filters=256,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_10_cv1_conv_weight',
    name='x2paddle_483',
    bias_attr=False)
x2paddle_493 = fluid.layers.conv2d(x2paddle_482,
                                   num_filters=256,
                                   filter_size=[1, 1],
                                   stride=[1, 1],
                                   padding=[0, 0],
                                   dilation=[1, 1],
                                   groups=1,
                                   param_attr='x2paddle_model_10_cv2_weight',
                                   name='x2paddle_493',
                                   bias_attr=False)
x2paddle_484 = fluid.layers.batch_norm(
    x2paddle_483,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_10_cv1_bn_weight',
    bias_attr='x2paddle_model_10_cv1_bn_bias',
    moving_mean_name='x2paddle_model_10_cv1_bn_running_mean',
    moving_variance_name='x2paddle_model_10_cv1_bn_running_var',
    use_global_stats=False,
    name='x2paddle_484')
x2paddle_485 = fluid.layers.leaky_relu(x2paddle_484,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_485')
x2paddle_486 = fluid.layers.conv2d(
    x2paddle_485,
    num_filters=256,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_10_m_0_cv1_conv_weight',
    name='x2paddle_486',
    bias_attr=False)
x2paddle_487 = fluid.layers.batch_norm(
    x2paddle_486,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_10_m_0_cv1_bn_weight',
    bias_attr='x2paddle_model_10_m_0_cv1_bn_bias',
    moving_mean_name='x2paddle_model_10_m_0_cv1_bn_running_mean',
    moving_variance_name='x2paddle_model_10_m_0_cv1_bn_running_var',
    use_global_stats=False,
    name='x2paddle_487')
x2paddle_488 = fluid.layers.leaky_relu(x2paddle_487,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_488')
x2paddle_489 = fluid.layers.conv2d(
    x2paddle_488,
    num_filters=256,
    filter_size=[3, 3],
    stride=[1, 1],
    padding=[1, 1],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_10_m_0_cv2_conv_weight',
    name='x2paddle_489',
    bias_attr=False)
x2paddle_490 = fluid.layers.batch_norm(
    x2paddle_489,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_10_m_0_cv2_bn_weight',
    bias_attr='x2paddle_model_10_m_0_cv2_bn_bias',
    moving_mean_name='x2paddle_model_10_m_0_cv2_bn_running_mean',
    moving_variance_name='x2paddle_model_10_m_0_cv2_bn_running_var',
    use_global_stats=False,
    name='x2paddle_490')
x2paddle_491 = fluid.layers.leaky_relu(x2paddle_490,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_491')
x2paddle_492 = fluid.layers.conv2d(x2paddle_491,
                                   num_filters=256,
                                   filter_size=[1, 1],
                                   stride=[1, 1],
                                   padding=[0, 0],
                                   dilation=[1, 1],
                                   groups=1,
                                   param_attr='x2paddle_model_10_cv3_weight',
                                   name='x2paddle_492',
                                   bias_attr=False)
x2paddle_494 = fluid.layers.concat([x2paddle_492, x2paddle_493], axis=1)
x2paddle_495 = fluid.layers.batch_norm(
    x2paddle_494,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_10_bn_weight',
    bias_attr='x2paddle_model_10_bn_bias',
    moving_mean_name='x2paddle_model_10_bn_running_mean',
    moving_variance_name='x2paddle_model_10_bn_running_var',
    use_global_stats=False,
    name='x2paddle_495')
x2paddle_496 = fluid.layers.leaky_relu(x2paddle_495,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_496')
x2paddle_497 = fluid.layers.conv2d(
    x2paddle_496,
    num_filters=512,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_10_cv4_conv_weight',
    name='x2paddle_497',
    bias_attr=False)
x2paddle_498 = fluid.layers.batch_norm(
    x2paddle_497,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_10_cv4_bn_weight',
    bias_attr='x2paddle_model_10_cv4_bn_bias',
    moving_mean_name='x2paddle_model_10_cv4_bn_running_mean',
    moving_variance_name='x2paddle_model_10_cv4_bn_running_var',
    use_global_stats=False,
    name='x2paddle_498')
x2paddle_499 = fluid.layers.leaky_relu(x2paddle_498,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_499')
x2paddle_500 = fluid.layers.conv2d(x2paddle_499,
                                   num_filters=255,
                                   filter_size=[1, 1],
                                   stride=[1, 1],
                                   padding=[0, 0],
                                   dilation=[1, 1],
                                   groups=1,
                                   param_attr='x2paddle_model_11_weight',
                                   name='x2paddle_500',
                                   bias_attr='x2paddle_model_11_bias')
x2paddle_501 = fluid.layers.shape(x2paddle_499)
x2paddle_501 = fluid.layers.cast(x2paddle_501, dtype='int64')
x2paddle_509 = fluid.layers.shape(x2paddle_499)
x2paddle_509 = fluid.layers.cast(x2paddle_509, dtype='int64')
x2paddle_521 = fluid.layers.shape(x2paddle_499)
x2paddle_521 = fluid.layers.cast(x2paddle_521, dtype='int64')
x2paddle_1167 = fluid.layers.shape(x2paddle_500)
x2paddle_1167 = fluid.layers.cast(x2paddle_1167, dtype='int64')
x2paddle_1170 = fluid.layers.shape(x2paddle_500)
x2paddle_1170 = fluid.layers.cast(x2paddle_1170, dtype='int64')
x2paddle_1173 = fluid.layers.shape(x2paddle_500)
x2paddle_1173 = fluid.layers.cast(x2paddle_1173, dtype='int64')
x2paddle_503 = fluid.layers.gather(input=x2paddle_501, index=x2paddle_502)
x2paddle_511 = fluid.layers.gather(input=x2paddle_509, index=x2paddle_510)
x2paddle_525 = fluid.layers.slice(x2paddle_521, axes=[0], starts=[0], ends=[2])
x2paddle_1169 = fluid.layers.gather(input=x2paddle_1167, index=x2paddle_1168)
x2paddle_1172 = fluid.layers.gather(input=x2paddle_1170, index=x2paddle_1171)
x2paddle_1175 = fluid.layers.gather(input=x2paddle_1173, index=x2paddle_1174)
x2paddle_504 = fluid.layers.cast(x2paddle_503, dtype='float32')
x2paddle_512 = fluid.layers.cast(x2paddle_511, dtype='float32')
x2paddle_1178 = fluid.layers.reshape(x2paddle_1169, shape=[1])
x2paddle_1444 = fluid.layers.reshape(x2paddle_1169, shape=[1])
x2paddle_1181 = fluid.layers.reshape(x2paddle_1172, shape=[1])
x2paddle_1182 = fluid.layers.reshape(x2paddle_1175, shape=[1])
x2paddle_506 = fluid.layers.elementwise_mul(x=x2paddle_504, y=x2paddle_505)
x2paddle_514 = fluid.layers.elementwise_mul(x=x2paddle_512, y=x2paddle_513)
x2paddle_1447 = fluid.layers.concat(
    [x2paddle_1444, x2paddle_1460, x2paddle_1461], axis=0)
x2paddle_1183 = fluid.layers.concat(
    [x2paddle_1178, x2paddle_1458, x2paddle_1459, x2paddle_1181, x2paddle_1182],
    axis=0)
x2paddle_507 = fluid.layers.cast(x2paddle_506, dtype='float32')
x2paddle_515 = fluid.layers.cast(x2paddle_514, dtype='float32')
x2paddle_1184 = fluid.layers.reshape(x=x2paddle_500, shape=[-1, 3, 85, 20, 20])
x2paddle_508 = fluid.layers.floor(x2paddle_507, name='x2paddle_508')
x2paddle_516 = fluid.layers.floor(x2paddle_515, name='x2paddle_516')
x2paddle_1185 = fluid.layers.transpose(x2paddle_1184,
                                       perm=[0, 1, 3, 4, 2],
                                       name='x2paddle_1185')
x2paddle_517 = fluid.layers.reshape(x2paddle_508, shape=[1])
x2paddle_518 = fluid.layers.reshape(x2paddle_516, shape=[1])
x2paddle_1186 = fluid.layers.sigmoid(x2paddle_1185, name='x2paddle_1186')
x2paddle_519 = fluid.layers.concat([x2paddle_517, x2paddle_518], axis=0)
x2paddle_1191 = fluid.layers.strided_slice(x2paddle_1186,
                                           axes=[4],
                                           starts=[0],
                                           ends=[2],
                                           strides=[1])
x2paddle_1211 = fluid.layers.shape(x2paddle_1186)
x2paddle_1211 = fluid.layers.cast(x2paddle_1211, dtype='int64')
x2paddle_1218 = fluid.layers.shape(x2paddle_1186)
x2paddle_1218 = fluid.layers.cast(x2paddle_1218, dtype='int64')
x2paddle_1225 = fluid.layers.shape(x2paddle_1186)
x2paddle_1225 = fluid.layers.cast(x2paddle_1225, dtype='int64')
x2paddle_1232 = fluid.layers.shape(x2paddle_1186)
x2paddle_1232 = fluid.layers.cast(x2paddle_1232, dtype='int64')
x2paddle_1239 = fluid.layers.shape(x2paddle_1186)
x2paddle_1239 = fluid.layers.cast(x2paddle_1239, dtype='int64')
x2paddle_1307 = fluid.layers.shape(x2paddle_1186)
x2paddle_1307 = fluid.layers.cast(x2paddle_1307, dtype='int64')
x2paddle_526 = fluid.layers.cast(x2paddle_519, dtype='int64')
x2paddle_1193 = fluid.layers.elementwise_mul(x=x2paddle_1191, y=x2paddle_1192)
x2paddle_1213 = fluid.layers.gather(input=x2paddle_1211, index=x2paddle_1212)
x2paddle_1220 = fluid.layers.gather(input=x2paddle_1218, index=x2paddle_1219)
x2paddle_1227 = fluid.layers.gather(input=x2paddle_1225, index=x2paddle_1226)
x2paddle_1234 = fluid.layers.gather(input=x2paddle_1232, index=x2paddle_1233)
x2paddle_1241 = fluid.layers.gather(input=x2paddle_1239, index=x2paddle_1240)
x2paddle_1311 = fluid.layers.slice(x2paddle_1307,
                                   axes=[0],
                                   starts=[4],
                                   ends=[5])
x2paddle_527 = fluid.layers.concat([x2paddle_525, x2paddle_526], axis=0)
x2paddle_1195 = fluid.layers.elementwise_sub(x=x2paddle_1193, y=x2paddle_1194)
x2paddle_1214 = fluid.layers.cast(x2paddle_1213, dtype='int64')
x2paddle_1221 = fluid.layers.cast(x2paddle_1220, dtype='int64')
x2paddle_1228 = fluid.layers.cast(x2paddle_1227, dtype='int64')
x2paddle_1235 = fluid.layers.cast(x2paddle_1234, dtype='int64')
x2paddle_1242 = fluid.layers.cast(x2paddle_1241, dtype='int64')
x2paddle_527_nc, x2paddle_527_hw = fluid.layers.split(x2paddle_527,
                                                      dim=0,
                                                      num_or_sections=[2, 2])
x2paddle_527_hw = fluid.layers.cast(x2paddle_527_hw, dtype='int32')
x2paddle_529 = fluid.layers.resize_nearest(input=x2paddle_499,
                                           out_shape=x2paddle_527_hw,
                                           name='x2paddle_529',
                                           align_corners=False)
x2paddle_1197 = fluid.layers.elementwise_add(x=x2paddle_1195, y=x2paddle_1196)
x2paddle_1217 = fluid.layers.range(start=x2paddle_1215,
                                   end=x2paddle_1214,
                                   step=x2paddle_1216,
                                   dtype='int64')
x2paddle_1224 = fluid.layers.range(start=x2paddle_1222,
                                   end=x2paddle_1221,
                                   step=x2paddle_1223,
                                   dtype='int64')
x2paddle_1231 = fluid.layers.range(start=x2paddle_1229,
                                   end=x2paddle_1228,
                                   step=x2paddle_1230,
                                   dtype='int64')
x2paddle_1238 = fluid.layers.range(start=x2paddle_1236,
                                   end=x2paddle_1235,
                                   step=x2paddle_1237,
                                   dtype='int64')
x2paddle_1245 = fluid.layers.range(start=x2paddle_1243,
                                   end=x2paddle_1242,
                                   step=x2paddle_1244,
                                   dtype='int64')
x2paddle_530 = fluid.layers.concat([x2paddle_529, x2paddle_444], axis=1)
x2paddle_1199 = fluid.layers.elementwise_mul(x=x2paddle_1197, y=x2paddle_1198)
x2paddle_1252 = fluid.layers.reshape(x=x2paddle_1217, shape=[-1, 1, 1, 1, 1])
x2paddle_1254 = fluid.layers.reshape(x=x2paddle_1224, shape=[-1, 1, 1, 1])
x2paddle_1256 = fluid.layers.reshape(x=x2paddle_1231, shape=[-1, 1, 1])
x2paddle_1258 = fluid.layers.reshape(x=x2paddle_1238, shape=[-1, 1])
x2paddle_1250 = fluid.layers.strided_slice(x2paddle_1245,
                                           axes=[0],
                                           starts=[0],
                                           ends=[2],
                                           strides=[1])
x2paddle_531 = fluid.layers.conv2d(x2paddle_530,
                                   num_filters=256,
                                   filter_size=[1, 1],
                                   stride=[1, 1],
                                   padding=[0, 0],
                                   dilation=[1, 1],
                                   groups=1,
                                   param_attr='x2paddle_model_14_conv_weight',
                                   name='x2paddle_531',
                                   bias_attr=False)
x2paddle_1201 = fluid.layers.reshape(x=x2paddle_1199, shape=[3, 20, 20, 2])
x2paddle_1261 = fluid.layers.elementwise_add(x=x2paddle_1252, y=x2paddle_1254)
x2paddle_1260 = fluid.layers.reshape(x=x2paddle_1250, shape=[-1])
x2paddle_532 = fluid.layers.batch_norm(
    x2paddle_531,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_14_bn_weight',
    bias_attr='x2paddle_model_14_bn_bias',
    moving_mean_name='x2paddle_model_14_bn_running_mean',
    moving_variance_name='x2paddle_model_14_bn_running_var',
    use_global_stats=False,
    name='x2paddle_532')
x2paddle_1210_ones = fluid.layers.fill_constant(shape=x2paddle_1209,
                                                dtype='float32',
                                                value=1)
x2paddle_1210 = fluid.layers.elementwise_mul(x=x2paddle_1210_ones,
                                             y=x2paddle_1201)
x2paddle_1262 = fluid.layers.elementwise_add(x=x2paddle_1261, y=x2paddle_1256)
x2paddle_533 = fluid.layers.leaky_relu(x2paddle_532,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_533')
x2paddle_1263 = fluid.layers.elementwise_add(x=x2paddle_1262, y=x2paddle_1258)
x2paddle_534 = fluid.layers.conv2d(
    x2paddle_533,
    num_filters=128,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_15_cv1_conv_weight',
    name='x2paddle_534',
    bias_attr=False)
x2paddle_544 = fluid.layers.conv2d(x2paddle_533,
                                   num_filters=128,
                                   filter_size=[1, 1],
                                   stride=[1, 1],
                                   padding=[0, 0],
                                   dilation=[1, 1],
                                   groups=1,
                                   param_attr='x2paddle_model_15_cv2_weight',
                                   name='x2paddle_544',
                                   bias_attr=False)
x2paddle_1264 = fluid.layers.elementwise_add(x=x2paddle_1263, y=x2paddle_1260)
x2paddle_535 = fluid.layers.batch_norm(
    x2paddle_534,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_15_cv1_bn_weight',
    bias_attr='x2paddle_model_15_cv1_bn_bias',
    moving_mean_name='x2paddle_model_15_cv1_bn_running_mean',
    moving_variance_name='x2paddle_model_15_cv1_bn_running_var',
    use_global_stats=False,
    name='x2paddle_535')
x2paddle_1265 = fluid.layers.shape(x2paddle_1264)
x2paddle_1265 = fluid.layers.cast(x2paddle_1265, dtype='int64')
x2paddle_536 = fluid.layers.leaky_relu(x2paddle_535,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_536')
x2paddle_1266 = fluid.layers.shape(x2paddle_1265)
x2paddle_1266 = fluid.layers.cast(x2paddle_1266, dtype='int64')
x2paddle_1274 = fluid.layers.shape(x2paddle_1265)
x2paddle_1274 = fluid.layers.cast(x2paddle_1274, dtype='int64')
x2paddle_1282 = fluid.layers.shape(x2paddle_1265)
x2paddle_1282 = fluid.layers.cast(x2paddle_1282, dtype='int64')
x2paddle_1290 = fluid.layers.shape(x2paddle_1265)
x2paddle_1290 = fluid.layers.cast(x2paddle_1290, dtype='int64')
x2paddle_1298 = fluid.layers.shape(x2paddle_1265)
x2paddle_1298 = fluid.layers.cast(x2paddle_1298, dtype='int64')
x2paddle_1312 = fluid.layers.concat([x2paddle_1265, x2paddle_1311], axis=0)
x2paddle_537 = fluid.layers.conv2d(
    x2paddle_536,
    num_filters=128,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_15_m_0_cv1_conv_weight',
    name='x2paddle_537',
    bias_attr=False)
x2paddle_1267 = fluid.layers.fill_constant(shape=x2paddle_1266,
                                           dtype='int64',
                                           value=1)
x2paddle_1275 = fluid.layers.fill_constant(shape=x2paddle_1274,
                                           dtype='int64',
                                           value=1)
x2paddle_1283 = fluid.layers.fill_constant(shape=x2paddle_1282,
                                           dtype='int64',
                                           value=1)
x2paddle_1291 = fluid.layers.fill_constant(shape=x2paddle_1290,
                                           dtype='int64',
                                           value=1)
x2paddle_1299 = fluid.layers.fill_constant(shape=x2paddle_1298,
                                           dtype='int64',
                                           value=1)
x2paddle_1313 = fluid.layers.reshape(x=x2paddle_1210, shape=[-1, 3, 20, 20, 2])
x2paddle_538 = fluid.layers.batch_norm(
    x2paddle_537,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_15_m_0_cv1_bn_weight',
    bias_attr='x2paddle_model_15_m_0_cv1_bn_bias',
    moving_mean_name='x2paddle_model_15_m_0_cv1_bn_running_mean',
    moving_variance_name='x2paddle_model_15_m_0_cv1_bn_running_var',
    use_global_stats=False,
    name='x2paddle_538')
x2paddle_1269 = fluid.layers.elementwise_mul(x=x2paddle_1267, y=x2paddle_1268)
x2paddle_1277 = fluid.layers.elementwise_mul(x=x2paddle_1275, y=x2paddle_1276)
x2paddle_1285 = fluid.layers.elementwise_mul(x=x2paddle_1283, y=x2paddle_1284)
x2paddle_1293 = fluid.layers.elementwise_mul(x=x2paddle_1291, y=x2paddle_1292)
x2paddle_1301 = fluid.layers.elementwise_mul(x=x2paddle_1299, y=x2paddle_1300)
x2paddle_539 = fluid.layers.leaky_relu(x2paddle_538,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_539')
x2paddle_1270 = fluid.layers.equal(x=x2paddle_1265, y=x2paddle_1269)
x2paddle_1278 = fluid.layers.equal(x=x2paddle_1265, y=x2paddle_1277)
x2paddle_1286 = fluid.layers.equal(x=x2paddle_1265, y=x2paddle_1285)
x2paddle_1294 = fluid.layers.equal(x=x2paddle_1265, y=x2paddle_1293)
x2paddle_1302 = fluid.layers.equal(x=x2paddle_1265, y=x2paddle_1301)
x2paddle_540 = fluid.layers.conv2d(
    x2paddle_539,
    num_filters=128,
    filter_size=[3, 3],
    stride=[1, 1],
    padding=[1, 1],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_15_m_0_cv2_conv_weight',
    name='x2paddle_540',
    bias_attr=False)
x2paddle_1270_not = fluid.layers.logical_not(x2paddle_1270)
x2paddle_1270_not_cast = fluid.layers.cast(x2paddle_1270_not, dtype='int64')
x2paddle_1270_cast = fluid.layers.cast(x2paddle_1270, dtype='int64')
x2paddle_1267_mul = fluid.layers.elementwise_mul(x=x2paddle_1267,
                                                 y=x2paddle_1270_cast)
x2paddle_1265_mul = fluid.layers.elementwise_mul(x=x2paddle_1265,
                                                 y=x2paddle_1270_not_cast)
x2paddle_1271 = fluid.layers.elementwise_add(x=x2paddle_1267_mul,
                                             y=x2paddle_1265_mul)
x2paddle_1278_not = fluid.layers.logical_not(x2paddle_1278)
x2paddle_1278_not_cast = fluid.layers.cast(x2paddle_1278_not, dtype='int64')
x2paddle_1278_cast = fluid.layers.cast(x2paddle_1278, dtype='int64')
x2paddle_1275_mul = fluid.layers.elementwise_mul(x=x2paddle_1275,
                                                 y=x2paddle_1278_cast)
x2paddle_1265_mul = fluid.layers.elementwise_mul(x=x2paddle_1265,
                                                 y=x2paddle_1278_not_cast)
x2paddle_1279 = fluid.layers.elementwise_add(x=x2paddle_1275_mul,
                                             y=x2paddle_1265_mul)
x2paddle_1286_not = fluid.layers.logical_not(x2paddle_1286)
x2paddle_1286_not_cast = fluid.layers.cast(x2paddle_1286_not, dtype='int64')
x2paddle_1286_cast = fluid.layers.cast(x2paddle_1286, dtype='int64')
x2paddle_1283_mul = fluid.layers.elementwise_mul(x=x2paddle_1283,
                                                 y=x2paddle_1286_cast)
x2paddle_1265_mul = fluid.layers.elementwise_mul(x=x2paddle_1265,
                                                 y=x2paddle_1286_not_cast)
x2paddle_1287 = fluid.layers.elementwise_add(x=x2paddle_1283_mul,
                                             y=x2paddle_1265_mul)
x2paddle_1294_not = fluid.layers.logical_not(x2paddle_1294)
x2paddle_1294_not_cast = fluid.layers.cast(x2paddle_1294_not, dtype='int64')
x2paddle_1294_cast = fluid.layers.cast(x2paddle_1294, dtype='int64')
x2paddle_1291_mul = fluid.layers.elementwise_mul(x=x2paddle_1291,
                                                 y=x2paddle_1294_cast)
x2paddle_1265_mul = fluid.layers.elementwise_mul(x=x2paddle_1265,
                                                 y=x2paddle_1294_not_cast)
x2paddle_1295 = fluid.layers.elementwise_add(x=x2paddle_1291_mul,
                                             y=x2paddle_1265_mul)
x2paddle_1302_not = fluid.layers.logical_not(x2paddle_1302)
x2paddle_1302_not_cast = fluid.layers.cast(x2paddle_1302_not, dtype='int64')
x2paddle_1302_cast = fluid.layers.cast(x2paddle_1302, dtype='int64')
x2paddle_1299_mul = fluid.layers.elementwise_mul(x=x2paddle_1299,
                                                 y=x2paddle_1302_cast)
x2paddle_1265_mul = fluid.layers.elementwise_mul(x=x2paddle_1265,
                                                 y=x2paddle_1302_not_cast)
x2paddle_1303 = fluid.layers.elementwise_add(x=x2paddle_1299_mul,
                                             y=x2paddle_1265_mul)
x2paddle_541 = fluid.layers.batch_norm(
    x2paddle_540,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_15_m_0_cv2_bn_weight',
    bias_attr='x2paddle_model_15_m_0_cv2_bn_bias',
    moving_mean_name='x2paddle_model_15_m_0_cv2_bn_running_mean',
    moving_variance_name='x2paddle_model_15_m_0_cv2_bn_running_var',
    use_global_stats=False,
    name='x2paddle_541')
x2paddle_1272_ones = fluid.layers.fill_constant(shape=x2paddle_1271,
                                                dtype='int64',
                                                value=1)
x2paddle_1272 = fluid.layers.elementwise_mul(x=x2paddle_1272_ones,
                                             y=x2paddle_1252)
x2paddle_1280_ones = fluid.layers.fill_constant(shape=x2paddle_1279,
                                                dtype='int64',
                                                value=1)
x2paddle_1280 = fluid.layers.elementwise_mul(x=x2paddle_1280_ones,
                                             y=x2paddle_1254)
x2paddle_1288_ones = fluid.layers.fill_constant(shape=x2paddle_1287,
                                                dtype='int64',
                                                value=1)
x2paddle_1288 = fluid.layers.elementwise_mul(x=x2paddle_1288_ones,
                                             y=x2paddle_1256)
x2paddle_1296_ones = fluid.layers.fill_constant(shape=x2paddle_1295,
                                                dtype='int64',
                                                value=1)
x2paddle_1296 = fluid.layers.elementwise_mul(x=x2paddle_1296_ones,
                                             y=x2paddle_1258)
x2paddle_1304_ones = fluid.layers.fill_constant(shape=x2paddle_1303,
                                                dtype='int64',
                                                value=1)
x2paddle_1304 = fluid.layers.elementwise_mul(x=x2paddle_1304_ones,
                                             y=x2paddle_1260)
x2paddle_542 = fluid.layers.leaky_relu(x2paddle_541,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_542')
x2paddle_1273 = fluid.layers.unsqueeze(x2paddle_1272,
                                       axes=[-1],
                                       name='x2paddle_1273')
x2paddle_1281 = fluid.layers.unsqueeze(x2paddle_1280,
                                       axes=[-1],
                                       name='x2paddle_1281')
x2paddle_1289 = fluid.layers.unsqueeze(x2paddle_1288,
                                       axes=[-1],
                                       name='x2paddle_1289')
x2paddle_1297 = fluid.layers.unsqueeze(x2paddle_1296,
                                       axes=[-1],
                                       name='x2paddle_1297')
x2paddle_1305 = fluid.layers.unsqueeze(x2paddle_1304,
                                       axes=[-1],
                                       name='x2paddle_1305')
x2paddle_543 = fluid.layers.conv2d(x2paddle_542,
                                   num_filters=128,
                                   filter_size=[1, 1],
                                   stride=[1, 1],
                                   padding=[0, 0],
                                   dilation=[1, 1],
                                   groups=1,
                                   param_attr='x2paddle_model_15_cv3_weight',
                                   name='x2paddle_543',
                                   bias_attr=False)
x2paddle_1306 = fluid.layers.concat(
    [x2paddle_1273, x2paddle_1281, x2paddle_1289, x2paddle_1297, x2paddle_1305],
    axis=-1)
x2paddle_545 = fluid.layers.concat([x2paddle_543, x2paddle_544], axis=1)
x2paddle_1306 = fluid.layers.reshape(x2paddle_1306, shape=[-1, 3, 20, 20, 2, 5])
x2paddle_1314 = fluid.layers.scatter_nd_add(ref=x2paddle_1186,
                                            index=x2paddle_1306,
                                            updates=x2paddle_1313)
x2paddle_546 = fluid.layers.batch_norm(
    x2paddle_545,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_15_bn_weight',
    bias_attr='x2paddle_model_15_bn_bias',
    moving_mean_name='x2paddle_model_15_bn_running_mean',
    moving_variance_name='x2paddle_model_15_bn_running_var',
    use_global_stats=False,
    name='x2paddle_546')
x2paddle_1319 = fluid.layers.strided_slice(x2paddle_1314,
                                           axes=[4],
                                           starts=[2],
                                           ends=[4],
                                           strides=[1])
x2paddle_1338 = fluid.layers.shape(x2paddle_1314)
x2paddle_1338 = fluid.layers.cast(x2paddle_1338, dtype='int64')
x2paddle_1345 = fluid.layers.shape(x2paddle_1314)
x2paddle_1345 = fluid.layers.cast(x2paddle_1345, dtype='int64')
x2paddle_1352 = fluid.layers.shape(x2paddle_1314)
x2paddle_1352 = fluid.layers.cast(x2paddle_1352, dtype='int64')
x2paddle_1359 = fluid.layers.shape(x2paddle_1314)
x2paddle_1359 = fluid.layers.cast(x2paddle_1359, dtype='int64')
x2paddle_1366 = fluid.layers.shape(x2paddle_1314)
x2paddle_1366 = fluid.layers.cast(x2paddle_1366, dtype='int64')
x2paddle_1434 = fluid.layers.shape(x2paddle_1314)
x2paddle_1434 = fluid.layers.cast(x2paddle_1434, dtype='int64')
x2paddle_547 = fluid.layers.leaky_relu(x2paddle_546,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_547')
x2paddle_1321 = fluid.layers.elementwise_mul(x=x2paddle_1319, y=x2paddle_1320)
x2paddle_1340 = fluid.layers.gather(input=x2paddle_1338, index=x2paddle_1339)
x2paddle_1347 = fluid.layers.gather(input=x2paddle_1345, index=x2paddle_1346)
x2paddle_1354 = fluid.layers.gather(input=x2paddle_1352, index=x2paddle_1353)
x2paddle_1361 = fluid.layers.gather(input=x2paddle_1359, index=x2paddle_1360)
x2paddle_1368 = fluid.layers.gather(input=x2paddle_1366, index=x2paddle_1367)
x2paddle_1438 = fluid.layers.slice(x2paddle_1434,
                                   axes=[0],
                                   starts=[4],
                                   ends=[5])
x2paddle_548 = fluid.layers.conv2d(
    x2paddle_547,
    num_filters=256,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_15_cv4_conv_weight',
    name='x2paddle_548',
    bias_attr=False)
x2paddle_1323 = fluid.layers.elementwise_pow(x=x2paddle_1321, y=x2paddle_1322)
x2paddle_1341 = fluid.layers.cast(x2paddle_1340, dtype='int64')
x2paddle_1348 = fluid.layers.cast(x2paddle_1347, dtype='int64')
x2paddle_1355 = fluid.layers.cast(x2paddle_1354, dtype='int64')
x2paddle_1362 = fluid.layers.cast(x2paddle_1361, dtype='int64')
x2paddle_1369 = fluid.layers.cast(x2paddle_1368, dtype='int64')
x2paddle_549 = fluid.layers.batch_norm(
    x2paddle_548,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_15_cv4_bn_weight',
    bias_attr='x2paddle_model_15_cv4_bn_bias',
    moving_mean_name='x2paddle_model_15_cv4_bn_running_mean',
    moving_variance_name='x2paddle_model_15_cv4_bn_running_var',
    use_global_stats=False,
    name='x2paddle_549')
x2paddle_1326 = fluid.layers.elementwise_mul(x=x2paddle_1323, y=x2paddle_1325)
x2paddle_1344 = fluid.layers.range(start=x2paddle_1342,
                                   end=x2paddle_1341,
                                   step=x2paddle_1343,
                                   dtype='int64')
x2paddle_1351 = fluid.layers.range(start=x2paddle_1349,
                                   end=x2paddle_1348,
                                   step=x2paddle_1350,
                                   dtype='int64')
x2paddle_1358 = fluid.layers.range(start=x2paddle_1356,
                                   end=x2paddle_1355,
                                   step=x2paddle_1357,
                                   dtype='int64')
x2paddle_1365 = fluid.layers.range(start=x2paddle_1363,
                                   end=x2paddle_1362,
                                   step=x2paddle_1364,
                                   dtype='int64')
x2paddle_1372 = fluid.layers.range(start=x2paddle_1370,
                                   end=x2paddle_1369,
                                   step=x2paddle_1371,
                                   dtype='int64')
x2paddle_550 = fluid.layers.leaky_relu(x2paddle_549,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_550')
x2paddle_1328 = fluid.layers.reshape(x=x2paddle_1326, shape=[3, 20, 20, 2])
x2paddle_1379 = fluid.layers.reshape(x=x2paddle_1344, shape=[-1, 1, 1, 1, 1])
x2paddle_1381 = fluid.layers.reshape(x=x2paddle_1351, shape=[-1, 1, 1, 1])
x2paddle_1383 = fluid.layers.reshape(x=x2paddle_1358, shape=[-1, 1, 1])
x2paddle_1385 = fluid.layers.reshape(x=x2paddle_1365, shape=[-1, 1])
x2paddle_1377 = fluid.layers.strided_slice(x2paddle_1372,
                                           axes=[0],
                                           starts=[2],
                                           ends=[4],
                                           strides=[1])
x2paddle_551 = fluid.layers.conv2d(x2paddle_550,
                                   num_filters=255,
                                   filter_size=[1, 1],
                                   stride=[1, 1],
                                   padding=[0, 0],
                                   dilation=[1, 1],
                                   groups=1,
                                   param_attr='x2paddle_model_16_weight',
                                   name='x2paddle_551',
                                   bias_attr='x2paddle_model_16_bias')
x2paddle_552 = fluid.layers.shape(x2paddle_550)
x2paddle_552 = fluid.layers.cast(x2paddle_552, dtype='int64')
x2paddle_560 = fluid.layers.shape(x2paddle_550)
x2paddle_560 = fluid.layers.cast(x2paddle_560, dtype='int64')
x2paddle_572 = fluid.layers.shape(x2paddle_550)
x2paddle_572 = fluid.layers.cast(x2paddle_572, dtype='int64')
x2paddle_1337_ones = fluid.layers.fill_constant(shape=x2paddle_1336,
                                                dtype='float32',
                                                value=1)
x2paddle_1337 = fluid.layers.elementwise_mul(x=x2paddle_1337_ones,
                                             y=x2paddle_1328)
x2paddle_1388 = fluid.layers.elementwise_add(x=x2paddle_1379, y=x2paddle_1381)
x2paddle_1387 = fluid.layers.reshape(x=x2paddle_1377, shape=[-1])
x2paddle_885 = fluid.layers.shape(x2paddle_551)
x2paddle_885 = fluid.layers.cast(x2paddle_885, dtype='int64')
x2paddle_888 = fluid.layers.shape(x2paddle_551)
x2paddle_888 = fluid.layers.cast(x2paddle_888, dtype='int64')
x2paddle_891 = fluid.layers.shape(x2paddle_551)
x2paddle_891 = fluid.layers.cast(x2paddle_891, dtype='int64')
x2paddle_554 = fluid.layers.gather(input=x2paddle_552, index=x2paddle_553)
x2paddle_562 = fluid.layers.gather(input=x2paddle_560, index=x2paddle_561)
x2paddle_576 = fluid.layers.slice(x2paddle_572, axes=[0], starts=[0], ends=[2])
x2paddle_1389 = fluid.layers.elementwise_add(x=x2paddle_1388, y=x2paddle_1383)
x2paddle_887 = fluid.layers.gather(input=x2paddle_885, index=x2paddle_886)
x2paddle_890 = fluid.layers.gather(input=x2paddle_888, index=x2paddle_889)
x2paddle_893 = fluid.layers.gather(input=x2paddle_891, index=x2paddle_892)
x2paddle_555 = fluid.layers.cast(x2paddle_554, dtype='float32')
x2paddle_563 = fluid.layers.cast(x2paddle_562, dtype='float32')
x2paddle_1390 = fluid.layers.elementwise_add(x=x2paddle_1389, y=x2paddle_1385)
x2paddle_896 = fluid.layers.reshape(x2paddle_887, shape=[1])
x2paddle_1162 = fluid.layers.reshape(x2paddle_887, shape=[1])
x2paddle_899 = fluid.layers.reshape(x2paddle_890, shape=[1])
x2paddle_900 = fluid.layers.reshape(x2paddle_893, shape=[1])
x2paddle_557 = fluid.layers.elementwise_mul(x=x2paddle_555, y=x2paddle_556)
x2paddle_565 = fluid.layers.elementwise_mul(x=x2paddle_563, y=x2paddle_564)
x2paddle_1391 = fluid.layers.elementwise_add(x=x2paddle_1390, y=x2paddle_1387)
x2paddle_1165 = fluid.layers.concat(
    [x2paddle_1162, x2paddle_1456, x2paddle_1457], axis=0)
x2paddle_901 = fluid.layers.concat(
    [x2paddle_896, x2paddle_1454, x2paddle_1455, x2paddle_899, x2paddle_900],
    axis=0)
x2paddle_558 = fluid.layers.cast(x2paddle_557, dtype='float32')
x2paddle_566 = fluid.layers.cast(x2paddle_565, dtype='float32')
x2paddle_1392 = fluid.layers.shape(x2paddle_1391)
x2paddle_1392 = fluid.layers.cast(x2paddle_1392, dtype='int64')
x2paddle_902 = fluid.layers.reshape(x=x2paddle_551, shape=[-1, 3, 85, 40, 40])
x2paddle_559 = fluid.layers.floor(x2paddle_558, name='x2paddle_559')
x2paddle_567 = fluid.layers.floor(x2paddle_566, name='x2paddle_567')
x2paddle_1393 = fluid.layers.shape(x2paddle_1392)
x2paddle_1393 = fluid.layers.cast(x2paddle_1393, dtype='int64')
x2paddle_1401 = fluid.layers.shape(x2paddle_1392)
x2paddle_1401 = fluid.layers.cast(x2paddle_1401, dtype='int64')
x2paddle_1409 = fluid.layers.shape(x2paddle_1392)
x2paddle_1409 = fluid.layers.cast(x2paddle_1409, dtype='int64')
x2paddle_1417 = fluid.layers.shape(x2paddle_1392)
x2paddle_1417 = fluid.layers.cast(x2paddle_1417, dtype='int64')
x2paddle_1425 = fluid.layers.shape(x2paddle_1392)
x2paddle_1425 = fluid.layers.cast(x2paddle_1425, dtype='int64')
x2paddle_1439 = fluid.layers.concat([x2paddle_1392, x2paddle_1438], axis=0)
x2paddle_903 = fluid.layers.transpose(x2paddle_902,
                                      perm=[0, 1, 3, 4, 2],
                                      name='x2paddle_903')
x2paddle_568 = fluid.layers.reshape(x2paddle_559, shape=[1])
x2paddle_569 = fluid.layers.reshape(x2paddle_567, shape=[1])
x2paddle_1394 = fluid.layers.fill_constant(shape=x2paddle_1393,
                                           dtype='int64',
                                           value=1)
x2paddle_1402 = fluid.layers.fill_constant(shape=x2paddle_1401,
                                           dtype='int64',
                                           value=1)
x2paddle_1410 = fluid.layers.fill_constant(shape=x2paddle_1409,
                                           dtype='int64',
                                           value=1)
x2paddle_1418 = fluid.layers.fill_constant(shape=x2paddle_1417,
                                           dtype='int64',
                                           value=1)
x2paddle_1426 = fluid.layers.fill_constant(shape=x2paddle_1425,
                                           dtype='int64',
                                           value=1)
x2paddle_1440 = fluid.layers.reshape(x=x2paddle_1337, shape=[-1, 3, 20, 20, 2])
x2paddle_904 = fluid.layers.sigmoid(x2paddle_903, name='x2paddle_904')
x2paddle_570 = fluid.layers.concat([x2paddle_568, x2paddle_569], axis=0)
x2paddle_1396 = fluid.layers.elementwise_mul(x=x2paddle_1394, y=x2paddle_1395)
x2paddle_1404 = fluid.layers.elementwise_mul(x=x2paddle_1402, y=x2paddle_1403)
x2paddle_1412 = fluid.layers.elementwise_mul(x=x2paddle_1410, y=x2paddle_1411)
x2paddle_1420 = fluid.layers.elementwise_mul(x=x2paddle_1418, y=x2paddle_1419)
x2paddle_1428 = fluid.layers.elementwise_mul(x=x2paddle_1426, y=x2paddle_1427)
x2paddle_909 = fluid.layers.strided_slice(x2paddle_904,
                                          axes=[4],
                                          starts=[0],
                                          ends=[2],
                                          strides=[1])
x2paddle_929 = fluid.layers.shape(x2paddle_904)
x2paddle_929 = fluid.layers.cast(x2paddle_929, dtype='int64')
x2paddle_936 = fluid.layers.shape(x2paddle_904)
x2paddle_936 = fluid.layers.cast(x2paddle_936, dtype='int64')
x2paddle_943 = fluid.layers.shape(x2paddle_904)
x2paddle_943 = fluid.layers.cast(x2paddle_943, dtype='int64')
x2paddle_950 = fluid.layers.shape(x2paddle_904)
x2paddle_950 = fluid.layers.cast(x2paddle_950, dtype='int64')
x2paddle_957 = fluid.layers.shape(x2paddle_904)
x2paddle_957 = fluid.layers.cast(x2paddle_957, dtype='int64')
x2paddle_1025 = fluid.layers.shape(x2paddle_904)
x2paddle_1025 = fluid.layers.cast(x2paddle_1025, dtype='int64')
x2paddle_577 = fluid.layers.cast(x2paddle_570, dtype='int64')
x2paddle_1397 = fluid.layers.equal(x=x2paddle_1392, y=x2paddle_1396)
x2paddle_1405 = fluid.layers.equal(x=x2paddle_1392, y=x2paddle_1404)
x2paddle_1413 = fluid.layers.equal(x=x2paddle_1392, y=x2paddle_1412)
x2paddle_1421 = fluid.layers.equal(x=x2paddle_1392, y=x2paddle_1420)
x2paddle_1429 = fluid.layers.equal(x=x2paddle_1392, y=x2paddle_1428)
x2paddle_911 = fluid.layers.elementwise_mul(x=x2paddle_909, y=x2paddle_910)
x2paddle_931 = fluid.layers.gather(input=x2paddle_929, index=x2paddle_930)
x2paddle_938 = fluid.layers.gather(input=x2paddle_936, index=x2paddle_937)
x2paddle_945 = fluid.layers.gather(input=x2paddle_943, index=x2paddle_944)
x2paddle_952 = fluid.layers.gather(input=x2paddle_950, index=x2paddle_951)
x2paddle_959 = fluid.layers.gather(input=x2paddle_957, index=x2paddle_958)
x2paddle_1029 = fluid.layers.slice(x2paddle_1025,
                                   axes=[0],
                                   starts=[4],
                                   ends=[5])
x2paddle_578 = fluid.layers.concat([x2paddle_576, x2paddle_577], axis=0)
x2paddle_1397_not = fluid.layers.logical_not(x2paddle_1397)
x2paddle_1397_not_cast = fluid.layers.cast(x2paddle_1397_not, dtype='int64')
x2paddle_1397_cast = fluid.layers.cast(x2paddle_1397, dtype='int64')
x2paddle_1394_mul = fluid.layers.elementwise_mul(x=x2paddle_1394,
                                                 y=x2paddle_1397_cast)
x2paddle_1392_mul = fluid.layers.elementwise_mul(x=x2paddle_1392,
                                                 y=x2paddle_1397_not_cast)
x2paddle_1398 = fluid.layers.elementwise_add(x=x2paddle_1394_mul,
                                             y=x2paddle_1392_mul)
x2paddle_1405_not = fluid.layers.logical_not(x2paddle_1405)
x2paddle_1405_not_cast = fluid.layers.cast(x2paddle_1405_not, dtype='int64')
x2paddle_1405_cast = fluid.layers.cast(x2paddle_1405, dtype='int64')
x2paddle_1402_mul = fluid.layers.elementwise_mul(x=x2paddle_1402,
                                                 y=x2paddle_1405_cast)
x2paddle_1392_mul = fluid.layers.elementwise_mul(x=x2paddle_1392,
                                                 y=x2paddle_1405_not_cast)
x2paddle_1406 = fluid.layers.elementwise_add(x=x2paddle_1402_mul,
                                             y=x2paddle_1392_mul)
x2paddle_1413_not = fluid.layers.logical_not(x2paddle_1413)
x2paddle_1413_not_cast = fluid.layers.cast(x2paddle_1413_not, dtype='int64')
x2paddle_1413_cast = fluid.layers.cast(x2paddle_1413, dtype='int64')
x2paddle_1410_mul = fluid.layers.elementwise_mul(x=x2paddle_1410,
                                                 y=x2paddle_1413_cast)
x2paddle_1392_mul = fluid.layers.elementwise_mul(x=x2paddle_1392,
                                                 y=x2paddle_1413_not_cast)
x2paddle_1414 = fluid.layers.elementwise_add(x=x2paddle_1410_mul,
                                             y=x2paddle_1392_mul)
x2paddle_1421_not = fluid.layers.logical_not(x2paddle_1421)
x2paddle_1421_not_cast = fluid.layers.cast(x2paddle_1421_not, dtype='int64')
x2paddle_1421_cast = fluid.layers.cast(x2paddle_1421, dtype='int64')
x2paddle_1418_mul = fluid.layers.elementwise_mul(x=x2paddle_1418,
                                                 y=x2paddle_1421_cast)
x2paddle_1392_mul = fluid.layers.elementwise_mul(x=x2paddle_1392,
                                                 y=x2paddle_1421_not_cast)
x2paddle_1422 = fluid.layers.elementwise_add(x=x2paddle_1418_mul,
                                             y=x2paddle_1392_mul)
x2paddle_1429_not = fluid.layers.logical_not(x2paddle_1429)
x2paddle_1429_not_cast = fluid.layers.cast(x2paddle_1429_not, dtype='int64')
x2paddle_1429_cast = fluid.layers.cast(x2paddle_1429, dtype='int64')
x2paddle_1426_mul = fluid.layers.elementwise_mul(x=x2paddle_1426,
                                                 y=x2paddle_1429_cast)
x2paddle_1392_mul = fluid.layers.elementwise_mul(x=x2paddle_1392,
                                                 y=x2paddle_1429_not_cast)
x2paddle_1430 = fluid.layers.elementwise_add(x=x2paddle_1426_mul,
                                             y=x2paddle_1392_mul)
x2paddle_913 = fluid.layers.elementwise_sub(x=x2paddle_911, y=x2paddle_912)
x2paddle_932 = fluid.layers.cast(x2paddle_931, dtype='int64')
x2paddle_939 = fluid.layers.cast(x2paddle_938, dtype='int64')
x2paddle_946 = fluid.layers.cast(x2paddle_945, dtype='int64')
x2paddle_953 = fluid.layers.cast(x2paddle_952, dtype='int64')
x2paddle_960 = fluid.layers.cast(x2paddle_959, dtype='int64')
x2paddle_578_nc, x2paddle_578_hw = fluid.layers.split(x2paddle_578,
                                                      dim=0,
                                                      num_or_sections=[2, 2])
x2paddle_578_hw = fluid.layers.cast(x2paddle_578_hw, dtype='int32')
x2paddle_580 = fluid.layers.resize_nearest(input=x2paddle_550,
                                           out_shape=x2paddle_578_hw,
                                           name='x2paddle_580',
                                           align_corners=False)
x2paddle_1399_ones = fluid.layers.fill_constant(shape=x2paddle_1398,
                                                dtype='int64',
                                                value=1)
x2paddle_1399 = fluid.layers.elementwise_mul(x=x2paddle_1399_ones,
                                             y=x2paddle_1379)
x2paddle_1407_ones = fluid.layers.fill_constant(shape=x2paddle_1406,
                                                dtype='int64',
                                                value=1)
x2paddle_1407 = fluid.layers.elementwise_mul(x=x2paddle_1407_ones,
                                             y=x2paddle_1381)
x2paddle_1415_ones = fluid.layers.fill_constant(shape=x2paddle_1414,
                                                dtype='int64',
                                                value=1)
x2paddle_1415 = fluid.layers.elementwise_mul(x=x2paddle_1415_ones,
                                             y=x2paddle_1383)
x2paddle_1423_ones = fluid.layers.fill_constant(shape=x2paddle_1422,
                                                dtype='int64',
                                                value=1)
x2paddle_1423 = fluid.layers.elementwise_mul(x=x2paddle_1423_ones,
                                             y=x2paddle_1385)
x2paddle_1431_ones = fluid.layers.fill_constant(shape=x2paddle_1430,
                                                dtype='int64',
                                                value=1)
x2paddle_1431 = fluid.layers.elementwise_mul(x=x2paddle_1431_ones,
                                             y=x2paddle_1387)
x2paddle_915 = fluid.layers.elementwise_add(x=x2paddle_913, y=x2paddle_914)
x2paddle_935 = fluid.layers.range(start=x2paddle_933,
                                  end=x2paddle_932,
                                  step=x2paddle_934,
                                  dtype='int64')
x2paddle_942 = fluid.layers.range(start=x2paddle_940,
                                  end=x2paddle_939,
                                  step=x2paddle_941,
                                  dtype='int64')
x2paddle_949 = fluid.layers.range(start=x2paddle_947,
                                  end=x2paddle_946,
                                  step=x2paddle_948,
                                  dtype='int64')
x2paddle_956 = fluid.layers.range(start=x2paddle_954,
                                  end=x2paddle_953,
                                  step=x2paddle_955,
                                  dtype='int64')
x2paddle_963 = fluid.layers.range(start=x2paddle_961,
                                  end=x2paddle_960,
                                  step=x2paddle_962,
                                  dtype='int64')
x2paddle_581 = fluid.layers.concat([x2paddle_580, x2paddle_409], axis=1)
x2paddle_1400 = fluid.layers.unsqueeze(x2paddle_1399,
                                       axes=[-1],
                                       name='x2paddle_1400')
x2paddle_1408 = fluid.layers.unsqueeze(x2paddle_1407,
                                       axes=[-1],
                                       name='x2paddle_1408')
x2paddle_1416 = fluid.layers.unsqueeze(x2paddle_1415,
                                       axes=[-1],
                                       name='x2paddle_1416')
x2paddle_1424 = fluid.layers.unsqueeze(x2paddle_1423,
                                       axes=[-1],
                                       name='x2paddle_1424')
x2paddle_1432 = fluid.layers.unsqueeze(x2paddle_1431,
                                       axes=[-1],
                                       name='x2paddle_1432')
x2paddle_917 = fluid.layers.elementwise_mul(x=x2paddle_915, y=x2paddle_916)
x2paddle_970 = fluid.layers.reshape(x=x2paddle_935, shape=[-1, 1, 1, 1, 1])
x2paddle_972 = fluid.layers.reshape(x=x2paddle_942, shape=[-1, 1, 1, 1])
x2paddle_974 = fluid.layers.reshape(x=x2paddle_949, shape=[-1, 1, 1])
x2paddle_976 = fluid.layers.reshape(x=x2paddle_956, shape=[-1, 1])
x2paddle_968 = fluid.layers.strided_slice(x2paddle_963,
                                          axes=[0],
                                          starts=[0],
                                          ends=[2],
                                          strides=[1])
x2paddle_582 = fluid.layers.conv2d(x2paddle_581,
                                   num_filters=128,
                                   filter_size=[1, 1],
                                   stride=[1, 1],
                                   padding=[0, 0],
                                   dilation=[1, 1],
                                   groups=1,
                                   param_attr='x2paddle_model_19_conv_weight',
                                   name='x2paddle_582',
                                   bias_attr=False)
x2paddle_1433 = fluid.layers.concat(
    [x2paddle_1400, x2paddle_1408, x2paddle_1416, x2paddle_1424, x2paddle_1432],
    axis=-1)
x2paddle_919 = fluid.layers.reshape(x=x2paddle_917, shape=[3, 40, 40, 2])
x2paddle_979 = fluid.layers.elementwise_add(x=x2paddle_970, y=x2paddle_972)
x2paddle_978 = fluid.layers.reshape(x=x2paddle_968, shape=[-1])
x2paddle_583 = fluid.layers.batch_norm(
    x2paddle_582,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_19_bn_weight',
    bias_attr='x2paddle_model_19_bn_bias',
    moving_mean_name='x2paddle_model_19_bn_running_mean',
    moving_variance_name='x2paddle_model_19_bn_running_var',
    use_global_stats=False,
    name='x2paddle_583')
x2paddle_1433 = fluid.layers.reshape(x2paddle_1433, shape=[-1, 3, 20, 20, 2, 5])
x2paddle_1441 = fluid.layers.scatter_nd_add(ref=x2paddle_1314,
                                            index=x2paddle_1433,
                                            updates=x2paddle_1440)
x2paddle_928_ones = fluid.layers.fill_constant(shape=x2paddle_927,
                                               dtype='float32',
                                               value=1)
x2paddle_928 = fluid.layers.elementwise_mul(x=x2paddle_928_ones, y=x2paddle_919)
x2paddle_980 = fluid.layers.elementwise_add(x=x2paddle_979, y=x2paddle_974)
x2paddle_584 = fluid.layers.leaky_relu(x2paddle_583,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_584')
x2paddle_1448 = fluid.layers.reshape(x=x2paddle_1441, shape=[-1, 1200, 85])
x2paddle_981 = fluid.layers.elementwise_add(x=x2paddle_980, y=x2paddle_976)
x2paddle_585 = fluid.layers.conv2d(
    x2paddle_584,
    num_filters=64,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_20_cv1_conv_weight',
    name='x2paddle_585',
    bias_attr=False)
x2paddle_595 = fluid.layers.conv2d(x2paddle_584,
                                   num_filters=64,
                                   filter_size=[1, 1],
                                   stride=[1, 1],
                                   padding=[0, 0],
                                   dilation=[1, 1],
                                   groups=1,
                                   param_attr='x2paddle_model_20_cv2_weight',
                                   name='x2paddle_595',
                                   bias_attr=False)
x2paddle_982 = fluid.layers.elementwise_add(x=x2paddle_981, y=x2paddle_978)
x2paddle_586 = fluid.layers.batch_norm(
    x2paddle_585,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_20_cv1_bn_weight',
    bias_attr='x2paddle_model_20_cv1_bn_bias',
    moving_mean_name='x2paddle_model_20_cv1_bn_running_mean',
    moving_variance_name='x2paddle_model_20_cv1_bn_running_var',
    use_global_stats=False,
    name='x2paddle_586')
x2paddle_983 = fluid.layers.shape(x2paddle_982)
x2paddle_983 = fluid.layers.cast(x2paddle_983, dtype='int64')
x2paddle_587 = fluid.layers.leaky_relu(x2paddle_586,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_587')
x2paddle_984 = fluid.layers.shape(x2paddle_983)
x2paddle_984 = fluid.layers.cast(x2paddle_984, dtype='int64')
x2paddle_992 = fluid.layers.shape(x2paddle_983)
x2paddle_992 = fluid.layers.cast(x2paddle_992, dtype='int64')
x2paddle_1000 = fluid.layers.shape(x2paddle_983)
x2paddle_1000 = fluid.layers.cast(x2paddle_1000, dtype='int64')
x2paddle_1008 = fluid.layers.shape(x2paddle_983)
x2paddle_1008 = fluid.layers.cast(x2paddle_1008, dtype='int64')
x2paddle_1016 = fluid.layers.shape(x2paddle_983)
x2paddle_1016 = fluid.layers.cast(x2paddle_1016, dtype='int64')
x2paddle_1030 = fluid.layers.concat([x2paddle_983, x2paddle_1029], axis=0)
x2paddle_588 = fluid.layers.conv2d(
    x2paddle_587,
    num_filters=64,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_20_m_0_cv1_conv_weight',
    name='x2paddle_588',
    bias_attr=False)
x2paddle_985 = fluid.layers.fill_constant(shape=x2paddle_984,
                                          dtype='int64',
                                          value=1)
x2paddle_993 = fluid.layers.fill_constant(shape=x2paddle_992,
                                          dtype='int64',
                                          value=1)
x2paddle_1001 = fluid.layers.fill_constant(shape=x2paddle_1000,
                                           dtype='int64',
                                           value=1)
x2paddle_1009 = fluid.layers.fill_constant(shape=x2paddle_1008,
                                           dtype='int64',
                                           value=1)
x2paddle_1017 = fluid.layers.fill_constant(shape=x2paddle_1016,
                                           dtype='int64',
                                           value=1)
x2paddle_1031 = fluid.layers.reshape(x=x2paddle_928, shape=[-1, 3, 40, 40, 2])
x2paddle_589 = fluid.layers.batch_norm(
    x2paddle_588,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_20_m_0_cv1_bn_weight',
    bias_attr='x2paddle_model_20_m_0_cv1_bn_bias',
    moving_mean_name='x2paddle_model_20_m_0_cv1_bn_running_mean',
    moving_variance_name='x2paddle_model_20_m_0_cv1_bn_running_var',
    use_global_stats=False,
    name='x2paddle_589')
x2paddle_987 = fluid.layers.elementwise_mul(x=x2paddle_985, y=x2paddle_986)
x2paddle_995 = fluid.layers.elementwise_mul(x=x2paddle_993, y=x2paddle_994)
x2paddle_1003 = fluid.layers.elementwise_mul(x=x2paddle_1001, y=x2paddle_1002)
x2paddle_1011 = fluid.layers.elementwise_mul(x=x2paddle_1009, y=x2paddle_1010)
x2paddle_1019 = fluid.layers.elementwise_mul(x=x2paddle_1017, y=x2paddle_1018)
x2paddle_590 = fluid.layers.leaky_relu(x2paddle_589,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_590')
x2paddle_988 = fluid.layers.equal(x=x2paddle_983, y=x2paddle_987)
x2paddle_996 = fluid.layers.equal(x=x2paddle_983, y=x2paddle_995)
x2paddle_1004 = fluid.layers.equal(x=x2paddle_983, y=x2paddle_1003)
x2paddle_1012 = fluid.layers.equal(x=x2paddle_983, y=x2paddle_1011)
x2paddle_1020 = fluid.layers.equal(x=x2paddle_983, y=x2paddle_1019)
x2paddle_591 = fluid.layers.conv2d(
    x2paddle_590,
    num_filters=64,
    filter_size=[3, 3],
    stride=[1, 1],
    padding=[1, 1],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_20_m_0_cv2_conv_weight',
    name='x2paddle_591',
    bias_attr=False)
x2paddle_988_not = fluid.layers.logical_not(x2paddle_988)
x2paddle_988_not_cast = fluid.layers.cast(x2paddle_988_not, dtype='int64')
x2paddle_988_cast = fluid.layers.cast(x2paddle_988, dtype='int64')
x2paddle_985_mul = fluid.layers.elementwise_mul(x=x2paddle_985,
                                                y=x2paddle_988_cast)
x2paddle_983_mul = fluid.layers.elementwise_mul(x=x2paddle_983,
                                                y=x2paddle_988_not_cast)
x2paddle_989 = fluid.layers.elementwise_add(x=x2paddle_985_mul,
                                            y=x2paddle_983_mul)
x2paddle_996_not = fluid.layers.logical_not(x2paddle_996)
x2paddle_996_not_cast = fluid.layers.cast(x2paddle_996_not, dtype='int64')
x2paddle_996_cast = fluid.layers.cast(x2paddle_996, dtype='int64')
x2paddle_993_mul = fluid.layers.elementwise_mul(x=x2paddle_993,
                                                y=x2paddle_996_cast)
x2paddle_983_mul = fluid.layers.elementwise_mul(x=x2paddle_983,
                                                y=x2paddle_996_not_cast)
x2paddle_997 = fluid.layers.elementwise_add(x=x2paddle_993_mul,
                                            y=x2paddle_983_mul)
x2paddle_1004_not = fluid.layers.logical_not(x2paddle_1004)
x2paddle_1004_not_cast = fluid.layers.cast(x2paddle_1004_not, dtype='int64')
x2paddle_1004_cast = fluid.layers.cast(x2paddle_1004, dtype='int64')
x2paddle_1001_mul = fluid.layers.elementwise_mul(x=x2paddle_1001,
                                                 y=x2paddle_1004_cast)
x2paddle_983_mul = fluid.layers.elementwise_mul(x=x2paddle_983,
                                                y=x2paddle_1004_not_cast)
x2paddle_1005 = fluid.layers.elementwise_add(x=x2paddle_1001_mul,
                                             y=x2paddle_983_mul)
x2paddle_1012_not = fluid.layers.logical_not(x2paddle_1012)
x2paddle_1012_not_cast = fluid.layers.cast(x2paddle_1012_not, dtype='int64')
x2paddle_1012_cast = fluid.layers.cast(x2paddle_1012, dtype='int64')
x2paddle_1009_mul = fluid.layers.elementwise_mul(x=x2paddle_1009,
                                                 y=x2paddle_1012_cast)
x2paddle_983_mul = fluid.layers.elementwise_mul(x=x2paddle_983,
                                                y=x2paddle_1012_not_cast)
x2paddle_1013 = fluid.layers.elementwise_add(x=x2paddle_1009_mul,
                                             y=x2paddle_983_mul)
x2paddle_1020_not = fluid.layers.logical_not(x2paddle_1020)
x2paddle_1020_not_cast = fluid.layers.cast(x2paddle_1020_not, dtype='int64')
x2paddle_1020_cast = fluid.layers.cast(x2paddle_1020, dtype='int64')
x2paddle_1017_mul = fluid.layers.elementwise_mul(x=x2paddle_1017,
                                                 y=x2paddle_1020_cast)
x2paddle_983_mul = fluid.layers.elementwise_mul(x=x2paddle_983,
                                                y=x2paddle_1020_not_cast)
x2paddle_1021 = fluid.layers.elementwise_add(x=x2paddle_1017_mul,
                                             y=x2paddle_983_mul)
x2paddle_592 = fluid.layers.batch_norm(
    x2paddle_591,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_20_m_0_cv2_bn_weight',
    bias_attr='x2paddle_model_20_m_0_cv2_bn_bias',
    moving_mean_name='x2paddle_model_20_m_0_cv2_bn_running_mean',
    moving_variance_name='x2paddle_model_20_m_0_cv2_bn_running_var',
    use_global_stats=False,
    name='x2paddle_592')
x2paddle_990_ones = fluid.layers.fill_constant(shape=x2paddle_989,
                                               dtype='int64',
                                               value=1)
x2paddle_990 = fluid.layers.elementwise_mul(x=x2paddle_990_ones, y=x2paddle_970)
x2paddle_998_ones = fluid.layers.fill_constant(shape=x2paddle_997,
                                               dtype='int64',
                                               value=1)
x2paddle_998 = fluid.layers.elementwise_mul(x=x2paddle_998_ones, y=x2paddle_972)
x2paddle_1006_ones = fluid.layers.fill_constant(shape=x2paddle_1005,
                                                dtype='int64',
                                                value=1)
x2paddle_1006 = fluid.layers.elementwise_mul(x=x2paddle_1006_ones,
                                             y=x2paddle_974)
x2paddle_1014_ones = fluid.layers.fill_constant(shape=x2paddle_1013,
                                                dtype='int64',
                                                value=1)
x2paddle_1014 = fluid.layers.elementwise_mul(x=x2paddle_1014_ones,
                                             y=x2paddle_976)
x2paddle_1022_ones = fluid.layers.fill_constant(shape=x2paddle_1021,
                                                dtype='int64',
                                                value=1)
x2paddle_1022 = fluid.layers.elementwise_mul(x=x2paddle_1022_ones,
                                             y=x2paddle_978)
x2paddle_593 = fluid.layers.leaky_relu(x2paddle_592,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_593')
x2paddle_991 = fluid.layers.unsqueeze(x2paddle_990,
                                      axes=[-1],
                                      name='x2paddle_991')
x2paddle_999 = fluid.layers.unsqueeze(x2paddle_998,
                                      axes=[-1],
                                      name='x2paddle_999')
x2paddle_1007 = fluid.layers.unsqueeze(x2paddle_1006,
                                       axes=[-1],
                                       name='x2paddle_1007')
x2paddle_1015 = fluid.layers.unsqueeze(x2paddle_1014,
                                       axes=[-1],
                                       name='x2paddle_1015')
x2paddle_1023 = fluid.layers.unsqueeze(x2paddle_1022,
                                       axes=[-1],
                                       name='x2paddle_1023')
x2paddle_594 = fluid.layers.conv2d(x2paddle_593,
                                   num_filters=64,
                                   filter_size=[1, 1],
                                   stride=[1, 1],
                                   padding=[0, 0],
                                   dilation=[1, 1],
                                   groups=1,
                                   param_attr='x2paddle_model_20_cv3_weight',
                                   name='x2paddle_594',
                                   bias_attr=False)
x2paddle_1024 = fluid.layers.concat(
    [x2paddle_991, x2paddle_999, x2paddle_1007, x2paddle_1015, x2paddle_1023],
    axis=-1)
x2paddle_596 = fluid.layers.concat([x2paddle_594, x2paddle_595], axis=1)
x2paddle_1024 = fluid.layers.reshape(x2paddle_1024, shape=[-1, 3, 40, 40, 2, 5])
x2paddle_1032 = fluid.layers.scatter_nd_add(ref=x2paddle_904,
                                            index=x2paddle_1024,
                                            updates=x2paddle_1031)
x2paddle_597 = fluid.layers.batch_norm(
    x2paddle_596,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_20_bn_weight',
    bias_attr='x2paddle_model_20_bn_bias',
    moving_mean_name='x2paddle_model_20_bn_running_mean',
    moving_variance_name='x2paddle_model_20_bn_running_var',
    use_global_stats=False,
    name='x2paddle_597')
x2paddle_1037 = fluid.layers.strided_slice(x2paddle_1032,
                                           axes=[4],
                                           starts=[2],
                                           ends=[4],
                                           strides=[1])
x2paddle_1056 = fluid.layers.shape(x2paddle_1032)
x2paddle_1056 = fluid.layers.cast(x2paddle_1056, dtype='int64')
x2paddle_1063 = fluid.layers.shape(x2paddle_1032)
x2paddle_1063 = fluid.layers.cast(x2paddle_1063, dtype='int64')
x2paddle_1070 = fluid.layers.shape(x2paddle_1032)
x2paddle_1070 = fluid.layers.cast(x2paddle_1070, dtype='int64')
x2paddle_1077 = fluid.layers.shape(x2paddle_1032)
x2paddle_1077 = fluid.layers.cast(x2paddle_1077, dtype='int64')
x2paddle_1084 = fluid.layers.shape(x2paddle_1032)
x2paddle_1084 = fluid.layers.cast(x2paddle_1084, dtype='int64')
x2paddle_1152 = fluid.layers.shape(x2paddle_1032)
x2paddle_1152 = fluid.layers.cast(x2paddle_1152, dtype='int64')
x2paddle_598 = fluid.layers.leaky_relu(x2paddle_597,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_598')
x2paddle_1039 = fluid.layers.elementwise_mul(x=x2paddle_1037, y=x2paddle_1038)
x2paddle_1058 = fluid.layers.gather(input=x2paddle_1056, index=x2paddle_1057)
x2paddle_1065 = fluid.layers.gather(input=x2paddle_1063, index=x2paddle_1064)
x2paddle_1072 = fluid.layers.gather(input=x2paddle_1070, index=x2paddle_1071)
x2paddle_1079 = fluid.layers.gather(input=x2paddle_1077, index=x2paddle_1078)
x2paddle_1086 = fluid.layers.gather(input=x2paddle_1084, index=x2paddle_1085)
x2paddle_1156 = fluid.layers.slice(x2paddle_1152,
                                   axes=[0],
                                   starts=[4],
                                   ends=[5])
x2paddle_599 = fluid.layers.conv2d(
    x2paddle_598,
    num_filters=128,
    filter_size=[1, 1],
    stride=[1, 1],
    padding=[0, 0],
    dilation=[1, 1],
    groups=1,
    param_attr='x2paddle_model_20_cv4_conv_weight',
    name='x2paddle_599',
    bias_attr=False)
x2paddle_1041 = fluid.layers.elementwise_pow(x=x2paddle_1039, y=x2paddle_1040)
x2paddle_1059 = fluid.layers.cast(x2paddle_1058, dtype='int64')
x2paddle_1066 = fluid.layers.cast(x2paddle_1065, dtype='int64')
x2paddle_1073 = fluid.layers.cast(x2paddle_1072, dtype='int64')
x2paddle_1080 = fluid.layers.cast(x2paddle_1079, dtype='int64')
x2paddle_1087 = fluid.layers.cast(x2paddle_1086, dtype='int64')
x2paddle_600 = fluid.layers.batch_norm(
    x2paddle_599,
    momentum=0.9700000286102295,
    epsilon=9.999999747378752e-05,
    data_layout='NCHW',
    is_test=True,
    param_attr='x2paddle_model_20_cv4_bn_weight',
    bias_attr='x2paddle_model_20_cv4_bn_bias',
    moving_mean_name='x2paddle_model_20_cv4_bn_running_mean',
    moving_variance_name='x2paddle_model_20_cv4_bn_running_var',
    use_global_stats=False,
    name='x2paddle_600')
x2paddle_1044 = fluid.layers.elementwise_mul(x=x2paddle_1041, y=x2paddle_1043)
x2paddle_1062 = fluid.layers.range(start=x2paddle_1060,
                                   end=x2paddle_1059,
                                   step=x2paddle_1061,
                                   dtype='int64')
x2paddle_1069 = fluid.layers.range(start=x2paddle_1067,
                                   end=x2paddle_1066,
                                   step=x2paddle_1068,
                                   dtype='int64')
x2paddle_1076 = fluid.layers.range(start=x2paddle_1074,
                                   end=x2paddle_1073,
                                   step=x2paddle_1075,
                                   dtype='int64')
x2paddle_1083 = fluid.layers.range(start=x2paddle_1081,
                                   end=x2paddle_1080,
                                   step=x2paddle_1082,
                                   dtype='int64')
x2paddle_1090 = fluid.layers.range(start=x2paddle_1088,
                                   end=x2paddle_1087,
                                   step=x2paddle_1089,
                                   dtype='int64')
x2paddle_601 = fluid.layers.leaky_relu(x2paddle_600,
                                       alpha=0.10000000149011612,
                                       name='x2paddle_601')
x2paddle_1046 = fluid.layers.reshape(x=x2paddle_1044, shape=[3, 40, 40, 2])
x2paddle_1097 = fluid.layers.reshape(x=x2paddle_1062, shape=[-1, 1, 1, 1, 1])
x2paddle_1099 = fluid.layers.reshape(x=x2paddle_1069, shape=[-1, 1, 1, 1])
x2paddle_1101 = fluid.layers.reshape(x=x2paddle_1076, shape=[-1, 1, 1])
x2paddle_1103 = fluid.layers.reshape(x=x2paddle_1083, shape=[-1, 1])
x2paddle_1095 = fluid.layers.strided_slice(x2paddle_1090,
                                           axes=[0],
                                           starts=[2],
                                           ends=[4],
                                           strides=[1])
x2paddle_602 = fluid.layers.conv2d(x2paddle_601,
                                   num_filters=255,
                                   filter_size=[1, 1],
                                   stride=[1, 1],
                                   padding=[0, 0],
                                   dilation=[1, 1],
                                   groups=1,
                                   param_attr='x2paddle_model_21_weight',
                                   name='x2paddle_602',
                                   bias_attr='x2paddle_model_21_bias')
x2paddle_1055_ones = fluid.layers.fill_constant(shape=x2paddle_1054,
                                                dtype='float32',
                                                value=1)
x2paddle_1055 = fluid.layers.elementwise_mul(x=x2paddle_1055_ones,
                                             y=x2paddle_1046)
x2paddle_1106 = fluid.layers.elementwise_add(x=x2paddle_1097, y=x2paddle_1099)
x2paddle_1105 = fluid.layers.reshape(x=x2paddle_1095, shape=[-1])
x2paddle_603 = fluid.layers.shape(x2paddle_602)
x2paddle_603 = fluid.layers.cast(x2paddle_603, dtype='int64')
x2paddle_606 = fluid.layers.shape(x2paddle_602)
x2paddle_606 = fluid.layers.cast(x2paddle_606, dtype='int64')
x2paddle_609 = fluid.layers.shape(x2paddle_602)
x2paddle_609 = fluid.layers.cast(x2paddle_609, dtype='int64')
x2paddle_1107 = fluid.layers.elementwise_add(x=x2paddle_1106, y=x2paddle_1101)
x2paddle_605 = fluid.layers.gather(input=x2paddle_603, index=x2paddle_604)
x2paddle_608 = fluid.layers.gather(input=x2paddle_606, index=x2paddle_607)
x2paddle_611 = fluid.layers.gather(input=x2paddle_609, index=x2paddle_610)
x2paddle_1108 = fluid.layers.elementwise_add(x=x2paddle_1107, y=x2paddle_1103)
x2paddle_614 = fluid.layers.reshape(x2paddle_605, shape=[1])
x2paddle_880 = fluid.layers.reshape(x2paddle_605, shape=[1])
x2paddle_617 = fluid.layers.reshape(x2paddle_608, shape=[1])
x2paddle_618 = fluid.layers.reshape(x2paddle_611, shape=[1])
x2paddle_1109 = fluid.layers.elementwise_add(x=x2paddle_1108, y=x2paddle_1105)
x2paddle_883 = fluid.layers.concat([x2paddle_880, x2paddle_1452, x2paddle_1453],
                                   axis=0)
x2paddle_619 = fluid.layers.concat(
    [x2paddle_614, x2paddle_1450, x2paddle_1451, x2paddle_617, x2paddle_618],
    axis=0)
x2paddle_1110 = fluid.layers.shape(x2paddle_1109)
x2paddle_1110 = fluid.layers.cast(x2paddle_1110, dtype='int64')
x2paddle_620 = fluid.layers.reshape(x=x2paddle_602, shape=[-1, 3, 85, 80, 80])
x2paddle_1111 = fluid.layers.shape(x2paddle_1110)
x2paddle_1111 = fluid.layers.cast(x2paddle_1111, dtype='int64')
x2paddle_1119 = fluid.layers.shape(x2paddle_1110)
x2paddle_1119 = fluid.layers.cast(x2paddle_1119, dtype='int64')
x2paddle_1127 = fluid.layers.shape(x2paddle_1110)
x2paddle_1127 = fluid.layers.cast(x2paddle_1127, dtype='int64')
x2paddle_1135 = fluid.layers.shape(x2paddle_1110)
x2paddle_1135 = fluid.layers.cast(x2paddle_1135, dtype='int64')
x2paddle_1143 = fluid.layers.shape(x2paddle_1110)
x2paddle_1143 = fluid.layers.cast(x2paddle_1143, dtype='int64')
x2paddle_1157 = fluid.layers.concat([x2paddle_1110, x2paddle_1156], axis=0)
x2paddle_621 = fluid.layers.transpose(x2paddle_620,
                                      perm=[0, 1, 3, 4, 2],
                                      name='x2paddle_621')
x2paddle_1112 = fluid.layers.fill_constant(shape=x2paddle_1111,
                                           dtype='int64',
                                           value=1)
x2paddle_1120 = fluid.layers.fill_constant(shape=x2paddle_1119,
                                           dtype='int64',
                                           value=1)
x2paddle_1128 = fluid.layers.fill_constant(shape=x2paddle_1127,
                                           dtype='int64',
                                           value=1)
x2paddle_1136 = fluid.layers.fill_constant(shape=x2paddle_1135,
                                           dtype='int64',
                                           value=1)
x2paddle_1144 = fluid.layers.fill_constant(shape=x2paddle_1143,
                                           dtype='int64',
                                           value=1)
x2paddle_1158 = fluid.layers.reshape(x=x2paddle_1055, shape=[-1, 3, 40, 40, 2])
x2paddle_622 = fluid.layers.sigmoid(x2paddle_621, name='x2paddle_622')
x2paddle_1114 = fluid.layers.elementwise_mul(x=x2paddle_1112, y=x2paddle_1113)
x2paddle_1122 = fluid.layers.elementwise_mul(x=x2paddle_1120, y=x2paddle_1121)
x2paddle_1130 = fluid.layers.elementwise_mul(x=x2paddle_1128, y=x2paddle_1129)
x2paddle_1138 = fluid.layers.elementwise_mul(x=x2paddle_1136, y=x2paddle_1137)
x2paddle_1146 = fluid.layers.elementwise_mul(x=x2paddle_1144, y=x2paddle_1145)
x2paddle_627 = fluid.layers.strided_slice(x2paddle_622,
                                          axes=[4],
                                          starts=[0],
                                          ends=[2],
                                          strides=[1])
x2paddle_647 = fluid.layers.shape(x2paddle_622)
x2paddle_647 = fluid.layers.cast(x2paddle_647, dtype='int64')
x2paddle_654 = fluid.layers.shape(x2paddle_622)
x2paddle_654 = fluid.layers.cast(x2paddle_654, dtype='int64')
x2paddle_661 = fluid.layers.shape(x2paddle_622)
x2paddle_661 = fluid.layers.cast(x2paddle_661, dtype='int64')
x2paddle_668 = fluid.layers.shape(x2paddle_622)
x2paddle_668 = fluid.layers.cast(x2paddle_668, dtype='int64')
x2paddle_675 = fluid.layers.shape(x2paddle_622)
x2paddle_675 = fluid.layers.cast(x2paddle_675, dtype='int64')
x2paddle_743 = fluid.layers.shape(x2paddle_622)
x2paddle_743 = fluid.layers.cast(x2paddle_743, dtype='int64')
x2paddle_1115 = fluid.layers.equal(x=x2paddle_1110, y=x2paddle_1114)
x2paddle_1123 = fluid.layers.equal(x=x2paddle_1110, y=x2paddle_1122)
x2paddle_1131 = fluid.layers.equal(x=x2paddle_1110, y=x2paddle_1130)
x2paddle_1139 = fluid.layers.equal(x=x2paddle_1110, y=x2paddle_1138)
x2paddle_1147 = fluid.layers.equal(x=x2paddle_1110, y=x2paddle_1146)
x2paddle_629 = fluid.layers.elementwise_mul(x=x2paddle_627, y=x2paddle_628)
x2paddle_649 = fluid.layers.gather(input=x2paddle_647, index=x2paddle_648)
x2paddle_656 = fluid.layers.gather(input=x2paddle_654, index=x2paddle_655)
x2paddle_663 = fluid.layers.gather(input=x2paddle_661, index=x2paddle_662)
x2paddle_670 = fluid.layers.gather(input=x2paddle_668, index=x2paddle_669)
x2paddle_677 = fluid.layers.gather(input=x2paddle_675, index=x2paddle_676)
x2paddle_747 = fluid.layers.slice(x2paddle_743, axes=[0], starts=[4], ends=[5])
x2paddle_1115_not = fluid.layers.logical_not(x2paddle_1115)
x2paddle_1115_not_cast = fluid.layers.cast(x2paddle_1115_not, dtype='int64')
x2paddle_1115_cast = fluid.layers.cast(x2paddle_1115, dtype='int64')
x2paddle_1112_mul = fluid.layers.elementwise_mul(x=x2paddle_1112,
                                                 y=x2paddle_1115_cast)
x2paddle_1110_mul = fluid.layers.elementwise_mul(x=x2paddle_1110,
                                                 y=x2paddle_1115_not_cast)
x2paddle_1116 = fluid.layers.elementwise_add(x=x2paddle_1112_mul,
                                             y=x2paddle_1110_mul)
x2paddle_1123_not = fluid.layers.logical_not(x2paddle_1123)
x2paddle_1123_not_cast = fluid.layers.cast(x2paddle_1123_not, dtype='int64')
x2paddle_1123_cast = fluid.layers.cast(x2paddle_1123, dtype='int64')
x2paddle_1120_mul = fluid.layers.elementwise_mul(x=x2paddle_1120,
                                                 y=x2paddle_1123_cast)
x2paddle_1110_mul = fluid.layers.elementwise_mul(x=x2paddle_1110,
                                                 y=x2paddle_1123_not_cast)
x2paddle_1124 = fluid.layers.elementwise_add(x=x2paddle_1120_mul,
                                             y=x2paddle_1110_mul)
x2paddle_1131_not = fluid.layers.logical_not(x2paddle_1131)
x2paddle_1131_not_cast = fluid.layers.cast(x2paddle_1131_not, dtype='int64')
x2paddle_1131_cast = fluid.layers.cast(x2paddle_1131, dtype='int64')
x2paddle_1128_mul = fluid.layers.elementwise_mul(x=x2paddle_1128,
                                                 y=x2paddle_1131_cast)
x2paddle_1110_mul = fluid.layers.elementwise_mul(x=x2paddle_1110,
                                                 y=x2paddle_1131_not_cast)
x2paddle_1132 = fluid.layers.elementwise_add(x=x2paddle_1128_mul,
                                             y=x2paddle_1110_mul)
x2paddle_1139_not = fluid.layers.logical_not(x2paddle_1139)
x2paddle_1139_not_cast = fluid.layers.cast(x2paddle_1139_not, dtype='int64')
x2paddle_1139_cast = fluid.layers.cast(x2paddle_1139, dtype='int64')
x2paddle_1136_mul = fluid.layers.elementwise_mul(x=x2paddle_1136,
                                                 y=x2paddle_1139_cast)
x2paddle_1110_mul = fluid.layers.elementwise_mul(x=x2paddle_1110,
                                                 y=x2paddle_1139_not_cast)
x2paddle_1140 = fluid.layers.elementwise_add(x=x2paddle_1136_mul,
                                             y=x2paddle_1110_mul)
x2paddle_1147_not = fluid.layers.logical_not(x2paddle_1147)
x2paddle_1147_not_cast = fluid.layers.cast(x2paddle_1147_not, dtype='int64')
x2paddle_1147_cast = fluid.layers.cast(x2paddle_1147, dtype='int64')
x2paddle_1144_mul = fluid.layers.elementwise_mul(x=x2paddle_1144,
                                                 y=x2paddle_1147_cast)
x2paddle_1110_mul = fluid.layers.elementwise_mul(x=x2paddle_1110,
                                                 y=x2paddle_1147_not_cast)
x2paddle_1148 = fluid.layers.elementwise_add(x=x2paddle_1144_mul,
                                             y=x2paddle_1110_mul)
x2paddle_631 = fluid.layers.elementwise_sub(x=x2paddle_629, y=x2paddle_630)
x2paddle_650 = fluid.layers.cast(x2paddle_649, dtype='int64')
x2paddle_657 = fluid.layers.cast(x2paddle_656, dtype='int64')
x2paddle_664 = fluid.layers.cast(x2paddle_663, dtype='int64')
x2paddle_671 = fluid.layers.cast(x2paddle_670, dtype='int64')
x2paddle_678 = fluid.layers.cast(x2paddle_677, dtype='int64')
x2paddle_1117_ones = fluid.layers.fill_constant(shape=x2paddle_1116,
                                                dtype='int64',
                                                value=1)
x2paddle_1117 = fluid.layers.elementwise_mul(x=x2paddle_1117_ones,
                                             y=x2paddle_1097)
x2paddle_1125_ones = fluid.layers.fill_constant(shape=x2paddle_1124,
                                                dtype='int64',
                                                value=1)
x2paddle_1125 = fluid.layers.elementwise_mul(x=x2paddle_1125_ones,
                                             y=x2paddle_1099)
x2paddle_1133_ones = fluid.layers.fill_constant(shape=x2paddle_1132,
                                                dtype='int64',
                                                value=1)
x2paddle_1133 = fluid.layers.elementwise_mul(x=x2paddle_1133_ones,
                                             y=x2paddle_1101)
x2paddle_1141_ones = fluid.layers.fill_constant(shape=x2paddle_1140,
                                                dtype='int64',
                                                value=1)
x2paddle_1141 = fluid.layers.elementwise_mul(x=x2paddle_1141_ones,
                                             y=x2paddle_1103)
x2paddle_1149_ones = fluid.layers.fill_constant(shape=x2paddle_1148,
                                                dtype='int64',
                                                value=1)
x2paddle_1149 = fluid.layers.elementwise_mul(x=x2paddle_1149_ones,
                                             y=x2paddle_1105)
x2paddle_633 = fluid.layers.elementwise_add(x=x2paddle_631, y=x2paddle_632)
x2paddle_653 = fluid.layers.range(start=x2paddle_651,
                                  end=x2paddle_650,
                                  step=x2paddle_652,
                                  dtype='int64')
x2paddle_660 = fluid.layers.range(start=x2paddle_658,
                                  end=x2paddle_657,
                                  step=x2paddle_659,
                                  dtype='int64')
x2paddle_667 = fluid.layers.range(start=x2paddle_665,
                                  end=x2paddle_664,
                                  step=x2paddle_666,
                                  dtype='int64')
x2paddle_674 = fluid.layers.range(start=x2paddle_672,
                                  end=x2paddle_671,
                                  step=x2paddle_673,
                                  dtype='int64')
x2paddle_681 = fluid.layers.range(start=x2paddle_679,
                                  end=x2paddle_678,
                                  step=x2paddle_680,
                                  dtype='int64')
x2paddle_1118 = fluid.layers.unsqueeze(x2paddle_1117,
                                       axes=[-1],
                                       name='x2paddle_1118')
x2paddle_1126 = fluid.layers.unsqueeze(x2paddle_1125,
                                       axes=[-1],
                                       name='x2paddle_1126')
x2paddle_1134 = fluid.layers.unsqueeze(x2paddle_1133,
                                       axes=[-1],
                                       name='x2paddle_1134')
x2paddle_1142 = fluid.layers.unsqueeze(x2paddle_1141,
                                       axes=[-1],
                                       name='x2paddle_1142')
x2paddle_1150 = fluid.layers.unsqueeze(x2paddle_1149,
                                       axes=[-1],
                                       name='x2paddle_1150')
x2paddle_635 = fluid.layers.elementwise_mul(x=x2paddle_633, y=x2paddle_634)
x2paddle_688 = fluid.layers.reshape(x=x2paddle_653, shape=[-1, 1, 1, 1, 1])
x2paddle_690 = fluid.layers.reshape(x=x2paddle_660, shape=[-1, 1, 1, 1])
x2paddle_692 = fluid.layers.reshape(x=x2paddle_667, shape=[-1, 1, 1])
x2paddle_694 = fluid.layers.reshape(x=x2paddle_674, shape=[-1, 1])
x2paddle_686 = fluid.layers.strided_slice(x2paddle_681,
                                          axes=[0],
                                          starts=[0],
                                          ends=[2],
                                          strides=[1])
x2paddle_1151 = fluid.layers.concat(
    [x2paddle_1118, x2paddle_1126, x2paddle_1134, x2paddle_1142, x2paddle_1150],
    axis=-1)
x2paddle_637 = fluid.layers.reshape(x=x2paddle_635, shape=[3, 80, 80, 2])
x2paddle_697 = fluid.layers.elementwise_add(x=x2paddle_688, y=x2paddle_690)
x2paddle_696 = fluid.layers.reshape(x=x2paddle_686, shape=[-1])
x2paddle_1151 = fluid.layers.reshape(x2paddle_1151, shape=[-1, 3, 40, 40, 2, 5])
x2paddle_1159 = fluid.layers.scatter_nd_add(ref=x2paddle_1032,
                                            index=x2paddle_1151,
                                            updates=x2paddle_1158)
x2paddle_646_ones = fluid.layers.fill_constant(shape=x2paddle_645,
                                               dtype='float32',
                                               value=1)
x2paddle_646 = fluid.layers.elementwise_mul(x=x2paddle_646_ones, y=x2paddle_637)
x2paddle_698 = fluid.layers.elementwise_add(x=x2paddle_697, y=x2paddle_692)
x2paddle_1166 = fluid.layers.reshape(x=x2paddle_1159, shape=[-1, 4800, 85])
x2paddle_699 = fluid.layers.elementwise_add(x=x2paddle_698, y=x2paddle_694)
x2paddle_700 = fluid.layers.elementwise_add(x=x2paddle_699, y=x2paddle_696)
x2paddle_701 = fluid.layers.shape(x2paddle_700)
x2paddle_701 = fluid.layers.cast(x2paddle_701, dtype='int64')
x2paddle_702 = fluid.layers.shape(x2paddle_701)
x2paddle_702 = fluid.layers.cast(x2paddle_702, dtype='int64')
x2paddle_710 = fluid.layers.shape(x2paddle_701)
x2paddle_710 = fluid.layers.cast(x2paddle_710, dtype='int64')
x2paddle_718 = fluid.layers.shape(x2paddle_701)
x2paddle_718 = fluid.layers.cast(x2paddle_718, dtype='int64')
x2paddle_726 = fluid.layers.shape(x2paddle_701)
x2paddle_726 = fluid.layers.cast(x2paddle_726, dtype='int64')
x2paddle_734 = fluid.layers.shape(x2paddle_701)
x2paddle_734 = fluid.layers.cast(x2paddle_734, dtype='int64')
x2paddle_748 = fluid.layers.concat([x2paddle_701, x2paddle_747], axis=0)
x2paddle_703 = fluid.layers.fill_constant(shape=x2paddle_702,
                                          dtype='int64',
                                          value=1)
x2paddle_711 = fluid.layers.fill_constant(shape=x2paddle_710,
                                          dtype='int64',
                                          value=1)
x2paddle_719 = fluid.layers.fill_constant(shape=x2paddle_718,
                                          dtype='int64',
                                          value=1)
x2paddle_727 = fluid.layers.fill_constant(shape=x2paddle_726,
                                          dtype='int64',
                                          value=1)
x2paddle_735 = fluid.layers.fill_constant(shape=x2paddle_734,
                                          dtype='int64',
                                          value=1)
x2paddle_749 = fluid.layers.reshape(x=x2paddle_646, shape=[-1, 3, 80, 80, 2])
x2paddle_705 = fluid.layers.elementwise_mul(x=x2paddle_703, y=x2paddle_704)
x2paddle_713 = fluid.layers.elementwise_mul(x=x2paddle_711, y=x2paddle_712)
x2paddle_721 = fluid.layers.elementwise_mul(x=x2paddle_719, y=x2paddle_720)
x2paddle_729 = fluid.layers.elementwise_mul(x=x2paddle_727, y=x2paddle_728)
x2paddle_737 = fluid.layers.elementwise_mul(x=x2paddle_735, y=x2paddle_736)
x2paddle_706 = fluid.layers.equal(x=x2paddle_701, y=x2paddle_705)
x2paddle_714 = fluid.layers.equal(x=x2paddle_701, y=x2paddle_713)
x2paddle_722 = fluid.layers.equal(x=x2paddle_701, y=x2paddle_721)
x2paddle_730 = fluid.layers.equal(x=x2paddle_701, y=x2paddle_729)
x2paddle_738 = fluid.layers.equal(x=x2paddle_701, y=x2paddle_737)
x2paddle_706_not = fluid.layers.logical_not(x2paddle_706)
x2paddle_706_not_cast = fluid.layers.cast(x2paddle_706_not, dtype='int64')
x2paddle_706_cast = fluid.layers.cast(x2paddle_706, dtype='int64')
x2paddle_703_mul = fluid.layers.elementwise_mul(x=x2paddle_703,
                                                y=x2paddle_706_cast)
x2paddle_701_mul = fluid.layers.elementwise_mul(x=x2paddle_701,
                                                y=x2paddle_706_not_cast)
x2paddle_707 = fluid.layers.elementwise_add(x=x2paddle_703_mul,
                                            y=x2paddle_701_mul)
x2paddle_714_not = fluid.layers.logical_not(x2paddle_714)
x2paddle_714_not_cast = fluid.layers.cast(x2paddle_714_not, dtype='int64')
x2paddle_714_cast = fluid.layers.cast(x2paddle_714, dtype='int64')
x2paddle_711_mul = fluid.layers.elementwise_mul(x=x2paddle_711,
                                                y=x2paddle_714_cast)
x2paddle_701_mul = fluid.layers.elementwise_mul(x=x2paddle_701,
                                                y=x2paddle_714_not_cast)
x2paddle_715 = fluid.layers.elementwise_add(x=x2paddle_711_mul,
                                            y=x2paddle_701_mul)
x2paddle_722_not = fluid.layers.logical_not(x2paddle_722)
x2paddle_722_not_cast = fluid.layers.cast(x2paddle_722_not, dtype='int64')
x2paddle_722_cast = fluid.layers.cast(x2paddle_722, dtype='int64')
x2paddle_719_mul = fluid.layers.elementwise_mul(x=x2paddle_719,
                                                y=x2paddle_722_cast)
x2paddle_701_mul = fluid.layers.elementwise_mul(x=x2paddle_701,
                                                y=x2paddle_722_not_cast)
x2paddle_723 = fluid.layers.elementwise_add(x=x2paddle_719_mul,
                                            y=x2paddle_701_mul)
x2paddle_730_not = fluid.layers.logical_not(x2paddle_730)
x2paddle_730_not_cast = fluid.layers.cast(x2paddle_730_not, dtype='int64')
x2paddle_730_cast = fluid.layers.cast(x2paddle_730, dtype='int64')
x2paddle_727_mul = fluid.layers.elementwise_mul(x=x2paddle_727,
                                                y=x2paddle_730_cast)
x2paddle_701_mul = fluid.layers.elementwise_mul(x=x2paddle_701,
                                                y=x2paddle_730_not_cast)
x2paddle_731 = fluid.layers.elementwise_add(x=x2paddle_727_mul,
                                            y=x2paddle_701_mul)
x2paddle_738_not = fluid.layers.logical_not(x2paddle_738)
x2paddle_738_not_cast = fluid.layers.cast(x2paddle_738_not, dtype='int64')
x2paddle_738_cast = fluid.layers.cast(x2paddle_738, dtype='int64')
x2paddle_735_mul = fluid.layers.elementwise_mul(x=x2paddle_735,
                                                y=x2paddle_738_cast)
x2paddle_701_mul = fluid.layers.elementwise_mul(x=x2paddle_701,
                                                y=x2paddle_738_not_cast)
x2paddle_739 = fluid.layers.elementwise_add(x=x2paddle_735_mul,
                                            y=x2paddle_701_mul)
x2paddle_708_ones = fluid.layers.fill_constant(shape=x2paddle_707,
                                               dtype='int64',
                                               value=1)
x2paddle_708 = fluid.layers.elementwise_mul(x=x2paddle_708_ones, y=x2paddle_688)
x2paddle_716_ones = fluid.layers.fill_constant(shape=x2paddle_715,
                                               dtype='int64',
                                               value=1)
x2paddle_716 = fluid.layers.elementwise_mul(x=x2paddle_716_ones, y=x2paddle_690)
x2paddle_724_ones = fluid.layers.fill_constant(shape=x2paddle_723,
                                               dtype='int64',
                                               value=1)
x2paddle_724 = fluid.layers.elementwise_mul(x=x2paddle_724_ones, y=x2paddle_692)
x2paddle_732_ones = fluid.layers.fill_constant(shape=x2paddle_731,
                                               dtype='int64',
                                               value=1)
x2paddle_732 = fluid.layers.elementwise_mul(x=x2paddle_732_ones, y=x2paddle_694)
x2paddle_740_ones = fluid.layers.fill_constant(shape=x2paddle_739,
                                               dtype='int64',
                                               value=1)
x2paddle_740 = fluid.layers.elementwise_mul(x=x2paddle_740_ones, y=x2paddle_696)
x2paddle_709 = fluid.layers.unsqueeze(x2paddle_708,
                                      axes=[-1],
                                      name='x2paddle_709')
x2paddle_717 = fluid.layers.unsqueeze(x2paddle_716,
                                      axes=[-1],
                                      name='x2paddle_717')
x2paddle_725 = fluid.layers.unsqueeze(x2paddle_724,
                                      axes=[-1],
                                      name='x2paddle_725')
x2paddle_733 = fluid.layers.unsqueeze(x2paddle_732,
                                      axes=[-1],
                                      name='x2paddle_733')
x2paddle_741 = fluid.layers.unsqueeze(x2paddle_740,
                                      axes=[-1],
                                      name='x2paddle_741')
x2paddle_742 = fluid.layers.concat(
    [x2paddle_709, x2paddle_717, x2paddle_725, x2paddle_733, x2paddle_741],
    axis=-1)
x2paddle_742 = fluid.layers.reshape(x2paddle_742, shape=[-1, 3, 80, 80, 2, 5])
x2paddle_750 = fluid.layers.scatter_nd_add(ref=x2paddle_622,
                                           index=x2paddle_742,
                                           updates=x2paddle_749)
x2paddle_755 = fluid.layers.strided_slice(x2paddle_750,
                                          axes=[4],
                                          starts=[2],
                                          ends=[4],
                                          strides=[1])
x2paddle_774 = fluid.layers.shape(x2paddle_750)
x2paddle_774 = fluid.layers.cast(x2paddle_774, dtype='int64')
x2paddle_781 = fluid.layers.shape(x2paddle_750)
x2paddle_781 = fluid.layers.cast(x2paddle_781, dtype='int64')
x2paddle_788 = fluid.layers.shape(x2paddle_750)
x2paddle_788 = fluid.layers.cast(x2paddle_788, dtype='int64')
x2paddle_795 = fluid.layers.shape(x2paddle_750)
x2paddle_795 = fluid.layers.cast(x2paddle_795, dtype='int64')
x2paddle_802 = fluid.layers.shape(x2paddle_750)
x2paddle_802 = fluid.layers.cast(x2paddle_802, dtype='int64')
x2paddle_870 = fluid.layers.shape(x2paddle_750)
x2paddle_870 = fluid.layers.cast(x2paddle_870, dtype='int64')
x2paddle_757 = fluid.layers.elementwise_mul(x=x2paddle_755, y=x2paddle_756)
x2paddle_776 = fluid.layers.gather(input=x2paddle_774, index=x2paddle_775)
x2paddle_783 = fluid.layers.gather(input=x2paddle_781, index=x2paddle_782)
x2paddle_790 = fluid.layers.gather(input=x2paddle_788, index=x2paddle_789)
x2paddle_797 = fluid.layers.gather(input=x2paddle_795, index=x2paddle_796)
x2paddle_804 = fluid.layers.gather(input=x2paddle_802, index=x2paddle_803)
x2paddle_874 = fluid.layers.slice(x2paddle_870, axes=[0], starts=[4], ends=[5])
x2paddle_759 = fluid.layers.elementwise_pow(x=x2paddle_757, y=x2paddle_758)
x2paddle_777 = fluid.layers.cast(x2paddle_776, dtype='int64')
x2paddle_784 = fluid.layers.cast(x2paddle_783, dtype='int64')
x2paddle_791 = fluid.layers.cast(x2paddle_790, dtype='int64')
x2paddle_798 = fluid.layers.cast(x2paddle_797, dtype='int64')
x2paddle_805 = fluid.layers.cast(x2paddle_804, dtype='int64')
x2paddle_762 = fluid.layers.elementwise_mul(x=x2paddle_759, y=x2paddle_761)
x2paddle_780 = fluid.layers.range(start=x2paddle_778,
                                  end=x2paddle_777,
                                  step=x2paddle_779,
                                  dtype='int64')
x2paddle_787 = fluid.layers.range(start=x2paddle_785,
                                  end=x2paddle_784,
                                  step=x2paddle_786,
                                  dtype='int64')
x2paddle_794 = fluid.layers.range(start=x2paddle_792,
                                  end=x2paddle_791,
                                  step=x2paddle_793,
                                  dtype='int64')
x2paddle_801 = fluid.layers.range(start=x2paddle_799,
                                  end=x2paddle_798,
                                  step=x2paddle_800,
                                  dtype='int64')
x2paddle_808 = fluid.layers.range(start=x2paddle_806,
                                  end=x2paddle_805,
                                  step=x2paddle_807,
                                  dtype='int64')
x2paddle_764 = fluid.layers.reshape(x=x2paddle_762, shape=[3, 80, 80, 2])
x2paddle_815 = fluid.layers.reshape(x=x2paddle_780, shape=[-1, 1, 1, 1, 1])
x2paddle_817 = fluid.layers.reshape(x=x2paddle_787, shape=[-1, 1, 1, 1])
x2paddle_819 = fluid.layers.reshape(x=x2paddle_794, shape=[-1, 1, 1])
x2paddle_821 = fluid.layers.reshape(x=x2paddle_801, shape=[-1, 1])
x2paddle_813 = fluid.layers.strided_slice(x2paddle_808,
                                          axes=[0],
                                          starts=[2],
                                          ends=[4],
                                          strides=[1])
x2paddle_773_ones = fluid.layers.fill_constant(shape=x2paddle_772,
                                               dtype='float32',
                                               value=1)
x2paddle_773 = fluid.layers.elementwise_mul(x=x2paddle_773_ones, y=x2paddle_764)
x2paddle_824 = fluid.layers.elementwise_add(x=x2paddle_815, y=x2paddle_817)
x2paddle_823 = fluid.layers.reshape(x=x2paddle_813, shape=[-1])
x2paddle_825 = fluid.layers.elementwise_add(x=x2paddle_824, y=x2paddle_819)
x2paddle_826 = fluid.layers.elementwise_add(x=x2paddle_825, y=x2paddle_821)
x2paddle_827 = fluid.layers.elementwise_add(x=x2paddle_826, y=x2paddle_823)
x2paddle_828 = fluid.layers.shape(x2paddle_827)
x2paddle_828 = fluid.layers.cast(x2paddle_828, dtype='int64')
x2paddle_829 = fluid.layers.shape(x2paddle_828)
x2paddle_829 = fluid.layers.cast(x2paddle_829, dtype='int64')
x2paddle_837 = fluid.layers.shape(x2paddle_828)
x2paddle_837 = fluid.layers.cast(x2paddle_837, dtype='int64')
x2paddle_845 = fluid.layers.shape(x2paddle_828)
x2paddle_845 = fluid.layers.cast(x2paddle_845, dtype='int64')
x2paddle_853 = fluid.layers.shape(x2paddle_828)
x2paddle_853 = fluid.layers.cast(x2paddle_853, dtype='int64')
x2paddle_861 = fluid.layers.shape(x2paddle_828)
x2paddle_861 = fluid.layers.cast(x2paddle_861, dtype='int64')
x2paddle_875 = fluid.layers.concat([x2paddle_828, x2paddle_874], axis=0)
x2paddle_830 = fluid.layers.fill_constant(shape=x2paddle_829,
                                          dtype='int64',
                                          value=1)
x2paddle_838 = fluid.layers.fill_constant(shape=x2paddle_837,
                                          dtype='int64',
                                          value=1)
x2paddle_846 = fluid.layers.fill_constant(shape=x2paddle_845,
                                          dtype='int64',
                                          value=1)
x2paddle_854 = fluid.layers.fill_constant(shape=x2paddle_853,
                                          dtype='int64',
                                          value=1)
x2paddle_862 = fluid.layers.fill_constant(shape=x2paddle_861,
                                          dtype='int64',
                                          value=1)
x2paddle_876 = fluid.layers.reshape(x=x2paddle_773, shape=[-1, 3, 80, 80, 2])
x2paddle_832 = fluid.layers.elementwise_mul(x=x2paddle_830, y=x2paddle_831)
x2paddle_840 = fluid.layers.elementwise_mul(x=x2paddle_838, y=x2paddle_839)
x2paddle_848 = fluid.layers.elementwise_mul(x=x2paddle_846, y=x2paddle_847)
x2paddle_856 = fluid.layers.elementwise_mul(x=x2paddle_854, y=x2paddle_855)
x2paddle_864 = fluid.layers.elementwise_mul(x=x2paddle_862, y=x2paddle_863)
x2paddle_833 = fluid.layers.equal(x=x2paddle_828, y=x2paddle_832)
x2paddle_841 = fluid.layers.equal(x=x2paddle_828, y=x2paddle_840)
x2paddle_849 = fluid.layers.equal(x=x2paddle_828, y=x2paddle_848)
x2paddle_857 = fluid.layers.equal(x=x2paddle_828, y=x2paddle_856)
x2paddle_865 = fluid.layers.equal(x=x2paddle_828, y=x2paddle_864)
x2paddle_833_not = fluid.layers.logical_not(x2paddle_833)
x2paddle_833_not_cast = fluid.layers.cast(x2paddle_833_not, dtype='int64')
x2paddle_833_cast = fluid.layers.cast(x2paddle_833, dtype='int64')
x2paddle_830_mul = fluid.layers.elementwise_mul(x=x2paddle_830,
                                                y=x2paddle_833_cast)
x2paddle_828_mul = fluid.layers.elementwise_mul(x=x2paddle_828,
                                                y=x2paddle_833_not_cast)
x2paddle_834 = fluid.layers.elementwise_add(x=x2paddle_830_mul,
                                            y=x2paddle_828_mul)
x2paddle_841_not = fluid.layers.logical_not(x2paddle_841)
x2paddle_841_not_cast = fluid.layers.cast(x2paddle_841_not, dtype='int64')
x2paddle_841_cast = fluid.layers.cast(x2paddle_841, dtype='int64')
x2paddle_838_mul = fluid.layers.elementwise_mul(x=x2paddle_838,
                                                y=x2paddle_841_cast)
x2paddle_828_mul = fluid.layers.elementwise_mul(x=x2paddle_828,
                                                y=x2paddle_841_not_cast)
x2paddle_842 = fluid.layers.elementwise_add(x=x2paddle_838_mul,
                                            y=x2paddle_828_mul)
x2paddle_849_not = fluid.layers.logical_not(x2paddle_849)
x2paddle_849_not_cast = fluid.layers.cast(x2paddle_849_not, dtype='int64')
x2paddle_849_cast = fluid.layers.cast(x2paddle_849, dtype='int64')
x2paddle_846_mul = fluid.layers.elementwise_mul(x=x2paddle_846,
                                                y=x2paddle_849_cast)
x2paddle_828_mul = fluid.layers.elementwise_mul(x=x2paddle_828,
                                                y=x2paddle_849_not_cast)
x2paddle_850 = fluid.layers.elementwise_add(x=x2paddle_846_mul,
                                            y=x2paddle_828_mul)
x2paddle_857_not = fluid.layers.logical_not(x2paddle_857)
x2paddle_857_not_cast = fluid.layers.cast(x2paddle_857_not, dtype='int64')
x2paddle_857_cast = fluid.layers.cast(x2paddle_857, dtype='int64')
x2paddle_854_mul = fluid.layers.elementwise_mul(x=x2paddle_854,
                                                y=x2paddle_857_cast)
x2paddle_828_mul = fluid.layers.elementwise_mul(x=x2paddle_828,
                                                y=x2paddle_857_not_cast)
x2paddle_858 = fluid.layers.elementwise_add(x=x2paddle_854_mul,
                                            y=x2paddle_828_mul)
x2paddle_865_not = fluid.layers.logical_not(x2paddle_865)
x2paddle_865_not_cast = fluid.layers.cast(x2paddle_865_not, dtype='int64')
x2paddle_865_cast = fluid.layers.cast(x2paddle_865, dtype='int64')
x2paddle_862_mul = fluid.layers.elementwise_mul(x=x2paddle_862,
                                                y=x2paddle_865_cast)
x2paddle_828_mul = fluid.layers.elementwise_mul(x=x2paddle_828,
                                                y=x2paddle_865_not_cast)
x2paddle_866 = fluid.layers.elementwise_add(x=x2paddle_862_mul,
                                            y=x2paddle_828_mul)
x2paddle_835_ones = fluid.layers.fill_constant(shape=x2paddle_834,
                                               dtype='int64',
                                               value=1)
x2paddle_835 = fluid.layers.elementwise_mul(x=x2paddle_835_ones, y=x2paddle_815)
x2paddle_843_ones = fluid.layers.fill_constant(shape=x2paddle_842,
                                               dtype='int64',
                                               value=1)
x2paddle_843 = fluid.layers.elementwise_mul(x=x2paddle_843_ones, y=x2paddle_817)
x2paddle_851_ones = fluid.layers.fill_constant(shape=x2paddle_850,
                                               dtype='int64',
                                               value=1)
x2paddle_851 = fluid.layers.elementwise_mul(x=x2paddle_851_ones, y=x2paddle_819)
x2paddle_859_ones = fluid.layers.fill_constant(shape=x2paddle_858,
                                               dtype='int64',
                                               value=1)
x2paddle_859 = fluid.layers.elementwise_mul(x=x2paddle_859_ones, y=x2paddle_821)
x2paddle_867_ones = fluid.layers.fill_constant(shape=x2paddle_866,
                                               dtype='int64',
                                               value=1)
x2paddle_867 = fluid.layers.elementwise_mul(x=x2paddle_867_ones, y=x2paddle_823)
x2paddle_836 = fluid.layers.unsqueeze(x2paddle_835,
                                      axes=[-1],
                                      name='x2paddle_836')
x2paddle_844 = fluid.layers.unsqueeze(x2paddle_843,
                                      axes=[-1],
                                      name='x2paddle_844')
x2paddle_852 = fluid.layers.unsqueeze(x2paddle_851,
                                      axes=[-1],
                                      name='x2paddle_852')
x2paddle_860 = fluid.layers.unsqueeze(x2paddle_859,
                                      axes=[-1],
                                      name='x2paddle_860')
x2paddle_868 = fluid.layers.unsqueeze(x2paddle_867,
                                      axes=[-1],
                                      name='x2paddle_868')
x2paddle_869 = fluid.layers.concat(
    [x2paddle_836, x2paddle_844, x2paddle_852, x2paddle_860, x2paddle_868],
    axis=-1)
x2paddle_869 = fluid.layers.reshape(x2paddle_869, shape=[-1, 3, 80, 80, 2, 5])
x2paddle_877 = fluid.layers.scatter_nd_add(ref=x2paddle_750,
                                           index=x2paddle_869,
                                           updates=x2paddle_876)
x2paddle_884 = fluid.layers.reshape(x=x2paddle_877, shape=[-1, 19200, 85])
x2paddle_output = fluid.layers.concat(
    [x2paddle_884, x2paddle_1166, x2paddle_1448], axis=1)

pwd = os.getcwd()
model_dir = 'model.onnx'
model_save_dir = 'pd-model/model_with_code/'
model_onnx = onnx.load(model_dir)

data = np.random.random((1, 3, 640, 640)).astype('float32')
results_of_inference = get_results_of_inference_rt(model_onnx, [data])


def if_exist(var):
    b = os.path.exists(os.path.join(model_save_dir, var.name))
    return b


exe = fluid.Executor(fluid.CPUPlace())
exe.run(fluid.default_startup_program())
fluid.io.load_vars(executor=exe, dirname=model_save_dir, predicate=if_exist)

# In[ ]:

max_diff = 0
all_diff = 0
node_num = 0
first_node = None
paddle_fetch_list = []
for out_name, out_put in results_of_inference.items():
    if out_name not in vars():
        continue
    output_layer = vars()[out_name]
    if isinstance(output_layer, (tuple, list)):
        paddle_fetch_list = paddle_fetch_list + list(output_layer)
    else:
        paddle_fetch_list.append(output_layer)
res = exe.run(fluid.default_main_program(),
              feed={'x2paddle_input': data},
              fetch_list=paddle_fetch_list)

# In[ ]:

idx = 0
for out_name, out_put in results_of_inference.items():
    if out_name not in vars():
        print('not find layer: {}'.format(out_name))
        continue
    #print(out_name)
    try:
        output_onnx = out_put.flatten().astype('float32')
        if res[idx] is None:
            idx += 1
            continue
        output_paddle = res[idx].flatten().astype('float32')
        diff = output_paddle - output_onnx
        max_diff_thislayer = np.max(np.fabs(diff))
        max_diff = max(max_diff_thislayer, max_diff)

        print("max_diff of layer {}: {}".format(out_name, max_diff_thislayer))
        if max_diff_thislayer > 10e-4:
            print('onnx res:', out_put)
            print('paddle res:', res[idx])
            break
        idx += 1
    except ValueError:
        idx += 1
print("max_diff of all nodes: {}".format(max_diff))

# In[17]:

#import time
#start = time.clock()
#data = np.random.rand(16, 256).astype('int64')
#res = exe.run(fluid.default_main_program(), feed={'x2paddle_input_1':data}, fetch_list=[x2paddle_220])# _Slice_676, _ConstantOfShape_678, _ConstantOfShape_680, _ConstantOfShape_682
#elapsed = (time.clock() - start)
#print("Time used:",elapsed)
#res[0].shape
