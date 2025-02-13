# Copyright (c) 2020  PaddlePaddle Authors. All Rights Reserved.
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

import paddle


class Normalize(object):

    def __init__(self, axis):
        self.axis = axis

    def __call__(self, x, param):
        l2_norm = paddle.norm(x=x, p=2, axis=1, keepdim=True)
        param = paddle.reshape(param, [param.shape[-1]])
        perm = list(range(len(l2_norm.shape)))
        perm.pop(self.axis)
        perm = perm + [self.axis]
        l2_norm = paddle.transpose(l2_norm, perm=perm)
        out = paddle.multiply(x=l2_norm, y=param)
        perm = list(range(len(l2_norm.shape)))
        dim = perm.pop(-1)
        perm.insert(self.axis, dim)
        out = paddle.transpose(out, perm=perm)
        return out
