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


class VirtualNetworkRule(Model):
    """Virtual Network rule.

    All required parameters must be populated in order to send to Azure.

    :param virtual_network_resource_id: Required. Resource ID of a subnet, for
     example:
     /subscriptions/{subscriptionId}/resourceGroups/{groupName}/providers/Microsoft.Network/virtualNetworks/{vnetName}/subnets/{subnetName}.
    :type virtual_network_resource_id: str
    :param action: The action of virtual network rule. Possible values
     include: 'Allow'. Default value: "Allow" .
    :type action: str or ~azure.mgmt.storage.v2018_11_01.models.Action
    :param state: Gets the state of virtual network rule. Possible values
     include: 'provisioning', 'deprovisioning', 'succeeded', 'failed',
     'networkSourceDeleted'
    :type state: str or ~azure.mgmt.storage.v2018_11_01.models.State
    """

    _validation = {
        'virtual_network_resource_id': {'required': True},
    }

    _attribute_map = {
        'virtual_network_resource_id': {'key': 'id', 'type': 'str'},
        'action': {'key': 'action', 'type': 'Action'},
        'state': {'key': 'state', 'type': 'State'},
    }

    def __init__(self, **kwargs):
        super(VirtualNetworkRule, self).__init__(**kwargs)
        self.virtual_network_resource_id = kwargs.get('virtual_network_resource_id', None)
        self.action = kwargs.get('action', "Allow")
        self.state = kwargs.get('state', None)
