#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
__author__ = 'stux!'


import warnings

# Since we are not going to render the ass-files
# we will be ignoring the warnings because of a
# missing LibASS so/ddl.
with warnings.catch_warnings():
    from ass import document

__all__ = ["document"]