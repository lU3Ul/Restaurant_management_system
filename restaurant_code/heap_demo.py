class MinHeap:

    def __init__(self):
        self._heap = []

    def push(self, item, priority=None):
        if priority is None:
            # For heap sort: store the value directly
            self._heap.append(item)
            self._sift_up(len(self._heap) - 1)
        else:
            # For priority queue: store as (priority, item)
            self._heap.append((priority, item))
            self._sift_up(len(self._heap) - 1)

    def _sift_up(self, idx):
        while idx > 0:
            parent = (idx - 1) // 2
            if self._heap[idx] < self._heap[parent]:
                self._heap[idx], self._heap[parent] = self._heap[parent], self._heap[idx]
                idx = parent
            else:
                break

    def pop(self):
        if not self._heap:
            return None
        if len(self._heap) == 1:
            return self._heap.pop()

        self._heap[0], self._heap[-1] = self._heap[-1], self._heap[0]
        min_item = self._heap.pop()
        self._sift_down(0)
        return min_item

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

    def is_empty(self):
        return len(self._heap) == 0

    def __len__(self):
        return len(self._heap)


def heap_sort(arr):
    heap = MinHeap()
    for val in arr:
        heap.push(val)
    sorted_arr = []
    while not heap.is_empty():
        sorted_arr.append(heap.pop())
    return sorted_arr


def demo_priority_queue():
    print("=== Priority Queue Demo (Hand-written Heap, Orders by Table Priority) ===")
    pq = MinHeap()

    orders = [
        ("Order A (Table 3)", 3),
        ("Order B (Table 1)", 1),
        ("Order C (Table 2)", 2),
        ("Order D (Table 1)", 1),
    ]

    for desc, priority in orders:
        pq.push(desc, priority)
        print(f"Enqueued: {desc} (priority {priority})")

    print("\nKitchen processing order (hand-written heap):")
    while not pq.is_empty():
        item = pq.pop()
        # pop returns (priority, desc) when priority was given
        if isinstance(item, tuple):
            print(item[1])  # extract the description
        else:
            print(item)


def demo_heap_sort():
    print("\n=== Heap Sort Demo (Hand-written Heap) ===")
    test_lists = [
        [5, 2, 9, 1, 5, 6],
        [3, 0, -1, 8, 7],
        ["banana", "apple", "cherry", "date"]
    ]

    for i, lst in enumerate(test_lists, 1):
        sorted_lst = heap_sort(lst)
        print(f"Original list {i}: {lst}")
        print(f"Sorted list   : {sorted_lst}")
        print()


if __name__ == "__main__":
    demo_priority_queue()
    demo_heap_sort()