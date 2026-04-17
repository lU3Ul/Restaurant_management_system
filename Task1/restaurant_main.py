from models import MenuItem, Food, Drink, Dessert, User, VIPUser, Order
from services import PriorityQueue, heap_sort, Restaurant, Payment
import json
import os

'''
To store all ratings permanently
we use JSON, taht can store all data after the program exits.
But we don't complete the related code independently,
We refer from online tutorials and the official Python documentation.
All rating data is stored in ratings.json
'''

#name the json file
RATINGS_FILE = "ratings.json"


#store global variables
restaurant=Restaurant()
#Restaurant instance
current_customer=None
#Current logged-in customer
current_order=None
#Current active order

def first_page():
    #Display main menu and get user role selection
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

def select_page():
    #Main loop for role selection and page routing
    while True:
        enter_code=first_page()
        if enter_code=='111':
            create_customer(VIP=True)
            order_page()
        elif enter_code=='222':
            create_customer(VIP=False)
            order_page()
        elif enter_code=='333':
            staff_page()
        elif enter_code=='444':
            chef_page()
        elif enter_code=='0':
            save_all_ratings()
            print('\nThank you for using system.')
            break
        else:
            print('\nThe code is incorrect,please enter correct code.')
        
def create_customer(VIP=False):
    global current_customer
    name=input('Enter your name:').strip()
    contact=input('Enter your contact number:')

    if VIP:
        current_customer=VIPUser(name,contact,priority=1)
        #Create VIPUser with priority level1
        print(f'\nWelcome {name}! You will enjoy 10% discount on your order today')
    else:
        current_customer=User(name,contact)
        #Create ordinary user
        print(f'\nWelcome {name}!')
    
def order_page():
    global current_order
    table=input('Enter the number of table:').strip()
    current_order=restaurant.create_order(table,current_customer,[])
    #Create new empty order
    while True:
        print('============= Welcome to the order system ===============\n')
        print('   [1]View Menu')
        print('   [2]Add Dishes')
        print('   [3]Remove Dishes')
        print('   [4]View Current Order')
        print('   [5]Search Dishes')
        print('   [6]Menu of the rating order')
        print('   [7]Checkout&Pay')
        print('   [0]Back to Main')
        print('\n=============== Welcome to the Restaurant! ===============')
        
        choice=input('Enter the number before the instruction:').strip()

        if choice=='1':
            display_menu()
        elif choice=='2':
            add_dish()
        elif choice=='3':
            remove_dish()
        elif choice=='4':
            view_current_order()
        elif choice=='5':
            search_dishes()
        elif choice=='6':
            display_menu_sorted()
        elif choice=='7':
            success=checkout()
            if success:
                break
            #Payment sucessful,exit the order page
        elif choice=='0':
            print('Returning to main menu...')
            break
        #Return to main menu
        else:
            print('The number is incorrect,please enter correct number.')

def display_menu():
    print('\n===============Menu===============')
    i=1
    for item in restaurant.menu:
        print(f'{i}.{item}')
        i+=1
    print('\n===============Menu===============')

def add_dish():
    display_menu()
    try:
        num=int(input('Enter the number of dish you want to order:').strip())
        if 1<=num<=len(restaurant.menu):
            dish=restaurant.menu[num-1]
            current_order.add_item(dish)
            #Composition:Order has MenuItem
            print(f'Added:{dish.name}')
        else:
            print('The number is error.')
    except ValueError:
        print('Please enter a valid number!')

def remove_dish():
    if not current_order.items:
        print('Order is not exist.')
        return
    #Display current items with numbers
    print('\nCurrent items:')
    i=1
    for item in current_order.items:
        print(f'{i}.{item}')
        i+=1

    try:
        num=int(input('Enter the number of dish you want to remove:').strip())
        if 1<=num<=len(current_order.items):
            removed = current_order.items[num-1]
            #Access private attribute
            current_order._Order__items.pop(num-1)
            print(f'Removed:{removed.name}')
        else:
            print('The number is error.')
    except ValueError:
        print('Please enter a valid number!')

def view_current_order():
    print(f"\n{current_order}")
    print(f"Subtotal: ${current_order.calculate_total():.2f}")
    print(f"After Discount: ${current_order.apply_discount():.2f}")
    #Polymorphism:different discount for VIPUser and ordinary User

def search_dishes():
    keyword = input('Enter search keyword:').strip().lower()
    found = False
    for i in range(len(restaurant.menu)):
        item = restaurant.menu[i]
        if keyword in item.name.lower():
            print(f"{i+1}. {item}")
            found = True
    if not found:
        print("No items found.")

def checkout():
    if not current_order.items:
        print("\nYou orderd nothing")
        input("Press enter return the menu...")
        return False
    view_current_order()
    total = current_order.apply_discount()
    print(f'\nTotal to pay is ${total:.2f}')
    try:
        paid = float(input("Enter payment amount: $").strip())
        change = Payment.process_payment(current_order, paid)
        #Static method call
        if change >= 0:
            print('Payment successful!Thank you!')
            rate_dishes(current_order)
            input('\nPress enter to return to main menu.')
            return True
        else:
            print('Payment failed! Insufficient amount.')
            input('\nPress enter to continue...')
            return False
    except ValueError:
        print('Invalid amount!')
        input('\nPress enter to continue...')
        return False

def display_menu_sorted():
    print("===============Rated menu===============\n")
    items_rating = []
    for i in range(len(restaurant.menu)):
        item = restaurant.menu[i]
        rating = item.get_average_rating() or 0
        items_rating.append((rating, i, item))
        
    sorted_pairs = heap_sort(items_rating)
    sorted_pairs.reverse() #make high-mark dish in the front
    sorted_menu = []
    for rating, i, item in sorted_pairs:
        sorted_menu.append(item)
    
    for i in range(len(sorted_menu)):
        item=sorted_menu[i]
        average_rating=item.get_average_rating()
        if average_rating is None:
            rating_mark="No Rate yet"
        else:
            rating_mark=f"{average_rating:.1f}/10"
        
        print(f"{i+1}.{item.name} ${item.price:.2f} >>>Rating:{rating_mark}")
    print("\n===============Rated menu===============")


def rate_dishes(order):
    
    print("\n===============Rating Dishes===============\n")
    print("Your feedback helps us do better!")
    for i in range(len(order.items)):
        dish=order.items[i]
        print(f"{i+1}.{dish.name}")
    print("Enter the number of the dish you want to rate.(or 0 to exit)\n")
    #use two loops to ensure the value user input is valid
    while True:
        rate_num=int(input("The number of dish(or 0 to exit):"))
        if rate_num==0:
            break
        if 1<=rate_num<=len(order.items):
            dish=order.items[rate_num-1]
            while True:
                score=float(input("You mark of the is(1-10):"))
                if 1<=score<=10:
                    dish.add_rating(score)
                    print("Thank you for your rating!")
                    save_all_ratings()
                    #save ratings to the file
                    break
                else:
                    print("The score should between 1-10.Please enter again.")
        else:
            print("Please enter the right number of the dishes.")


def load_ratings():
    if not os.path.exists(RATINGS_FILE):
        return {}
    #open json file, read only
    with open(RATINGS_FILE,'r',encoding='utf-8') as f:
        try:
            data=json.load(f)
            return data
        except json.JSONDecodeError:
            return {}

def save_ratings(ratings_dict):
    #store ratings into json file
    with open(RATINGS_FILE,'w',encoding='utf-8') as f:
        json.dump(ratings_dict, f,indent=2, ensure_ascii=False)

def save_all_ratings():
    ratings_dict={}
    for item in restaurant.menu:
        ratings=item.get_ratings()
        if ratings:
            ratings_dict[item.name]=ratings
    save_ratings(ratings_dict)
    
    

def init_menu():
    ratings_data=load_ratings()
    foods=[
        Food("Kung Pao Chicken", 68.0, "Medium", "Sichuan classic"),
        Food("Spaghetti Bologness", 58.0, "Medium", "Italian classic"),
        Food("Filet Mignon", 128.0, "Medium", "Australian imported"),
        Food("Seafood Pizza", 88.0, "spicy-free", "Turkish classic"),
        Food("Turkish Kebab", 68.0, "Medium", "Turkish style"),
        Food("Curry Beef Rice", 56.0, "Mild spicy", "Japanese style curry rice")
        ]
    drink=[
        Drink("Cola", 12.0, 330, "Iced"),
        Drink("Sprite", 12.0, 330, "Iced"),
        Drink("Latte", 22.0, 300, "Iced/hot"),
        Drink("Blue mountain coffee", 38.0, 250, "hot"),
        Drink("Black Tea", 15.0, 450, "Iced/hot"),
        Drink("Vodka", 350.0, 400, "Iced"),
        Drink("Red wine", 88.0, 300, "Iced"),
        Drink("Mojito", 58.0, 350, "Iced")
        
        ]
    dessert=[
        Dessert("Tiramisu", 38.0, "Normal", "Italian dessert"),
        Dessert("Chocolate cake", 35.0, "Normal", "Belgian chocolate"),
        Dessert("Cheesecake", 35.0, "Normal", "New York dessert"),
        Dessert("Mango Pudding", 25.0, "Normal", "Fresh mango flavor"),
        Dessert("Cream phff", 28.0, "Normal", "Cream filling"),
        Dessert("Apple pie", 38.0, "Normal", "fresh apple flavor")        
        ]
    for item in foods+drink+dessert:
        if item.name in ratings_data:
            item.set_ratings(ratings_data[item.name])
        restaurant.add_menu_item(item)
        
        
        
def staff_page():
    while True:
        print('=============== Staff System ===============\n')
        print('   [1]View all Bills')
        print('   [2]View the rate of dishes')
        print('   [0]Back to Main')
        print('\n=============== Staff System ===============')
        choice=input('Enter the number before the instruction:').strip()
        if choice=='1':
            display_bills()
        elif choice=='2':
            display_ratings()
        elif choice=='0':
            print('Returning to main menu...')
            break
        else:
            print('The number is incorrect,please enter correct number.')
        
def display_bills():
    print('===============Bills system===============\n')
    if not restaurant.orders:
        print('No order yet.')
        return
    print(f'Total orders:{len(restaurant.orders)}')
    total_revenue=0
    #Iterate through all orders
    for order in restaurant.orders:
        print(f'\n{order}')
        final=order.apply_discount()
        total_revenue+=final
        print(f'Final Amount:${final:.2f}')
    print(f'\nTotal revenue:${total_revenue:.2f}')
    print('\n===============Bills system===============')

def display_ratings():
    display_menu_sorted()


def chef_page():
    print('=============== Chef System ===============')
    print(f"\nPending Orders in Queue: {len(restaurant.order_queue)}")
    if restaurant.order_queue._heap:
        print("\nProcessing Order (Priority by Table ):")
        restaurant.process_kitchen_queue()
        #Heap-based priority processing
    else:
        print("No pending orders.")





#Run code  
init_menu()
select_page()


#========Test code========
def test_main():
    #Simple test for main functions
    init_menu()
    print("=== Starting Simple Test ===\n")
    
    # Test 1: Create customers
    vip = VIPUser("TestVIP", "123", priority=1)
    regular = User("TestRegular", "456")
    print(f"VIP level: {vip.member_level}, discount: {vip.apply_discount(100)}")
    print(f"Regular level: {regular.member_level}, discount: {regular.apply_discount(100)}")
    assert vip.apply_discount(100) == 90.0, "VIPUser 10% discount"
    assert regular.apply_discount(100) == 100.0, "Ordinary User no discount"
    print("PASS\n")
    
    # Test 2: Create order and add items
    order1 = restaurant.create_order("1", vip, [])
    order1.add_item(restaurant.menu[0])  # Add Kung Pao Chicken
    print(f"Order ID: {order1.order_id}")
    print(f"Subtotal: {order1.calculate_total()}")
    print(f"After discount: {order1.apply_discount()}")
    assert order1.apply_discount() == 61.2
    print("PASS\n")
    
    # Test 3: Payment
    change = Payment.process_payment(order1, 70.0)
    print(f"Change: {change:.2f}")
    assert order1.status == "Completed"
    print("PASS\n")

'''
#If want to test,please uncomment below and comment the Run code above
if __name__ == "__main__":
    test_main()
'''
   

