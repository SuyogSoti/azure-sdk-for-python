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


class FollowerDatabaseRequest(Model):
    """A class representing follower database request.

    All required parameters must be populated in order to send to Azure.

    :param cluster_resource_id: Required. Resource id of the cluster that
     follows a database owned by this cluster.
    :type cluster_resource_id: str
    :param database_name: Required. The database name owned by this cluster
     that was followed. * in case following all databases.
    :type database_name: str
    """

    _validation = {
        'cluster_resource_id': {'required': True},
        'database_name': {'required': True},
    }

    _attribute_map = {
        'cluster_resource_id': {'key': 'clusterResourceId', 'type': 'str'},
        'database_name': {'key': 'databaseName', 'type': 'str'},
    }

    def __init__(self, *, cluster_resource_id: str, database_name: str, **kwargs) -> None:
        super(FollowerDatabaseRequest, self).__init__(**kwargs)
        self.cluster_resource_id = cluster_resource_id
        self.database_name = database_name
