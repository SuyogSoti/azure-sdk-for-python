# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class VirtualMachineFamilyCoreQuota(Model):
    """A VM Family and its associated core quota for the Batch account.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar name: The Virtual Machine family name.
    :vartype name: str
    :ivar core_quota: The core quota for the VM family for the Batch account.
    :vartype core_quota: int
    """

    _validation = {
        'name': {'readonly': True},
        'core_quota': {'readonly': True},
    }

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'core_quota': {'key': 'coreQuota', 'type': 'int'},
    }

    def __init__(self, **kwargs) -> None:
        super(VirtualMachineFamilyCoreQuota, self).__init__(**kwargs)
        self.name = None
        self.core_quota = None
