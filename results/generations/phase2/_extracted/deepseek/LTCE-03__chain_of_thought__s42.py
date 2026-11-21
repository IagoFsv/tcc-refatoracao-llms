class Interpreter:
  def visit_takeElementNode(self, node, context):
    res = RTResult()
    list_name = res.register(self.visit(node.list_name, context))
    if res.should_return(): return res 

    index = res.register(self.visit(node.index_name, context))
    if res.should_return(): return res

    lses = []

    if isinstance(list_name, List):
      if isinstance(index, Number):
        if index.value < len(list_name.elements):
          lses.append(list_name.elements[index.value])
        else:
          print("RUNTIME ERROR: index out of range")
          sys.exit("Index Out of Range: " + str(index.value))
      else:
        print("RUNTIME ERROR: index is not a number")
        sys.exit("Index is not a number: " + str(index))
    elif isinstance(list_name, String):
      if isinstance(index, Number):
        if index.value < len(list_name.value):
          lses.append(String(list_name.value[index.value]))
        else:
          print("RUNTIME ERROR: index out of range")
          sys.exit("Index Out of Range: " + str(index.value))
      else:
        print("RUNTIME ERROR: index is not a number")
        sys.exit("Index is not a number: " + str(index))
    else:
      print("RUNTIME ERROR: list is not a list or string")
      sys.exit("List is not a list or string: " + str(list_name))

    return res.success(
      Number.null if node.should_return_null else
      List(lses).set_context(context).set_pos(node.pos_start, node.pos_end)
    )
