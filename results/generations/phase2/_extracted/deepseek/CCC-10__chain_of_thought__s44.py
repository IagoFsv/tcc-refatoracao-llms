import collections

def build_worker_instruction(*args):
    tuple_class = collections.namedtuple(*args)
    tuple_class.__str__ = worker_object_to_string
    tuple_class.__repr__ = worker_object_to_string
    return tuple_class

def worker_printable_fields(workerproto):
    return_list = []
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
            return_list.append('%s=%s' % (name, value))
    return return_list

def worker_object_to_string(worker_object):
    return '%s(%s)' % (
        worker_object.__class__.__name__,
        ', '.join(worker_printable_fields(worker_object)))

def run(type_name, fields):
    record_class = build_worker_instruction(type_name, list(fields))
    return str(record_class(**fields))
