import os
import sys
import store
import products

STORE_MENU = """
   Store Menu
   ----------
1. List all products in store
2. Show total amount in store
3. Make an order
4. Quit

Please choose a number: """

def clear_the_terminal():
    """
    Clears the terminal.
    :return: None
    """
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For macOS and Linux
    else:
        os.system('clear')


def ask_number(message="Give a number: ",
               lower_limit=0,
               upper_limit=None,
               return_type=int,
               allow_empty=False):
    """
    Checks that the user enters a number and not something else
    :param return_type: int or float
    :param allow_empty: If yes, allows the user to not enter anything. In this case, returns None
    :param upper_limit: The number from the user needs to be below or equal to this
    :param lower_limit: The number from the user needs to be higher or equal to this
    :param message: What we display to xplain to the user what number we need
    :return: the number, duh! Or if allow_empty=True and user enters nothing, returns None
    """
    valid_number = False
    user_input_number = None
    while not valid_number:
        user_input_number = input(f"{message}").strip()
        if len(user_input_number) == 0 and allow_empty:
            return None
        try:
            if return_type is int:
                user_input_number = int(user_input_number)
            elif return_type is float:
                user_input_number = float(user_input_number)
            else:
                raise TypeError("Return type must be either int or float")
            valid_number = True
        except ValueError:
            user_input_number = lower_limit - 1

        if lower_limit is not None and user_input_number < lower_limit:
            valid_number = False
        if upper_limit is not None and user_input_number > upper_limit:
            valid_number = False

    return user_input_number


def setup_store():
    """setup initial stock of inventory"""
    product_list = [ products.Product("MacBook Air M2", price=1450, quantity=100),
                     products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                     products.Product("Google Pixel 7", price=500, quantity=250),
                     products.ImmaterialProduct("Windows License", price=125),
                     products.ImmaterialProduct("XYZ Service Contract", price=400),
                     products.LimitedImmaterialProduct("Shipping", price=10, maximum=1),
                     products.LimitedProduct("Rare coffee", price=100, maximum=1, quantity=100),
                   ]
    best_buy = store.Store(product_list)
    return best_buy


def print_products(best_buy):
    """
    List products in the store
    :param best_buy: instance of the class Store
    :return: None
    """
    for product_num, product in enumerate(best_buy.get_all_products()):
        print(f"{product_num+1}. {product.show()}")


def show_total_items_in_store(best_buy):
    """ Print total items in the store """
    total_products_in_store = sum(product.get_quantity() for product in best_buy.get_all_products()
                                  if isinstance(product, products.Product))
    print(f"Total of {total_products_in_store} items in store")

def print_order(order_list):
    """
    Print the quantity, products, and total price of each order item in the order list
    :param order_list: A list of tuples. The tuple: (instance of Product class, quantity)
    :return: None
    """
    for order_item_no, order_item in enumerate(order_list):
        product, quantity = order_item
        product_name, product_price = product.name_and_price(quantity)
        print(f"{order_item_no+1:>5}. {quantity:5} * {product_name:.<30} ${product_price}")

def get_order(best_buy):
    """
    Get a validated order from the user. Ensure the store can provide the order.
    :param best_buy: instance of the class Store
    :return: A list of tuples. The tuple: (instance of Product class, quantity)
    """
    order_list = []
    available_products = best_buy.get_all_products()
    clear_the_terminal()
    print("   Available products")
    print("   ------------------")
    print_products(best_buy)
    while True:
        print("\nWhen you want to finish the order, enter empty text.\n")
        product_number = (ask_number(message="Which product # do you want to add to the order? ",
                            lower_limit=1,
                            upper_limit=len(available_products),
                            return_type=int,
                            allow_empty=True)
                       or None
            )
        if product_number is None:
            break
        if isinstance(available_products[product_number - 1], products.ImmaterialProduct):
            upper_limit = None
        else:
            upper_limit = available_products[product_number - 1].get_quantity()
        quantity = (ask_number(message="What amount do you want? ",
                                lower_limit=1,
                                upper_limit=upper_limit,
                                return_type=int,
                                allow_empty=True)
                        or None
                    )
        if quantity is None:
            break
        order_list.append((available_products[product_number - 1], quantity))
        validation_result, message = best_buy.validate_shopping_list(order_list)
        if validation_result is not True:
            order_list.pop()
            print(f"Could not add that to the order because {message}.")
        else:
            clear_the_terminal()
            print("   Your order so far")
            print("   -----------------")
            print_order(order_list)
            print("\n   Available products")
            print("   ------------------")
            print_products(best_buy)
    return order_list


def make_an_order(best_buy):
    """
    Get an order from the user and then make the order to the store
    :param best_buy: An instance of the Store class
    :return: None
    """
    order_list = get_order(best_buy)
    if len(order_list) == 0 :
        print("Order was empty. Smart move!")
        return
    print("\n********\n")
    payment_needed, message = best_buy.order(order_list)
    if payment_needed is None:
        print(f"Error while making an order. The store did not accept the order because {message}")
        return
    print("Order made!\n")
    print_order(order_list)
    print(f"\nTotal payment: ${payment_needed}")


def quit_best_buy():
    """
    Quit the program
    """
    print("      Goodbye!\n\n")
    sys.exit()()


def start(best_buy):
    """
    Receive user commands
    :param best_buy: An instance of the Store class
    :return: None
    """
    commands = {
        1: print_products,
        2: show_total_items_in_store,
        3: make_an_order,
    }
    clear_the_terminal()
    while True:
        command_num = (ask_number(message=STORE_MENU,
                                 lower_limit=1,
                                 upper_limit=4,
                                 return_type=int,
                                 allow_empty=True)
                       or 4)
        clear_the_terminal()
        print("   Command output")
        print("   --------------")
        if command_num in commands:
            commands[command_num](best_buy)
        elif command_num == 4:
            quit_best_buy()


def main():
    """
    Setup the store and start receiving user commands.
    """
    best_buy = setup_store()
    start(best_buy)

if __name__ == '__main__':
    main()
