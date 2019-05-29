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


class RegenerateCredentialParameters(Model):
    """The parameters used to regenerate the login credential.

    All required parameters must be populated in order to send to Azure.

    :param name: Required. Specifies name of the password which should be
     regenerated -- password or password2. Possible values include: 'password',
     'password2'
    :type name: str or
     ~azure.mgmt.containerregistry.v2019_05_01.models.PasswordName
    """

    _validation = {
        'name': {'required': True},
    }

    _attribute_map = {
        'name': {'key': 'name', 'type': 'PasswordName'},
    }

    def __init__(self, **kwargs):
        super(RegenerateCredentialParameters, self).__init__(**kwargs)
        self.name = kwargs.get('name', None)
