import pydantic

import typing

class BaseModel(pydantic.BaseModel): pass

class Pivot(BaseModel):
    title:      str
    type:       str
    browse_id:  str

class Dimensions(BaseModel):
    height: int
    width:  int

class Thumbnail(BaseModel):
    url:        str
    dimensions: Dimensions

class Stream(BaseModel):
    class Ranges(BaseModel):
        class Range(BaseModel):
            start: int
            end:   int

        index: Range
        init:  Range

    class Quality(BaseModel):
        label: typing.Optional[str]
        type:  str

    class MimeType(BaseModel):
        type:    str
        subtype: str

    class Codec(BaseModel):
        type:    str
        version: typing.Optional[str]

    class Audio(BaseModel):
        channels:    int
        quality:     str
        sample_rate: int

    class Video(BaseModel):
        dimensions: Dimensions
        fps:        int

    itag:           int
    bitrate:        int
    duration:       float
    last_modified:  float
    projection:     str
    mime:           MimeType
    quality:        Quality
    content_length: typing.Optional[int]
    url:            typing.Optional[str]
    ranges:         typing.Optional[Ranges]
    codecs:         typing.List[Codec]
    audio:          typing.Optional[Audio]
    video:          typing.Optional[Video]
    # loudness:       typing.Optional[float]

class VideoDetails(BaseModel):
    class Flags(BaseModel):
        ratable:          bool
        crawlable:        bool
        live_content:     bool
        owner_viewing:    bool
        private:          bool
        unplugged_corpus: bool

    video_id:    str
    author:      str
    channel_id:  str
    duration:    int
    description: str
    title:       str
    rating:      float
    view_count:  int
    flags:       Flags
    keywords:    typing.List[str]
    thumbnails:  typing.List[Thumbnail]

class Microformat(BaseModel):
    class Channel(BaseModel):
        id:   str
        name: str
        url:  str

    class Flags(BaseModel):
        ypc_metadata: bool
        family_safe:  bool
        unlisted:     bool

    category:       str
    description:    str
    date_published: str
    date_uploaded:  str
    duration:       int
    title:          str
    view_count:     int
    flags:          Flags
    channel:        Channel
    thumbnails:     typing.List[Thumbnail]
    countries:      typing.List[str]

class PlayerResponse(BaseModel):
    video_details: VideoDetails
    streams:       typing.List[Stream]
    microformat:   typing.Optional[Microformat]
