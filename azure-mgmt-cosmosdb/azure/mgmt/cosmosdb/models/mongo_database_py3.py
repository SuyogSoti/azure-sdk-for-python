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

from .resource_py3 import Resource


class MongoDatabase(Resource):
    """An Azure Cosmos DB Mongo database.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    All required parameters must be populated in order to send to Azure.

    :ivar id: The unique resource identifier of the database account.
    :vartype id: str
    :ivar name: The name of the database account.
    :vartype name: str
    :ivar type: The type of Azure resource.
    :vartype type: str
    :param location: The location of the resource group to which the resource
     belongs.
    :type location: str
    :param tags:
    :type tags: dict[str, str]
    :param mongo_database_id: Required. Name of the Cosmos DB Mongo database
    :type mongo_database_id: str
    """

    _validation = {
        'id': {'readonly': True},
        'name': {'readonly': True},
        'type': {'readonly': True},
        'mongo_database_id': {'required': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
        'location': {'key': 'location', 'type': 'str'},
        'tags': {'key': 'tags', 'type': '{str}'},
        'mongo_database_id': {'key': 'properties.id', 'type': 'str'},
    }

    def __init__(self, *, mongo_database_id: str, location: str=None, tags=None, **kwargs) -> None:
        super(MongoDatabase, self).__init__(location=location, tags=tags, **kwargs)
        self.mongo_database_id = mongo_database_id
