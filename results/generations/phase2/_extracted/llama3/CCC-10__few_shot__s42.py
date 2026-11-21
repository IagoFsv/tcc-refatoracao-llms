"""Compact text representation of worker instruction records.

Public entry point: run(type_name, fields). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

import collections


def build_worker_instruction(*args):
  """Create an object representing a ParallelInstruction protobuf.

  This will be a collections.namedtuple with a custom __str__ method.

  Alas, this wrapper is not known to pylint, which thinks it creates
  constants.  You may have to put a disable=invalid-name pylint
  annotation on any use of this, depending on your names.

  Args:
    *args: first argument is the name of the type to create.  Should
      start with "Worker".  Second arguments is alist of the
      attributes of this object.
  Returns:
    A new class, a subclass of tuple, that represents the protobuf.
  """
  tuple_class = collections.namedtuple(*args)
  tuple_class.__str__ = worker_object_to_string
  tuple_class.__repr__ = worker_object_to_string
  return tuple_class


def worker_printable_fields(workerproto):
  """Returns the interesting fields of a Worker* object."""
  report = []
  for name, value in workerproto._asdict().items():
    if (value or value == 0) and name not in (
        'coder',
        'coders',
        'output_coders',
        'elements',
        'combine_fn',
        'serialized_fn',
        'window_fn',
        'append_trailing_newlines',
        'strip_trailing_newlines',
        'compression_type',
        'context',
        'start_shuffle_position',
        'end_shuffle_position',
        'shuffle_reader_config',
        'shuffle_writer_config'):
      report.append('%s=%s' % (name, value))
  return report


def worker_object_to_string(worker_object):
  """Returns a string compactly representing a Worker* object."""
  return '%s(%s)' % (
      worker_object.__class__.__name__,
      ', '.join(worker_printable_fields(worker_object)))


def run(type_name, fields):
  """Builds a record type with the given name and fields, creates a record
  with the field values and returns its text. Public entry point of this
  unit."""
  record_class = build_worker_instruction(type_name, list(fields))
  record = record_class(**fields)
  return str(record)
