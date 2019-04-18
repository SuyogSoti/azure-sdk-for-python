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
    from .image_object_py3 import ImageObject
    from .video_object_py3 import VideoObject
    from .query_py3 import Query
    from .pivot_suggestions_py3 import PivotSuggestions
    from .videos_py3 import Videos
    from .search_results_answer_py3 import SearchResultsAnswer
    from .answer_py3 import Answer
    from .query_context_py3 import QueryContext
    from .media_object_py3 import MediaObject
    from .response_py3 import Response
    from .thing_py3 import Thing
    from .creative_work_py3 import CreativeWork
    from .identifiable_py3 import Identifiable
    from .error_py3 import Error
    from .error_response_py3 import ErrorResponse, ErrorResponseException
    from .trending_videos_tile_py3 import TrendingVideosTile
    from .trending_videos_subcategory_py3 import TrendingVideosSubcategory
    from .trending_videos_category_py3 import TrendingVideosCategory
    from .trending_videos_py3 import TrendingVideos
    from .videos_module_py3 import VideosModule
    from .video_details_py3 import VideoDetails
    from .response_base_py3 import ResponseBase
except (SyntaxError, ImportError):
    from .image_object import ImageObject
    from .video_object import VideoObject
    from .query import Query
    from .pivot_suggestions import PivotSuggestions
    from .videos import Videos
    from .search_results_answer import SearchResultsAnswer
    from .answer import Answer
    from .query_context import QueryContext
    from .media_object import MediaObject
    from .response import Response
    from .thing import Thing
    from .creative_work import CreativeWork
    from .identifiable import Identifiable
    from .error import Error
    from .error_response import ErrorResponse, ErrorResponseException
    from .trending_videos_tile import TrendingVideosTile
    from .trending_videos_subcategory import TrendingVideosSubcategory
    from .trending_videos_category import TrendingVideosCategory
    from .trending_videos import TrendingVideos
    from .videos_module import VideosModule
    from .video_details import VideoDetails
    from .response_base import ResponseBase
from .video_search_client_enums import (
    VideoQueryScenario,
    ErrorCode,
    ErrorSubCode,
    Freshness,
    VideoLength,
    VideoPricing,
    VideoResolution,
    SafeSearch,
    TextFormat,
    VideoInsightModule,
)

__all__ = [
    'ImageObject',
    'VideoObject',
    'Query',
    'PivotSuggestions',
    'Videos',
    'SearchResultsAnswer',
    'Answer',
    'QueryContext',
    'MediaObject',
    'Response',
    'Thing',
    'CreativeWork',
    'Identifiable',
    'Error',
    'ErrorResponse', 'ErrorResponseException',
    'TrendingVideosTile',
    'TrendingVideosSubcategory',
    'TrendingVideosCategory',
    'TrendingVideos',
    'VideosModule',
    'VideoDetails',
    'ResponseBase',
    'VideoQueryScenario',
    'ErrorCode',
    'ErrorSubCode',
    'Freshness',
    'VideoLength',
    'VideoPricing',
    'VideoResolution',
    'SafeSearch',
    'TextFormat',
    'VideoInsightModule',
]
