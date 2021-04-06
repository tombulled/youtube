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

class StrEnum(str, enum.Enum): pass

class AudioQuality(StrEnum):
    LOW    = 'AUDIO_QUALITY_LOW'
    MEDIUM = 'AUDIO_QUALITY_MEDIUM'
    HIGH   = 'AUDIO_QUALITY_HIGH'

class ProjectionType(StrEnum):
    RECTANGULAR = 'RECTANGULAR'

class QualityType(StrEnum):
    LARGE  = 'large'
    MEDIUM = 'medium'
    SMALL  = 'small'
    TINY   = 'tiny'

    HD_1080 = 'hd1080'
    HD_720  = 'hd720'

class QualityLabel(StrEnum):
    HD_1080 = '1080p'
    HD_720  = '720p'

    SD_480 = '480p'
    SD_360 = '360p'
    SD_240 = '240p'
    SD_144 = '144p'

class AudioChannels(enum.Enum):
    MONO   = 1
    STEREO = 2

class CategoryType(StrEnum):
    MUSIC = 'Music'

class ContinuationType(StrEnum):
    WATCH_NEXT = 'WATCH_NEXT'

class ContinuationRequestType(StrEnum):
    WATCH_NEXT = 'CONTINUATION_REQUEST_TYPE_WATCH_NEXT'

    @property
    def type(self):
        return ContinuationType(self.name)

class BrowseId(StrEnum):
    HASHTAG       = 'FEhashtag'
    HOME          = 'FEwhat_to_watch'
    EXPLORE       = 'FEexplore'
    SUBSCRIPTIONS = 'FEsubscriptions'
    LIBRARY       = 'FElibrary'

class BadgeType(StrEnum):
    VERIFIED        = 'VERIFIED'
    VERIFIED_ARTIST = 'VERIFIED_ARTIST'
    LIVE_NOW        = 'LIVE_NOW'
    SIMPLE          = 'SIMPLE'
    YPC             = 'YPC'

class BadgeStyleType(StrEnum):
    VERIFIED        = 'BADGE_STYLE_TYPE_VERIFIED'
    VERIFIED_ARTIST = 'BADGE_STYLE_TYPE_VERIFIED_ARTIST'
    LIVE_NOW        = 'BADGE_STYLE_TYPE_LIVE_NOW'
    SIMPLE          = 'BADGE_STYLE_TYPE_SIMPLE'
    YPC             = 'BADGE_STYLE_TYPE_YPC'

    @property
    def type(self):
        return BadgeType(self.name)

class PivotType(StrEnum):
    HOME          = 'HOME'
    EXPLORE       = 'EXPLORE'
    SUBSCRIPTIONS = 'SUBSCRIPTIONS'
    LIBRARY       = 'LIBRARY'

class PivotIdentifier(StrEnum):
    HOME          = 'pivot-w2w'
    EXPLORE       = 'pivot-explore'
    SUBSCRIPTIONS = 'pivot-subs'
    LIBRARY       = 'pivot-library'

    @property
    def type(self):
        return PivotType(self.name)

class CodecType(StrEnum):
    _generate_next_value_ = lambda name, *_: name.lower()

    AV01 = enum.auto()
    AVC1 = enum.auto()
    MP4A = enum.auto()
    MP4V = enum.auto()
    VP9  = enum.auto()
    OPUS = enum.auto()

class MediaType(StrEnum):
    _generate_next_value_ = lambda name, *_: name.lower().replace('_', '')

    WEBM  = enum.auto()
    MP4   = enum.auto()
    _3GP = enum.auto()

class MediaSubtype(StrEnum):
    _generate_next_value_ = lambda name, *_: name.lower().replace('_', '')

    WEBM  = enum.auto()
    MP4   = enum.auto()
    _3GPP = enum.auto()
