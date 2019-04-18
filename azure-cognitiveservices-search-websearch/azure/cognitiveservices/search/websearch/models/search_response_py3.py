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

from .response_py3 import Response


class SearchResponse(Response):
    """Defines the top-level object that the response includes when the request
    succeeds.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    All required parameters must be populated in order to send to Azure.

    :param _type: Required. Constant filled by server.
    :type _type: str
    :ivar id: A String identifier.
    :vartype id: str
    :ivar web_search_url: The URL To Bing's search result for this item.
    :vartype web_search_url: str
    :ivar query_context: An object that contains the query string that Bing
     used for the request. This object contains the query string as entered by
     the user. It may also contain an altered query string that Bing used for
     the query if the query string contained a spelling mistake.
    :vartype query_context:
     ~azure.cognitiveservices.search.websearch.models.QueryContext
    :ivar web_pages: A list of webpages that are relevant to the search query.
    :vartype web_pages:
     ~azure.cognitiveservices.search.websearch.models.WebWebAnswer
    :ivar images: A list of images that are relevant to the search query.
    :vartype images: ~azure.cognitiveservices.search.websearch.models.Images
    :ivar news: A list of news articles that are relevant to the search query.
    :vartype news: ~azure.cognitiveservices.search.websearch.models.News
    :ivar related_searches: A list of related queries made by others.
    :vartype related_searches:
     ~azure.cognitiveservices.search.websearch.models.RelatedSearchesRelatedSearchAnswer
    :ivar spell_suggestions: The query string that likely represents the
     user's intent.
    :vartype spell_suggestions:
     ~azure.cognitiveservices.search.websearch.models.SpellSuggestions
    :ivar time_zone: The date and time of one or more geographic locations.
    :vartype time_zone:
     ~azure.cognitiveservices.search.websearch.models.TimeZone
    :ivar videos: A list of videos that are relevant to the search query.
    :vartype videos: ~azure.cognitiveservices.search.websearch.models.Videos
    :ivar computation: The answer to a math expression or units conversion
     expression.
    :vartype computation:
     ~azure.cognitiveservices.search.websearch.models.Computation
    :ivar ranking_response: The order that Bing suggests that you display the
     search results in.
    :vartype ranking_response:
     ~azure.cognitiveservices.search.websearch.models.RankingRankingResponse
    """

    _validation = {
        '_type': {'required': True},
        'id': {'readonly': True},
        'web_search_url': {'readonly': True},
        'query_context': {'readonly': True},
        'web_pages': {'readonly': True},
        'images': {'readonly': True},
        'news': {'readonly': True},
        'related_searches': {'readonly': True},
        'spell_suggestions': {'readonly': True},
        'time_zone': {'readonly': True},
        'videos': {'readonly': True},
        'computation': {'readonly': True},
        'ranking_response': {'readonly': True},
    }

    _attribute_map = {
        '_type': {'key': '_type', 'type': 'str'},
        'id': {'key': 'id', 'type': 'str'},
        'web_search_url': {'key': 'webSearchUrl', 'type': 'str'},
        'query_context': {'key': 'queryContext', 'type': 'QueryContext'},
        'web_pages': {'key': 'webPages', 'type': 'WebWebAnswer'},
        'images': {'key': 'images', 'type': 'Images'},
        'news': {'key': 'news', 'type': 'News'},
        'related_searches': {'key': 'relatedSearches', 'type': 'RelatedSearchesRelatedSearchAnswer'},
        'spell_suggestions': {'key': 'spellSuggestions', 'type': 'SpellSuggestions'},
        'time_zone': {'key': 'timeZone', 'type': 'TimeZone'},
        'videos': {'key': 'videos', 'type': 'Videos'},
        'computation': {'key': 'computation', 'type': 'Computation'},
        'ranking_response': {'key': 'rankingResponse', 'type': 'RankingRankingResponse'},
    }

    def __init__(self, **kwargs) -> None:
        super(SearchResponse, self).__init__(**kwargs)
        self.query_context = None
        self.web_pages = None
        self.images = None
        self.news = None
        self.related_searches = None
        self.spell_suggestions = None
        self.time_zone = None
        self.videos = None
        self.computation = None
        self.ranking_response = None
        self._type = 'SearchResponse'
