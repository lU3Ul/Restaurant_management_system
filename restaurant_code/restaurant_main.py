from models import MenuItem, Food, Drink, Dessert, User, VIPUser, Order
from services import PriorityQueue, heap_sort, Restaurant, Payment


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
        print('   [2]Add Dishes)')
        print('   [3]Remove Dishes')
        print('   [4]View Current Order')
        print('   [5]Search Dishes')
        print('   [6]Checkout&Pay')
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
    keyword=input('Enter search keyword:').strip().lower()
    #List comprehension filter
    result=[item for item in restaurant.menu if keyword in item.name.lower()]
    if result:
        print(f"\nFound {len(result)} items:")
        for item in result:
            print(f"{item}")
    else:
        print("No items found.")

def checkout():
    view_current_order()
    total = current_order.apply_discount()
    print(f'\nTotal to pay is ${total:.2f}')
    try:
        paid = float(input("Enter payment amount: $").strip())
        change = Payment.process_payment(current_order, paid)
        #Static method call
        if change >= 0:
            print('Payment successful!Thank you!')
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
        
    
#Only a simple example,will be improved later.
def init_menu():
    foods=[
        Food("Kung Pao Chicken", 68.0, "Medium", "Sichuan classic")
        ]
    drink=[
        Drink("Cola", 12.0, 330, "Iced")
        ]
    dessert=[
        Dessert("Tiramisu", 38.0, "Normal", "Italian dessert")
        ]
    for item in foods+drink+dessert:
        restaurant.add_menu_item(item)
        
        
        
def staff_page():
    print('=============== Staff System ===============')
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
   

