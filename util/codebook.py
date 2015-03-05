# -*- mode: Python; coding: utf-8 -*-

class CodeBook(object):
    """A bi-directional map between names and auto-generated indices.
    Useful for both features and labels in classifiers."""

    def __init__(self, names):
        self.names = dict((index, name) for index, name in enumerate(names))
        self.index = dict((name, index) for index, name in enumerate(names))

    def __contains__(self, name):
        return name in self.index

    def __getitem__(self, name):
        return self.index[name]

    def __iter__(self):
        return iter(self.index)

    def __len__(self):
        return len(self.index)

    def __repr__(self):
        return "<%s with %d entries>" % (self.__class__.__name__, len(self))

    def add(self, name):
        """Add the given name with a generated index."""
        if name not in self:
            index = len(self)
            self.names[index] = name
            self.index[name] = index
        return name
