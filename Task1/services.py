from models import MenuItem, Food, Drink, Dessert, User, VIPUser, Order

# ---------- Hand-written MinHeap (for PriorityQueue and heap_sort) ----------
class MinHeap:
    """Min-heap implemented from scratch using a list."""
    def __init__(self):
        self._heap = []

    def push(self, item):
        """Insert an item into the heap. Item can be a comparable value or a tuple."""
        self._heap.append(item)
        self._sift_up(len(self._heap) - 1)

    def pop(self):
        """Remove and return the smallest item. Returns None if empty."""
        if not self._heap:
            return None
        if len(self._heap) == 1:
            return self._heap.pop()
        # Swap root with last element
        self._heap[0], self._heap[-1] = self._heap[-1], self._heap[0]
        min_item = self._heap.pop()
        self._sift_down(0)
        return min_item

    def peek(self):
        """Return the smallest item without removing it."""
        return self._heap[0] if self._heap else None

    def is_empty(self):
        return len(self._heap) == 0

    def __len__(self):
        return len(self._heap)

    def _sift_up(self, idx):
        """Sift up the element at index idx to maintain heap property."""
        while idx > 0:
            parent = (idx - 1) // 2
            if self._heap[idx] < self._heap[parent]:
                self._heap[idx], self._heap[parent] = self._heap[parent], self._heap[idx]
                idx = parent
            else:
                break

    def _sift_down(self, idx):
        """Sift down the element at index idx to maintain heap property."""
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


# ---------- Priority Queue using hand-written MinHeap ----------
class PriorityQueue:
    """Min-heap based priority queue. Smaller priority value means higher priority.
       Hand-written, no external libraries.
    """
    def __init__(self):
        self._heap = MinHeap()
        self._index = 0   # to maintain FIFO for equal priorities

    def push(self, item, priority):
        """
        Insert an element with a given priority.
        :param item: any object
        :param priority: smaller value = higher priority
        """
        # Store (priority, index, item). The index ensures that for equal priorities,
        # the one inserted first will be popped first (since tuple compares second element).
        self._heap.push((priority, self._index, item))
        self._index += 1

    def pop(self):
        """Remove and return the highest priority element (lowest priority number)."""
        if self._heap.is_empty():
            return None
        return self._heap.pop()[2]   # return the item part

    def is_empty(self):
        return self._heap.is_empty()

    def __len__(self):
        return len(self._heap)


# ---------- Heap Sort using hand-written MinHeap ----------
def heap_sort(arr):
    """
    Heap sort implemented from scratch (ascending order).
    :param arr: list of sortable elements
    :return: new sorted list
    """
    heap = MinHeap()
    for val in arr:
        heap.push(val)
    sorted_arr = []
    while not heap.is_empty():
        sorted_arr.append(heap.pop())
    return sorted_arr


# ---------- Restaurant Management Class ----------
class Restaurant:
    """Core restaurant management class, handling menu, orders, etc."""
    def __init__(self):
        self.menu = []
        self.orders = []
        self.order_queue = PriorityQueue()   # now using hand-written heap
        self._order_tables = {}
        self._next_order_id = 1

    def add_menu_item(self, item):
        """Add a dish to the menu."""
        self.menu.append(item)

    def create_order(self, table_number, customer, items):
        """
        Create a new order.
        :param table_number: table number (used for kitchen priority)
        :param customer: User or VIPUser instance
        :param items: list of MenuItem instances
        :return: newly created Order instance
        """ 

        order_id = f"ORD{self._next_order_id:03d}"
        self._next_order_id += 1

        new_order = Order(order_id, customer)

        for item in items:
            new_order.add_item(item)

        self._order_tables[new_order.order_id] = table_number
        self.orders.append(new_order)

        #make the VIPuser's order in the front
        priority = 0 if isinstance(customer, VIPUser) else 1
        self.order_queue.push(new_order, priority=priority)
        print(f"Order {new_order.order_id} (Table {table_number}) created and added to kitchen queue.")
        return new_order

    def display_menu(self):
        """Print the menu."""
        if not self.menu:
            print("Menu is empty")
            return
        print("====== MENU ======")
        for item in self.menu:
            print(f"{item.name} - ${item.price:.2f}  ({item.get_type()})")
        print("==================")

    def process_kitchen_queue(self):
        """Simulate kitchen processing: pop orders by priority."""
        print("Kitchen starts processing orders:")
        while not self.order_queue.is_empty():
            order = self.order_queue.pop()
            table = self._order_tables.get(order.order_id, "Unknown table")
            print(f"Preparing order {order.order_id} (Table {table})")
            order.status = "Completed"
        print("All orders processed.")

    # ---------- Additional staff functions ----------
    def get_completed_orders_report(self):
        """
        Return detailed report of all completed orders.
        Shows each order's table, items, final amount, and summary.
        """
        completed = [order for order in self.orders if order.status == "Completed"]
        if not completed:
            return "No completed orders yet."

        lines = []
        lines.append("=" * 60)
        lines.append("           COMPLETED ORDERS REPORT")
        lines.append("=" * 60)

        total_revenue = 0
        for i, order in enumerate(completed, 1):
            table = self._order_tables.get(order.order_id, "Unknown")
            items_str = ", ".join([item.name for item in order.items])
            final_amount = order.apply_discount()
            lines.append(f"\nOrder #{i}: {order.order_id}")
            lines.append(f"  Table: {table}")
            lines.append(f"  Customer: {order.customer.name}")
            lines.append(f"  Items: {items_str}")
            lines.append(f"  Total after discount: ${final_amount:.2f}")
            total_revenue += final_amount

        lines.append("\n" + "=" * 60)
        lines.append("SUMMARY")
        lines.append(f"  Total Completed Orders: {len(completed)}")
        lines.append(f"  Total Revenue: ${total_revenue:.2f}")
        lines.append("=" * 60)
        return "\n".join(lines)


# ---------- Payment Processing Class ----------
class Payment:
    """Payment utility class with static methods."""
    @staticmethod
    def process_payment(order, amount_paid):
        """
        Process payment for an order.
        :param order: Order instance
        :param amount_paid: amount paid
        :return: change amount, or -1 if insufficient payment
        """
        total = order.apply_discount()
        if amount_paid >= total:
            change = amount_paid - total
            print(f"Payment successful, change: ${change:.2f}")
            order.status = "Completed"
            return change
        else:
            print("Payment failed: insufficient amount")
            return -1


# ---------- Independent Tests ----------
if __name__ == "__main__":
    print("=== Testing MinHeap (hand-written) ===")
    h = MinHeap()
    for val in [5, 2, 9, 1, 5, 6]:
        h.push(val)
    print("Pop order (should be sorted):")
    while not h.is_empty():
        print(h.pop(), end=" ")
    print("\n")

    print("=== Testing PriorityQueue (hand-written) ===")
    pq = PriorityQueue()
    pq.push("Task A", priority=3)
    pq.push("Task B", priority=1)
    pq.push("Task C", priority=2)
    pq.push("Task D", priority=1)
    while not pq.is_empty():
        print(pq.pop())
    # Expected order: Task B, Task D, Task C, Task A (FIFO for equal priority)

    print("\n=== Testing heap_sort (hand-written) ===")
    arr = [5, 2, 9, 1, 5, 6]
    sorted_arr = heap_sort(arr)
    print("Original:", arr)
    print("Sorted:  ", sorted_arr)

    print("\n=== Testing restaurant system ===")
    # Create a few menu items
    food1 = Food("Hamburger", 25.0, "lightly spicy", "Classic beef burger")
    drink1 = Drink("Cola", 8.0, 330, "Iced")
    rest = Restaurant()
    rest.add_menu_item(food1)
    rest.add_menu_item(drink1)
    rest.display_menu()

    user = User("Alice", "12345678")
    order = rest.create_order(3, user, [food1, drink1])
    print(f"Order created: {order.order_id}")
    print("Processing kitchen queue...")
    rest.process_kitchen_queue()
    print("Payment test:")
    Payment.process_payment(order, 40.0)
    print("Completed orders report:")
    print(rest.get_completed_orders_report())
