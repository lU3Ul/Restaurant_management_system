import heapq
from models import MenuItem, Food, Drink, Dessert, User, VIPUser, Order

class PriorityQueue:
    """Min-heap based priority queue. Smaller priority value means higher priority."""
    def __init__(self):
        self._heap = []
        self._index = 0

    def push(self, item, priority):
        """
        Insert an element into the queue.
        :param item: any comparable element
        :param priority: priority value (smaller is more urgent)
        """
        heapq.heappush(self._heap, (priority, self._index, item))
        self._index += 1

    def pop(self):
        """Pop and return the highest priority element (returns None if queue is empty)."""
        if self._heap:
            return heapq.heappop(self._heap)[-1]
        return None

    def is_empty(self):
        return len(self._heap) == 0

    def __len__(self):
        return len(self._heap)


def heap_sort(arr):
    """
    Heap sort (ascending order for lists).
    :param arr: list of sortable elements
    :return: new sorted list
    """
    heap = list(arr)
    heapq.heapify(heap)
    sorted_arr = []
    while heap:
        sorted_arr.append(heapq.heappop(heap))
    return sorted_arr


class Restaurant:
    """Core restaurant management class, handling menu, orders, etc."""
    def __init__(self):
        self.menu = []
        self.orders = []
        self.order_queue = PriorityQueue()
        self._order_tables = {}
        self._next_order_id = 1

    def add_menu_item(self, item):
        """Add a dish to the menu."""
        self.menu.append(item)
        print(f"Added item: {item.name}")

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

        self.order_queue.push(new_order, priority=table_number)
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
        """Simulate kitchen processing: pop orders by priority (for testing)."""
        print("Kitchen starts processing orders:")
        while not self.order_queue.is_empty():
            order = self.order_queue.pop()
            table = self._order_tables.get(order.order_id, "Unknown table")
            print(f"Preparing order {order.order_id} (Table {table})")
            order.status = "Completed"
        print("All orders processed.")


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


if __name__ == "__main__":
    print("=== Testing PriorityQueue ===")
    pq = PriorityQueue()
    pq.push("Task A", priority=3)
    pq.push("Task B", priority=1)
    pq.push("Task C", priority=2)
    while not pq.is_empty():
        print(pq.pop())

    print("\n=== Testing heap_sort ===")
    arr = [5, 2, 9, 1, 5, 6]
    sorted_arr = heap_sort(arr)
    print("Original array:", arr)
    print("Sorted array:  ", sorted_arr)

    print("\n=== Testing restaurant system (using real models) ===")
    food1 = Food("Hamburger", 25.0, "lightly spicy", "Classic beef burger")
    drink1 = Drink("Cola", 8.0, 330, "Iced")
    dessert1 = Dessert("Tiramisu", 38.0, "normal", "Italian dessert")

    rest = Restaurant()
    rest.add_menu_item(food1)
    rest.add_menu_item(drink1)
    rest.add_menu_item(dessert1)
    rest.display_menu()

    user = User("Zhang San", "12345678")
    vip = VIPUser("Li Si", "87654321", priority=5)

    order1 = rest.create_order(5, user, [food1, drink1])
    print(f"Order {order1.order_id} created, subtotal (before discount): ${order1.calculate_total():.2f}, after discount: ${order1.apply_discount():.2f}")

    order2 = rest.create_order(2, vip, [food1, dessert1])
    print(f"Order {order2.order_id} created, subtotal (before discount): ${order2.calculate_total():.2f}, after discount: ${order2.apply_discount():.2f}")

    print("\n--- Payment test ---")
    Payment.process_payment(order1, 40.0)
    Payment.process_payment(order2, 70.0)

    print("\n--- Kitchen queue simulation ---")
    rest.process_kitchen_queue()
