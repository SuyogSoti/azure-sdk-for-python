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


class MetricId(str, Enum):

    requestscount = "requests/count"
    requestsduration = "requests/duration"
    requestsfailed = "requests/failed"
    userscount = "users/count"
    usersauthenticated = "users/authenticated"
    page_viewscount = "pageViews/count"
    page_viewsduration = "pageViews/duration"
    clientprocessing_duration = "client/processingDuration"
    clientreceive_duration = "client/receiveDuration"
    clientnetwork_duration = "client/networkDuration"
    clientsend_duration = "client/sendDuration"
    clienttotal_duration = "client/totalDuration"
    dependenciescount = "dependencies/count"
    dependenciesfailed = "dependencies/failed"
    dependenciesduration = "dependencies/duration"
    exceptionscount = "exceptions/count"
    exceptionsbrowser = "exceptions/browser"
    exceptionsserver = "exceptions/server"
    sessionscount = "sessions/count"
    performance_countersrequest_execution_time = "performanceCounters/requestExecutionTime"
    performance_countersrequests_per_second = "performanceCounters/requestsPerSecond"
    performance_countersrequests_in_queue = "performanceCounters/requestsInQueue"
    performance_countersmemory_available_bytes = "performanceCounters/memoryAvailableBytes"
    performance_countersexceptions_per_second = "performanceCounters/exceptionsPerSecond"
    performance_countersprocess_cpu_percentage = "performanceCounters/processCpuPercentage"
    performance_countersprocess_io_bytes_per_second = "performanceCounters/processIOBytesPerSecond"
    performance_countersprocess_private_bytes = "performanceCounters/processPrivateBytes"
    performance_countersprocessor_cpu_percentage = "performanceCounters/processorCpuPercentage"
    availability_resultsavailability_percentage = "availabilityResults/availabilityPercentage"
    availability_resultsduration = "availabilityResults/duration"
    billingtelemetry_count = "billing/telemetryCount"
    custom_eventscount = "customEvents/count"


class MetricsAggregation(str, Enum):

    min = "min"
    max = "max"
    avg = "avg"
    sum = "sum"
    count = "count"
    unique = "unique"


class MetricsSegment(str, Enum):

    application_build = "applicationBuild"
    application_version = "applicationVersion"
    authenticated_or_anonymous_traffic = "authenticatedOrAnonymousTraffic"
    browser = "browser"
    browser_version = "browserVersion"
    city = "city"
    cloud_role_name = "cloudRoleName"
    cloud_service_name = "cloudServiceName"
    continent = "continent"
    country_or_region = "countryOrRegion"
    deployment_id = "deploymentId"
    deployment_unit = "deploymentUnit"
    device_type = "deviceType"
    environment = "environment"
    hosting_location = "hostingLocation"
    instance_name = "instanceName"


class EventType(str, Enum):

    all = "$all"
    traces = "traces"
    custom_events = "customEvents"
    page_views = "pageViews"
    browser_timings = "browserTimings"
    requests = "requests"
    dependencies = "dependencies"
    exceptions = "exceptions"
    availability_results = "availabilityResults"
    performance_counters = "performanceCounters"
    custom_metrics = "customMetrics"
