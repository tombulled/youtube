import addict
import innertube.models
# import innertube.devices
# import innertube.services
from . import utils
from . import operations

from innertube.models import \
(
    AppInfo,
)

from typing import \
(
    Any,
)

# def get_web_app_info() -> AppInfo:
#     data = addict.Dict \
#     (
#         operations.video_info \
#         (
#             video_id = constants.SAMPLE_VIDEO_ID,
#         )
#     )
#
#     return innertube.models.AppInfo \
#     (
#         client = innertube.models.ClientInfo \
#         (
#             name    = utils.get(data.c),
#             version = utils.get(data.cver),
#         ),
#         device  = innertube.devices.Web,
#         service = innertube.services.YouTube,
#         api     = innertube.models.ApiInfo \
#         (
#             key     = utils.get(data.innertube_api_key),
#             version = utils.get(data.innertube_api_version, lambda value: value.lstrip('v')),
#         ),
#     )

def flatten(items) -> addict.Dict:
    flat = addict.Dict()

    for item in items:
        for key, val in item.items():
            flat.setdefault(key, []).append(val)

    return flat

def get(value: Any, *formatters):
    if value in (None, {}):
        return

    for formatter in formatters:
        try:
            value = formatter(value)
        except:
            raise # TEMP

            return

    return value
