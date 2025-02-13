## torch.nn.ConvTranspose2d
### [torch.nn.ConvTranspose2d](https://pytorch.org/docs/stable/generated/torch.nn.ConvTranspose2d.html?highlight=convtranspose2d#torch.nn.ConvTranspose2d)
```python
torch.nn.ConvTranspose1d(in_channels,
                         out_channels,
                         kernel_size,
                         stride=1,
                         padding=0,
                         output_padding=0,
                         groups=1,
                         bias=True,
                         dilation=1,
                         padding_mode='zeros')
```

### [paddle.nn.Conv2DTranspose](https://www.paddlepaddle.org.cn/documentation/docs/zh/api/paddle/nn/Conv2DTranspose_cn.html#conv2dtranspose)
```python
paddle.nn.Conv2DTranspose(in_channels,
                          out_channels,
                          kernel_size,
                          stride=1,
                          padding=0,
                          output_padding=0,
                          groups=1,
                          dilation=1,
                          weight_attr=None,
                          bias_attr=None,
                          data_format='NCHW')
```
### 功能差异
#### 输入格式
***PyTorch***：只支持`NCHW`的输入。
***PaddlePaddle***：支持`NCHW`和`NHWC`两种格式的输入（通过`data_format`设置）。

#### 更新参数设置
***PyTorch***：`bias`默认为True，表示使用可更新的偏置参数。
***PaddlePaddle***：`weight_attr`/`bias_attr`默认使用默认的权重/偏置参数属性，否则为指定的权重/偏置参数属性，具体用法参见[ParamAttr](https://www.paddlepaddle.org.cn/documentation/docs/zh/api/paddle/ParamAttr_cn.html#paramattr)；当`bias_attr`设置为bool类型与PyTorch的作用一致。

#### padding大小的设置
***PyTorch***：`padding`只能支持list或tuple类型。
***PaddlePaddle***：`padding`支持list或tuple类型或str类型。

#### padding值的设置
***PyTorch***：通过设置`padding_mode`确定padding的值。
***PaddlePaddle***：PaddlePaddle无此参数。
