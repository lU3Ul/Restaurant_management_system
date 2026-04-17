# Self-Studied Data Structure & Algorithm

## Introduce video link:https://www.bilibili.com/video/BV1MrdeBUEm8?spm_id_from=333.788.recommend_more_video.-1&trackid=web_related_0.router-related-2479604-dplt2.1776397202270.502&vd_source=d2c03edd984ad00ccbcdfc20b7acf764

## 1. How to Run

1. Ensure Python 3.7+ is insstalled.
2. Run the demo:
   ```bash
   python heap_demo.py
   ```
## 2. Overview 

This folder contains implementations of a self-studied data structure and a self-studied algorithm:

| Component | Topic | Reason for selection |
|-----------|-------|--------------|
| **Data Structure** | Heap (Priority Queue) |Sort orders through the table number in Task1|
| **Algorithm** | Heap Sort |Sort the dished rated in Task1|
## 3. Demo & Usage Examples
### 3.1 Priority Queue Demo
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
### 3.2 Heap Sort Demo
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