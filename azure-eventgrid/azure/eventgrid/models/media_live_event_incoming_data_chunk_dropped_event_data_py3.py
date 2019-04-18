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


class MediaLiveEventIncomingDataChunkDroppedEventData(Model):
    """Ingest fragment dropped event data.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar timestamp: Gets the timestamp of the data chunk dropped.
    :vartype timestamp: str
    :ivar track_type: Gets the type of the track (Audio / Video).
    :vartype track_type: str
    :ivar bitrate: Gets the bitrate of the track.
    :vartype bitrate: long
    :ivar timescale: Gets the timescale of the Timestamp.
    :vartype timescale: str
    :ivar result_code: Gets the result code for fragment drop operation.
    :vartype result_code: str
    :ivar track_name: Gets the name of the track for which fragment is
     dropped.
    :vartype track_name: str
    """

    _validation = {
        'timestamp': {'readonly': True},
        'track_type': {'readonly': True},
        'bitrate': {'readonly': True},
        'timescale': {'readonly': True},
        'result_code': {'readonly': True},
        'track_name': {'readonly': True},
    }

    _attribute_map = {
        'timestamp': {'key': 'timestamp', 'type': 'str'},
        'track_type': {'key': 'trackType', 'type': 'str'},
        'bitrate': {'key': 'bitrate', 'type': 'long'},
        'timescale': {'key': 'timescale', 'type': 'str'},
        'result_code': {'key': 'resultCode', 'type': 'str'},
        'track_name': {'key': 'trackName', 'type': 'str'},
    }

    def __init__(self, **kwargs) -> None:
        super(MediaLiveEventIncomingDataChunkDroppedEventData, self).__init__(**kwargs)
        self.timestamp = None
        self.track_type = None
        self.bitrate = None
        self.timescale = None
        self.result_code = None
        self.track_name = None
