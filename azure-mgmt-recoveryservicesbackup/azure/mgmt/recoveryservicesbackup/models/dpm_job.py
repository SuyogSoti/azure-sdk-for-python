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

from .job import Job


class DpmJob(Job):
    """DPM workload-specific job object.

    All required parameters must be populated in order to send to Azure.

    :param entity_friendly_name: Friendly name of the entity on which the
     current job is executing.
    :type entity_friendly_name: str
    :param backup_management_type: Backup management type to execute the
     current job. Possible values include: 'Invalid', 'AzureIaasVM', 'MAB',
     'DPM', 'AzureBackupServer', 'AzureSql', 'AzureStorage', 'AzureWorkload',
     'DefaultBackup'
    :type backup_management_type: str or
     ~azure.mgmt.recoveryservicesbackup.models.BackupManagementType
    :param operation: The operation name.
    :type operation: str
    :param status: Job status.
    :type status: str
    :param start_time: The start time.
    :type start_time: datetime
    :param end_time: The end time.
    :type end_time: datetime
    :param activity_id: ActivityId of job.
    :type activity_id: str
    :param job_type: Required. Constant filled by server.
    :type job_type: str
    :param duration: Time elapsed for job.
    :type duration: timedelta
    :param dpm_server_name: DPM server name managing the backup item or backup
     job.
    :type dpm_server_name: str
    :param container_name: Name of cluster/server protecting current backup
     item, if any.
    :type container_name: str
    :param container_type: Type of container.
    :type container_type: str
    :param workload_type: Type of backup item.
    :type workload_type: str
    :param actions_info: The state/actions applicable on this job like
     cancel/retry.
    :type actions_info: list[str or
     ~azure.mgmt.recoveryservicesbackup.models.JobSupportedAction]
    :param error_details: The errors.
    :type error_details:
     list[~azure.mgmt.recoveryservicesbackup.models.DpmErrorInfo]
    :param extended_info: Additional information for this job.
    :type extended_info:
     ~azure.mgmt.recoveryservicesbackup.models.DpmJobExtendedInfo
    """

    _validation = {
        'job_type': {'required': True},
    }

    _attribute_map = {
        'entity_friendly_name': {'key': 'entityFriendlyName', 'type': 'str'},
        'backup_management_type': {'key': 'backupManagementType', 'type': 'str'},
        'operation': {'key': 'operation', 'type': 'str'},
        'status': {'key': 'status', 'type': 'str'},
        'start_time': {'key': 'startTime', 'type': 'iso-8601'},
        'end_time': {'key': 'endTime', 'type': 'iso-8601'},
        'activity_id': {'key': 'activityId', 'type': 'str'},
        'job_type': {'key': 'jobType', 'type': 'str'},
        'duration': {'key': 'duration', 'type': 'duration'},
        'dpm_server_name': {'key': 'dpmServerName', 'type': 'str'},
        'container_name': {'key': 'containerName', 'type': 'str'},
        'container_type': {'key': 'containerType', 'type': 'str'},
        'workload_type': {'key': 'workloadType', 'type': 'str'},
        'actions_info': {'key': 'actionsInfo', 'type': '[JobSupportedAction]'},
        'error_details': {'key': 'errorDetails', 'type': '[DpmErrorInfo]'},
        'extended_info': {'key': 'extendedInfo', 'type': 'DpmJobExtendedInfo'},
    }

    def __init__(self, **kwargs):
        super(DpmJob, self).__init__(**kwargs)
        self.duration = kwargs.get('duration', None)
        self.dpm_server_name = kwargs.get('dpm_server_name', None)
        self.container_name = kwargs.get('container_name', None)
        self.container_type = kwargs.get('container_type', None)
        self.workload_type = kwargs.get('workload_type', None)
        self.actions_info = kwargs.get('actions_info', None)
        self.error_details = kwargs.get('error_details', None)
        self.extended_info = kwargs.get('extended_info', None)
        self.job_type = 'DpmJob'
