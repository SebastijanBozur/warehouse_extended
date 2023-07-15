import os

WAREHOUSE_FILE = "warehouse.txt"


class Warehouse:
    def __init__(self):
        self.items = {}
        self.operations = []
        self.balance = 0.0
        self.amount = 0.0

    def review(self):
        index_from = int(input("Please enter starting point of log: "))
        index_to = int(input("Please enter ending point of log: "))
        for operation in self.operations[index_from:index_to]:
            operation.print()

    def list(self):
        print('Total Warehouse inventory: ')
        for name, value in self.items.items():
            print(name, value)

    def find(self):
        name = input("Enter item name in warehouse: ")
        if name in self.items:
             quantity = self.items[name]
             print(f"Quantity: {quantity}")
        else:
            print("Item not in warehouse")

    def save(self, file_path):
        with open(file_path, 'w') as file:
            file.write(f'{self.balance}\n{self.amount}\n')
            for name, qty in self.items.items():
                file.write(f'{name}\n{qty}\n')
            file.write('\n')
            for operation in self.operations:
                operation.save(file, self)
            file.write('end\n')

    def load(self, file_path):
        with open(file_path) as file:
            self.balance = float(file.readline())
            self.amount = float(file.readline())
            while True:
                name = file.readline().strip()
                if not name:
                    break
                qty = int(file.readline())
                self.items[name] = qty
            while True:
                operation_name = file.readline().strip()
                operation = None
                if operation_name == 'balance':
                    operation = Balance()
                if operation_name == 'sale':
                    operation = Sale()
                if operation_name == 'purchase':
                    operation = Purchase()
                if operation:
                    operation.load(file)
                    self.operations.append(operation)
                if operation_name == 'end':
                    break


class Balance:
    def __init__(self):
        self.amount = 0.0
        self.mode = 0

    def input(self):
        self.mode = int(input("Would you like to deposit(1), withdraw(2) or look at balance(3)"))
        if self.mode != 3:
            self.amount = float(input('Please enter the amount you would like to deposit or withdraw'))

    def print(self):
        if self.mode == 1:
            print(f"You deposited {self.amount}")
        if self.mode == 2:
            print(f"You withdrawn {self.amount}")
    def execute(self, warehouse):
        if self.amount < 0:
            print('Invalid amount')
            return
        if self.mode == 2:
            if self.amount > warehouse.balance:
                print("Not enough funds.")
                return
            warehouse.balance -= self.amount
        if self.mode == 1:
            warehouse.balance += self.amount
        if self.mode == 3:
            print(f'Your current balance is {warehouse.balance}')
            return
        warehouse.operations.append(self)

    def save(self, file, warehouse):
        file.write(f'balance\n{self.amount}\n{self.mode}\n')

    def load(self, file):
        self.amount = float(file.readline())
        self.mode = int(file.readline())


class Purchase:
    def __init__(self):
        self.item = ""
        self.price = 0
        self.quantity = 0

    def input(self):
        self.item = input("Enter item name: ")
        self.price = float(input("Enter item price: "))
        self.quantity = int(input("Enter item quantity: "))

    def execute(self, warehouse):
        if warehouse.balance < self.price * self.quantity:
            print("not enough funds")
            return
        warehouse.balance -= self.price * self.quantity
        if self.item not in warehouse.items:
            warehouse.items[self.item] = 0
        warehouse.items[self.item] += self.quantity
        warehouse.operations.append(self)

    def print(self):
        print(f"Bought {self.item} of item: {self.quantity}, {self.price}€ each")

    def save(self, file, warehouse):
        file.write(f'purchase\n{self.item}\n{self.price}\n{self.quantity}\n')

    def load(self, file):
        self.item = file.readline()
        self.price = float(file.readline())
        self.quantity = int(file.readline())


class Sale:
    def __init__(self):
        self.item = ""
        self.price = 0
        self.quantity = 0

    def input(self):
        self.item = input("Enter item name: ")

    def print(self):
        print(f"Sold {self.item} of item: {self.quantity}, {self.price}€ each")

    def execute(self, warehouse):
        if self.item not in warehouse.items:
            print(f"Item({self.item}) not in warehouse")
            return
        self.quantity = int(input("Enter item amount: "))
        if warehouse.items[self.item] < self.quantity:
            print("Insufficient quantity")
            return
        self.price = float(input("Enter item price: "))
        warehouse.balance += self.price * self.quantity
        warehouse.items[self.item] -= self.quantity
        warehouse.operations.append(self)

    def save(self, file, warehouse):
        file.write(f'sale\n{self.item}\n{self.price}\n{self.quantity}\n')

    def load(self, file):
        self.item = file.readline()
        self.price = float(file.readline())
        self.quantity = int(file.readline())


def menu():
    warehouse = Warehouse()
    warehouse.load(WAREHOUSE_FILE)

    while True:
        print("- balance")
        print("- sale")
        print("- purchase")
        print("- account")
        print("- list")
        print("- warehouse")
        print("- review")
        print("- end")
        user_input = input("Enter one of the commands: ").lower().strip()

        if user_input == "account":
            print(f'Your current balance is {warehouse.balance}')
            continue
        if user_input == "list":
            warehouse.list()
        if user_input == "warehouse":
            warehouse.find()
            continue
        if user_input == "review":
            warehouse.review()
            continue
        if user_input == "end":
            warehouse.save(WAREHOUSE_FILE)
            break
        operation = None
        if user_input == "balance":
            operation = Balance()
        if user_input == "sale":
            operation = Sale()
        if user_input == "purchase":
            operation = Purchase()
        if operation:
            operation.input()
            operation.execute(warehouse)
            continue


menu()
