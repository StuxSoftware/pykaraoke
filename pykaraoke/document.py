#! /usr/bin/env python3
from collections import namedtuple, OrderedDict
from operator import itemgetter


class Time(tuple):
    """Time(start, end)'"""

    __slots__ = ()

    _fields = ('start', 'end')

    def __new__(cls, start, end):
        """Create new instance of Time(start, end)'"""
        return tuple.__new__(cls, (start, end))

    @classmethod
    def _make(cls, iterable, new=tuple.__new__, len=len):
        """Make a new Time object from a sequence or iterable'"""
        result = new(cls, iterable)
        if len(result) != 2:
            raise TypeError('Expected 2 arguments, got %d' % len(result))
        return result

    def _replace(self, **kwds):
        """Return a new Time object replacing specified fields with new values'"""
        result = self._make(map(kwds.pop, ('start', 'end'), self))
        if kwds:
            raise ValueError('Got unexpected field names: %r' % list(kwds))
        return result

    def __repr__(self):
        """Return a nicely formatted representation string'"""
        return self.__class__.__name__ + '(start=%r, end=%r)' % self

    @property
    def __dict__(self):
        """A new OrderedDict mapping field names to their values'"""
        return OrderedDict(zip(self._fields, self))

    def _asdict(self):
        """Return a new OrderedDict which maps field names to their values.'"""
        return self.__dict__

    def __getnewargs__(self):
        """Return self as a plain tuple.  Used by copy and pickle.'"""
        return tuple(self)

    def __getstate__(self):
        """Exclude the OrderedDict from pickling'"""
        return None

    start = property(itemgetter(0), doc='Alias for field number 0')
    end = property(itemgetter(1), doc='Alias for field number 1')

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