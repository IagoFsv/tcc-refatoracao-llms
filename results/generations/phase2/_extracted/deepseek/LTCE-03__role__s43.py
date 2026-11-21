"""Interpreter of a small scripting language: indexing of lists and strings.

Public entry point: run(container, index, should_return_null=False). Do not
change its name or signature; the rest of the file may be freely
reorganized.
"""

import sys


class takeElementNode:
  def  __init__(self, list_name, index_name, should_return_null):
    self.list_name = list_name
    self.index_name = index_name
    self.should_return_null = should_return_null

    self.pos_start = self.list_name.pos_start
    self.pos_end = self.index_name.pos_end


class ValueNode:
  """Node whose evaluation is an already computed value."""
  def  __init__(self, value):
    self.value = value
    self.pos_start = None
    self.pos_end = None


class RTResult:
  def  __init__(self):
    self.reset()

  def reset(self):
    self.value = None
    self.error = None
    self.func_return_value = None
    self.loop_should_continue = False
    self.loop_should_break = False

  def register(self, res):
    self.error = res.error
    self.func_return_value = res.func_return_value
    self.loop_should_continue = res.loop_should_continue
    self.loop_should_break = res.loop_should_break
    return res.value

  def success(self, value):
    self.reset()
    self.value = value
    return self

  def should_return(self):
    return self.error or self.func_return_value or self.loop_should_continue or self.loop_should_break

class Value:
  def  __init__(self):
    self.set_pos()
    self.set_context()

  def set_pos(self, pos_start=None, pos_end=None):
    self.pos_start = pos_start
    self.pos_end = pos_end
    return self

  def set_context(self, context=None):
    self.context = context
    return self

class Number(Value):
  def  __init__(self, value):
    super().__init__()
    self.value = value

  def  __str__(self):
    return str(self.value)
  
  def  __repr__(self):
    return str(self.value)

Number.null = Number("\n")

class String(Value):
  def  __init__(self, value):
    super().__init__()
    self.value = value

  def  __str__(self):
    return self.value

  def  __repr__(self):
    return f'"{self.value}"'

class List(Value):
  def  __init__(self, elements):
    super().__init__()
    self.elements = elements

  def  __str__(self):
    return ", ".join([str(x) for x in self.elements])

  def  __repr__(self):
    return f'[{", ".join([repr(x) for x in self.elements])}]'

class Interpreter:
  def visit(self, node, context):
    method_name = f'visit_{type(node).__name__}'
    method = getattr(self, method_name, self.no_visit_method)
    return method(node, context)

  def no_visit_method(self, node, context):
    raise Exception(f'No visit_{type(node).__name__} method defined')

  def visit_ValueNode(self, node, context):
    return RTResult().success(node.value)

  def visit_takeElementNode(self, node, context):
    res = RTResult()
    lses = []

    list_name = res.register(self.visit(node.list_name, context))
    if res.should_return(): return res 

    index = res.register(self.visit(node.index_name, context))
    if res.should_return(): return res

    def take_element(list_name, index):
      if isinstance(list_name, List):
        if isinstance(index, Number):
          if index.value < len(list_name.elements):
            return list_name.elements[index.value]
          else:
            print("RUNTIME ERROR: index out of range")
            sys.exit("Index Out of Range: " + str(index.value))
        else:
          print("RUNTIME ERROR: index is not a number")
          sys.exit("Index is not a number: " + str(index))
      elif isinstance(list_name, String):
        if isinstance(index, Number):
          if index.value < len(list_name.value):
            return String(list_name.value[index.value])
          else:
            print("RUNTIME ERROR: index out of range")
            sys.exit("Index Out of Range: " + str(index.value))
        else:
          print("RUNTIME ERROR: index is not a number")
          sys.exit("Index is not a number: " + str(index))
      else:
        print("RUNTIME ERROR: list is not a list or string")
        sys.exit("List is not a list or string: " + str(list_name))
    lses.append(take_element(list_name, index))

    try:
      take_element(list_name, index)
    except Exception as e:
      print("RUNTIME ERROR: " + str(e))

    return res.success(
      Number.null if node.should_return_null else
      List(lses).set_context(context).set_pos(node.pos_start, node.pos_end)
     )


def _to_value(item):
  if isinstance(item, list):
    return List([_to_value(x) for x in item])
  if isinstance(item, str):
    return String(item)
  return Number(item)


def _to_python(value):
  if isinstance(value, List):
    return [_to_python(x) for x in value.elements]
  return value.value


def run(container, index, should_return_null=False):
  """Evaluates container[index] in the language: Python lists, strings and
  numbers become values of the language, and the result comes back as
  Python objects. Public entry point of this unit."""
  node = takeElementNode(ValueNode(_to_value(container)), ValueNode(_to_value(index)), should_return_null)
  result = Interpreter().visit(node, None)
  return _to_python(result.value)
