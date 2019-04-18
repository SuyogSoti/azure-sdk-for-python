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


class Frame(Model):
    """Video frame property details.

    :param timestamp: Timestamp of the frame.
    :type timestamp: str
    :param frame_image: Frame image.
    :type frame_image: str
    :param metadata: Array of KeyValue.
    :type metadata:
     list[~azure.cognitiveservices.vision.contentmoderator.models.KeyValuePair]
    :param reviewer_result_tags: Reviewer result tags.
    :type reviewer_result_tags:
     list[~azure.cognitiveservices.vision.contentmoderator.models.Tag]
    """

    _attribute_map = {
        'timestamp': {'key': 'Timestamp', 'type': 'str'},
        'frame_image': {'key': 'FrameImage', 'type': 'str'},
        'metadata': {'key': 'Metadata', 'type': '[KeyValuePair]'},
        'reviewer_result_tags': {'key': 'ReviewerResultTags', 'type': '[Tag]'},
    }

    def __init__(self, **kwargs):
        super(Frame, self).__init__(**kwargs)
        self.timestamp = kwargs.get('timestamp', None)
        self.frame_image = kwargs.get('frame_image', None)
        self.metadata = kwargs.get('metadata', None)
        self.reviewer_result_tags = kwargs.get('reviewer_result_tags', None)
