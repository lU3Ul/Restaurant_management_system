# Restaurant Management System

## Introduce video link:https://www.bilibili.com/video/BV1ySdeBGEgZ/?spm_id_from=333.1387.homepage.video_card.click&vd_source=d2c03edd984ad00ccbcdfc20b7acf764


## About JSON: 
To store the ratings permanently, we use json.The code for saving and loading ratings (save_all_ratings(), load_ratings(), save_ratings()) are not writen by ourselves independently. We refer from online tutorials and the official Python documentation.


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
| **Customer management** | Supports registration for both regular and VIP users. VIPs automatically enjoy a 10% discount and priority service.|
| **Menu management** | Manages three categories of dishes: foods, drinks, and desserts. Supports display and search. |
| **Order Management** | Creates orders, adds and remove dishes, calculates prices in real time (including discounts), and tracks status. |
| **Payment system** |Processes payments, calculates change, and verifies sufficient payment amount. |
| **Staff system** | Staffs can check the bills，menu sorted by ratings and the revenue of the day, while chefs can view and process pending orders.|
| **Rating system** | After checkout, every customer asked to rate the dishes they ordered.|
---


## 3. Usage Examples
**This section demonstrates the core functionality and code logic of the system through practical scenarios.**
### 3.1 System Enter & Role Selection
- As the program start, it will show a ***Role-selection page*** :
```python
=============== Welcome to the Restaurant! ===============

   Please select your role

     [111] Customer (VIP)
     [222] Customer (Regular)
     [333] Staff (Check bills)
     [444] Chef (Check order)
     [0] Exit the system

=============== Welcome to the Restaurant! ===============
Please enter your code:
```
- There are five different executing results:
  - 111 or 222 is all for customers
  - 333 is for staff view bills and ratings of dishes
  - 444 is for chef check current orders
  - 0 is exit the system
- All result will be explain later:
if you enter 0:
```python
=============== Welcome to the Restaurant! ===============
Please enter your code:0

Thank you for using system.
```

### 3.2 Core Function execute(customer111 and 222)
- The following example demonstrates the full execute cycle of an order：
After choose your role(VIP/ordinary user), Let me show you the full process:
```python
============= Welcome to the order system ===============

   [1]View Menu
   [2]Add Dishes
   [3]Remove Dishes
   [4]View Current Order
   [5]Search Dishes
   [6]Menu of the rating order
   [7]Checkout&Pay
   [0]Back to Main

=============== Welcome to the Restaurant! ===============
Enter the number before the instruction:
```
- if you want to view the whole Menu, press 1:
```python
===============Menu===============
1.Kung Pao Chicken ($68.00) - Sichuan classic [Spiciness: Medium]
2.Spaghetti Bologness ($58.00) - Italian classic [Spiciness: Medium]
3.Filet Mignon ($128.00) - Australian imported [Spiciness: Medium]
... #will show all dishes when you run it
===============Menu===============
```
it will show you all dishes with price and details.
- You see the Menu found there are so many dishes that you can't fint the dish you want.Then, press 5.(The example is with "cake".)
```python
=============== Welcome to the Restaurant! ===============
Enter the number before the instruction:5
Enter search keyword:cake
16. Chocolate cake ($35.00) - Belgian chocolate [Sugar: Normal]
17. Cheesecake ($35.00) - New York dessert [Sugar: Normal]
```
This fuction makes you can search dishes with the key word.
- From searching, you know the number of chocolate cake is 16 and you want to add.
- You press 2 and enter the number of chocolate cake 16.
```python
=============== Welcome to the Restaurant! ===============
Enter the number before the instruction:2

===============Menu===============
1.Kung Pao Chicken ($68.00) - Sichuan classic [Spiciness: Medium]
2.Spaghetti Bologness ($58.00) - Italian classic [Spiciness: Medium]
3.Filet Mignon ($128.00) - Australian imported [Spiciness: Medium]
...
===============Menu===============
Enter the number of dish you want to order:16
Added:Chocolate cake
```
- But after a while, you don't want a chocolate cake, you want a Tiramisu.
- So you press 3 and remove it.
```python
=============== Welcome to the Restaurant! ===============
Enter the number before the instruction:3

Current items:
1.Chocolate cake ($35.00) - Belgian chocolate [Sugar: Normal]
Enter the number of dish you want to remove:1
Removed:Chocolate cake
```
- Then you press 2 to order Tiramisu(15).
```python
=============== Welcome to the Restaurant! ===============
Enter the number before the instruction:2

===============Menu===============
1.Kung Pao Chicken ($68.00) - Sichuan classic [Spiciness: Medium]
2.Spaghetti Bologness ($58.00) - Italian classic [Spiciness: Medium]
3.Filet Mignon ($128.00) - Australian imported [Spiciness: Medium]
...
===============Menu===============
Enter the number of dish you want to order:15
Added:Tiramisu
```
- Later, you want to checkout, but you want to know if chocolate cake is removed.
- So you press 4.
```python
=============== Welcome to the Restaurant! ===============
Enter the number before the instruction:4

Order ORD004
Customer: Amy
Status: Pending
Items: [1.Tiramisu $38.00]
Subtotal: $38.00
Subtotal: $38.00
After Discount: $34.20
```
- You see you whole order and price.
- If you want to checkout.
- You can press 7.
```python
=============== Welcome to the Restaurant! ===============
Enter the number before the instruction:7

Order ORD004
Customer: Amy
Status: Pending
Items: [1.Tiramisu $38.00]
Subtotal: $38.00
Subtotal: $38.00
After Discount: $34.20

Total to pay is $34.20
Enter payment amount: $40
Payment successful, change: $5.80
Payment successful!Thank you!
```
- Then you notice you can rate the dish.
- So you follow the instroduction and rate 10 points!
```python
===============Rating Dishes===============

Your feedback helps us do better!
1.Tiramisu
Enter the number of the dish you want to rate.(or 0 to exit)

The number of dish(or 0 to exit):1
You mark of the is(1-10):10
Thank you for your rating!
```
- That's all about a VIP user's process of ordering.
- The process of VIP user and ordinary user is the same but two differences:
  - The price of VIP user has 10%d iscount.
  - The order of VIP user will have higher priority than ordinary user.

### 3.3 Core Function execute(staff 333)
- The function of staff is simpler than custom, just two functions:
  - View all bills
  - View the rate of dishes
```python
=============== Welcome to the Restaurant! ===============
Please enter your code:333
=============== Staff System ===============

   [1]View all Bills
   [2]View the rate of dishes
   [0]Back to Main

=============== Staff System ===============
Enter the number before the instruction:
```
- press 1, you can see all bills:
```python
Enter the number before the instruction:1
===============Bills system===============

Total orders:4

Order ORD001
Customer: 1
Status: Completed
Items: [1.Sprite $12.00]
Subtotal: $12.00
Final Amount:$10.80
...
Order ORD004
Customer: Amy
Status: Completed
Items: [1.Tiramisu $38.00]
Subtotal: $38.00
Final Amount:$34.20

Total revenue:$182.20

===============Bills system===============
```
- press 2, you can see the rate of dishes:
```python
===============Rated menu===============

1.Tiramisu $38.00 >>>Rating:10.0/10
2.Filet Mignon $128.00 >>>Rating:10.0/10
3.Cream phff $28.00 >>>Rating:9.0/10
4.Curry Beef Rice $56.00 >>>Rating:9.0/10
5.Kung Pao Chicken $68.00 >>>Rating:8.8/10
6.Apple pie $38.00 >>>Rating:8.0/10
7.Chocolate cake $35.00 >>>Rating:8.0/10
8.Sprite $12.00 >>>Rating:8.0/10
9.Cola $12.00 >>>Rating:6.7/10
10.Mango Pudding $25.00 >>>Rating:No Rate yet
...
20.Spaghetti Bologness $58.00 >>>Rating:No Rate yet

===============Rated menu===============
```
- That's all the functions about staff.

### 3.4 Core Function execute(chef 444) 
- Kitchen Queue Processing (Heap-based PriorityQueue)
- The system uses a **min-heap** to manage kitchen orders. Priority is determined by table number (smaller table = higher priority).
- The VIP user's priority is higher than ordinary user.
- The function of chef is only check current orders.
```python
=============== Welcome to the Restaurant! ===============
Please enter your code:444
=============== Chef System ===============

Pending Orders in Queue: 3

Processing Order (Priority by Table ):
Kitchen starts processing orders:
Preparing order ORD001 (Table 1)
Preparing order ORD003 (Table 3)
Preparing order ORD002 (Table 2)
All orders processed.
```
In this code, ORD001 and ORD003 is order of VIP.

#### Data Structure: Min-heap ensures O(log n) insertion and **O(log n)** extraction of highest priority item (smallest table number).


## 4. Future improvements
### Customer System:
- Add two or three dishes in a time that reduce repeated operations.
- Customize the spiciness and sweetness of the dishes.
### Staff System:
- Add order cancellation and refund functionality
- Real-time revenue statistics with daily reports
- Adding or removing some dishes from the menu
### Chef System:
- Mark individual dishes as "preparing" / "ready" 
### The menu
- Enrich the menu content,add more dishes.
- Personalize the dishes, allow users to adjust the spiciness and sweetness.
  
## 5. Project structure
- restaurant-system/
  - models.py
  - services.py
  - restaurant_main.py
  - Task1_README.md         









