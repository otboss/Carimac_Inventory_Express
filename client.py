import os
import getpass
import time
import requests
import ast
import datetime
import sys
import random

########
#CLASSES
########

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
        
class Item:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

class Invoice:
    def __init__(self, id, staffIdNum):
        self.id = id
        self.items = []
        if datetime.datetime.now().month < 10:
           self.date = str(datetime.datetime.now().year)+"-0"+str(datetime.datetime.now().month)+"-"+str(datetime.datetime.now().day)
        else:
           self.date = str(datetime.datetime.now().year)+"-"+str(datetime.datetime.now().month)+"-"+str(datetime.datetime.now().day)
        self.staffIdNum = staffIdNum
        self.filled = False
        
class Employee:
    def __init__(self, id, fname, mname, lname):
        self.id = id
        self.fname = fname
        self.lname = lname

class Staff(Employee):
    pass
    def __init__(self, staffId):
        self.staffId = staffId
    def createOrder(self):
        global url
        invoice = Invoice(random.randint(0,100000), username)
        item = ""
        available = 0
        quantity = 0
        while(True):
            search(input("\nEnter a substring of the item name: "))
            selection = input("See what you want? if not enter 'exit' to cancel, 'quit' to quit\n\n enter the item name: ")
            if(selection == 'exit'):
                continue
            if(selection  == 'quit'):
                return
            r = requests.get(url+"getquantity?name="+str(selection))
            try:
                available = int(ast.literal_eval(r.text))
                if available <= 0:
                    print(" The item is entered is currently not in stock")
                    continue
            except:
                print("Enter a valid option shown")
                continue                
            printf("\nThere are %.1f of this item available.\n\n", available)
            while True:
                try:
                    quantity = int(input("Enter your desired quantity  "))
                    while(quantity > available):
                        print("\nPlease enter a desired quantity that is less than the items is stock\n")
                        quantity = int(input("Enter your desired quantity  "))
                    break
                except:
                    print("\nInvalid Entry. Input must be numerical\n")
            item = Item(selection, quantity)
            if(selection != "" and quantity > 0):
                invoice.items.append(item.__dict__)
            ch = input("add more items? [y/N]: ")
            if ch == "y" or ch == "Y":
                continue
            else:
                print(invoice.__dict__)
                r = requests.get(url+"addinvoice?invoice="+str(invoice.__dict__))
                print(r.text)
                break
    def viewOrders(self, staffId):
        r = requests.get(url+"getorders?id="+str(staffId))
        orders = ast.literal_eval(r.text)
        print("==============================")
        print("|        ORDER HISTORY       |")
        print("==============================")
        print()
        for i in range(len(orders)):
            print("-------------------------")
            print("ID: "+ str(orders[i]["id"]))
            print("Date: "+orders[i]["date"]+"\n\n")
            for j in orders[i]["items"]:
                printf("%7s%8d\n", j["name"], j["quantity"])
            print("\n-------------------------\n\n")             
        
class UserAccount:
    def __init__(self, id, password):
        self.id = id
        self.password = password  
        

#~ class Notification:
    #~ def __init__(self, title, message):
        #~ self.title = title
        #~ self.message = message
        
#NOTIFICATIONS WOULD BE DISPLAYED ON THE USERS CONSOLE ITSELF AS THEY APPEAR, 
#THEREFORE A NOTIFICATION CLASS IS NOT NECESSARY

isAdmin = 0

def printf(format, *args):
    sys.stdout.write(format % args)
    
    
def login(id, password):
    global isAdmin
    r = requests.post(url+"login", data={'id': id, 'password': password})
    if(r.text == "1"):
        if id == "admin":
            isAdmin = 1
        return 1
    return 0


def logout():
    global isAdmin
    global running
    isAdmin = 0
    running = False
    os.system('reset || cls')
    

def search(query):
    r = requests.get(url+"search?query="+query)
    lst = ast.literal_eval(r.text)
    print("==========================")
    print("ITEM RELATED TO YOUR QUERY")
    print("==========================")
    print()
    if len(lst) == 0:
        print("    No results found")
    for i in range(len(lst)): 
        print(" "+ str(i+1)+"] "+lst[i])
    print("\n")


def search2(query):
    #SEARCH2 RETURNS A LIST UPON COMPLETION
    r = requests.get(url+"search?query="+query)
    lst = ast.literal_eval(r.text)
    print("==========================")
    print("ITEM RELATED TO YOUR QUERY")
    print("==========================")
    print()
    if len(lst) == 0:
        print("    No results found")
    for i in range(len(lst)): 
        print(" "+ str(i+1)+"] "+lst[i])
    print("\n")
    return lst
    
    
def deleteItem(query):
    p = search2(query)
    if(len(p) == 0):
        print("No results found..")
        return
    item = ""
    while(True):
        try:
            item = input("Select the desired item to delete: ")
            if(item == 'exit'):
                return
            item = int(item)
            break
        except:
            print("\nEnter a valid option shown or 'exit' to cancel\n")
    r = requests.get(url+"deleteitem?item="+p[item-1])
    print("\n"+r.text+"\n")
    
def getInvoices(selection):
    global url
    r = requests.get(url+"viewinvoices?selection="+str(selection))
    print(r.text)
    #AN ERROR OCCURS HERE. CREATE AN INVOICE AND ATTEMPT TO VIEW IT
    invoices = ast.literal_eval(r.text)
    if(len(invoices) == 0):
        print("\nNo invoices fall under the this category\n\n")
    print("\n\n\n")
    for i in invoices:
        print("======================")
        print("INVOICE NO: " + str(i["id"]))
        print("======================\n")
        print("Employee ID: " + str(i["staffIdNum"]))
        print("Date: " + i["date"] + "\n")
        for j in range(len(i["items"])):
            printf(" %2d] %13s %5.1f\n", j, i["items"][j]["name"], i["items"][j]["quantity"])
        print("\n\n\n")
        
        
def addAccount(id, password):
    global url
    r = requests.get(url+"addaccount?id="+str(id)+"&password="+str(password))
    print()
    print(r.text)
    print()
    
def removeAccount():
    global url
    r = requests.get(url+"getaccounts")
    accs = ast.literal_eval(r.text)
    print("\nEmployee accounts: \n")
    for i in range(len(accs)):
        printf("%5d %7s\n", i, str(accs[i]))
    while True:
        try:
            choice = input("\n\nSelect from the accounts list above or enter 'exit' to cancel: ")
            if(choice == "exit"):
                return
            choice = int(choice)
            if(choice < 0 and choice > len(accs)-1):
                raise Exception()
            break
        except:
            print("Enter a valid selection from the list")
    r = requests.get(url+"deleteaccount?id="+str(choice))
    print(r.text)
    
def adminMenu():
    print("Select an option shown below: ")
    print(" 1] Search Item")
    print(" 2] Add Item")
    print(" 3] Add Account")  
    print(" 4] Remove Item") 
    print(" 5] Remove Account") 
    print(" 6] View Invoices") 
    print(" 7] Clear Screen")
    print(" 8] Log Off\n") 

def mainMenu():
    print("Select an option shown below: ")
    print(" 1] Search Item")
    print(" 2] Place Order") 
    print(" 3] View Orders") 
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

def insertItem(item):
    r = requests.get(url+"additem?item="+item)
    print("\n"+r.text+"\n")


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
                print("\nLogged in as: "+username+"\n")
                if(isAdmin == 1):
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
                        search(input("\nEnter the search query: "))
                        
                    if(choice == 2):
                        name = input("Enter the item name: ")
                        while(True):
                            try:
                                quantity = float(input("Enter the item quantity: "))
                                break
                            except:
                                print("Enter a valid quantity")
                        item = Item(name, quantity)
                        insertItem(str(item.__dict__))
                        
                    if(choice == 3):
                        while True:
                            try:
                                addAccount(int(input("\nEnter the new account's id number: ")), input("Enter the new account's password: "))
                                break
                            except:
                                print("\nEnter an integer value\n")
                        
                    if(choice == 4):
                        deleteItem(input("\nEnter a substring of the item name: "))
                        
                    if(choice == 5):
                        removeAccount()
                        
                    if(choice == 6):
                        while True: 
                            print("\nSelect an option shown: ")
                            print(" 1] View Unfilled invoices")
                            print(" 2] View Filled invoices")
                            print(" 3] View All Invoices\n")
                            try:
                                selection = int(input("Choice: " ))
                                break
                            except:
                                print("\nEnter a valid selection\n")
                                
                        getInvoices(selection)
                        
                    if(choice == 7):
                        os.system('reset || cls')
                else:
                    currentStaff = Staff(username)
                    mainMenu()
                    while True:
                        try:                
                            choice = int(input("Choice: "))
                            if choice < 1 or choice > 5:
                                raise Exception()
                            break
                        except:
                            print("\nInvalid Selection\n")
                            mainMenu()
                    if choice == 5:
                        #LOG OUT
                        logout()       
                        break      
                    if choice == 1:
                        search(input("\nEnter the search query: "))
                        
                    if choice == 2:
                        currentStaff.createOrder()
                        
                    if choice == 3:
                        currentStaff.viewOrders(username)  
                        
                                            
                    if choice == 4:
                        os.system('reset || cls')
        else:
            print("Failed to login\n")
