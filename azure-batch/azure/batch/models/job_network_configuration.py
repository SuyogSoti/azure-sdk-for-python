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


class JobNetworkConfiguration(Model):
    """The network configuration for the job.

    All required parameters must be populated in order to send to Azure.

    :param subnet_id: Required. The ARM resource identifier of the virtual
     network subnet which nodes running tasks from the job will join for the
     duration of the task. This is only supported for jobs running on
     VirtualMachineConfiguration pools. This is of the form
     /subscriptions/{subscription}/resourceGroups/{group}/providers/{provider}/virtualNetworks/{network}/subnets/{subnet}.
     The virtual network must be in the same region and subscription as the
     Azure Batch account. The specified subnet should have enough free IP
     addresses to accommodate the number of nodes which will run tasks from the
     job. For more details, see
     https://docs.microsoft.com/en-us/azure/batch/batch-api-basics#virtual-network-vnet-and-firewall-configuration.
    :type subnet_id: str
    """

    _validation = {
        'subnet_id': {'required': True},
    }

    _attribute_map = {
        'subnet_id': {'key': 'subnetId', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(JobNetworkConfiguration, self).__init__(**kwargs)
        self.subnet_id = kwargs.get('subnet_id', None)
