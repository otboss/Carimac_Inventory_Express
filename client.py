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
        self.lname = lname
        self.pwd = pwd

class Notification:
    def __init__(self, id, title, message):
        self.id = id
        self.title = title
        self.message = message
        
#INVENTORY CLASS NOT INCLUDED, THE INVENTORY WOULD BE AN SQLLITE FILE RATHER THAN A PYTHON OBJECT
#THE SQLLITE FIEL WOULD STORE ALL ACCOUNTS, NOTIFICATIONS, 




#FUNCTIONS

'''
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
'''

isAdmin = False

def login(id, password):
    global isAdmin
    r = requests.post(url+"login", data={'id': id, 'password': password})
    if(r.text == "1"):
        if id == "admin":
            isAdmin = True
        return 1
    return 0

def logout():
    global running
    isAdmin = False
    running = False
    os.system('reset || cls')
    

def search(query, sorting):
    r = requests.get(url+"search?query="+query)
    print(r.text)
    if sorting == 123:
        print("")
    else:
        print("")
    results = []
    return results


def adminMenu():
    print("Select an option shown below: ")
    print(" 1] Search Item")
    print(" 2] Add Item")
    print(" 3] Add Account")  
    print(" 4] Remove Item") 
    print(" 5] Remove Account") 
    print(" 6] View Orders") 
    print(" 7] Clear Screen")
    print(" 8] Log Off\n") 

def mainMenu():
    print("Select an option shown below: ")
    print(" 1] Search Item")
    print(" 2] Place Order")
    print(" 3] View Notifications")  
    print(" 4] Clear Screen")  
    print(" 5] Log Off\n") 

def title():
    print("=========================")
    print("CARIMAC INVENTORY EXPRESS")
    print("=========================\n")


url = ""
def connect(ip, port):
    try:
        body = requests.get('http://'+ip+":"+port+"/").text
        global url
        url = "http://"+ip+":"+port+"/"
        return 1
    except:
        return 0
    



 
#VARIABLES

order = []
choice = 0

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
        print("\nCONNECTION ESTABLISHED\n")
        username =  input("Enter Username: ")
        password = getpass.getpass("Enter Password: ")
        if login(username, password):
            #LOGIN SUCCESSFUL
            running = True
            os.system('reset || cls')
            while(running):
                print("Logged in as: "+username+"\n")
                if(isAdmin):
                    adminMenu()
                    while(True):
                        try:                
                            choice = int(input("Choice: "))
                            if choice < 1 or choice > 8:
                                raise Exception()
                            break
                        except:
                            print("\nInvalid Selection\n")
                            
                    if(choice == 8):
                        logout()
                    
                    if(choice == 1):
                        query = input("Enter the search query :")
                        print(search(query, 123))
                        
                    if(choice == 2):
                        item = Item()
                        item.name = input("Enter the item name: ")
                        item.quantity = float(input("Enter the item quantity: "))
                        
                        query = input("Enter the search query :")
                        
                    if(choice == 3):
                        query = input("Enter the search query :")
                        
                    if(choice == 4):
                        os.system('reset || cls')
                        
                    if(choice == 4):
                        os.system('reset || cls')
                        
                    if(choice == 4):
                        os.system('reset || cls')
                        
                    if(choice == 7):
                        os.system('reset || cls')
                else:
                    mainMenu()
                    while True:
                        try:                
                            choice = int(input("Choice: "))
                            if choice < 1 or choice > 7:
                                raise Exception()
                            break
                        except:
                            print("\nInvalid Selection\n")
                            mainMenu()
                    if choice == 4:
                        #LOG OUT
                        logout()       
                        break      
                    if choice == 1:
                        query = input("Enter Search Query: ")
                        print (search)
                    if choice == 2:
                        #COMPLETE OPTION 2
                        print()
                    if choice == 3:
                        #COMPLETE OPTION 2
                        print()
        else:
            print("Failed to login\n")
