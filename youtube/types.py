import pendulum
import pydantype
import furl
import humanize
import string

from typing import \
(
    Union,
    Any,
)

class Params(pydantype.String): pass

class Integer(pydantype.Integer):
    @pydantype.validator()
    def validate_any(cls, value: Any):
        if isinstance(value, str):
            value = ''.join(char for char in value if char in string.digits)

        return cls.new(value)

class Loudness(pydantype.Float): pass

class CodecVersion(pydantype.String): pass

class FileExtension(pydantype.String): pass

class Description(pydantype.String): pass

class VideoDescription(Description): pass

class Keyword(pydantype.String): pass

class ChannelName(pydantype.String): pass

class Id(pydantype.String): pass
class VideoId(Id): pass
class ChannelId(Id): pass
class PlaylistId(Id): pass

class Rating(pydantype.Float): pass

class Title(pydantype.String): pass
class VideoTitle(Title): pass

# Temp
class DataSize(Integer): pass
class ContentLength(Integer): pass
class Bitrate(Integer): pass
class SampleRate(Integer): pass

class ContinuationToken(pydantype.String): pass

class Url(pydantype.String, furl.furl): pass

class ChannelUrl(Url): pass

class ViewCount(pydantype.BaseType, int):
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({humanize.intcomma(int(self))})'

    @pydantype.validator(int)
    def validate_any(cls, value: int):
        return cls.new(value)

    @pydantype.validator(str)
    def validate_str(cls, value: str):
        return cls.new(''.join(char for char in value if char in string.digits))

class Date(pendulum.Date, pydantype.BaseType):
    @pydantype.validator(str)
    def validate_str(cls, value: str):
        return cls.fromdate(cls.fromisoformat(value))

    @pydantype.validator(pendulum.Date)
    def validate_date(cls, value: pendulum.Date):
        return cls.fromdate(value)

    @classmethod
    def fromdate(cls, date: pendulum.Date):
        return cls \
        (
            year  = date.year,
            month = date.month,
            day   = date.day,
        )

class DateTime(pendulum.DateTime, pydantype.BaseType):
    @pydantype.validator(int, float)
    def validate_numeric(cls, value: Union[int, float]):
        return cls.fromdatetime(cls.fromtimestamp(value))

    @classmethod
    def fromdatetime(cls, datetime: pendulum.DateTime):
        return cls \
        (
            year        = datetime.year,
            month       = datetime.month,
            day         = datetime.day,
            hour        = datetime.hour,
            minute      = datetime.minute,
            second      = datetime.second,
            microsecond = datetime.microsecond,
            tzinfo      = datetime.tzinfo,
        )

class Duration(pendulum.Duration, pydantype.BaseType):
    @classmethod
    def fromtime(cls, time: pendulum.Time):
        return cls \
        (
            hours   = time.hour,
            minutes = time.minute,
            seconds = time.second,
        )

    @pydantype.validator(int, float)
    def validate_numeric(cls, value: Union[int, float]):
        return cls(seconds = value)

    @pydantype.validator(str)
    def validate_str(cls, value: str):
        if not any(char for char in value if char not in string.digits):
            return cls(seconds = int(value))

        if ':' in value:
            return cls.fromtime(pendulum.parse(':'.join(f'0:0:0:{value}'.split(':')[-3:])).time())

        raise ValueError('Invalid duration string format')
