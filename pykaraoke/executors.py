#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
from pykaraoke.document import Line
__author__ = "stux!"


class TemplateExecutorData(object):
	"""
	Base Class for Template executor settings.
	"""
	pass


class BaseExecutor(object):
	"""
	Base Executor
	"""
	
	def parse_template(self, *args, **kwargs) -> TemplateExecutorData:
		"""
		Parses a template
		"""
		raise NotImplemented
		
	def execute_template(self, func: callable, settings: TemplateExecutorData) -> Line:
		"""
		Executes the template.
		"""
		raise NotImplemented
		
	