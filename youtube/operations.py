'''
Library containing (non-innertube) YouTube related operations

These operations are used by the YouTube service, but do not go through
the InnerTube API.

Usage:
    >>> from youtube import operations
    >>>
    >>> dir(operations)
    ...
    >>>
    >>> operations.video_info
    <function video_info at 0x7fd5476ec670>
    >>>
'''

import innertube
import innertube.utils
import innertube.enums
import innertube.errors

import requests
import furl

import json
import re
import urllib.parse

from typing import \
(
    Union,
    Optional,
)

def watch \
        (
            *,
            video_id:    Optional[str] = None,
            playlist_id: Optional[str] = None,
            index:       Optional[int] = None,
        ) -> dict:
    '''
    Dispatch a 'watch' request to YouTube
    '''

    client = innertube.client \
    (
        service = innertube.services.YouTube,
        device  = innertube.devices.Web,
    )

    response = client.adaptor.session.get \
    (
        url = furl.furl \
        (
            scheme = innertube.enums.Scheme.HTTPS.value,
            host   = client.info.service.domain,
            path   = 'watch',
        ),
        params = innertube.utils.filtered_dict \
        (
            v     = 'dQw4w9WgXcQ',
            list  = playlist_id,
            index = index,
            pbj   = 1,
            # Note: Another option is 'pp' which == playerParams
        ),
    )

    return \
    {
        key: value
        for item in response.json()
        for key, value in item.items()
    }

# TODO: Add localisation support
def video_info(*, video_id: str) -> dict:
    '''
    Dispatch a 'video_info' request to YouTube
    '''

    response = requests.get \
    (
        url = furl.furl \
        (
            scheme = innertube.enums.Scheme.HTTPS.value,
            host   = innertube.services.YouTube.domain,
            path   = 'get_video_info',
        ),
        params = dict \
        (
            video_id = video_id,
            el       = 'detailpage',
            ps       = 'default',
            hl       = 'en',
            gl       = 'US',
        ),
    )

    data = dict(urllib.parse.parse_qsl(response.text))

    if 'errorcode' in data:
        raise innertube.errors.YouTubeException \
        (
            dict \
            (
                code    = data.get('errorcode'),
                status  = data.get('status'),
                message = data.get('reason'),
            )
        )

    def fflags(data):
        fflags = query_string(data)

        js_types = dict \
        (
            true  = True,
            false = False,
            null  = None,
        )

        new_fflags = {}

        for fflag_key, fflag_val in fflags.items():
            if fflag_val in js_types:
                fflag_val = js_types[fflag_val]
            elif fflag_val.isdigit():
                fflag_val = int(fflag_val)
            elif re.match(r'^\d+\.\d+$', fflag_val.strip()) is not None:
                fflag_val = float(fflag_val)

            new_fflags[fflag_key] = fflag_val

        return new_fflags

    def csv(data):
        return data.strip(',').split(',')

    def query_string(data):
        return dict(urllib.parse.parse_qsl(data))

    def b64(data):
        return base64.b64decode(data.encode()).decode()

    def boolean(data):
        return bool(int(data))

    def csv_of(type):
        def wrapper(data):
            return list(map(type, csv(data)))

        return wrapper

    parsers = dict \
    (
        fexp                   = csv_of(int),
        fflags                 = fflags,
        account_playback_token = b64,
        timestamp              = int,
        enablecsi              = boolean,
        use_miniplayer_ui      = boolean,
        autoplay_count         = int,
        player_response        = json.loads,
        watch_next_response    = json.loads,
        watermark              = csv,
        rvs                    = query_string,
    )

    for key, value in data.items():
        if key in parsers:
            data[key] = parsers[key](value)

    return data
