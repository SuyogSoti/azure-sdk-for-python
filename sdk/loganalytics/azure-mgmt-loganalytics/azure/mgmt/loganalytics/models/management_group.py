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


class ManagementGroup(Model):
    """A management group that is connected to a workspace.

    :param server_count: The number of servers connected to the management
     group.
    :type server_count: int
    :param is_gateway: Gets or sets a value indicating whether the management
     group is a gateway.
    :type is_gateway: bool
    :param name: The name of the management group.
    :type name: str
    :param id: The unique ID of the management group.
    :type id: str
    :param created: The datetime that the management group was created.
    :type created: datetime
    :param data_received: The last datetime that the management group received
     data.
    :type data_received: datetime
    :param version: The version of System Center that is managing the
     management group.
    :type version: str
    :param sku: The SKU of System Center that is managing the management
     group.
    :type sku: str
    """

    _attribute_map = {
        'server_count': {'key': 'properties.serverCount', 'type': 'int'},
        'is_gateway': {'key': 'properties.isGateway', 'type': 'bool'},
        'name': {'key': 'properties.name', 'type': 'str'},
        'id': {'key': 'properties.id', 'type': 'str'},
        'created': {'key': 'properties.created', 'type': 'iso-8601'},
        'data_received': {'key': 'properties.dataReceived', 'type': 'iso-8601'},
        'version': {'key': 'properties.version', 'type': 'str'},
        'sku': {'key': 'properties.sku', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(ManagementGroup, self).__init__(**kwargs)
        self.server_count = kwargs.get('server_count', None)
        self.is_gateway = kwargs.get('is_gateway', None)
        self.name = kwargs.get('name', None)
        self.id = kwargs.get('id', None)
        self.created = kwargs.get('created', None)
        self.data_received = kwargs.get('data_received', None)
        self.version = kwargs.get('version', None)
        self.sku = kwargs.get('sku', None)
