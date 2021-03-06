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


class Environment(Resource):
    """Represents an environment instance.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar id: The identifier of the resource.
    :vartype id: str
    :ivar name: The name of the resource.
    :vartype name: str
    :ivar type: The type of the resource.
    :vartype type: str
    :param location: The location of the resource.
    :type location: str
    :param tags: The tags of the resource.
    :type tags: dict[str, str]
    :param resource_sets: The set of a VM and the setting id it was created
     for
    :type resource_sets: ~azure.mgmt.labservices.models.ResourceSet
    :ivar claimed_by_user_object_id: The AAD object Id of the user who has
     claimed the environment
    :vartype claimed_by_user_object_id: str
    :ivar claimed_by_user_principal_id: The user principal Id of the user who
     has claimed the environment
    :vartype claimed_by_user_principal_id: str
    :ivar claimed_by_user_name: The name or email address of the user who has
     claimed the environment
    :vartype claimed_by_user_name: str
    :ivar is_claimed: Is the environment claimed or not
    :vartype is_claimed: bool
    :ivar last_known_power_state: Last known power state of the environment
    :vartype last_known_power_state: str
    :ivar network_interface: Network details of the environment
    :vartype network_interface:
     ~azure.mgmt.labservices.models.NetworkInterface
    :ivar total_usage: How long the environment has been used by a lab user
    :vartype total_usage: timedelta
    :ivar password_last_reset: When the password was last reset on the
     environment.
    :vartype password_last_reset: datetime
    :param provisioning_state: The provisioning status of the resource.
    :type provisioning_state: str
    :param unique_identifier: The unique immutable identifier of a resource
     (Guid).
    :type unique_identifier: str
    :ivar latest_operation_result: The details of the latest operation. ex:
     status, error
    :vartype latest_operation_result:
     ~azure.mgmt.labservices.models.LatestOperationResult
    """

    _validation = {
        'id': {'readonly': True},
        'name': {'readonly': True},
        'type': {'readonly': True},
        'claimed_by_user_object_id': {'readonly': True},
        'claimed_by_user_principal_id': {'readonly': True},
        'claimed_by_user_name': {'readonly': True},
        'is_claimed': {'readonly': True},
        'last_known_power_state': {'readonly': True},
        'network_interface': {'readonly': True},
        'total_usage': {'readonly': True},
        'password_last_reset': {'readonly': True},
        'latest_operation_result': {'readonly': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
        'location': {'key': 'location', 'type': 'str'},
        'tags': {'key': 'tags', 'type': '{str}'},
        'resource_sets': {'key': 'properties.resourceSets', 'type': 'ResourceSet'},
        'claimed_by_user_object_id': {'key': 'properties.claimedByUserObjectId', 'type': 'str'},
        'claimed_by_user_principal_id': {'key': 'properties.claimedByUserPrincipalId', 'type': 'str'},
        'claimed_by_user_name': {'key': 'properties.claimedByUserName', 'type': 'str'},
        'is_claimed': {'key': 'properties.isClaimed', 'type': 'bool'},
        'last_known_power_state': {'key': 'properties.lastKnownPowerState', 'type': 'str'},
        'network_interface': {'key': 'properties.networkInterface', 'type': 'NetworkInterface'},
        'total_usage': {'key': 'properties.totalUsage', 'type': 'duration'},
        'password_last_reset': {'key': 'properties.passwordLastReset', 'type': 'iso-8601'},
        'provisioning_state': {'key': 'properties.provisioningState', 'type': 'str'},
        'unique_identifier': {'key': 'properties.uniqueIdentifier', 'type': 'str'},
        'latest_operation_result': {'key': 'properties.latestOperationResult', 'type': 'LatestOperationResult'},
    }

    def __init__(self, *, location: str=None, tags=None, resource_sets=None, provisioning_state: str=None, unique_identifier: str=None, **kwargs) -> None:
        super(Environment, self).__init__(location=location, tags=tags, **kwargs)
        self.resource_sets = resource_sets
        self.claimed_by_user_object_id = None
        self.claimed_by_user_principal_id = None
        self.claimed_by_user_name = None
        self.is_claimed = None
        self.last_known_power_state = None
        self.network_interface = None
        self.total_usage = None
        self.password_last_reset = None
        self.provisioning_state = provisioning_state
        self.unique_identifier = unique_identifier
        self.latest_operation_result = None
