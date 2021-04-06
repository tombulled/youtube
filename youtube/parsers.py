import addict
import pendulum

import mime

import datetime
import typing

from . import models
from . import enums
from . import maps
from . import utils
from . import types

def parse_guide(data: dict) -> typing.List[models.Pivot]:
    return \
    [
        models.Pivot \
        (
            title     = utils.get(item.title.runs[0].text),
            type      = utils.get(item.targetId, lambda value: enums.PivotIdentifier(value).type),
            browse_id = utils.get(item.navigationEndpoint.browseEndpoint.browseId),
        )
        for item in list(addict.Dict(data)['items'][0].values())[0]['items']
        for item in item.values()
    ]

def parse_player(data: dict) -> models.PlayerResponse:
    data = addict.Dict(data)

    streams = []

    for stream in [*data.streamingData.formats, *data.streamingData.adaptiveFormats]:
        has_audio = bool(stream.audioQuality)
        has_video = bool(stream.fps)

        mime_type = utils.get \
        (
            stream.mimeType,
            mime.parse,
            lambda value: addict.Dict(value.dict()),
        )

        stream_data = dict \
        (
            itag = utils.get(stream.itag),
            loudness = utils.get(stream.loudnessDb),
            url = utils.get(stream.url, models.Url),
            content_length = utils.get(stream.contentLength),
            bitrate = utils.get(stream.averageBitrate or stream.bitrate),
            projection = utils.get(stream.projectionType),
            duration = utils.get(stream.approxDurationMs, int, 1e-3.__mul__),
            last_modified = utils.get(stream.lastModified, int, 1e-6.__mul__),
            mime = utils.get \
            (
                mime_type,
                lambda value: models.Stream.MimeType \
                (
                    type    = value.type,
                    subtype = value.subtype,
                ),
            ),
            extension = utils.get \
            (
                mime_type,
                lambda value: maps.file_extensions.get(value.subtype),
            ),
            codecs = utils.get \
            (
                mime_type,
                lambda value: \
                [
                    models.Stream.Codec \
                    (
                        type    = codec_type,
                        version = codec_version,
                    )
                    for codec in value.parameters.codecs.split(',')
                    for codec_type, codec_version, *_ in \
                    (
                        (
                            *codec.strip().split('.', 1),
                            None,
                        ),
                    )
                ],
            ),
            range = utils.get \
            (
                stream.indexRange or stream.initRange,
                lambda _: models.Stream.Range \
                (
                    ** \
                    {
                        key: utils.get \
                        (
                            value,
                            lambda range: models.Stream.Range.IntegerRange \
                            (
                                start = utils.get(range.start),
                                end   = utils.get(range.end),
                            )
                        )
                        for key, value in dict \
                        (
                            index = stream.indexRange,
                            init  = stream.initRange,
                        ).items()
                    }
                )
            ),
            quality = utils.get \
            (
                stream.quality or stream.qualityLabel,
                lambda _: models.Stream.Quality \
                (
                    type  = utils.get(stream.quality),
                    label = utils.get(stream.qualityLabel),
                ),
            ),
            video = utils.get \
            (
                has_video or None,
                lambda _: models.VideoStream.Video \
                (
                    fps = utils.get(stream.fps),
                    dimensions = utils.get \
                    (
                        stream.width or stream.height,
                        lambda _: models.Dimensions \
                        (
                            width  = utils.get(stream.width),
                            height = utils.get(stream.height),
                        ),
                    ),
                ),
            ),
            audio = utils.get \
            (
                has_audio or None,
                lambda _: models.AudioStream.Audio \
                (
                    channels    = utils.get(stream.audioChannels),
                    quality     = utils.get(stream.audioQuality),
                    sample_rate = utils.get(stream.audioSampleRate),
                ),
            ),
        )

        stream_class = \
        (
            models.Stream,
            models.AudioStream,
            models.VideoStream,
            models.AudioVideoStream,
        )[has_audio + 2 * has_video]

        streams.append(stream_class(**stream_data))

        from pprint import pprint as pp
        pp(streams[-1].dict())

    video_details = models.PlayerResponse.VideoDetails \
    (
        video_id    = utils.get(data.videoDetails.videoId),
        author      = utils.get(data.videoDetails.author),
        channel_id  = utils.get(data.videoDetails.channelId),
        keywords    = utils.get(data.videoDetails.keywords),
        description = utils.get(data.videoDetails.shortDescription),
        title       = utils.get(data.videoDetails.title),
        rating      = utils.get(data.videoDetails.averageRating),
        view_count  = utils.get(data.videoDetails.viewCount),
        duration    = utils.get(data.videoDetails.lengthSeconds, int),
        thumbnails  = \
        [
            models.Thumbnail \
            (
                url = utils.get(thumbnail.url, models.Url),
                dimensions = utils.get \
                (
                    thumbnail.width or thumbnail.height,
                    lambda _: models.Dimensions \
                    (
                        width  = utils.get(thumbnail.width),
                        height = utils.get(thumbnail.height),
                    ),
                ),
            )
            for thumbnail in data.videoDetails.thumbnail.thumbnails
        ],
        flags = models.PlayerResponse.VideoDetails.Flags \
        (
            ratable          = utils.get(data.videoDetails.allowRatings),
            crawlable        = utils.get(data.videoDetails.isCrawlable),
            live_content     = utils.get(data.videoDetails.isLiveContent),
            owner_viewing    = utils.get(data.videoDetails.isOwnerViewing),
            private          = utils.get(data.videoDetails.isPrivate),
            unplugged_corpus = utils.get(data.videoDetails.isUnpluggedCorpus),
        ),
    )

    microformat = utils.get \
    (
        data.microformat.playerMicroformatRenderer,
        lambda data: models.PlayerResponse.Microformat \
        (
            countries      = utils.get(data.availableCountries),
            category       = utils.get(data.category),
            description    = utils.get(data.description.simpleText),
            title          = utils.get(data.title.simpleText),
            view_count     = utils.get(data.viewCount),
            date_published = utils.get(data.publishDate),
            date_uploaded  = utils.get(data.uploadDate),
            duration       = utils.get(data.lengthSeconds, int),
            channel = models.PlayerResponse.Microformat.Channel \
            (
                id   = utils.get(data.externalChannelId),
                name = utils.get(data.ownerChannelName),
                url  = utils.get(data.ownerProfileUrl),
            ),
            thumbnails = \
            [
                models.Thumbnail \
                (
                    url = utils.get(thumbnail.url, models.Url),
                    dimensions = utils.get \
                    (
                        thumbnail.width or thumbnail.height,
                        lambda _: models.Dimensions \
                        (
                            width  = utils.get(thumbnail.width),
                            height = utils.get(thumbnail.height),
                        ),
                    ),
                )
                for thumbnail in data.thumbnail.thumbnails
            ],
            flags = models.PlayerResponse.Microformat.Flags \
            (
                ypc_metadata = utils.get(data.hasYpcMetadata),
                family_safe  = utils.get(data.isFamilySafe),
                unlisted     = utils.get(data.isUnlisted),
            ),
        ),
    )

    return models.PlayerResponse \
    (
        video_details = video_details,
        streams       = streams,
        microformat   = microformat,
    )

def parse_next(data: dict) -> models.WatchNextResponse:
    data = addict.Dict(data)

    watch_next_results           = utils.flatten(data.contents.twoColumnWatchNextResults.results.results.contents)
    watch_next_results_secondary = utils.flatten(data.contents.twoColumnWatchNextResults.secondaryResults.secondaryResults.results)

    video_info_primary   = watch_next_results.videoPrimaryInfoRenderer[0]
    video_info_secondary = watch_next_results.videoSecondaryInfoRenderer[0]

    continuation_item = watch_next_results_secondary.continuationItemRenderer[0]

    return models.WatchNextResponse \
    (
        video_info = models.WatchNextResponse.VideoInfo \
        (
            video_id      = utils.get(data.currentVideoEndpoint.watchEndpoint.videoId),
            title         = utils.get(video_info_primary.title.runs[0].text),
            view_count    = utils.get(video_info_primary.viewCount.videoViewCountRenderer.viewCount.simpleText),
            like_count    = utils.get(video_info_primary.sentimentBar.sentimentBarRenderer.tooltip, lambda value: value.split('/')[0]),
            dislike_count = utils.get(video_info_primary.sentimentBar.sentimentBarRenderer.tooltip, lambda value: value.split('/')[1]),
            # date          = utils.get(video_info_primary.dateText.simpleText, lambda value: pendulum.instance(datetime.datetime.strptime(value.replace('.', ''), '%d %b %Y')).date()),
            date          = utils.get(video_info_primary.dateText.simpleText),
            hashtags = \
            [
                models.Hashtag \
                (
                    text   = utils.get(run.text, lambda value: value.lstrip('#')),
                    params = utils.get(run.navigationEndpoint.browseEndpoint.params),
                )
                for run in video_info_primary.superTitleLink.runs
                if run.navigationEndpoint
            ],
            owner = models.WatchNextResponse.VideoInfo.Owner \
            (
                channel_name = utils.get(video_info_secondary.owner.videoOwnerRenderer.title.runs[0].text),
                channel_id = utils.get(video_info_secondary.owner.videoOwnerRenderer.navigationEndpoint.browseEndpoint.browseId),
                subscribers = utils.get(video_info_secondary.owner.videoOwnerRenderer.subscriberCountText.simpleText, lambda value: value.split(' ')[0].strip()),
                thumbnails = \
                [
                    models.Thumbnail \
                    (
                        url = utils.get(thumbnail.url, models.Url),
                        dimensions = utils.get \
                        (
                            thumbnail.width or thumbnail.height,
                            lambda _: models.Dimensions \
                            (
                                width  = utils.get(thumbnail.width),
                                height = utils.get(thumbnail.height),
                            ),
                        ),
                    )
                    for thumbnail in video_info_secondary.owner.videoOwnerRenderer.thumbnail.thumbnails
                ],
                badges = \
                [
                    models.Badge \
                    (
                        style = utils.get(badge.style, lambda value: enums.BadgeStyleType(value).type),
                        label = utils.get(badge.tooltip),
                    )
                    for badge in video_info_secondary.owner.videoOwnerRenderer.badges
                    for badge in badge.values()
                ],
            ),
            metadata = \
            [
                models.WatchNextResponse.VideoInfo.Metadata \
                (
                    title   = utils.get(metadata.title.simpleText),
                    content = utils.get(metadata.contents[0].simpleText),
                )
                for row in video_info_secondary.metadataRowContainer.metadataRowContainerRenderer.rows
                for metadata in row.values()
                if metadata.contents[0] and metadata.title
            ],
            description = \
            [
                (
                    run.navigationEndpoint.urlEndpoint \
                    and models.Link \
                    (
                        text = utils.get(run.text),
                        url  = utils.get(run.navigationEndpoint.urlEndpoint.url),
                    )
                ) or \
                (
                    run.navigationEndpoint.browseEndpoint \
                    and \
                    (
                        run.navigationEndpoint.browseEndpoint.browseId == enums.BrowseId.HASHTAG \
                        and models.Hashtag \
                        (
                            text = utils.get(run.text),
                            params = utils.get(run.navigationEndpoint.browseEndpoint.params),
                        )
                    )
                ) or \
                models.Text \
                (
                    text = utils.get(run.text),
                )
                for run in video_info_secondary.description.runs
            ],
        ),
        continuation = models.Continuation \
        (
            type  = utils.get(continuation_item.continuationEndpoint.continuationCommand.request),
            token = utils.get(continuation_item.continuationEndpoint.continuationCommand.token),
        ),
        recommendations = \
        [
            * \
            (
                models.VideoRecommendation \
                (
                    id = utils.get(data.currentVideoEndpoint.watchEndpoint.videoId),
                    duration = utils.get(item.lengthText.simpleText),
                    view_count = utils.get(item.viewCountText.simpleText, lambda value: value.split(' ')[0].replace(',', '')) \
                        or utils.get(item.viewCountText.runs[0].text),
                    rich_thumbnail = utils.get \
                    (
                        [
                            models.MovingThumbnail \
                            (
                                url = utils.get(thumbnail.url, models.Url),
                                dimensions = utils.get \
                                (
                                    thumbnail.width or thumbnail.height,
                                    lambda _: models.Dimensions \
                                    (
                                        width  = utils.get(thumbnail.width),
                                        height = utils.get(thumbnail.height),
                                    ),
                                ),
                            )
                            for thumbnail in item.richThumbnail.movingThumbnailRenderer.movingThumbnailDetails.thumbnails
                        ] or None,
                        lambda thumbnails: thumbnails[0],
                    ),
                    published_time = utils.get(item.publishedTimeText.simpleText),
                    title = utils.get(item.title.simpleText),
                    watch = models.WatchEndpoint \
                    (
                        video_id = utils.get(data.currentVideoEndpoint.watchEndpoint.videoId),
                    ),
                    thumbnails = \
                    [
                        models.Thumbnail \
                        (
                            url = utils.get(thumbnail.url, models.Url),
                            dimensions = utils.get \
                            (
                                thumbnail.width or thumbnail.height,
                                lambda _: models.Dimensions \
                                (
                                    width  = utils.get(thumbnail.width),
                                    height = utils.get(thumbnail.height),
                                ),
                            ),
                        )
                        for thumbnail in item.thumbnail.thumbnails
                    ],
                    badges = \
                    [
                        models.Badge \
                        (
                            style = utils.get(badge.style, lambda value: enums.BadgeStyleType(value).type),
                            label = utils.get(badge.label),
                        )
                        for badge in item.badges
                        for badge in badge.values()
                    ],
                    channel = models.VideoRecommendation.Channel \
                    (
                        id = utils.get(item.longBylineText.runs[0].navigationEndpoint.browseEndpoint.browseId),
                        name = utils.get(item.longBylineText.runs[0].text),
                        thumbnail = \
                        [
                            models.Thumbnail \
                            (
                                url = utils.get(thumbnail.url, models.Url),
                                dimensions = utils.get \
                                (
                                    thumbnail.width or thumbnail.height,
                                    lambda _: models.Dimensions \
                                    (
                                        width  = utils.get(thumbnail.width),
                                        height = utils.get(thumbnail.height),
                                    ),
                                ),
                            )
                            for thumbnail in item.channelThumbnail.thumbnails
                        ][0],
                        badges = \
                        [
                            models.Badge \
                            (
                                style = utils.get(badge.style, lambda value: enums.BadgeStyleType(value).type),
                                label = utils.get(badge.tooltip),
                            )
                            for badge in item.ownerBadges
                            for badge in badge.values()
                        ],
                    ),
                )
                for item in watch_next_results_secondary.compactVideoRenderer
            ),
            * \
            (
                models.PlaylistRecommendation \
                (
                    id = utils.get(item.playlistId),
                    video_count = utils.get(item.videoCountShortText.simpleText),
                    title = utils.get(item.title.simpleText),
                    watch = models.WatchEndpoint \
                    (
                        params = utils.get(item.navigationEndpoint.watchEndpoint.params),
                        playlist_id = utils.get(item.navigationEndpoint.watchEndpoint.playlistId),
                        video_id = utils.get(item.navigationEndpoint.watchEndpoint.videoId),
                    ),
                    thumbnails = \
                    [
                        models.Thumbnail \
                        (
                            url = utils.get(thumbnail.url, models.Url),
                            dimensions = utils.get \
                            (
                                thumbnail.width or thumbnail.height,
                                lambda _: models.Dimensions \
                                (
                                    width  = utils.get(thumbnail.width),
                                    height = utils.get(thumbnail.height),
                                ),
                            ),
                        )
                        for thumbnail in item.thumbnailRenderer.playlistCustomThumbnailRenderer.thumbnail.thumbnails
                    ],
                    channel = models.PlaylistRecommendation.Channel \
                    (
                        id = utils.get(item.longBylineText.runs[0].navigationEndpoint.browseEndpoint.browseId),
                        name = utils.get(item.longBylineText.runs[0].text),
                    ),
                )
                for item in watch_next_results_secondary.compactPlaylistRenderer
            ),
            * \
            (
                models.RadioRecommendation \
                (
                    id = utils.get(item.playlistId),
                    video_count = utils.get(item.videoCountShortText.runs[0].text),
                    title = utils.get(item.title.simpleText),
                    watch = models.WatchEndpoint \
                    (
                        params = utils.get(item.navigationEndpoint.watchEndpoint.params),
                        playlist_id = utils.get(item.navigationEndpoint.watchEndpoint.playlistId),
                        video_id = utils.get(item.navigationEndpoint.watchEndpoint.videoId),
                    ),
                    thumbnails = \
                    [
                        models.Thumbnail \
                        (
                            url = utils.get(thumbnail.url, models.Url),
                            dimensions = utils.get \
                            (
                                thumbnail.width or thumbnail.height,
                                lambda _: models.Dimensions \
                                (
                                    width  = utils.get(thumbnail.width),
                                    height = utils.get(thumbnail.height),
                                ),
                            ),
                        )
                        for thumbnail in item.thumbnail.thumbnails
                    ],
                    channel = models.RadioRecommendation.Channel \
                    (
                        id = None,
                        name = utils.get(item.longBylineText.simpleText),
                    ),
                )
                for item in watch_next_results_secondary.compactRadioRenderer
            ),
        ],
    )

def parse_video_info(data: dict) -> models.PlayerResponse:
    return parse_player(addict.Dict(data).player_response)

def parse_watch(data: dict) -> models.WatchResponse:
    data = addict.Dict(data)

    return models.WatchResponse \
    (
        player     = parse_player(data.playerResponse),
        watch_next = parse_next(data.response),
    )
