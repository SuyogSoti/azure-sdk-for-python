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

from azure.core.paging import Paged


class KeyItemPaged(Paged):
    """
    A paging container for iterating over a list of :class:`KeyItem <azure.keyvault.v7_0.models.KeyItem>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[KeyItem]'}
    }

    def __init__(self, *args, **kwargs):

        super(KeyItemPaged, self).__init__(*args, **kwargs)
class DeletedKeyItemPaged(Paged):
    """
    A paging container for iterating over a list of :class:`DeletedKeyItem <azure.keyvault.v7_0.models.DeletedKeyItem>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[DeletedKeyItem]'}
    }

    def __init__(self, *args, **kwargs):

        super(DeletedKeyItemPaged, self).__init__(*args, **kwargs)
class SecretItemPaged(Paged):
    """
    A paging container for iterating over a list of :class:`SecretItem <azure.keyvault.v7_0.models.SecretItem>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[SecretItem]'}
    }

    def __init__(self, *args, **kwargs):

        super(SecretItemPaged, self).__init__(*args, **kwargs)
class DeletedSecretItemPaged(Paged):
    """
    A paging container for iterating over a list of :class:`DeletedSecretItem <azure.keyvault.v7_0.models.DeletedSecretItem>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[DeletedSecretItem]'}
    }

    def __init__(self, *args, **kwargs):

        super(DeletedSecretItemPaged, self).__init__(*args, **kwargs)
class CertificateItemPaged(Paged):
    """
    A paging container for iterating over a list of :class:`CertificateItem <azure.keyvault.v7_0.models.CertificateItem>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[CertificateItem]'}
    }

    def __init__(self, *args, **kwargs):

        super(CertificateItemPaged, self).__init__(*args, **kwargs)
class CertificateIssuerItemPaged(Paged):
    """
    A paging container for iterating over a list of :class:`CertificateIssuerItem <azure.keyvault.v7_0.models.CertificateIssuerItem>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[CertificateIssuerItem]'}
    }

    def __init__(self, *args, **kwargs):

        super(CertificateIssuerItemPaged, self).__init__(*args, **kwargs)
class DeletedCertificateItemPaged(Paged):
    """
    A paging container for iterating over a list of :class:`DeletedCertificateItem <azure.keyvault.v7_0.models.DeletedCertificateItem>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[DeletedCertificateItem]'}
    }

    def __init__(self, *args, **kwargs):

        super(DeletedCertificateItemPaged, self).__init__(*args, **kwargs)
class StorageAccountItemPaged(Paged):
    """
    A paging container for iterating over a list of :class:`StorageAccountItem <azure.keyvault.v7_0.models.StorageAccountItem>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[StorageAccountItem]'}
    }

    def __init__(self, *args, **kwargs):

        super(StorageAccountItemPaged, self).__init__(*args, **kwargs)
class DeletedStorageAccountItemPaged(Paged):
    """
    A paging container for iterating over a list of :class:`DeletedStorageAccountItem <azure.keyvault.v7_0.models.DeletedStorageAccountItem>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[DeletedStorageAccountItem]'}
    }

    def __init__(self, *args, **kwargs):

        super(DeletedStorageAccountItemPaged, self).__init__(*args, **kwargs)
class SasDefinitionItemPaged(Paged):
    """
    A paging container for iterating over a list of :class:`SasDefinitionItem <azure.keyvault.v7_0.models.SasDefinitionItem>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[SasDefinitionItem]'}
    }

    def __init__(self, *args, **kwargs):

        super(SasDefinitionItemPaged, self).__init__(*args, **kwargs)
class DeletedSasDefinitionItemPaged(Paged):
    """
    A paging container for iterating over a list of :class:`DeletedSasDefinitionItem <azure.keyvault.v7_0.models.DeletedSasDefinitionItem>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[DeletedSasDefinitionItem]'}
    }

    def __init__(self, *args, **kwargs):

        super(DeletedSasDefinitionItemPaged, self).__init__(*args, **kwargs)
