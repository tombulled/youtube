import venum

import enum

class StrEnum(str, enum.Enum): pass
class ParsedStrEnum(str, venum.ParsedEnum): pass

class PivotType(StrEnum):
    _generate_next_value_ = lambda name, *_: name

    HOME          = enum.auto()
    EXPLORE       = enum.auto()
    SUBSCRIPTIONS = enum.auto()
    LIBRARY       = enum.auto()

class PivotIdentifier(ParsedStrEnum):
    _generate_next_value_ = lambda name, *_: name.lower()

    __parse__ = lambda cls, name, value: f'pivot-{value}'

    HOME          = 'w2w'
    SUBSCRIPTIONS = 'subs'
    LIBRARY       = enum.auto()
    EXPLORE       = enum.auto()

    @property
    def type(self):
        return PivotType(self.name)
