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

import uuid
from msrest.pipeline import ClientRawResponse
from msrest.polling import LROPoller, NoPolling
from msrestazure.polling.arm_polling import ARMPolling

from .. import models


class OriginsOperations(object):
    """OriginsOperations operations.

    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    :ivar api_version: Version of the API to be used with the client request. Current version is 2017-04-02. Constant value: "2025-01-01".
    """

    models = models

    def __init__(self, client, config, serializer, deserializer):

        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer
        self.api_version = "2025-01-01"

        self.config = config

    def list_by_endpoint(
            self, resource_group_name, profile_name, endpoint_name, custom_headers=None, raw=False, **operation_config):
        """Lists all of the existing origins within an endpoint.

        :param resource_group_name: Name of the Resource group within the
         Azure subscription.
        :type resource_group_name: str
        :param profile_name: Name of the CDN profile which is unique within
         the resource group.
        :type profile_name: str
        :param endpoint_name: Name of the endpoint under the profile which is
         unique globally.
        :type endpoint_name: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: An iterator like instance of Origin
        :rtype:
         ~azure.mgmt.cdn.models.OriginPaged[~azure.mgmt.cdn.models.Origin]
        :raises:
         :class:`ErrorResponseException<azure.mgmt.cdn.models.ErrorResponseException>`
        """
        def internal_paging(next_link=None, raw=False):

            if not next_link:
                # Construct URL
                url = self.list_by_endpoint.metadata['url']
                path_format_arguments = {
                    'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str', max_length=90, min_length=1, pattern=r'^[-\w\._\(\)]+$'),
                    'profileName': self._serialize.url("profile_name", profile_name, 'str'),
                    'endpointName': self._serialize.url("endpoint_name", endpoint_name, 'str'),
                    'subscriptionId': self._serialize.url("self.config.subscription_id", self.config.subscription_id, 'str')
                }
                url = self._client.format_url(url, **path_format_arguments)

                # Construct parameters
                query_parameters = {}
                query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

            else:
                url = next_link
                query_parameters = {}

            # Construct headers
            header_parameters = {}
            header_parameters['Accept'] = 'application/json'
            if self.config.generate_client_request_id:
                header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
            if custom_headers:
                header_parameters.update(custom_headers)
            if self.config.accept_language is not None:
                header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

            # Construct and send request
            request = self._client.get(url, query_parameters, header_parameters)
            response = self._client.send(request, stream=False, **operation_config)

            if response.status_code not in [200]:
                raise models.ErrorResponseException(self._deserialize, response)

            return response

        # Deserialize response
        deserialized = models.OriginPaged(internal_paging, self._deserialize.dependencies)

        if raw:
            header_dict = {}
            client_raw_response = models.OriginPaged(internal_paging, self._deserialize.dependencies, header_dict)
            return client_raw_response

        return deserialized
    list_by_endpoint.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/profiles/{profileName}/endpoints/{endpointName}/origins'}

    def get(
            self, resource_group_name, profile_name, endpoint_name, origin_name, custom_headers=None, raw=False, **operation_config):
        """Gets an existing origin within an endpoint.

        :param resource_group_name: Name of the Resource group within the
         Azure subscription.
        :type resource_group_name: str
        :param profile_name: Name of the CDN profile which is unique within
         the resource group.
        :type profile_name: str
        :param endpoint_name: Name of the endpoint under the profile which is
         unique globally.
        :type endpoint_name: str
        :param origin_name: Name of the origin which is unique within the
         endpoint.
        :type origin_name: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: Origin or ClientRawResponse if raw=true
        :rtype: ~azure.mgmt.cdn.models.Origin or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<azure.mgmt.cdn.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.get.metadata['url']
        path_format_arguments = {
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str', max_length=90, min_length=1, pattern=r'^[-\w\._\(\)]+$'),
            'profileName': self._serialize.url("profile_name", profile_name, 'str'),
            'endpointName': self._serialize.url("endpoint_name", endpoint_name, 'str'),
            'originName': self._serialize.url("origin_name", origin_name, 'str'),
            'subscriptionId': self._serialize.url("self.config.subscription_id", self.config.subscription_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Accept'] = 'application/json'
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

        # Construct and send request
        request = self._client.get(url, query_parameters, header_parameters)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('Origin', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    get.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/profiles/{profileName}/endpoints/{endpointName}/origins/{originName}'}


    def _update_initial(
            self, resource_group_name, profile_name, endpoint_name, origin_name, origin_update_properties, custom_headers=None, raw=False, **operation_config):
        # Construct URL
        url = self.update.metadata['url']
        path_format_arguments = {
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str', max_length=90, min_length=1, pattern=r'^[-\w\._\(\)]+$'),
            'profileName': self._serialize.url("profile_name", profile_name, 'str'),
            'endpointName': self._serialize.url("endpoint_name", endpoint_name, 'str'),
            'originName': self._serialize.url("origin_name", origin_name, 'str'),
            'subscriptionId': self._serialize.url("self.config.subscription_id", self.config.subscription_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Accept'] = 'application/json'
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

        # Construct body
        body_content = self._serialize.body(origin_update_properties, 'OriginUpdateParameters')

        # Construct and send request
        request = self._client.patch(url, query_parameters, header_parameters, body_content)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200, 202]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('Origin', response)
        if response.status_code == 202:
            deserialized = self._deserialize('Origin', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    def update(
            self, resource_group_name, profile_name, endpoint_name, origin_name, origin_update_properties, custom_headers=None, raw=False, polling=True, **operation_config):
        """Updates an existing origin within an endpoint.

        :param resource_group_name: Name of the Resource group within the
         Azure subscription.
        :type resource_group_name: str
        :param profile_name: Name of the CDN profile which is unique within
         the resource group.
        :type profile_name: str
        :param endpoint_name: Name of the endpoint under the profile which is
         unique globally.
        :type endpoint_name: str
        :param origin_name: Name of the origin which is unique within the
         endpoint.
        :type origin_name: str
        :param origin_update_properties: Origin properties
        :type origin_update_properties:
         ~azure.mgmt.cdn.models.OriginUpdateParameters
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: The poller return type is ClientRawResponse, the
         direct response alongside the deserialized response
        :param polling: True for ARMPolling, False for no polling, or a
         polling object for personal polling strategy
        :return: An instance of LROPoller that returns Origin or
         ClientRawResponse<Origin> if raw==True
        :rtype:
         ~msrestazure.azure_operation.AzureOperationPoller[~azure.mgmt.cdn.models.Origin]
         or
         ~msrestazure.azure_operation.AzureOperationPoller[~msrest.pipeline.ClientRawResponse[~azure.mgmt.cdn.models.Origin]]
        :raises:
         :class:`ErrorResponseException<azure.mgmt.cdn.models.ErrorResponseException>`
        """
        raw_result = self._update_initial(
            resource_group_name=resource_group_name,
            profile_name=profile_name,
            endpoint_name=endpoint_name,
            origin_name=origin_name,
            origin_update_properties=origin_update_properties,
            custom_headers=custom_headers,
            raw=True,
            **operation_config
        )

        def get_long_running_output(response):
            deserialized = self._deserialize('Origin', response)

            if raw:
                client_raw_response = ClientRawResponse(deserialized, response)
                return client_raw_response

            return deserialized

        lro_delay = operation_config.get(
            'long_running_operation_timeout',
            self.config.long_running_operation_timeout)
        if polling is True: polling_method = ARMPolling(lro_delay, **operation_config)
        elif polling is False: polling_method = NoPolling()
        else: polling_method = polling
        return LROPoller(self._client, raw_result, get_long_running_output, polling_method)
    update.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/profiles/{profileName}/endpoints/{endpointName}/origins/{originName}'}
