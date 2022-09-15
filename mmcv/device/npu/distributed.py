# Copyright Huawei Technologies Co., Ltd. All rights reserved.
# Copyright (c) OpenMMLab. All rights reserved.

from mmcv.parallel import MMDistributedDataParallel
from .scatter_gather import scatter_kwargs


class NPUDistributedDataParallel(MMDistributedDataParallel):
    """The DDP module supports DataContainer.

    NPUDDP has one difference from MMDDP which moves data to NPU with coping
    instead of scattering.
    """

    def to_kwargs(self, inputs, kwargs, device_id):
        # Use `self.to_kwargs` instead of `self.scatter` in pytorch1.8
        # to move all tensors to device_id
        return scatter_kwargs(inputs, kwargs, [device_id], dim=self.dim)

    def scatter(self, inputs, kwargs, device_ids):
        return scatter_kwargs(inputs, kwargs, device_ids, dim=self.dim)

    def forward(self, *inputs, **kwargs):
        if self.device_ids:
            inputs, kwargs = self.scatter(inputs, kwargs, self.device_ids)
        return super().forward(*inputs[0], **kwargs[0])
