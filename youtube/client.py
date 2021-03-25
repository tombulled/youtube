import babel

import functools
import typing

import innertube
import innertube.enums
import innertube.clients
import innertube.operations

from . import models
from . import operations
from . import parsers
from . import decorators

def wraps(wrapped):
    def decorator(func):
        return_annotation = getattr(func, '__annotations__', {}).get('return')

        wrapper = functools.wraps(wrapped)(func)

        getattr(wrapper, '__annotations__', {})['return'] = return_annotation

        return wrapper

    return decorator

class YouTube(innertube.ClientGroup):
    def __init__(self, locale: babel.Locale = None):
        super().__init__ \
        (
            service = innertube.enums.ServiceType.YOUTUBE,
            devices =  \
            (
                innertube.enums.DeviceType.WEB,
                innertube.enums.DeviceType.ANDROID,
                innertube.enums.DeviceType.TV,
            ),
            locale = locale,
        )

    @wraps(innertube.operations.complete_search)
    def complete_search(self, *args, **kwargs) -> typing.List[str]:
        return super().complete_search \
        (
            *args,
            client = self(innertube.enums.DeviceType.TV).info.identifier,
            locale = self.locale,
            **kwargs,
        )

    @decorators.parse(parsers.parse_watch)
    @wraps(operations.watch)
    def watch(self, *args, **kwargs) -> models.WatchResponse:
        return operations.watch(*args, **kwargs)

    @decorators.parse(parsers.parse_video_info)
    @wraps(operations.video_info)
    def video_info(self, *args, **kwargs) -> models.PlayerResponse:
        return operations.video_info(*args, **kwargs)

    @decorators.parse(parsers.parse_guide)
    @wraps(innertube.clients.Client.guide)
    def guide(self, *args, **kwargs) -> typing.List[models.Pivot]:
        return self(innertube.enums.DeviceType.ANDROID).guide(*args, **kwargs)

    @decorators.parse(parsers.parse_player)
    @wraps(innertube.clients.Client.player)
    def player(self, *args, **kwargs) -> models.PlayerResponse:
        return self(innertube.enums.DeviceType.ANDROID).player(*args, **kwargs)

    @decorators.parse(parsers.parse_next)
    @wraps(innertube.clients.Client.next)
    def next(self, *args, **kwargs) -> models.WatchNextResponse:
        return self(innertube.enums.DeviceType.WEB).next(*args, **kwargs)
