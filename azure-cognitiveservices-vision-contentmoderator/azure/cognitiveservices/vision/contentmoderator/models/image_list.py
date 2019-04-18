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


class ImageList(Model):
    """Image List Properties.

    :param id: Image List Id.
    :type id: int
    :param name: Image List Name.
    :type name: str
    :param description: Description for image list.
    :type description: str
    :param metadata: Image List Metadata.
    :type metadata: dict[str, str]
    """

    _attribute_map = {
        'id': {'key': 'Id', 'type': 'int'},
        'name': {'key': 'Name', 'type': 'str'},
        'description': {'key': 'Description', 'type': 'str'},
        'metadata': {'key': 'Metadata', 'type': '{str}'},
    }

    def __init__(self, **kwargs):
        super(ImageList, self).__init__(**kwargs)
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.description = kwargs.get('description', None)
        self.metadata = kwargs.get('metadata', None)
