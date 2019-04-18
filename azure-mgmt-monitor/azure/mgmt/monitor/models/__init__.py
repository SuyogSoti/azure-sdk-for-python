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

try:
    from .resource_py3 import Resource
    from .scale_capacity_py3 import ScaleCapacity
    from .metric_trigger_py3 import MetricTrigger
    from .scale_action_py3 import ScaleAction
    from .scale_rule_py3 import ScaleRule
    from .time_window_py3 import TimeWindow
    from .recurrent_schedule_py3 import RecurrentSchedule
    from .recurrence_py3 import Recurrence
    from .autoscale_profile_py3 import AutoscaleProfile
    from .email_notification_py3 import EmailNotification
    from .webhook_notification_py3 import WebhookNotification
    from .autoscale_notification_py3 import AutoscaleNotification
    from .autoscale_setting_resource_py3 import AutoscaleSettingResource
    from .autoscale_setting_resource_patch_py3 import AutoscaleSettingResourcePatch
    from .error_response_py3 import ErrorResponse, ErrorResponseException
    from .operation_display_py3 import OperationDisplay
    from .operation_py3 import Operation
    from .operation_list_result_py3 import OperationListResult
    from .incident_py3 import Incident
    from .rule_data_source_py3 import RuleDataSource
    from .rule_condition_py3 import RuleCondition
    from .rule_metric_data_source_py3 import RuleMetricDataSource
    from .rule_management_event_claims_data_source_py3 import RuleManagementEventClaimsDataSource
    from .rule_management_event_data_source_py3 import RuleManagementEventDataSource
    from .threshold_rule_condition_py3 import ThresholdRuleCondition
    from .location_threshold_rule_condition_py3 import LocationThresholdRuleCondition
    from .management_event_aggregation_condition_py3 import ManagementEventAggregationCondition
    from .management_event_rule_condition_py3 import ManagementEventRuleCondition
    from .rule_action_py3 import RuleAction
    from .rule_email_action_py3 import RuleEmailAction
    from .rule_webhook_action_py3 import RuleWebhookAction
    from .alert_rule_resource_py3 import AlertRuleResource
    from .alert_rule_resource_patch_py3 import AlertRuleResourcePatch
    from .retention_policy_py3 import RetentionPolicy
    from .log_profile_resource_py3 import LogProfileResource
    from .log_profile_resource_patch_py3 import LogProfileResourcePatch
    from .proxy_only_resource_py3 import ProxyOnlyResource
    from .metric_settings_py3 import MetricSettings
    from .log_settings_py3 import LogSettings
    from .diagnostic_settings_resource_py3 import DiagnosticSettingsResource
    from .diagnostic_settings_resource_collection_py3 import DiagnosticSettingsResourceCollection
    from .diagnostic_settings_category_resource_py3 import DiagnosticSettingsCategoryResource
    from .diagnostic_settings_category_resource_collection_py3 import DiagnosticSettingsCategoryResourceCollection
    from .email_receiver_py3 import EmailReceiver
    from .sms_receiver_py3 import SmsReceiver
    from .webhook_receiver_py3 import WebhookReceiver
    from .itsm_receiver_py3 import ItsmReceiver
    from .azure_app_push_receiver_py3 import AzureAppPushReceiver
    from .automation_runbook_receiver_py3 import AutomationRunbookReceiver
    from .voice_receiver_py3 import VoiceReceiver
    from .logic_app_receiver_py3 import LogicAppReceiver
    from .azure_function_receiver_py3 import AzureFunctionReceiver
    from .arm_role_receiver_py3 import ArmRoleReceiver
    from .action_group_resource_py3 import ActionGroupResource
    from .enable_request_py3 import EnableRequest
    from .action_group_patch_body_py3 import ActionGroupPatchBody
    from .activity_log_alert_leaf_condition_py3 import ActivityLogAlertLeafCondition
    from .activity_log_alert_all_of_condition_py3 import ActivityLogAlertAllOfCondition
    from .activity_log_alert_action_group_py3 import ActivityLogAlertActionGroup
    from .activity_log_alert_action_list_py3 import ActivityLogAlertActionList
    from .activity_log_alert_resource_py3 import ActivityLogAlertResource
    from .activity_log_alert_patch_body_py3 import ActivityLogAlertPatchBody
    from .localizable_string_py3 import LocalizableString
    from .sender_authorization_py3 import SenderAuthorization
    from .http_request_info_py3 import HttpRequestInfo
    from .event_data_py3 import EventData
    from .metric_availability_py3 import MetricAvailability
    from .metric_definition_py3 import MetricDefinition
    from .metric_value_py3 import MetricValue
    from .metadata_value_py3 import MetadataValue
    from .time_series_element_py3 import TimeSeriesElement
    from .metric_py3 import Metric
    from .response_py3 import Response
    from .baseline_metadata_value_py3 import BaselineMetadataValue
    from .baseline_py3 import Baseline
    from .baseline_response_py3 import BaselineResponse
    from .time_series_information_py3 import TimeSeriesInformation
    from .calculate_baseline_response_py3 import CalculateBaselineResponse
    from .metric_single_dimension_py3 import MetricSingleDimension
    from .single_baseline_py3 import SingleBaseline
    from .baseline_metadata_py3 import BaselineMetadata
    from .time_series_baseline_py3 import TimeSeriesBaseline
    from .single_metric_baseline_py3 import SingleMetricBaseline
    from .metric_alert_action_py3 import MetricAlertAction
    from .metric_alert_criteria_py3 import MetricAlertCriteria
    from .metric_alert_resource_py3 import MetricAlertResource
    from .metric_alert_resource_patch_py3 import MetricAlertResourcePatch
    from .metric_alert_status_properties_py3 import MetricAlertStatusProperties
    from .metric_alert_status_py3 import MetricAlertStatus
    from .metric_alert_status_collection_py3 import MetricAlertStatusCollection
    from .metric_dimension_py3 import MetricDimension
    from .metric_criteria_py3 import MetricCriteria
    from .metric_alert_single_resource_multiple_metric_criteria_py3 import MetricAlertSingleResourceMultipleMetricCriteria
    from .multi_metric_criteria_py3 import MultiMetricCriteria
    from .metric_alert_multiple_resource_multiple_metric_criteria_py3 import MetricAlertMultipleResourceMultipleMetricCriteria
    from .source_py3 import Source
    from .schedule_py3 import Schedule
    from .action_py3 import Action
    from .log_search_rule_resource_py3 import LogSearchRuleResource
    from .log_search_rule_resource_patch_py3 import LogSearchRuleResourcePatch
    from .log_metric_trigger_py3 import LogMetricTrigger
    from .trigger_condition_py3 import TriggerCondition
    from .az_ns_action_group_py3 import AzNsActionGroup
    from .alerting_action_py3 import AlertingAction
    from .dimension_py3 import Dimension
    from .criteria_py3 import Criteria
    from .log_to_metric_action_py3 import LogToMetricAction
    from .metric_namespace_name_py3 import MetricNamespaceName
    from .metric_namespace_py3 import MetricNamespace
    from .proxy_resource_py3 import ProxyResource
    from .error_py3 import Error
    from .response_with_error_py3 import ResponseWithError, ResponseWithErrorException
    from .workspace_info_py3 import WorkspaceInfo
    from .data_container_py3 import DataContainer
    from .vm_insights_onboarding_status_py3 import VMInsightsOnboardingStatus
except (SyntaxError, ImportError):
    from .resource import Resource
    from .scale_capacity import ScaleCapacity
    from .metric_trigger import MetricTrigger
    from .scale_action import ScaleAction
    from .scale_rule import ScaleRule
    from .time_window import TimeWindow
    from .recurrent_schedule import RecurrentSchedule
    from .recurrence import Recurrence
    from .autoscale_profile import AutoscaleProfile
    from .email_notification import EmailNotification
    from .webhook_notification import WebhookNotification
    from .autoscale_notification import AutoscaleNotification
    from .autoscale_setting_resource import AutoscaleSettingResource
    from .autoscale_setting_resource_patch import AutoscaleSettingResourcePatch
    from .error_response import ErrorResponse, ErrorResponseException
    from .operation_display import OperationDisplay
    from .operation import Operation
    from .operation_list_result import OperationListResult
    from .incident import Incident
    from .rule_data_source import RuleDataSource
    from .rule_condition import RuleCondition
    from .rule_metric_data_source import RuleMetricDataSource
    from .rule_management_event_claims_data_source import RuleManagementEventClaimsDataSource
    from .rule_management_event_data_source import RuleManagementEventDataSource
    from .threshold_rule_condition import ThresholdRuleCondition
    from .location_threshold_rule_condition import LocationThresholdRuleCondition
    from .management_event_aggregation_condition import ManagementEventAggregationCondition
    from .management_event_rule_condition import ManagementEventRuleCondition
    from .rule_action import RuleAction
    from .rule_email_action import RuleEmailAction
    from .rule_webhook_action import RuleWebhookAction
    from .alert_rule_resource import AlertRuleResource
    from .alert_rule_resource_patch import AlertRuleResourcePatch
    from .retention_policy import RetentionPolicy
    from .log_profile_resource import LogProfileResource
    from .log_profile_resource_patch import LogProfileResourcePatch
    from .proxy_only_resource import ProxyOnlyResource
    from .metric_settings import MetricSettings
    from .log_settings import LogSettings
    from .diagnostic_settings_resource import DiagnosticSettingsResource
    from .diagnostic_settings_resource_collection import DiagnosticSettingsResourceCollection
    from .diagnostic_settings_category_resource import DiagnosticSettingsCategoryResource
    from .diagnostic_settings_category_resource_collection import DiagnosticSettingsCategoryResourceCollection
    from .email_receiver import EmailReceiver
    from .sms_receiver import SmsReceiver
    from .webhook_receiver import WebhookReceiver
    from .itsm_receiver import ItsmReceiver
    from .azure_app_push_receiver import AzureAppPushReceiver
    from .automation_runbook_receiver import AutomationRunbookReceiver
    from .voice_receiver import VoiceReceiver
    from .logic_app_receiver import LogicAppReceiver
    from .azure_function_receiver import AzureFunctionReceiver
    from .arm_role_receiver import ArmRoleReceiver
    from .action_group_resource import ActionGroupResource
    from .enable_request import EnableRequest
    from .action_group_patch_body import ActionGroupPatchBody
    from .activity_log_alert_leaf_condition import ActivityLogAlertLeafCondition
    from .activity_log_alert_all_of_condition import ActivityLogAlertAllOfCondition
    from .activity_log_alert_action_group import ActivityLogAlertActionGroup
    from .activity_log_alert_action_list import ActivityLogAlertActionList
    from .activity_log_alert_resource import ActivityLogAlertResource
    from .activity_log_alert_patch_body import ActivityLogAlertPatchBody
    from .localizable_string import LocalizableString
    from .sender_authorization import SenderAuthorization
    from .http_request_info import HttpRequestInfo
    from .event_data import EventData
    from .metric_availability import MetricAvailability
    from .metric_definition import MetricDefinition
    from .metric_value import MetricValue
    from .metadata_value import MetadataValue
    from .time_series_element import TimeSeriesElement
    from .metric import Metric
    from .response import Response
    from .baseline_metadata_value import BaselineMetadataValue
    from .baseline import Baseline
    from .baseline_response import BaselineResponse
    from .time_series_information import TimeSeriesInformation
    from .calculate_baseline_response import CalculateBaselineResponse
    from .metric_single_dimension import MetricSingleDimension
    from .single_baseline import SingleBaseline
    from .baseline_metadata import BaselineMetadata
    from .time_series_baseline import TimeSeriesBaseline
    from .single_metric_baseline import SingleMetricBaseline
    from .metric_alert_action import MetricAlertAction
    from .metric_alert_criteria import MetricAlertCriteria
    from .metric_alert_resource import MetricAlertResource
    from .metric_alert_resource_patch import MetricAlertResourcePatch
    from .metric_alert_status_properties import MetricAlertStatusProperties
    from .metric_alert_status import MetricAlertStatus
    from .metric_alert_status_collection import MetricAlertStatusCollection
    from .metric_dimension import MetricDimension
    from .metric_criteria import MetricCriteria
    from .metric_alert_single_resource_multiple_metric_criteria import MetricAlertSingleResourceMultipleMetricCriteria
    from .multi_metric_criteria import MultiMetricCriteria
    from .metric_alert_multiple_resource_multiple_metric_criteria import MetricAlertMultipleResourceMultipleMetricCriteria
    from .source import Source
    from .schedule import Schedule
    from .action import Action
    from .log_search_rule_resource import LogSearchRuleResource
    from .log_search_rule_resource_patch import LogSearchRuleResourcePatch
    from .log_metric_trigger import LogMetricTrigger
    from .trigger_condition import TriggerCondition
    from .az_ns_action_group import AzNsActionGroup
    from .alerting_action import AlertingAction
    from .dimension import Dimension
    from .criteria import Criteria
    from .log_to_metric_action import LogToMetricAction
    from .metric_namespace_name import MetricNamespaceName
    from .metric_namespace import MetricNamespace
    from .proxy_resource import ProxyResource
    from .error import Error
    from .response_with_error import ResponseWithError, ResponseWithErrorException
    from .workspace_info import WorkspaceInfo
    from .data_container import DataContainer
    from .vm_insights_onboarding_status import VMInsightsOnboardingStatus
from .autoscale_setting_resource_paged import AutoscaleSettingResourcePaged
from .incident_paged import IncidentPaged
from .alert_rule_resource_paged import AlertRuleResourcePaged
from .log_profile_resource_paged import LogProfileResourcePaged
from .action_group_resource_paged import ActionGroupResourcePaged
from .activity_log_alert_resource_paged import ActivityLogAlertResourcePaged
from .event_data_paged import EventDataPaged
from .localizable_string_paged import LocalizableStringPaged
from .metric_definition_paged import MetricDefinitionPaged
from .single_metric_baseline_paged import SingleMetricBaselinePaged
from .metric_alert_resource_paged import MetricAlertResourcePaged
from .log_search_rule_resource_paged import LogSearchRuleResourcePaged
from .metric_namespace_paged import MetricNamespacePaged
from .monitor_management_client_enums import (
    MetricStatisticType,
    TimeAggregationType,
    ComparisonOperationType,
    ScaleDirection,
    ScaleType,
    RecurrenceFrequency,
    ConditionOperator,
    TimeAggregationOperator,
    CategoryType,
    ReceiverStatus,
    EventLevel,
    Unit,
    AggregationType,
    Sensitivity,
    BaselineSensitivity,
    Enabled,
    ProvisioningState,
    QueryType,
    ConditionalOperator,
    MetricTriggerType,
    AlertSeverity,
    OnboardingStatus,
    DataStatus,
    ResultType,
)

__all__ = [
    'Resource',
    'ScaleCapacity',
    'MetricTrigger',
    'ScaleAction',
    'ScaleRule',
    'TimeWindow',
    'RecurrentSchedule',
    'Recurrence',
    'AutoscaleProfile',
    'EmailNotification',
    'WebhookNotification',
    'AutoscaleNotification',
    'AutoscaleSettingResource',
    'AutoscaleSettingResourcePatch',
    'ErrorResponse', 'ErrorResponseException',
    'OperationDisplay',
    'Operation',
    'OperationListResult',
    'Incident',
    'RuleDataSource',
    'RuleCondition',
    'RuleMetricDataSource',
    'RuleManagementEventClaimsDataSource',
    'RuleManagementEventDataSource',
    'ThresholdRuleCondition',
    'LocationThresholdRuleCondition',
    'ManagementEventAggregationCondition',
    'ManagementEventRuleCondition',
    'RuleAction',
    'RuleEmailAction',
    'RuleWebhookAction',
    'AlertRuleResource',
    'AlertRuleResourcePatch',
    'RetentionPolicy',
    'LogProfileResource',
    'LogProfileResourcePatch',
    'ProxyOnlyResource',
    'MetricSettings',
    'LogSettings',
    'DiagnosticSettingsResource',
    'DiagnosticSettingsResourceCollection',
    'DiagnosticSettingsCategoryResource',
    'DiagnosticSettingsCategoryResourceCollection',
    'EmailReceiver',
    'SmsReceiver',
    'WebhookReceiver',
    'ItsmReceiver',
    'AzureAppPushReceiver',
    'AutomationRunbookReceiver',
    'VoiceReceiver',
    'LogicAppReceiver',
    'AzureFunctionReceiver',
    'ArmRoleReceiver',
    'ActionGroupResource',
    'EnableRequest',
    'ActionGroupPatchBody',
    'ActivityLogAlertLeafCondition',
    'ActivityLogAlertAllOfCondition',
    'ActivityLogAlertActionGroup',
    'ActivityLogAlertActionList',
    'ActivityLogAlertResource',
    'ActivityLogAlertPatchBody',
    'LocalizableString',
    'SenderAuthorization',
    'HttpRequestInfo',
    'EventData',
    'MetricAvailability',
    'MetricDefinition',
    'MetricValue',
    'MetadataValue',
    'TimeSeriesElement',
    'Metric',
    'Response',
    'BaselineMetadataValue',
    'Baseline',
    'BaselineResponse',
    'TimeSeriesInformation',
    'CalculateBaselineResponse',
    'MetricSingleDimension',
    'SingleBaseline',
    'BaselineMetadata',
    'TimeSeriesBaseline',
    'SingleMetricBaseline',
    'MetricAlertAction',
    'MetricAlertCriteria',
    'MetricAlertResource',
    'MetricAlertResourcePatch',
    'MetricAlertStatusProperties',
    'MetricAlertStatus',
    'MetricAlertStatusCollection',
    'MetricDimension',
    'MetricCriteria',
    'MetricAlertSingleResourceMultipleMetricCriteria',
    'MultiMetricCriteria',
    'MetricAlertMultipleResourceMultipleMetricCriteria',
    'Source',
    'Schedule',
    'Action',
    'LogSearchRuleResource',
    'LogSearchRuleResourcePatch',
    'LogMetricTrigger',
    'TriggerCondition',
    'AzNsActionGroup',
    'AlertingAction',
    'Dimension',
    'Criteria',
    'LogToMetricAction',
    'MetricNamespaceName',
    'MetricNamespace',
    'ProxyResource',
    'Error',
    'ResponseWithError', 'ResponseWithErrorException',
    'WorkspaceInfo',
    'DataContainer',
    'VMInsightsOnboardingStatus',
    'AutoscaleSettingResourcePaged',
    'IncidentPaged',
    'AlertRuleResourcePaged',
    'LogProfileResourcePaged',
    'ActionGroupResourcePaged',
    'ActivityLogAlertResourcePaged',
    'EventDataPaged',
    'LocalizableStringPaged',
    'MetricDefinitionPaged',
    'SingleMetricBaselinePaged',
    'MetricAlertResourcePaged',
    'LogSearchRuleResourcePaged',
    'MetricNamespacePaged',
    'MetricStatisticType',
    'TimeAggregationType',
    'ComparisonOperationType',
    'ScaleDirection',
    'ScaleType',
    'RecurrenceFrequency',
    'ConditionOperator',
    'TimeAggregationOperator',
    'CategoryType',
    'ReceiverStatus',
    'EventLevel',
    'Unit',
    'AggregationType',
    'Sensitivity',
    'BaselineSensitivity',
    'Enabled',
    'ProvisioningState',
    'QueryType',
    'ConditionalOperator',
    'MetricTriggerType',
    'AlertSeverity',
    'OnboardingStatus',
    'DataStatus',
    'ResultType',
]
