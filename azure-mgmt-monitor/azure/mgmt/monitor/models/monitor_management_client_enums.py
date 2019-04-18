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

from enum import Enum


class MetricStatisticType(str, Enum):

    average = "Average"
    min = "Min"
    max = "Max"
    sum = "Sum"


class TimeAggregationType(str, Enum):

    average = "Average"
    minimum = "Minimum"
    maximum = "Maximum"
    total = "Total"
    count = "Count"
    last = "Last"


class ComparisonOperationType(str, Enum):

    equals = "Equals"
    not_equals = "NotEquals"
    greater_than = "GreaterThan"
    greater_than_or_equal = "GreaterThanOrEqual"
    less_than = "LessThan"
    less_than_or_equal = "LessThanOrEqual"


class ScaleDirection(str, Enum):

    none = "None"
    increase = "Increase"
    decrease = "Decrease"


class ScaleType(str, Enum):

    change_count = "ChangeCount"
    percent_change_count = "PercentChangeCount"
    exact_count = "ExactCount"


class RecurrenceFrequency(str, Enum):

    none = "None"
    second = "Second"
    minute = "Minute"
    hour = "Hour"
    day = "Day"
    week = "Week"
    month = "Month"
    year = "Year"


class ConditionOperator(str, Enum):

    greater_than = "GreaterThan"
    greater_than_or_equal = "GreaterThanOrEqual"
    less_than = "LessThan"
    less_than_or_equal = "LessThanOrEqual"


class TimeAggregationOperator(str, Enum):

    average = "Average"
    minimum = "Minimum"
    maximum = "Maximum"
    total = "Total"
    last = "Last"


class CategoryType(str, Enum):

    metrics = "Metrics"
    logs = "Logs"


class ReceiverStatus(str, Enum):

    not_specified = "NotSpecified"
    enabled = "Enabled"
    disabled = "Disabled"


class EventLevel(str, Enum):

    critical = "Critical"
    error = "Error"
    warning = "Warning"
    informational = "Informational"
    verbose = "Verbose"


class Unit(str, Enum):

    count = "Count"
    bytes = "Bytes"
    seconds = "Seconds"
    count_per_second = "CountPerSecond"
    bytes_per_second = "BytesPerSecond"
    percent = "Percent"
    milli_seconds = "MilliSeconds"
    byte_seconds = "ByteSeconds"
    unspecified = "Unspecified"


class AggregationType(str, Enum):

    none = "None"
    average = "Average"
    count = "Count"
    minimum = "Minimum"
    maximum = "Maximum"
    total = "Total"


class Sensitivity(str, Enum):

    low = "Low"
    medium = "Medium"
    high = "High"


class BaselineSensitivity(str, Enum):

    low = "Low"
    medium = "Medium"
    high = "High"


class Enabled(str, Enum):

    true = "true"
    false = "false"


class ProvisioningState(str, Enum):

    succeeded = "Succeeded"
    deploying = "Deploying"
    canceled = "Canceled"
    failed = "Failed"


class QueryType(str, Enum):

    result_count = "ResultCount"


class ConditionalOperator(str, Enum):

    greater_than = "GreaterThan"
    less_than = "LessThan"
    equal = "Equal"


class MetricTriggerType(str, Enum):

    consecutive = "Consecutive"
    total = "Total"


class AlertSeverity(str, Enum):

    zero = "0"
    one = "1"
    two = "2"
    three = "3"
    four = "4"


class OnboardingStatus(str, Enum):

    onboarded = "onboarded"
    not_onboarded = "notOnboarded"
    unknown = "unknown"


class DataStatus(str, Enum):

    present = "present"
    not_present = "notPresent"


class ResultType(str, Enum):

    data = "Data"
    metadata = "Metadata"
