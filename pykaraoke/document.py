#! /usr/bin/env python3
from collections import namedtuple


class Time(namedtuple("_Time", "start end")):
    """
    Defines the time in a pythonic manner.
    """

    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super(Time, self).__init__(*args, **kwargs)

    def retime(self, *, start: int=0, end: int=0) -> object:
        """
        Retimes the time relative to the given time object.
        """
        return self.__class__(self.start - start, self.end - end)

    def shift(self, delta: int) -> object:
        """
        Shifts the time.
        """
        return self.retime(start=delta, end=delta)


Margins = namedtuple("Margins", "l r v")
Line = namedtuple("Line", "type style margins time actor effect line")