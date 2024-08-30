from tkinter import *
from tkinter import messagebox


# class to handle customer functions like adding items to the cart and placing orders
class Customer:
    def __init__(self, name, phone):
        # constructor to take phone number and name, then initialize an empty cart and total
        self.name = name
        self.phone = phone
        self.cart = []
        self.total = 0.0

    def add_to_cart(self, item_name, item_price):  # function to add items to the cart and update the total price
        self.cart.append((item_name, item_price))
        self.total += item_price

    def view_cart(self):  # function to properly display all the contents of the cart
        cart_contents = "Cart: \n"
        for item, price in self.cart:
            cart_contents += item + " - $" + str(price) + "\n"
        cart_contents += "Total: $" + str(round(self.total, 2))
        return cart_contents

    def place_order(self):    # method to write the order into a text file with name and phone number
        order_details = "Name: " + self.name + "\nPhone: " + self.phone + "\n"
        order_details += self.view_cart()

        # Save the order to a file
        with open("orders.txt", "a") as file:  # open the text file in append mode
            file.write(order_details + "\n---\n")

        self.cart = []  # reset cart and total
        self.total = 0.0
        return order_details


# class to handle delivery person functions like retrieving and viewing orders
class DeliveryPerson:
    def retrieve_orders(self):
        with open("orders.txt", "r") as file:  # open orders.txt in read mode
            orders = file.read().strip()  # read file and remove any extra space

        if orders:  # check if there are any orders
            orders_list = orders.split("\n---\n")
        else:
            orders_list = []

        return orders_list  # return the list of orders


# class to manage the entire application including GUI
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Delivery App")
        self.root.geometry("400x400")
        self.main_menu()

    def main_menu(self):
        self.clear_window()  # clear any widgets on the screen
        label = Label(self.root, text="Select Your Role:")
        label.pack()

        customer_button = Button(self.root, text="Customer", command=self.customer_info_screen)
        customer_button.pack()  # display customer button

        delivery_button = Button(self.root, text="Delivery Person", command=self.delivery_person_screen)
        delivery_button.pack()  # display the delivery person button

    def customer_info_screen(self):
        self.clear_window()  # clear any widgets on the screen

        name_label = Label(self.root, text="Enter your name:")
        name_label.pack()
        self.name_entry = Entry(self.root)
        self.name_entry.pack()

        phone_label = Label(self.root, text="Enter your phone number:")
        phone_label.pack()
        self.phone_entry = Entry(self.root)
        self.phone_entry.pack()

        next_button = Button(self.root, text="Next", command=self.save_customer_info)
        next_button.pack()

        back_button = Button(self.root, text="Back", command=self.main_menu)  # button to go back to main menu
        back_button.pack()

    def save_customer_info(self):
        name = self.name_entry.get()  # get the customer's name and number from the entry
        phone = self.phone_entry.get()

        # exception handling to make sure the phone number is an integer
        try:
            if len(phone) != 10:  # raises error if length is not 10
                raise ValueError
            int(phone)  # makes sure the number is digits only

        except ValueError:
            messagebox.showerror("Invalid Phone Number", "Please enter a phone number with 10 digits and no characters.")
            return

        self.customer = Customer(name, phone)  # create a new Customer object
        self.customer_screen()  # move to the customer screen

    def customer_screen(self):
        self.clear_window()  # clear the screen

        menu_label = Label(self.root, text="Menu:")
        menu_label.pack()

        menu_items = [("Pizza", 10.99), ("Burger", 5.99), ("Shawarma", 2.99)]
        for item, price in menu_items:
            # create a button for each menu item
            button = Button(self.root, text=item + " - $" + str(price), command=lambda i=item, p=price: self.add_to_cart(i, p))
            button.pack()

        self.cart_label = Label(self.root, text="Cart:\n")
        self.cart_label.pack()

        place_order_button = Button(self.root, text="Place Order", command=self.place_order)
        place_order_button.pack()

        back_button = Button(self.root, text="Back", command=self.main_menu)
        back_button.pack()

    def add_to_cart(self, item_name, item_price):
        self.customer.add_to_cart(item_name, item_price)  # add the item to the cart
        self.cart_label.config(text=self.customer.view_cart())  # update the cart label with the new items

    def place_order(self):
        order_details = self.customer.place_order()
        messagebox.showinfo("Order Placed", order_details)
        self.main_menu()

    def delivery_person_screen(self):
        self.clear_window()  # Clear the screen
        self.delivery_person = DeliveryPerson()

        orders = self.delivery_person.retrieve_orders()
        if not orders:
            no_orders_label = Label(self.root, text="No Orders Available")
            no_orders_label.pack()  # Display the no orders label
        else:
            select_order_label = Label(self.root, text="Select an Order to View:")
            select_order_label.pack()  # Display the select order label

            order_number = 1  # counter for order numbers
            for order in orders:  # go through list of orders
                button = Button(self.root, text="Order " + str(order_number), command=lambda o=order: self.view_order(o))
                button.pack()
                order_number += 1

        back_button = Button(self.root, text="Back", command=self.main_menu)  # back to the main menu button
        back_button.pack()  # display the back button

    def view_order(self, order):
        messagebox.showinfo("Order Details", order)  # pop up message with the order

    def clear_window(self):
        for widget in self.root.winfo_children():  # go through all widgets
            widget.destroy()  # destroy them all


# main
root = Tk()
app = App(root)
root.mainloop()