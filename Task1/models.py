from abc import ABC, abstractmethod

class MenuItem(ABC):
    """Abstract base class for all menu items."""
    def __init__(self, name: str, price: float, description: str = ""):
        self.__name = name          # private attribute
        self.__price = price
        self.__description = description

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def description(self) -> str:
        return self.__description

    @abstractmethod
    def get_type(self) -> str:
        """Return the type of menu item (to be implemented by subclasses)."""
        pass

    def __str__(self) -> str:
        return f"{self.__name} (${self.__price:.2f}) - {self.__description}"


class Food(MenuItem):
    """Food item, inherits from MenuItem."""
    def __init__(self, name: str, price: float, spiciness: str, description: str = ""):
        super().__init__(name, price, description)
        self.__spiciness = spiciness

    @property
    def spiciness(self) -> str:
        return self.__spiciness

    def get_type(self) -> str:
        return "Food"

    def __str__(self) -> str:
        return super().__str__() + f" [Spiciness: {self.__spiciness}]"


class Drink(MenuItem):
    """Drink item."""
    def __init__(self, name: str, price: float, volume: int, description: str = ""):
        super().__init__(name, price, description)
        self.__volume = volume  # milliliters

    @property
    def volume(self) -> int:
        return self.__volume

    def get_type(self) -> str:
        return "Drink"

    def __str__(self) -> str:
        return super().__str__() + f" [{self.__volume}ml]"

class Dessert(MenuItem):
    """Dessert item."""
    def __init__(self, name: str, price: float, sugar_level: str, description: str = ""):
        super().__init__(name, price, description)
        self.__sugar_level = sugar_level

    @property
    def sugar_level(self) -> str:
        return self.__sugar_level

    def get_type(self) -> str:
        return "Dessert"

    def __str__(self) -> str:
        return super().__str__() + f" [Sugar: {self.__sugar_level}]"


class User:
    """Regular user class."""
    def __init__(self, name: str, contact: str):
        self.__name = name
        self.__contact = contact
        self._member_level = "Normal"   # protected, allows subclass modification

    @property
    def name(self) -> str:
        return self.__name

    @property
    def contact(self) -> str:
        return self.__contact

    @property
    def member_level(self) -> str:
        return self._member_level

    def apply_discount(self, amount: float) -> float:
        """Regular user gets no discount."""
        return amount

    def __str__(self) -> str:
        return f"User: {self.__name}, Contact: {self.__contact}, Level: {self._member_level}"


class VIPUser(User):
    """VIP user, inherits from User."""
    def __init__(self, name: str, contact: str, priority: int = 1):
        super().__init__(name, contact)
        self._member_level = "VIP"      # change member level
        self.__priority = priority      # VIP-specific priority

    @property
    def priority(self) -> int:
        return self.__priority

    def apply_discount(self, amount: float) -> float:
        """VIP users get 10% discount (overrides parent method, demonstrating polymorphism)."""
        return amount * 0.9

    def __str__(self) -> str:
        return super().__str__() + f" (Priority: {self.__priority})"

class Order:
    """Order class, contains a user and a list of menu items."""
    def __init__(self, order_id: str, customer: User):
        self.__order_id = order_id
        self.__customer = customer          # composition: Order has a User
        self.__items = []                   # composition: Order has many MenuItems
        self.__status = "Pending"           # Order status: Pending, Completed, Cancelled

    @property
    def order_id(self) -> str:
        return self.__order_id

    @property
    def customer(self) -> User:
        return self.__customer

    @property
    def items(self) -> list:
        """Return a copy of items list to prevent external modification."""
        return self.__items.copy()

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, new_status: str):
        allowed = ["Pending", "Completed", "Cancelled"]
        if new_status in allowed:
            self.__status = new_status
        else:
            raise ValueError(f"Invalid status. Allowed: {allowed}")

    def add_item(self, item: MenuItem):
        """Add a menu item to the order."""
        self.__items.append(item)

    def calculate_total(self) -> float:
        """Calculate total price before discount."""
        return sum(item.price for item in self.__items)

    def apply_discount(self) -> float:
        """Apply user discount and return final total."""
        total = self.calculate_total()
        return self.__customer.apply_discount(total)

    def __str__(self) -> str:
        item_names = ", ".join([item.name for item in self.__items])
        return (f"Order {self.__order_id}\nCustomer: {self.__customer.name}\n"
                f"Status: {self.__status}\nItems: [{item_names}]\n"
                f"Subtotal: ${self.calculate_total():.2f}")


# ========== Test code ==========
if __name__ == "__main__":
    print("=== Testing MenuItem subclasses ===")
    food = Food("Kung Pao Chicken", 68.0, "Medium", "Sichuan classic")
    drink = Drink("Cola", 12.0, 330, "Iced")
    dessert = Dessert("Tiramisu", 38.0, "Normal", "Italian dessert")

    print(food)
    print(drink)
    print(dessert)
    print(f"Types: {food.get_type()}, {drink.get_type()}, {dessert.get_type()}")

    print("\n=== Testing User and VIPUser ===")
    user = User("Zhang San", "12345678")
    vip = VIPUser("Li Si", "87654321", priority=5)

    print(user)
    print(vip)

    amount = 100.0
    print(f"Regular user after discount: {user.apply_discount(amount)}")
    print(f"VIP user after discount: {vip.apply_discount(amount)}")

    print("\n=== Testing Order ===")
    order1 = Order("001", user)
    order1.add_item(food)
    order1.add_item(drink)

    order2 = Order("002", vip)
    order2.add_item(food)
    order2.add_item(dessert)

    print(order1)
    print(order2)

    print(f"Order1 subtotal: {order1.calculate_total():.2f}, after discount: {order1.apply_discount():.2f}")
    print(f"Order2 subtotal: {order2.calculate_total():.2f}, after discount: {order2.apply_discount():.2f}")

    # Change order status
    order1.status = "Completed"
    print(f"Order1 status after change: {order1.status}")
