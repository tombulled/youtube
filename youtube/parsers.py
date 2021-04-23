import addict
import pydantic

import mime

import typing
import functools
import itertools

from . import utils
from . import enums

def guide(data: addict.Dict) -> typing.List[addict.Dict]:
    return \
    [
        utils.filter \
        (
            title     = item.title.runs[0].text,
            browse_id = item.navigationEndpoint.browseEndpoint.browseId,
            type      = utils.parse \
            (
                item.targetId,
                enums.PivotIdentifier,
                lambda value: value.type.value,
            ),
        )
        for item in utils.flatten \
        (
            utils.flatten(data['items']).pivotBarRenderer[0]['items']
        ).pivotBarItemRenderer
    ]

def player(data: addict.Dict):
    streams = \
    [
        utils.filter \
        (
            itag           = stream.itag,
            loudness       = stream.loudnessDb,
            url            = stream.url,
            bitrate        = stream.averageBitrate or stream.bitrate,
            projection     = stream.projectionType,
            content_length = utils.parse(stream.contentLength, int),
            duration       = utils.parse(stream.approxDurationMs, int, 1e-3.__mul__),
            last_modified  = utils.parse(stream.lastModified, int, 1e-6.__mul__),
            ranges = stream.indexRange and \
            {
                key: utils.filter \
                (
                    start = utils.parse(range.start, int),
                    end   = utils.parse(range.end,   int),
                )
                for key, range in utils.filter \
                (
                    index = stream.indexRange,
                    init  = stream.initRange,
                ).items()
            },
            quality = utils.filter \
            (
                type  = stream.quality,
                label = stream.qualityLabel,
            ),
            video = stream.fps and utils.filter \
            (
                fps = stream.fps,
                dimensions = utils.filter \
                (
                    width  = stream.width,
                    height = stream.height,
                ),
            ),
            audio = stream.audioQuality and utils.filter \
            (
                channels    = stream.audioChannels,
                sample_rate = utils.parse(stream.audioSampleRate, int),
                quality     = utils.parse \
                (
                    stream.audioQuality,
                    str.upper,
                    functools.partial \
                    (
                        utils.lstrip,
                        substring = 'AUDIO_QUALITY_',
                    ),
                ),
            ),
            ** utils.parse \
            (
                stream.mimeType,
                mime.parse,
                pydantic.BaseModel.dict,
                addict.Dict,
                lambda mime: utils.filter \
                (
                    mime = utils.filter \
                    (
                        type    = mime.type,
                        subtype = mime.subtype,
                    ),
                    codecs = \
                    [
                        utils.filter \
                        (
                            type    = codec[0],
                            version = codec[1],
                        )
                        for codec in map \
                        (
                            lambda item: utils.parse \
                            (
                                item,
                                str.strip,
                                functools.partial \
                                (
                                    str.split,
                                    sep      = '.',
                                    maxsplit = 1,
                                ),
                                enumerate,
                                addict.Dict,
                            ),
                            utils.parse \
                            (
                                mime.parameters.codecs,
                                functools.partial \
                                (
                                    str.split,
                                    sep = ',',
                                ),
                            )
                        )
                    ],
                ),
            ),
        )
        for stream in itertools.chain \
        (
            data.streamingData.formats,
            data.streamingData.adaptiveFormats,
        )
    ]

    video_details = utils.filter \
    (
        video_id    = data.videoDetails.videoId,
        author      = data.videoDetails.author,
        channel_id  = data.videoDetails.channelId,
        keywords    = data.videoDetails.keywords,
        description = data.videoDetails.shortDescription,
        title       = data.videoDetails.title,
        rating      = data.videoDetails.averageRating,
        view_count  = utils.parse(data.videoDetails.viewCount, int),
        duration    = utils.parse(data.videoDetails.lengthSeconds, int),
        flags = utils.filter \
        (
            ratable          = data.videoDetails.allowRatings,
            crawlable        = data.videoDetails.isCrawlable,
            live_content     = data.videoDetails.isLiveContent,
            owner_viewing    = data.videoDetails.isOwnerViewing,
            private          = data.videoDetails.isPrivate,
            unplugged_corpus = data.videoDetails.isUnpluggedCorpus,
        ),
        thumbnails = \
        [
            thumbnail
            for item in data.videoDetails.thumbnail.thumbnails
            if \
            (
                thumbnail := utils.filter \
                (
                    url = item.url,
                    dimensions = utils.filter \
                    (
                        width  = item.width,
                        height = item.height,
                    ),
                )
            )
        ],
    )

    microformat = utils.parse \
    (
        data.microformat.playerMicroformatRenderer,
        lambda microformat: utils.filter \
        (
            countries      = microformat.availableCountries,
            category       = microformat.category,
            description    = microformat.description.simpleText,
            title          = microformat.title.simpleText,
            view_count     = utils.parse(microformat.viewCount, int),
            date_published = microformat.publishDate,
            date_uploaded  = microformat.uploadDate,
            duration       = utils.parse(microformat.lengthSeconds, int),
            channel = utils.filter \
            (
                id   = microformat.externalChannelId,
                name = microformat.ownerChannelName,
                url  = microformat.ownerProfileUrl,
            ),
            flags = utils.filter \
            (
                ypc_metadata = microformat.hasYpcMetadata,
                family_safe  = microformat.isFamilySafe,
                unlisted     = microformat.isUnlisted,
            ),
            thumbnails = \
            [
                thumbnail
                for item in microformat.thumbnail.thumbnails
                if \
                (
                    thumbnail := utils.filter \
                    (
                        url = item.url,
                        dimensions = utils.filter \
                        (
                            width  = item.width,
                            height = item.height,
                        ),
                    )
                )
            ],
        ),
    )

    return utils.filter \
    (
        streams       = streams,
        video_details = video_details,
        microformat   = microformat
    )

def watch(data: addict.Dict) -> addict.Dict:
    return data

def video_info(data: addict.Dict) -> addict.Dict:
    return player(data.player_response)
