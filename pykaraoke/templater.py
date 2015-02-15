#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
from collections import namedtuple
from functools import wraps
import inspect
import sys

from pykaraoke.executors import BaseExecutor
from pykaraoke.document import Document, Line

__author__ = "stux!"

Template = namedtuple("Template", "type func settings")


class BaseTemplater(object):
    """
    The basic templater class.
    """

    def __init__(self, *, fps=24000 / 1001, resolution=(1280, 720)):
        self.fps = fps
        self.resolution = resolution

        self.types = {}
        self.templates = []

    def process_lines(self, line_iter: Line) -> Line:
        """
        Processes the raw lines.
        :param line_iter: The input iterator.
        :return: The return file.
        """
        pass

    def run_for_file(self, fin: open, fout: open) -> None:
        """
        The file object.
        :param fin: The input file.
        :param fout: The output file.
        """
        idoc = Document(fin)


    def run(self, args: tuple=None) -> int:
        """
        Runs the effect. Returns the status-code.
        """
        if args is None:
            args = sys.argv[1:]

        # If we get no arguments provided, we will assume
        # we get an ASS-File streamed into stdin
        # and will return the ASS-File from stdout.
        fin = sys.stdin
        fout = sys.stdout

        state = None
        for arg in args:
            if state == "INPUT":
                fin = open(arg, "r")
            elif state == "OUTPUT":
                fout = open(arg, "w")
            else:
                # To make this code easier understandable,
                # we will use an else instead of yet more elifs.
                if arg in ["--input", "-i"]:
                    state = "INPUT"
                elif arg in ["--output", "-o"]:
                    state = "OUTPUT"
                elif arg == "--":
                    fout = sys.stdout

        # Run the effect with the given streams.
        self.run_for_file(fin, fout)

        return 0

    def register_type(self, type: str, executor: BaseExecutor) -> None:
        """
        Registers a new type
        """
        self.types[type] = executor

    def _register_template(self, type: str, func: callable, args: tuple, settings: dict) -> None:
        """
        Registers a new template.
        """
        if type not in self.types:
            raise ValueError("Unknown template type.")
        type = self.types[type]
        data = type.parse_attributes(args, settings)
        self.templates.append(Template(type, func, data))

    def __call__(self, type: str, *args, **kwargs) -> callable:
        """
        Registers a new template
        """

        def _decorator(func: callable) -> callable:
            # Make sure we get a generator as the templater
            # will be iterate over the template executors.
            if inspect.isgeneratorfunction(func):
                _wrapper = func
            else:
                @wraps(func)
                def _wrapper(*fargs, **fkwargs):
                    # Ensure we have a generator.
                    res = func(*fargs, **fkwargs)
                    if inspect.isgenerator(res):
                        yield from res
                    else:
                        yield res
            self._register_template(type, _wrapper, args, kwargs)
            return func
        return _decorator
    add = __call__