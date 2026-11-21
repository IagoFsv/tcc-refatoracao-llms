# Test case 1: Indexing a list
print(run([1, 2, 3], 1))  # Output: 2

# Test case 2: Indexing a string
print(run("hello", 1))  # Output: e

# Test case 3: Index out of range
try:
  print(run([1, 2, 3], 3))
except SystemExit as e:
  print(e)  # Output: Index Out of Range: 3

# Test case 4: Index is not a number
try:
  print(run([1, 2, 3], "a"))
except SystemExit as e:
  print(e)  # Output: Index is not a number: a

# Test case 5: List is not a list or string
try:
  print(run(123, 1))
except SystemExit as e:
  print(e)  # Output: List is not a list or string: 123
