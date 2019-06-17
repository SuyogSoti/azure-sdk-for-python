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

from msrest.paging import Paged


class OperationPaged(Paged):
    """
    A paging container for iterating over a list of :class:`Operation <azure.mgmt.resource.subscriptions.v2018_06_01.models.Operation>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[Operation]'}
    }

    def __init__(self, *args, **kwargs):

        super(OperationPaged, self).__init__(*args, **kwargs)
class LocationPaged(Paged):
    """
    A paging container for iterating over a list of :class:`Location <azure.mgmt.resource.subscriptions.v2018_06_01.models.Location>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[Location]'}
    }

    def __init__(self, *args, **kwargs):

        super(LocationPaged, self).__init__(*args, **kwargs)
class SubscriptionPaged(Paged):
    """
    A paging container for iterating over a list of :class:`Subscription <azure.mgmt.resource.subscriptions.v2018_06_01.models.Subscription>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[Subscription]'}
    }

    def __init__(self, *args, **kwargs):

        super(SubscriptionPaged, self).__init__(*args, **kwargs)
class TenantIdDescriptionPaged(Paged):
    """
    A paging container for iterating over a list of :class:`TenantIdDescription <azure.mgmt.resource.subscriptions.v2018_06_01.models.TenantIdDescription>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[TenantIdDescription]'}
    }

    def __init__(self, *args, **kwargs):

        super(TenantIdDescriptionPaged, self).__init__(*args, **kwargs)
