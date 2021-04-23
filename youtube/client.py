import innertube
import innertube.enums
import innertube.operations

import typing

from . import parsers
from . import decorators
from . import models
from . import operations

class YouTube(innertube.ClientGroup):
    def __init__(self, locale: innertube.Locale = None):
        super().__init__ \
        (
            service = innertube.Service.YOUTUBE,
            devices =  \
            (
                innertube.enums.Device.WEB,
                innertube.enums.Device.ANDROID,
                innertube.enums.Device.TV,
            ),
            locale = locale,
        )

    @decorators.method(innertube.operations.complete_search)
    def complete_search(self, *args, **kwargs) -> typing.List[str]:
        app = innertube.infos.apps[innertube.enums.App.YOUTUBE_TV]

        return innertube.operations.complete_search \
        (
            *args,
            client = app.client.identifier,
            locale = self.locale,
            **kwargs,
        )

    @decorators.method(operations.get_video_info, parsers.video_info)
    def video_info(self, *args, **kwargs) -> models.PlayerResponse:
        return operations.get_video_info(*args, **kwargs)

    @decorators.method(operations.watch, parsers.watch)
    # def watch(self, *args, **kwargs) -> models.WatchResponse:
    def watch(self, *args, **kwargs):
        return operations.watch(*args, **kwargs)

    @decorators.method(innertube.Client.guide, parsers.guide)
    def guide(self, *args, **kwargs) -> typing.List[models.Pivot]:
        return self(innertube.enums.Device.ANDROID).guide(*args, **kwargs)

    @decorators.method(innertube.Client.player, parsers.player)
    # def player(self, *args, **kwargs) -> models.PlayerResponse:
    def player(self, *args, **kwargs):
        return self(innertube.enums.Device.ANDROID).player(*args, **kwargs)
