import os
import getpass
import sqlite3


db = sqlite3.connect("cmac.db").cursor()

#FUNCTIONS

def login(username, password):
    return 1

def search(string, sorting, sortBy):
    if sorting == 123:
        print("")
    else:
        print("")
    results = []
    return results

#CLASSES

class Item:
    def __init__(self, id, name, price, stock):
        seld.id = id
        self.name = name
        self.price = price
        self.stock = stock
    



#VARIABLES



if __name__ == "__main__":
    print()
