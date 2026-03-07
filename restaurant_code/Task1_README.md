# Restaurant Management System


## 1. Project introduction

### 1.1 Overview

This project is a Python-based **object-oriented restaurant management system**,aim to improve work efficiency and manage orders in an orderly manner.

**Current problems**
- **Chaotic order management**：Traditional paper orders are easy to lose and difficult to classify
- **Checkout mistakes**：Manual calculation produces errors
- **Customer-graded service**：Unable to automatically identify VIP customers to provide differentiated services

**Application scenario：**
- small and medium-size Western/Chinese restaurant
- Cafe and dessert shop
- Fast food chain store
  
### 1.2 Quick Start 
- **Python**: 3.7+
```bash
python restaurant_main.py        
python models.py                 
python services.py               
```
---

## 2. Core Function

| Functional module | Function introduction |
|---------|---------|
| **Customer management** | Supports registration for both regular and VIP users. VIPs automatically enjoy a 10% discount and priority service. |
| **Menu management** | Manages three categories of dishes: foods, drinks, and desserts. Supports categorized display and search. |
| **Order Management** | Creates orders, adds and remove dishes, calculates prices in real time (including discounts), and tracks status. |
| **Payment system** |Processes payments, calculates change, and verifies sufficient payment amount. |
| **Staff system** | Staffs can check the bills and the revenue of the day, while chefs can view and process pending orders.|

---

## 3. Application of OOP concepts

This project **fully applies** the core concept of object-oriented programming:

### 3.1 Classes and Objects
- Define a class:MenuItem,Food,Drink,Dessert,User,VIPUser,Order,Restaurant,Payment...
- Create an class:
```python
food=Food("Kung Pao Chicken",68.0,"Medium","Sichuan classic")
```

### 3.2 Instance Method
- Define method within a class
```python
MenuItem.get_type()
Order.calculate_total()
Restaurant.create_order()
```
- The ```__init__``` constructor is used to initialize object attributes
  
### 3.3 Encapsulation
- Private attributes:```MenuItem._name```,```Order._Items```.
- Accessor method:Read-only access is provided via ```@property ```.
```python
@property
def name(self)->str:
    return self.__name
```
- Setter method:```Order.status.setter``` control state modifications

### 3.4 Inheritance
- ```Food```,```Drink```,```Dessert```inherits from ```Menu```
,```VIPUser```inherits from```User```
```python
class Food(MenuItem):
class Drink(MenuItem):
class Dessert(MenuItem):
class VIPUser(User):
```
- Calling the parent class constructor from the subclass:```super().__init__(name,price,description)```
  
### 3.5 Polymorphism
- Method overriding
  - ```get_type()```return different strings in```Food```,```Drink```,```Dessert```.
  - ```apply_discount()```return original price in```User```,return 10% discount price in ```VIPUser```.

### 3.6 Abstraction
- ```MenuItem``` inherits from```ABC```and contains the abstract method ```get_type```
```python
from abc import ABC, abstractmethod
class MenuItem(ABC):
    @abstractmethod
    def get_type(self)->str:
        pass
```

### 3.7 Static Method
- ```process_payment```in class```Payment```is implemented using```@staticmethod```:.
```python
class Payment:
    @staticmethod
    def process_payment(order,amount_paid):
```
- Invocation style:```Payment.process_payment(order,40.0)```

### 3.8 Magic Method
- ```__init__```:The constructor for all classes
- ```__str__```:Customize the string representation of an object, such as ```MenuItem.__str__```,```Order.__str__```.
```python
def __str__(self)->str:
    return f"{self.__name}(${self.__price:.2f})-{self.__description}"
```

### 3.9 Composition
- Class```Order```contains ```User```object (```self.__customer```) and list of ```MenuItem```objects (```self.__items```).
- Class ```Restaurant```contains a list of ```Order```objects and a ```PriorityQueue```object.

---

## 4. Demo & Usage Examples
**This section demonstrates the core functionality and code logic of the system through practical scenarios.**
### 4.1 System Enter & Role Selection
- As the program start, it will show a ***Role-selection page*** through a simple CLI menu:
```python
def first_page():
    print('=============== Welcome to the Restaurant! ===============\n')
    print('   Please select your role\n')
    print('     [111] Customer (VIP)')
    print('     [222] Customer (Regular)')
    print('     [333] Staff (Check bills)')
    print('     [444] Chef (Check order)')
    print('     [0] Exit the system')
    print('\n=============== Welcome to the Restaurant! ===============')
    enter_code=input('Please enter your code:').strip()
    return enter_code
```
- There are five different executing results:
  
-**If enter 111**
  
  -**The VIPUser page**
```python
  =============== Welcome to the Restaurant! ===============
Please enter your code:111
Enter your name:Zhangsan
Enter your contact number:123456

Welcome Zhangsan! You will enjoy 10% discount on your order today
Enter the number of table:1
Order ORD001 (Table 1) created and added to kitchen queue.
============= Welcome to the order system ===============

   [1]View Menu
   [2]Add Dishes)
   [3]Remove Dishes
   [4]View Current Order
   [5]Search Dishes
   [6]Checkout&Pay
   [0]Back to Main

=============== Welcome to the Restaurant! ===============
Enter the number before the instruction:
```
-**If enter 222**

  -**The ordinary user page**
```python
=============== Welcome to the Restaurant! ===============
Please enter your code:222
Enter your name:Lisi
Enter your contact number:234567

Welcome Lisi!
Enter the number of table:2
Order ORD002 (Table 2) created and added to kitchen queue.
============= Welcome to the order system ===============

   [1]View Menu
   [2]Add Dishes)
   [3]Remove Dishes
   [4]View Current Order
   [5]Search Dishes
   [6]Checkout&Pay
   [0]Back to Main

=============== Welcome to the Restaurant! ===============
Enter the number before the instruction:
```
-**If enter 333**

  -**The staff page**
```python


=============== Welcome to the Restaurant! ===============
Please enter your code:333
=============== Staff System ===============
Total orders:2

Order ORD001
Customer: Zhangsan
Status: Pending
Items: []
Subtotal: $0.00
Final Amount:$0.00

Order ORD002
Customer: Lisi
Status: Pending
Items: []
Subtotal: $0.00
Final Amount:$0.00

Total revenue:$0.00
```
-**If enter 444**

  -**The chef page**
```python
=============== Welcome to the Restaurant! ===============
Please enter your code:444
=============== Chef System ===============

Pending Orders in Queue: 2

Processing Order (Priority by Table ):
Kitchen starts processing orders:
Preparing order ORD001 (Table 1)
Preparing order ORD002 (Table 2)
All orders processed.
```

### 4.2 Core Function Demo
- The following example demonstrates the full execute cycle of an order, showing multiple OOP concepts:


| Step | User Input | System Output | OOP Concept Demonstrated |
|---|---|---|---|
| 1 | `111` (VIP) | `Welcome Zhangsan! You will enjoy 10% discount` | **Inheritance** - VIPUser inherits from User |
| 2 | Table: `1` | `Order ORD001 created` | **Factory Method** - Auto-generated unique ID |
| 3 | `[1] View Menu` | Display 3 items with formatted prices | **Magic Method** - `__str__` formatting |
| 4 | `[2] Add Dish` → `1` | `Added: Kung Pao Chicken` | **Composition** - Order contains MenuItem |
| 5 | `[4] View Order` | `Subtotal: $68.00`<br>`After Discount: $61.20` | **Polymorphism** - VIP applies 10% off automatically |
| 6 | `[6] Checkout` → Pay `$70` | `Payment successful, change: $8.80` | **Static Method** - Payment.process_payment() |
| 7 | `[0] Back` | Return to main menu | - |

**Key Observation:** At Step 5, the same `apply_discount()` method produces different results based on customer type (Zhangsan: $61.20 vs Lisi: $68.00).

---

#### Detailed Code Execution for Step 4-5 (Composition + Polymorphism)

```python
#Step 4: Adding item (Composition)
current_order.add_item(dish)  
#Order.__items list now contains: [Food("Kung Pao Chicken", 68.0, "Medium", "Sichuan classic")]

#Step 5: Price calculation (Polymorphism in action)
print(f"Subtotal: ${current_order.calculate_total():.2f}")      
# $68.00 (ordinary)
print(f"After Discount: ${current_order.apply_discount():.2f}") 
# $61.20 (10% discount)
```
#### Complete executing result of VIPUser
```python
=============== Welcome to the Restaurant! ===============
Please enter your code: 111
Enter your name: Zhangsan
Enter your contact number: 123456
Welcome Zhangsan! You will enjoy 10% discount on your order today
Enter the number of table: 1

============= Welcome to the order system ===============
   [1] View Menu
   [2] Add Dishes
   [3] Remove Dishes
   [4] View Current Order
   [5] Search Dishes
   [6] Checkout & Pay
   [0] Back to Main
======================================================
Enter choice: 1

=============== Menu ===============
1. Kung Pao Chicken ($68.00) - Sichuan classic [Spiciness: Medium]
2. Cola ($12.00) - Iced [330ml]
3. Tiramisu ($38.00) - Italian dessert [Sugar: Normal]
===================================

Enter choice: 2
Enter dish number: 1
Added: Kung Pao Chicken

Enter choice: 4

Order ORD001
Customer: Zhangsan
Status: Pending
Items: [Kung Pao Chicken]
Subtotal: $68.00
After Discount: $61.20          

Enter choice: 6
Total to pay is $61.20
Enter payment amount: $70
Payment successful, change: $8.80
Payment successful! Thank you!
```
### 4.3 Kitchen Queue Processing (Heap-based PriorityQueue)

The system uses a **min-heap** to manage kitchen orders. Priority is determined by table number (smaller table = higher priority).

```python
=============== Welcome to the Restaurant! ===============
Please enter your code:444
=============== Chef System ===============

Pending Orders in Queue: 2

Processing Order (Priority by Table ):
Kitchen starts processing orders:
Preparing order ORD001 (Table 1)
Preparing order ORD002 (Table 2)
All orders processed.
```
#### Data Structure: Min-heap ensures O(log n) insertion and **O(log n)** extraction of highest priority item (smallest table number).


## 5. Future improvements

### Staff System:
- Add order cancellation and refund functionality
- Real-time revenue statistics with daily reports
- Adding or removing some dishes from the menu
### Chef System:
- Mark individual dishes as "preparing" / "ready" 
- Prioritize the completion of VIPUsers'orders
### The menu
- Enrich the menu content,add more dishes.
- Personalize the dishes, allow users to adjust the spiciness and sweetness.
  
## 6. Project structure
- restaurant-system/
  - models.py
  - services.py
  - restaurant_main.py
  - Task1_README.md         









