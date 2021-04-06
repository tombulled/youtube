import pydantic
import humanize

import mime.enums

import urllib.parse

from . import enums

from typing import \
(
    Optional,
    List,
    Dict,
)

from pydantype import \
(
    String,
    Float,
    Boolean,
)

from .enums import \
(
    AudioQuality,
    # MimeType,
    CodecType,
    ProjectionType,
    QualityType,
    QualityLabel,
    AudioChannels,
    CountryCode,
    CategoryType,
    ContinuationRequestType,
    BadgeType,
    BrowseId,
    PivotType,
)

from .types import \
(
    Integer,
    Url,
    DataSize,
    ContentLength,
    Bitrate,
    SampleRate,
    ContinuationToken,
    Duration,
    DateTime,
    Date,
    VideoId,
    ViewCount,
    Rating,
    VideoTitle,
    Keyword,
    ChannelId,
    VideoDescription,
    FileExtension,
    CodecVersion,
    Loudness,
    ChannelName,
    Params,
    PlaylistId,
    Id,
    ChannelUrl,
)

class BaseModel(pydantic.BaseModel): pass

class Pivot(BaseModel):
    title:      String
    type:       PivotType
    browse_id:  BrowseId

class Continuation(BaseModel):
    type:  ContinuationRequestType
    token: ContinuationToken

class Badge(BaseModel):
    label: String # (Localised)
    style: BadgeType

class Text(BaseModel):
    text: String

class Hashtag(Text):
    params: Params

class Link(Text):
    url: Url

class Dimensions(BaseModel):
    height: Integer
    width:  Integer

class Thumbnail(BaseModel):
    url:        Url
    dimensions: Dimensions

class MovingThumbnail(Thumbnail): pass

class Stream(BaseModel):
    class Range(BaseModel):
        class IntegerRange(BaseModel):
            start: Integer
            end:   Integer

        index: IntegerRange
        init:  IntegerRange

    # class MimeType(BaseModel):
    #     class Codec(BaseModel):
    #         type:    CodecType
    #         version: Optional[CodecVersion]
    #
    #     type:      MimeType
    #     subtype:   MimeType
    #     codecs:    List[Codec]
    #     extension: FileExtension

    class Quality(BaseModel):
        label: Optional[QualityLabel]
        type:  QualityType

    class MimeType(BaseModel):
        type:    mime.enums.MediaType
        subtype: enums.MediaSubtype

    class Codec(BaseModel):
        type:    CodecType
        version: Optional[CodecVersion]

    itag:           Integer
    duration:       Duration
    last_modified:  DateTime
    content_length: Optional[ContentLength]
    mime:           MimeType
    url:            Optional[Url]
    bitrate:        Bitrate
    projection:     ProjectionType
    quality:        Quality
    range:          Optional[Range]
    loudness:       Optional[Loudness]

    codecs:    List[Codec]
    extension: FileExtension
    mime:      MimeType

class AudioStream(Stream):
    class Audio(BaseModel):
        channels:    AudioChannels
        quality:     AudioQuality
        sample_rate: SampleRate

    audio: Audio

class VideoStream(Stream):
    class Video(BaseModel):
        dimensions: Dimensions
        fps:        Integer

    video: Video

class AudioVideoStream(AudioStream, VideoStream): pass

class PlayerResponse(BaseModel):
    class VideoDetails(BaseModel):
        class Flags(BaseModel):
            ratable:          Boolean
            crawlable:        Boolean
            live_content:     Boolean
            owner_viewing:    Boolean
            private:          Boolean
            unplugged_corpus: Boolean

        video_id:    VideoId
        author:      str
        channel_id:  ChannelId
        keywords:    List[Keyword]
        duration:    Duration
        description: VideoDescription
        thumbnails:  List[Thumbnail]
        title:       VideoTitle
        rating:      Rating
        view_count:  ViewCount
        flags:       Flags

    class Microformat(BaseModel):
        class Channel(BaseModel):
            id:   ChannelId
            name: ChannelName
            url:  ChannelUrl

        class Flags(BaseModel):
            ypc_metadata: Boolean
            family_safe:  Boolean
            unlisted:     Boolean

        countries:      List[CountryCode]
        category:       CategoryType
        description:    VideoDescription
        date_published: Date
        date_uploaded:  Date
        duration:       Duration
        thumbnails:     List[Thumbnail]
        title:          VideoTitle
        view_count:     Integer
        flags:          Flags
        channel:        Channel

    streams:       List[Stream]
    video_details: VideoDetails
    microformat:   Optional[Microformat]

class WatchEndpoint(BaseModel):
    params:      Optional[Params]
    video_id:    Optional[VideoId]
    playlist_id: Optional[PlaylistId]

# Named: CompactItem?
class Recommendation(BaseModel):
    class Channel(BaseModel):
        id: Optional[str]
        name: ChannelName
        thumbnail: Optional[Thumbnail]
        badges: Optional[List[Badge]]

    title: str
    watch: WatchEndpoint
    thumbnails: List[Thumbnail]
    id: Id
    channel: Channel

# Named: CompactVideo?
class VideoRecommendation(Recommendation):
    duration: Optional[Duration]
    view_count: ViewCount
    rich_thumbnail: Optional[Thumbnail]
    published_time: Optional[str]
    badges: Optional[List[Badge]]

class PlaylistRecommendation(Recommendation):
    video_count: str # E.g. could be '50+'

class RadioRecommendation(PlaylistRecommendation): pass

class WatchNextResponse(BaseModel):
    class VideoInfo(BaseModel):
        class Owner(BaseModel):
            channel_name: ChannelName
            channel_id:   ChannelId
            subscribers:  str
            thumbnails:   List[Thumbnail]
            badges:       List[Badge]

        class Metadata(BaseModel):
            title:   String # (Localised)
            content: String # (Localised) TODO: Some can be 'rich' (e.g. have links)

        video_id: VideoId
        title: VideoTitle
        view_count: ViewCount
        like_count: Integer
        dislike_count: Integer
        hashtags: List[Hashtag]
        # date: Date
        date: String # This gets localised, needs proper parsing (babel?)
        owner: Owner
        metadata: List[Metadata]
        description: List[Text]

    video_info:      VideoInfo
    recommendations: List[Recommendation]
    continuation:    Continuation

class WatchResponse(BaseModel):
    watch_next: WatchNextResponse
    player:     PlayerResponse
