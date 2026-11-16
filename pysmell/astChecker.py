"""Python 3 port of astChecker.py from Pysmell (Chen et al.).

Source: https://github.com/chenzhifei731/Pysmell, commit
233afebac24c910be89d065ffa661ec72458a62c (2018-07-06), file
pysmell/detection/astChecker.py. The original is Python 2 and does not run
here; the Zhang et al. (2024) dataset is Python 3, so even with Python 2
installed it could not be analyzed (f-strings do not parse).

Changes from the original (THESE ARE THE ONLY ONES; the metric logic and the
visitors are intact):

1. `import customast` and `import astunparse` became `from compat import ...`.
   The original `customast` only read the file and detected its encoding;
   here `detect.py` does that, with `ast.parse`.
2. `astunparse.unparse(...)` became `unparse(...)`, which is the SAME
   `astunparse.unparse`, only imported from `compat` (which applies the
   `Constant.n`/`Constant.s` shim). See compat.py: switching to `ast.unparse`
   changes the NOC metric and breaks the reproduction of Zhang et al.
3. The two (identical) `type_filters` lists became `ignored_types()`, which
   builds the same list while skipping AST types removed in Python 3.
4. A `print` with Python 2 syntax (visit_ImportFrom, exception branch) became
   `pass`. It was only debugging output.

Note on `visit_TryExcept`: in Python 3 the node is called `ast.Try`, so this
visitor never fires. This is kept on purpose. It only produced the
UselessExceptionHandling smell, which is not used here, and the original
method does not call `generic_visit` in the normal flow: renaming it to
`visit_Try` would make the detector skip the body of every `try` block,
losing instances that Zhang et al. report (e.g. Natsar-main/modules/tele.py).
"""

import ast,_ast
import re

from compat import unparse, ignored_types
# import yaml

# stream = open("config",'r')
# config = yaml.load(stream)

class MyAst(ast.NodeVisitor):
    def __init__(self):
        self.fileName = None
        self.defmagic = set()
        self.usedmagic = set()
        self.subscriptnodes = [] #avoid replicate node code smell reports
        self.containernodes = [] #avoid replicate node code smell reports
        self.messagenodes = [] #avoid replicate node code smell reports
        self.scopenodes = []
        self.imports = set()
        self.result = []

    def count_lines(self,node):
        childnodes = list(ast.walk(node))
        lines = set()
        for n in childnodes:
          if hasattr(n,'lineno'):
            lines.add(n.lineno)
        return len(lines)

    def visit_Lambda(self,node):
        expr = unparse(node)
        exprLength = len(expr.strip()) - expr.count(' ') - 2
        par = len(node.args.args)
        noo = 0
        type_filters = ignored_types()
        for i in ast.walk(node.body):
            if type(i) not in type_filters:
                noo = noo + 1
        self.result.append((9,self.fileName,node.lineno,exprLength,par,noo))
        self.generic_visit(node) 

    def visit_TryExcept(self,node):
        exceptions = ["BaseException","Exception","StandardError"]
        i = len(node.handlers)
        for item in node.handlers:
            i = i-1
            if i!=0 and unparse(item.body[0]).strip() == "pass":
                self.result.append((7,self.fileName,node.lineno,'pass'))
                self.generic_visit(node) 
                return
            if item.type is not None:
                if isinstance(item.type,_ast.Tuple) or isinstance(item.type,_ast.List):
                    for e in item.type.elts:
                        if hasattr(e,"id") and e.id in exceptions:
                            self.result.append((7,self.fileName,node.lineno,'genrallist'))
                            self.generic_visit(node) 
                            return
                elif i!=0 and hasattr(item.type,"id") and item.type.id in exceptions:
                    self.result.append((7,self.fileName,node.lineno,'general'))
                    self.generic_visit(node) 
                    return
            elif i!=0:
              self.result.append((7,self.fileName,node.lineno,'general'))
              self.generic_visit(node)
              return

    def visit_ClassDef(self,node):
      # baseClassesSize
      className = node.name
      baseClassesSize = len(node.bases)
      if baseClassesSize>0:
        self.result.append((4,self.fileName,node.lineno,baseClassesSize))
      lines = set()
      res = [node]
      while len(res) >= 1:
        t = res[0]
        for n in ast.iter_child_nodes(t):
          if not hasattr(n,'lineno') or ((isinstance(t,_ast.FunctionDef) or isinstance(t,_ast.ClassDef)) and n == t.body[0] and isinstance(n,_ast.Expr)):
            continue
          lines.add(n.lineno)
          if isinstance(n,_ast.ClassDef) or isinstance(n,_ast.FunctionDef):
            continue
          else:
            res.append(n)
        del res[0]
      self.result.append((5,self.fileName,node.lineno,len(lines)))
      self.generic_visit(node)

    def visit_FunctionDef(self,node):
      # argsCount
      def findCharacter(s,d):
        try:
          value = s.index(d)
        except ValueError:
          return -1
        else:
          return value
      funcName = node.name.strip()
      p = re.compile("^(__[a-zA-Z0-9]+__)$")
      if p.match(funcName.strip()) and funcName != "__import__" and funcName != "__all__":
        self.defmagic.add((funcName,self.fileName,node.lineno))
      stmt = unparse(node.args)
      arguments = stmt.split(",")
      argsCount = 0
      for element in arguments:
        if findCharacter(element,'=') == -1:
          argsCount += 1
      self.result.append((1,self.fileName,node.lineno,argsCount))
      #function length
      lines = set()
      res = [node]
      while len(res) >= 1:
        t = res[0]
        for n in ast.iter_child_nodes(t):
          if not hasattr(n,'lineno') or ((isinstance(t,_ast.FunctionDef) or isinstance(t,_ast.ClassDef)) and n == t.body[0] and isinstance(n,_ast.Expr)):
            continue
          lines.add(n.lineno)
          if isinstance(n,_ast.ClassDef) or isinstance(n,_ast.FunctionDef):
            continue
          else:
            res.append(n)
        del res[0]
      self.result.append((2,self.fileName,node.lineno,len(lines))) 
      #nested scope depth
      if node in self.scopenodes:
        self.scopenodes.remove(node)
        self.generic_visit(node)
        return
      dep = [[node,1]] #node,nestedlevel
      maxlevel = 1
      while len(dep) >= 1:
        t = dep[0][0]
        currentlevel = dep[0][1]
        for n in ast.iter_child_nodes(t):
          if isinstance(n,_ast.FunctionDef):
            self.scopenodes.append(n)
            dep.append([n,currentlevel+1])
        maxlevel = max(maxlevel,currentlevel)
        del dep[0]
      if maxlevel>1:
        self.result.append((3,self.fileName,node.lineno,maxlevel)) #DOC
      self.generic_visit(node) 

    def visit_Call(self,node):
      funcName = unparse(node.func).strip()
      p = re.compile("^(__[a-zA-Z0-9]+__)$")
      if p.match(funcName) and funcName != "__import__" and funcName != "__all__":
        self.usedmagic.add((funcName,self.fileName,node.lineno))
      self.generic_visit(node)

    def visit_ListComp(self,node):
        count = 0
        expr = unparse(node)
        exprLength = len(expr.strip()) - expr.count(' ')
        for item in expr.split(" "):
            if item.strip() == "if" or item.strip() == "for":
                count += 1
        noo = -1
        type_filters = ignored_types()
        for i in ast.walk(node):
            if type(i) not in type_filters:
                noo = noo + 1
        self.result.append((11,self.fileName,node.lineno,exprLength,count,noo))
        self.generic_visit(node)  
           
    def visit_SetComp(self,node):
        self.visit_ListComp(node)

    def visit_DictComp(self,node):
        self.visit_ListComp(node)

    def visit_GeneratorExp(self,node):
        self.visit_ListComp(node)

    def visit_IfExp(self,node):
      expr = unparse(node)
      exprLength = len(expr.strip()) - expr.count(' ') - 2
      childnodes = list(ast.walk(node))
      lines = 0
      for n in childnodes:
        if hasattr(n,'lineno'):
          lines = max(n.lineno-node.lineno,lines)
      lines = lines + 1
      self.result.append((10,self.fileName,node.lineno,exprLength,lines))
      self.generic_visit(node) 

    def visit_Subscript(self,node):
      if node in self.subscriptnodes:
        self.subscriptnodes.remove(node)
        self.generic_visit(node)
        return
      maxcount = 1
      t = node
      while True:
        if isinstance(t.value,_ast.Subscript):
          self.subscriptnodes.append(t.value)
          maxcount = maxcount + 1
          t = t.value
        else:
          break
      self.result.append((6,self.fileName,node.lineno,maxcount)) #LEC
      self.generic_visit(node) 

    def visit_List(self,node):
      if node in self.containernodes:
        self.containernodes.remove(node)
        self.generic_visit(node)
        return
      res = [[node,1]] #node,nestedlevel,type
      maxlevel = 1
      maxtype = 0
      while len(res) >= 1:
        t = res[0][0]
        currentlevel = res[0][1]
        if type(t) in [_ast.Tuple,_ast.List,_ast.Set,_ast.Dict]:
          childnodes = t.keys if isinstance(t,_ast.Dict) else t.elts
          for n in childnodes:
            if type(n) in [_ast.Tuple,_ast.Dict,_ast.List,_ast.Set]:
              self.containernodes.append(n)
              if type(n) not in res[0]:
                res[0].append(type(n))
              res.append([n,currentlevel+1])
        maxlevel = max(maxlevel,currentlevel)
        maxtype = max(maxtype,len(res[0])-2)
        del res[0]
        if isinstance(t,_ast.Dict):
          childnodes = t.values
          valuestype = set()
          for n in childnodes:
            if type(n) in [_ast.Tuple,_ast.Dict,_ast.List,_ast.Set]:
              self.containernodes.append(n)
              valuestype.add(type(n))
              res.append([n,currentlevel+1])
          maxtype = max(maxtype,len(valuestype))
      if maxlevel>1 or maxtype>0:
        self.result.append((6,self.fileName,node.lineno,maxlevel,maxtype)) #DNC,NCT
      self.generic_visit(node)

    def visit_Tuple(self,node):
      self.visit_List(node)

    def visit_Dict(self,node):
      self.visit_List(node)

    def visit_Set(self,node):
      self.visit_List(node) 

    def visit_Attribute(self,node):
      if node in self.messagenodes:
        self.messagenodes.remove(node)
        self.generic_visit(node)
        return
      maxcount = 1
      t = node
      while True:
        if isinstance(t.value,_ast.Attribute):
          self.messagenodes.append(t.value)
          maxcount = maxcount + 1
          t = t.value
        else:
          break
      if maxcount>1:
        self.result.append((13,self.fileName,node.lineno,maxcount)) #LMC
      self.generic_visit(node)

    def visit_Import(self,node):
      if self.fileName[-12:] == '\\__init__.py':
        self.generic_visit(node)
        return
      for alias in node.names:
        if len(alias.name)>4 and alias.name[0:2] == '__' and alias.name[-2:] == '__':
            continue
        if alias.asname is not None:
          for (name,file,lineno) in self.imports:
            if name==alias.asname and self.fileName==file:
              break
          else:
            self.imports.add((alias.asname,self.fileName,node.lineno))
        elif alias.name != '*':
          for (name,file,lineno) in self.imports:
            if name==alias.name and self.fileName==file:
              break
          else:
            self.imports.add((alias.name,self.fileName,node.lineno))
      self.generic_visit(node)

    def visit_ImportFrom(self,node):
      if self.fileName[-12:] == '\\__init__.py':
        self.generic_visit(node)
        return
      try:
        if node.module is not None and len(node.module)>4 and node.module[0:2] == '__' and node.module[-2:] == '__':
          self.generic_visit(node)
          return
      except:
        pass
      for alias in node.names:
        if len(alias.name)>4 and alias.name[0:2] == '__' and alias.name[-2:] == '__':
            continue
        if alias.asname is not None:
          for (name,file,lineno) in self.imports:
            if name==alias.asname and self.fileName==file:
              break
          else:
            self.imports.add((alias.asname,self.fileName,node.lineno))
        elif alias.name != '*':
          for (name,file,lineno) in self.imports:
            if name==alias.name and self.fileName==file:
              break
          else:
            self.imports.add((alias.name,self.fileName,node.lineno))
      self.generic_visit(node)

if __name__ == '__main__':
    pass