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


class MediaLiveEventEncoderConnectedEventData(Model):
    """Encoder connect event data.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar ingest_url: Gets the ingest URL provided by the live event.
    :vartype ingest_url: str
    :ivar stream_id: Gets the stream Id.
    :vartype stream_id: str
    :ivar encoder_ip: Gets the remote IP.
    :vartype encoder_ip: str
    :ivar encoder_port: Gets the remote port.
    :vartype encoder_port: str
    """

    _validation = {
        'ingest_url': {'readonly': True},
        'stream_id': {'readonly': True},
        'encoder_ip': {'readonly': True},
        'encoder_port': {'readonly': True},
    }

    _attribute_map = {
        'ingest_url': {'key': 'ingestUrl', 'type': 'str'},
        'stream_id': {'key': 'streamId', 'type': 'str'},
        'encoder_ip': {'key': 'encoderIp', 'type': 'str'},
        'encoder_port': {'key': 'encoderPort', 'type': 'str'},
    }

    def __init__(self, **kwargs) -> None:
        super(MediaLiveEventEncoderConnectedEventData, self).__init__(**kwargs)
        self.ingest_url = None
        self.stream_id = None
        self.encoder_ip = None
        self.encoder_port = None
