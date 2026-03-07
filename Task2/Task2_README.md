# Self-Studied Data Structure & Algorithm

## 1. How to Run

1. Ensure Python 3.7+ is installed.
2. Run the demo:
   ```bash
   python heap_demo.py
   ```
## 2. Overview 

This folder contains implementations of a self-studied data structure and a self-studied algorithm:

| Component | Topic | Reason for selection |
|-----------|-------|--------------|
| **Data Structure** | Heap (Priority Queue) |Sort orders through the table number in Task1|
| **Algorithm** | Heap Sort |Demonstrates practical application of heap structure for sorting|

**Key Difference from Task 1**: 
- Task 1 uses Python's built-in `heapq` library for priority queue operations.
- Task 2 implements heap data structure from scratch, including core operations like `_sift_up` and `_sift_down`, demonstrating understanding of internal mechanisms.

## 3. Difference between Heap and Heap Sort

1. **Different abstraction levels** 
   - Heap = Data structure (storage & organization) 
   - Heap Sort = Algorithm (procedure to solve sorting problem) 

2. **Different operations** 
   - Heap focuses on: insert, extract-min/max, peek 
   - Heap Sort focuses on: sorting array in-place 

3. **Different complexity analysis** 
   - Heap operations: O(log n) per operation 
   - Heap Sort: O(n log n) total for complete sorting 

---

## 4. Heap Data Structure 

### 4.1 Definition 

**heap** is an abstract data structure that can quickly obtain the max-heap or min-heap by using a complete binary tree structure.
 **heap property**:

- **Max-Heap**: For every node `i`, `value[i] ≥ value[children(i)]`
  
- **Min-Heap**: For every node `i`, `value[i] ≤ value[children(i)]`
- Our implementation uses min-heap (smaller value = higher priority).
### 4.2 Abstract Data Type (ADT) 
**Data:** Collection of elements with comparable keys

**Operations:**
- `push(item, priority)`: Insert element with priority
- `pop()`: Remove and return highest priority (minimum) element
- `is_empty()`: Check if heap contains elements
- `__len__()`: Return number of elements
- `peek()`: Return highest priority element without removing it
### 4.3 Core Operations

| Operation | Description | Time Complexity | Space Complexity|
|-----------|-------------|-----------------|-----|
| `push(item, priority)` | Insert element with priority | O(log n) |O(1)|
| `pop()` | Remove and return highest priority element | O(log n) |O(1)|
| `peek()` | View highest priority without removal | O(1) |O(1)|
| `is_empty()` | Check if heap is empty | O(1) |O(1)|
| `heapify()` | Build heap from unordered array | O(n) |O(1)|

**Properties:**
- **Complete Binary Tree**: All levels filled except possibly last 
- **Array Implementation**: Efficient storage without pointers  
  - Parent of `i`: `(i-1) // 2` 
  - Left child of `i`: `2*i + 1` 
  - Right child of `i`: `2*i + 2` 

### 4.4 Implementation 
#### 4.4.1 MinHeap Class Structure
```python
class MinHeap:
    def __init__(self)                      # Initialize empty heap
    def push(self, item, priority=None)     # Insert element
    def _sift_up(self, idx)                 # Maintain heap property upward
    def pop(self)                           # Extract minimum element
    def _sift_down(self, idx)               # Maintain heap property downward
    def is_empty(self)                      # Check if heap is empty
    def __len__(self)                       # Get heap size
```
#### 4.4.2 Sift-Up Operation
**Purpose:** Restore heap property after insertion at bottom.
**Algorithm:**
1. Start from inserted node (index `i`)
2. Compare with parent at `(i-1)//2`
3. If child < parent, swap
4. Move up to parent position, repeat until root or property satisfied

**Implementation:**
```python
def _sift_up(self, idx):
    while idx > 0:
        parent = (idx - 1) // 2
        if self._heap[idx] < self._heap[parent]:
            self._heap[idx], self._heap[parent] = self._heap[parent], self._heap[idx]
            idx = parent
        else:
            break
```
**Time Complexity:** O(log n) — at most tree height operations.

#### 4.4.3 Sift-Down Operation
**Purpose:** Restore heap property after removal from root.

**Algorithm:**
1. Move last element to root (after swap and pop)
2. Compare with both children at `2i+1` and `2i+2`
3. If larger than smaller child, swap with that child
4. Move down to child position, repeat until leaf or property satisfied

**Implementation:**
```python
def _sift_down(self, idx):
    n = len(self._heap)
    while True:
        left = 2 * idx + 1
        right = 2 * idx + 2
        smallest = idx

        if left < n and self._heap[left] < self._heap[smallest]:
            smallest = left
        if right < n and self._heap[right] < self._heap[smallest]:
            smallest = right

        if smallest != idx:
            self._heap[idx], self._heap[smallest] = self._heap[smallest], self._heap[idx]
            idx = smallest
        else:
            break
```
**Time Complexity:** O(log n) — at most tree height operations.

#### 4.4.4 Dual-Mode Push Operation
**Our implementation supports two usage patterns:**
| Mode               | Usage                  | Storage                  | Purpose                     |
| ----------------- | --------------------- | ----------------------- | -------------------------- |
| **Priority Queue** | `push(item, priority)` | `(priority, item)` tuple | Restaurant order scheduling |
| **Heap Sort**      | `push(value)`          | `value` directly         | Sorting arrays              |
**Implementation:**
```python
def push(self, item, priority=None):
    if priority is None:
        # For heap sort: store the value directly
        self._heap.append(item)
        self._sift_up(len(self._heap) - 1)
    else:
        # For priority queue: store as (priority, item)
        self._heap.append((priority, item))
        self._sift_up(len(self._heap) - 1)
```
### 4.5 Possible Applications

| Application Domain | Heap Usage | Benefit | Real Example |
|-------------------|------------|---------|--------------|
| **OS Task Scheduling** | Ready queue for process priorities | O(log n) priority management | Linux kernel scheduler |
| **Event Simulation** | Event queue by timestamp | Efficient next-event retrieval | Bank queue simulation |
| **Median Maintenance** | Two heaps for streaming data | O(log n) update, O(1) median | Real-time stock prices |
| **Our Restaurant System** | Kitchen order queue by table | Fair order processing | Small tables served faster |

## 5. Heap Sort Algorithm

### 5.1 Algorithm Description
**Heap sort is an in-place sorting algorithm that uses the heap data structure:**

1. **Build Heap**: Convert unsorted array to heap (using sift-down)
2. **Extract Repeatedly**: 
   - Swap root (min/max) with last element
   - Reduce heap size by 1
   - Sift-down new root to maintain heap property

3. **Result**: Array sorted in-place

### 5.2 Time Complexity
| Phase | Complexity |Explanation |
|:---|:---|:---|
| **Build Heap** | O(n) |Using bottom-up heapification (sift-down from last non-leaf node) |
| **n extractions** | O(n log n) |Each extraction takes O(log n) to restore heap property |
| **Total** | O(n log n) |Dominated by extraction phase |
| **Space** | O(1) | In-place sorting, no extra heap storage needed |

**Note**: If heap is built by n insertions, build phase would be O(n log n) , but standard heap sort uses **bottom-up heapification** to achieve O(n) construction.

## 6. Demo & Usage Examples
### 6.1 Priority Queue Demo
**Scenario:** Kitchen processes orders by table number (smaller = higher priority).
```python
orders = [
    ("Order A (Table 3)", 3),
    ("Order B (Table 1)", 1),
    ("Order C (Table 2)", 2),
    ("Order D (Table 1)", 1),
]

for desc, priority in orders:
    pq.push(desc, priority)
```
**Execution Order:**
```python
Order B (Table 1)   # First (priority 1)
Order D (Table 1)   # Second (priority 1, inserted after B)
Order C (Table 2)   # Third (priority 2)
Order A (Table 3)   # Fourth (priority 3)
```
**Output**
```python
=== Priority Queue Demo (Hand-written Heap, Orders by Table Priority) ===
Enqueued: Order A (Table 3) (priority 3)
Enqueued: Order B (Table 1) (priority 1)
Enqueued: Order C (Table 2) (priority 2)
Enqueued: Order D (Table 1) (priority 1)

Kitchen processing order (hand-written heap):
Order B (Table 1)
Order D (Table 1)
Order C (Table 2)
Order A (Table 3)
```
### 6.2 Heap Sort Demo
**Test Cases:**
- Integer array with duplicates
- Mixed positive/negative numbers
- String sorting

**Output:**
```python
=== Heap Sort Demo (Hand-written Heap) ===
Original list 1: [5, 2, 9, 1, 5, 6]
Sorted list   : [1, 2, 5, 5, 6, 9]

Original list 2: [3, 0, -1, 8, 7]
Sorted list   : [-1, 0, 3, 7, 8]

Original list 3: ['banana', 'apple', 'cherry', 'date']
Sorted list   : ['apple', 'banana', 'cherry', 'date']
```
