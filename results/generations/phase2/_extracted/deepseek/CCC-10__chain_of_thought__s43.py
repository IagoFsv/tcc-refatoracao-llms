def worker_printable_fields(workerproto):
   """Returns the interesting fields of a Worker* object."""
  fields = []
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
          fields.append('%s=%s' % (name, value))
  return fields
