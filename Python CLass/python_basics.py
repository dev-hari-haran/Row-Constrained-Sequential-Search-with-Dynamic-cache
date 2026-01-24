# ==========================================================
# PYTHON BASICS – VARIABLES, DATA TYPES, OPERATORS
# ==========================================================

# A variable is a name that stores a value in memory
x = 10          # integer
y = 3.5         # float
name = "AI"     # string
is_active = True  # boolean

# Python is dynamically typed (no need to declare data type)
print(x, y, name, is_active)

# ---------------- OPERATORS ----------------
# Arithmetic operators
a = 10
b = 3
print(a + b)   # addition
print(a - b)   # subtraction
print(a * b)   # multiplication
print(a / b)   # division (float)
print(a // b)  # floor division
print(a % b)   # modulus
print(a ** b)  # power

# Comparison operators
print(a > b)
print(a == b)

# Logical operators
print(a > 5 and b < 5)
print(a > 5 or b > 10)
print(not is_active)

# ==========================================================
# LOOPS – FOR & WHILE
# ==========================================================

# FOR LOOP: used when number of iterations is known
for i in range(5):
    print("For loop value:", i)

# WHILE LOOP: runs until condition becomes False
count = 0
while count < 3:
    print("While loop count:", count)
    count += 1

# ==========================================================
# FUNCTIONS – REUSABLE BLOCK OF CODE
# ==========================================================

def add_numbers(a, b):
    """
    This function takes two numbers
    and returns their sum
    """
    return a + b

result = add_numbers(5, 7)
print("Sum:", result)

#String

s = "Robotics and AI"

# Indexing (0-based)
print(s[0])        # First character
print(s[-1])       # Last character

# Slicing
print(s[0:8])      # 'Robotics'
print(s[::-1])     # Reverse string

# Searching
print(s.find("AI"))      # returns index or -1
print("AI" in s)         # boolean check

# Counting
print(s.count("o"))

# Checking properties
print(s.isalpha())       # False (spaces exist)
print(s.islower())
print(s.startswith("Rob"))
print(s.endswith("AI"))

# Joining
words = ["Python", "for", "AI"]
joined = " ".join(words)
print(joined)

# Formatting
name = "Hari"
age = 20
print(f"My name is {name} and age is {age}")

#List
lst = [10, 20, 30, 40]

# Access
print(lst[1])
print(lst[-1])

# Update
lst[2] = 99

# Add elements
lst.append(50)
lst.extend([60, 70])
lst.insert(1, 15)

# Remove elements
lst.remove(99)        # removes by value
last = lst.pop()      # removes last
index_val = lst.pop(2)

# Search
print(lst.index(20))
print(30 in lst)

# Sorting
lst.sort()
lst.sort(reverse=True)

# Reverse
lst.reverse()

# Copying
lst_copy = lst.copy()

# Length
print(len(lst))

# Traversal with index
for i, val in enumerate(lst):
    print(i, val)

print(lst)

#Tuple
t = (1, 2, 3, 2, 4)

# Access
print(t[0])
print(t[-1])

# Count & search
print(t.count(2))
print(t.index(3))

# Slicing
print(t[1:4])

# Tuple unpacking
a, b, c, d, e = t
print(a, b)

# Conversion (important trick)
temp_list = list(t)
temp_list.append(5)
t = tuple(temp_list)
print(t)

#Set
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}

# Add / Remove
A.add(10)
A.discard(2)     # no error if missing
A.remove(1)      # error if missing

# Membership
print(3 in A)

# Set operations
print(A | B)     # Union
print(A & B)     # Intersection
print(A - B)     # Difference
print(A ^ B)     # Symmetric difference

# Subset / Superset
print({3, 4}.issubset(A))
print(A.issuperset({3}))

#Dictionary
student = {
    "name": "Hari",
    "dept": "Robotics",
    "year": 2
}

# Access
print(student["name"])
print(student.get("cgpa", "Not Found"))

# Update
student["year"] = 3

# Add
student["cgpa"] = 8.8

# Remove
student.pop("dept")
del student["year"]

# Keys, Values, Items
print(student.keys())
print(student.values())
print(student.items())

# Traversal
for key, value in student.items():
    print(key, ":", value)

# Dictionary comprehension
squares = {x: x*x for x in range(5)}
print(squares)

#Linked List
class LinkedList:
    def __init__(self):
        self.head = None

    def insert_front(self, data):
        node = Node(data)
        node.next = self.head
        self.head = node

    def delete(self, key):
        temp = self.head

        if temp and temp.data == key:
            self.head = temp.next
            return

        prev = None
        while temp and temp.data != key:
            prev = temp
            temp = temp.next

        if temp:
            prev.next = temp.next

    def search(self, key):
        temp = self.head
        while temp:
            if temp.data == key:
                return True
            temp = temp.next
        return False

#Stack
stack = []

# Push
stack.append(10)
stack.append(20)

# Peek
print(stack[-1])

# Pop
stack.pop()

# Size
print(len(stack))

# Empty check
print(len(stack) == 0)


#Queue
from collections import deque

q = deque()

# Enqueue
q.append(10)
q.append(20)

# Peek
print(q[0])

# Dequeue
q.popleft()

# Size
print(len(q))

# Empty check
print(len(q) == 0)

#Tree
# ===============================
# TREE (Binary Search Tree)
# ===============================

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    # INSERT
    def insert(self, data):
        self.root = self._insert(self.root, data)

    def _insert(self, node, data):
        if not node:
            return TreeNode(data)
        if data < node.data:
            node.left = self._insert(node.left, data)
        elif data > node.data:
            node.right = self._insert(node.right, data)
        return node

    # SEARCH
    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if not node:
            return False
        if node.data == key:
            return True
        if key < node.data:
            return self._search(node.left, key)
        return self._search(node.right, key)

    # TRAVERSALS
    def inorder(self, node):
        if node:
            self.inorder(node.left)
            print(node.data, end=" ")
            self.inorder(node.right)

    def preorder(self, node):
        if node:
            print(node.data, end=" ")
            self.preorder(node.left)
            self.preorder(node.right)

    def postorder(self, node):
        if node:
            self.postorder(node.left)
            self.postorder(node.right)
            print(node.data, end=" ")

    # FIND MIN
    def find_min(self, node):
        while node.left:
            node = node.left
        return node.data

    # DELETE
    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return node

        if key < node.data:
            node.left = self._delete(node.left, key)
        elif key > node.data:
            node.right = self._delete(node.right, key)
        else:
            # Case 1 & 2: one or zero child
            if not node.left:
                return node.right
            if not node.right:
                return node.left

            # Case 3: two children
            node.data = self.find_min(node.right)
            node.right = self._delete(node.right, node.data)

        return node

    # HEIGHT
    def height(self, node):
        if not node:
            return -1
        return 1 + max(self.height(node.left), self.height(node.right))

#Graph
# ===============================
# GRAPH (Adjacency List)
# ===============================

from collections import deque

class Graph:
    def __init__(self):
        self.graph = {}

    # ADD VERTEX
    def add_vertex(self, v):
        if v not in self.graph:
            self.graph[v] = []

    # ADD EDGE (Undirected)
    def add_edge(self, u, v):
        self.add_vertex(u)
        self.add_vertex(v)
        self.graph[u].append(v)
        self.graph[v].append(u)

    # REMOVE EDGE
    def remove_edge(self, u, v):
        if u in self.graph and v in self.graph[u]:
            self.graph[u].remove(v)
            self.graph[v].remove(u)

    # REMOVE VERTEX
    def remove_vertex(self, v):
        if v in self.graph:
            for nbr in self.graph[v]:
                self.graph[nbr].remove(v)
            del self.graph[v]

    # DFS
    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()
        if start not in visited:
            print(start, end=" ")
            visited.add(start)
            for nbr in self.graph[start]:
                self.dfs(nbr, visited)

    # BFS
    def bfs(self, start):
        visited = set()
        queue = deque([start])

        while queue:
            node = queue.popleft()
            if node not in visited:
                print(node, end=" ")
                visited.add(node)
                queue.extend(self.graph[node])

    # PATH EXISTS
    def has_path(self, src, dest, visited=None):
        if visited is None:
            visited = set()
        if src == dest:
            return True
        visited.add(src)
        for nbr in self.graph[src]:
            if nbr not in visited:
                if self.has_path(nbr, dest, visited):
                    return True
        return False

    # DISPLAY
    def display(self):
        for v in self.graph:
            print(v, "->", self.graph[v])


#Hashing
# ===============================
# HASHING OPERATIONS
# ===============================

# CREATE
data = {}

# INSERT / UPDATE
data["robot"] = "ROS"
data["ai"] = "Python"
data["ai"] = "ML"      # update

# ACCESS
print(data["robot"])
print(data.get("cv", "Not Found"))

# DELETE
del data["robot"]

# SEARCH
print("ai" in data)

# ITERATION
for key, value in data.items():
    print(key, value)

# HASH VALUE (internal use)
print(hash("robotics"))

# FREQUENCY COUNT (classic hashing problem)
word = "mississippi"
freq = {}

for ch in word:
    freq[ch] = freq.get(ch, 0) + 1

print(freq)

# SET-BASED HASHING
nums = [1, 2, 2, 3, 4, 4]
unique = set(nums)
print(unique)

# COLLISION NOTE:
# Python handles collisions internally using probing.
# Developers do NOT manage it manually.
