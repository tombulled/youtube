import enum
import mimetypes
import pycountry

CountryCode = enum.Enum \
(
    'CountryCode',
    {
        country.alpha_2: country.alpha_2
        for country in pycountry.countries
    }
)

class AudioQuality(enum.Enum):
    LOW    = 'AUDIO_QUALITY_LOW'
    MEDIUM = 'AUDIO_QUALITY_MEDIUM'
    HIGH   = 'AUDIO_QUALITY_HIGH'

class MimeType(enum.Enum):
    AUDIO_WEBM = 'audio/webm'
    AUDIO_MP4  = 'audio/mp4'
    VIDEO_WEBM = 'video/webm'
    VIDEO_MP4  = 'video/mp4'
    VIDEO_3GPP = 'video/3gpp'

    def guess_extension(self):
        return mimetypes.guess_extension(self.value)

    def guess_all_extensions(self):
        return mimetypes.guess_all_extensions(self.value)

class CodecType(enum.Enum):
    AV1  = 'av01'
    AVC1 = 'avc1'
    MP4A = 'mp4a'
    MP4V = 'mp4v'
    VP9  = 'vp9'
    OPUS = 'opus'

class ProjectionType(enum.Enum):
    RECTANGULAR = 'RECTANGULAR'

class QualityType(enum.Enum):
    LARGE  = 'large'
    MEDIUM = 'medium'
    SMALL  = 'small'
    TINY   = 'tiny'

    HD_1080 = 'hd1080'
    HD_720  = 'hd720'

class QualityLabel(enum.Enum):
    HD_1080 = '1080p'
    HD_720  = '720p'

    SD_480 = '480p'
    SD_360 = '360p'
    SD_240 = '240p'
    SD_144 = '144p'

class AudioChannels(enum.Enum):
    STEREO = 2
    MONO   = 1

class CategoryType(enum.Enum):
    MUSIC = 'Music'

class ContinuationType(str, enum.Enum):
    WATCH_NEXT = 'WATCH_NEXT'

class ContinuationRequestType(str, enum.Enum):
    WATCH_NEXT = 'CONTINUATION_REQUEST_TYPE_WATCH_NEXT'

    @property
    def type(self):
        return ContinuationType(self.name)

class BrowseId(str, enum.Enum):
    HASHTAG       = 'FEhashtag'
    HOME          = 'FEwhat_to_watch'
    EXPLORE       = 'FEexplore'
    SUBSCRIPTIONS = 'FEsubscriptions'
    LIBRARY       = 'FElibrary'

class BadgeType(str, enum.Enum):
    VERIFIED        = 'VERIFIED'
    VERIFIED_ARTIST = 'VERIFIED_ARTIST'
    LIVE_NOW        = 'LIVE_NOW'
    SIMPLE          = 'SIMPLE'
    YPC             = 'YPC'

class BadgeStyleType(str, enum.Enum):
    VERIFIED        = 'BADGE_STYLE_TYPE_VERIFIED'
    VERIFIED_ARTIST = 'BADGE_STYLE_TYPE_VERIFIED_ARTIST'
    LIVE_NOW        = 'BADGE_STYLE_TYPE_LIVE_NOW'
    SIMPLE          = 'BADGE_STYLE_TYPE_SIMPLE'
    YPC             = 'BADGE_STYLE_TYPE_YPC'

    @property
    def type(self):
        return BadgeType(self.name)

class PivotType(str, enum.Enum):
    HOME          = 'HOME'
    EXPLORE       = 'EXPLORE'
    SUBSCRIPTIONS = 'SUBSCRIPTIONS'
    LIBRARY       = 'LIBRARY'

class PivotIdentifier(str, enum.Enum):
    HOME          = 'pivot-w2w'
    EXPLORE       = 'pivot-explore'
    SUBSCRIPTIONS = 'pivot-subs'
    LIBRARY       = 'pivot-library'

    @property
    def type(self):
        return PivotType(self.name)
