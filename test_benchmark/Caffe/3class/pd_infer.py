from __future__ import print_function
import paddle
import paddle.fluid as fluid
import sys
import os
import numpy as np
import pickle

f = open("result.txt", "w")
f.write("======3class: \n")

try:
    with open('../dataset/AlexNet/caffe_input.pkl', 'rb') as inp:
        input_data = np.random.rand(8, 3, 224, 224).astype("float32")

    paddle.enable_static()
    exe = paddle.static.Executor(paddle.CPUPlace())
    # test dygraph
    [prog, inputs, outputs] = fluid.io.load_inference_model(
        dirname="pd_model_dygraph/inference_model/",
        executor=exe,
        model_filename="model.pdmodel",
        params_filename="model.pdiparams")
    # test dygraph
    paddle.disable_static()
    from pd_model_dygraph.x2paddle_code import main
    input_data = paddle.to_tensor(input_data)
    result = main(input_data)
    f.write("Dygraph Successed\n")

except:
    f.write("!!!!!Failed\n")

f.close()
