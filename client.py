import os
import getpass
import time
import requests

########
#CLASSES
########
 
class Item:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

class Invoice:
    def __init__(self, id, InventoryRecordId, quantity):
        self.id = id
        self.item = InventoryRecordId
        self.quantity = quantity
        
class Account:
    def __init__(self, id, employeeId, login, pwd, slt, isAdm):
        self.id = id
        self.employeeId = employeeId
        self.login = login
        self.pwd = pwd
        self.slt = slt
        self.isAdm = isAdm    
        
class Employee:
    def __init__(self, id, fname, mname, lname, dob, email, phone, date):
        self.id = id
        self.fname = fname
        self.mname = mname
        self.lname = lname
        self.dob = dob
        self.email = email
        self.phone = phone
        self.login = login
        self.pwd = pwd
        self.slt = slt
        self.isAdm = isAdm
        self.date = date

class Notification:
    def __init__(self, id, title, message):
        self.id = id
        self.title = title
        self.message = message
        
#INVENTORY CLASS NOT INCLUDED, THE INVENTORY WOULD BE AN SQLLITE FILE RATHER THAN A PYTHON OBJECT
#THE SQLLITE FIEL WOULD STORE ALL ACCOUNTS, NOTIFICATIONS, 




#FUNCTIONS


database = [
    [   
        {"id":"", 
        "fname":"", "mname":"", "lname":"", "dob":"", "eml":"", "fname":"", "fname":"", "fname":"", "fname":"", "fname":""}
    
    ],
    
    [
        
    
    ],
    
    [
        
    
    ]
]



def login(username, password):
    return 1


def search(string, sorting, sortBy):
    if sorting == 123:
        print("")
    else:
        print("")
    results = []
    return results


def mainMenu():
    print("Select an option shown below: ")
    print(" 1] Search Query")
    print(" 2] Place Order")
    print(" 3] View Notifications")  
    print(" 4] Log Off\n") 

def title():
    print("=========================")
    print("CARIMAC INVENTORY EXPRESS")
    print("=========================\n")

def connect(ip, port):
    return 0
    



 
#VARIABLES

order = []
chances = 3
running = True;


if __name__ == "__main__":
    while True:
        #PROGRAM LOOP START
        title()
        ip , port = "" , ""
        while connect(ip, port) == False:
            ip = input("Enter Host Ip: ")
            port = input("Enter Host Port: ")
            print("\nConnecting...")
            if connect(ip, port) == False:
                print("\nCould not connect to host machine. Please ensure that the server is running and try again.\n")
        print("\nCONNECTION ESTABLISHED")
        username =  input("Enter Username: ")
        password = getpass.getpass("Enter Password: ")
        if login(username, password):
            #LOGIN SUCCESSFUL
            while(running):
                os.system('reset || cls')
                print("Logged in as: "+username+"\n")
                mainMenu()
                while True:
                    try:                
                        choice = int(input("Choice: "))
                        if choice < 1 or choice > 4:
                            raise Exception()
                        break
                    except:
                        print("\nInvalid Selection\n")
                        mainMenu()
                if choice == 4:
                    #LOG OUT
                    os.system('reset || cls')
                    break      
                if choice == 1:
                    query = raw_input("Enter Search Query: ")
                    print (search)
                if choice == 2:
                    #COMPLETE OPTION 2
                    print()
                if choice == 3:
                    #COMPLETE OPTION 2
                    print()
        else:
            chances -= 1
            print("Failed to login")
