'''
Library containing (non-innertube) YouTube related operations

These operations are used by the YouTube service, but do not go through
the InnerTube API.
'''

import innertube
# import innertube.utils
import innertube.enums
# import innertube.errors
import innertube.infos
import innertube.sessions
# import innertube.models
import innertube.clients

# import requests
# import furl
import addict

import json
import re
import urllib.parse
import typing

class BaseAppClient(innertube.clients.BaseClient):
    def __call__(self, *args, **kwargs):
        return self.session.get(*args, **kwargs)

class AppClient(BaseAppClient):
    # TODO: Investigate if localisation can be added
    def watch \
            (
                self,
                *,
                video_id:    typing.Optional[str] = None,
                playlist_id: typing.Optional[str] = None,
                index:       typing.Optional[int] = None,
            ) -> dict:
        '''
        Dispatch a 'watch' request to YouTube
        '''

        response = self \
        (
            'watch',
            params = dict \
            (
                v     = video_id,
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
    def get_video_info(self, *, video_id: str) -> dict:
        '''
        Dispatch a 'get_video_info' request to YouTube
        '''

        response = self \
        (
            'get_video_info',
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
            # TODO: Raise correct exception
            raise Exception \
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

        return addict.Dict(data)

def app_client(app: innertube.enums.App):
    schema  = innertube.infos.schemas[app]
    app     = innertube.infos.apps[app]
    service = innertube.infos.services[schema.service]

    session = innertube.sessions.BaseUrlSession \
    (
        base_url = str(service.host()),
    )

    session.headers.update \
    (
        app.headers().dict \
        (
            by_alias     = True,
            exclude_none = True,
        ),
    )

    return AppClient \
    (
        session = session,
    )
