"""
==========================================================
30 BASIC & ESSENTIAL ALGORITHMS FOR AI
Single Python File | Fully Runnable | With Examples
==========================================================
"""

import math
from collections import deque

# ---------------------------------------------------------
# 1. LINEAR SEARCH
# ---------------------------------------------------------
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

print("1. Linear Search:", linear_search([10, 20, 30, 40], 30))


# ---------------------------------------------------------
# 2. BINARY SEARCH (ARRAY MUST BE SORTED)
# ---------------------------------------------------------
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif target < arr[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return -1

print("2. Binary Search:", binary_search([1, 3, 5, 7, 9], 7))


# ---------------------------------------------------------
# 3. BUBBLE SORT
# ---------------------------------------------------------
def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

print("3. Bubble Sort:", bubble_sort([5, 3, 8, 4]))


# ---------------------------------------------------------
# 4. SELECTION SORT
# ---------------------------------------------------------
def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

print("4. Selection Sort:", selection_sort([64, 25, 12, 22]))


# ---------------------------------------------------------
# 5. INSERTION SORT
# ---------------------------------------------------------
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

print("5. Insertion Sort:", insertion_sort([9, 5, 1, 4]))


# ---------------------------------------------------------
# 6. MERGE SORT
# ---------------------------------------------------------
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        merge_sort(L)
        merge_sort(R)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr

print("6. Merge Sort:", merge_sort([38, 27, 43, 3]))


# ---------------------------------------------------------
# 7. QUICK SORT
# ---------------------------------------------------------
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)

print("7. Quick Sort:", quick_sort([10, 7, 8, 9, 1]))


# ---------------------------------------------------------
# 8. FACTORIAL
# ---------------------------------------------------------
def factorial(n):
    return 1 if n == 0 else n * factorial(n - 1)

print("8. Factorial:", factorial(5))


# ---------------------------------------------------------
# 9. FIBONACCI SERIES
# ---------------------------------------------------------
def fibonacci(n):
    a, b = 0, 1
    seq = []
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    return seq

print("9. Fibonacci:", fibonacci(7))


# ---------------------------------------------------------
# 10. MEAN
# ---------------------------------------------------------
def mean(arr):
    return sum(arr) / len(arr)

print("10. Mean:", mean([2, 4, 6, 8]))


# ---------------------------------------------------------
# 11. MEDIAN
# ---------------------------------------------------------
def median(arr):
    arr = sorted(arr)
    n = len(arr)
    mid = n // 2
    return (arr[mid - 1] + arr[mid]) / 2 if n % 2 == 0 else arr[mid]

print("11. Median:", median([3, 1, 2, 4]))


# ---------------------------------------------------------
# 12. STANDARD DEVIATION
# ---------------------------------------------------------
def standard_deviation(arr):
    m = mean(arr)
    return math.sqrt(sum((x - m) ** 2 for x in arr) / len(arr))

print("12. Std Deviation:", standard_deviation([2, 4, 6, 8]))


# ---------------------------------------------------------
# 13. REVERSE ARRAY
# ---------------------------------------------------------
def reverse_array(arr):
    return arr[::-1]

print("13. Reverse Array:", reverse_array([1, 2, 3]))


# ---------------------------------------------------------
# 14. MAX ELEMENT
# ---------------------------------------------------------
def find_max(arr):
    max_val = arr[0]
    for x in arr:
        if x > max_val:
            max_val = x
    return max_val

print("14. Max Element:", find_max([3, 7, 2, 9]))


# ---------------------------------------------------------
# 15. FREQUENCY COUNT (HASHING)
# ---------------------------------------------------------
def frequency_count(arr):
    freq = {}
    for x in arr:
        freq[x] = freq.get(x, 0) + 1
    return freq

print("15. Frequency Count:", frequency_count([1, 2, 2, 3, 3, 3]))


# ---------------------------------------------------------
# 16. PALINDROME CHECK
# ---------------------------------------------------------
def is_palindrome(s):
    return s == s[::-1]

print("16. Palindrome:", is_palindrome("madam"))


# ---------------------------------------------------------
# 17. DFS (GRAPH)
# ---------------------------------------------------------
def dfs(graph, node, visited):
    if node not in visited:
        visited.add(node)
        for nbr in graph[node]:
            dfs(graph, nbr, visited)
    return visited

graph = {'A': ['B', 'C'], 'B': ['D'], 'C': [], 'D': []}
print("17. DFS:", dfs(graph, 'A', set()))


# ---------------------------------------------------------
# 18. BFS (GRAPH)
# ---------------------------------------------------------
def bfs(graph, start):
    visited = set()
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            queue.extend(graph[node])
    return visited

print("18. BFS:", bfs(graph, 'A'))


# ---------------------------------------------------------
# 19. GREEDY COIN CHANGE
# ---------------------------------------------------------
def coin_change(coins, amount):
    coins.sort(reverse=True)
    count = 0
    for coin in coins:
        while amount >= coin:
            amount -= coin
            count += 1
    return count

print("19. Coin Change:", coin_change([1, 2, 5], 11))


# ---------------------------------------------------------
# 20. ACTIVITY SELECTION
# ---------------------------------------------------------
def activity_selection(start, end):
    activities = sorted(zip(start, end), key=lambda x: x[1])
    selected = [activities[0]]
    for i in range(1, len(activities)):
        if activities[i][0] >= selected[-1][1]:
            selected.append(activities[i])
    return selected

print("20. Activity Selection:", activity_selection([1,3,0,5], [2,4,6,7]))


# ---------------------------------------------------------
# 21. FIBONACCI (DP)
# ---------------------------------------------------------
def fibonacci_dp(n):
    dp = [0, 1]
    for i in range(2, n + 1):
        dp.append(dp[i - 1] + dp[i - 2])
    return dp[n]

print("21. Fibonacci DP:", fibonacci_dp(6))


# ---------------------------------------------------------
# 22. KNAPSACK (0/1)
# ---------------------------------------------------------
def knapsack(wt, val, W):
    n = len(val)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(W + 1):
            if wt[i - 1] <= w:
                dp[i][w] = max(val[i - 1] + dp[i - 1][w - wt[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]
    return dp[n][W]

print("22. Knapsack:", knapsack([1,3,4], [15,20,30], 4))


# ---------------------------------------------------------
# 23. HILL CLIMBING (SIMPLE)
# ---------------------------------------------------------
def hill_climbing(start, goal):
    while start < goal:
        start += 1
    return start

print("23. Hill Climbing:", hill_climbing(2, 5))


# ---------------------------------------------------------
# 24. BRUTE FORCE MIN
# ---------------------------------------------------------
def brute_force_min(arr):
    min_val = arr[0]
    for x in arr:
        if x < min_val:
            min_val = x
    return min_val

print("24. Brute Min:", brute_force_min([5, 1, 9]))


# ---------------------------------------------------------
# 25. EUCLIDEAN DISTANCE
# ---------------------------------------------------------
def euclidean_distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

print("25. Euclidean Distance:", euclidean_distance([1,2], [4,6]))


# ---------------------------------------------------------
# 26. MANHATTAN DISTANCE
# ---------------------------------------------------------
def manhattan_distance(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))

print("26. Manhattan Distance:", manhattan_distance([1,2], [4,6]))


# ---------------------------------------------------------
# 27. KNN DISTANCE COMPUTATION
# ---------------------------------------------------------
def knn_distance(data, query):
    return [euclidean_distance(point, query) for point in data]

print("27. KNN Distance:", knn_distance([[1,2], [3,4]], [2,3]))


# ---------------------------------------------------------
# 28. PROBABILITY
# ---------------------------------------------------------
def probability(success, total):
    return success / total

print("28. Probability:", probability(3, 10))


# ---------------------------------------------------------
# 29. LOGICAL AND CLASSIFIER
# ---------------------------------------------------------
def and_classifier(x1, x2):
    return 1 if x1 == 1 and x2 == 1 else 0

print("29. AND Classifier:", and_classifier(1, 0))


# ---------------------------------------------------------
# 30. LINEAR MODEL (y = mx + c)
# ---------------------------------------------------------
def linear_model(x, m, c):
    return m * x + c

print("30. Linear Model:", linear_model(5, 2, 1))


print("\nAll 30 algorithms executed successfully ✅")
