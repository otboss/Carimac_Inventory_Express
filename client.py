import os
import getpass
import time
import requests
import ast
import datetime
import sys

########
#CLASSES
########
 
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
        
class UserAccount:
    def __init__(self, id, password):
        self.id = id
        self.password = password   
        
class Employee:
    def __init__(self, id, fname, mname, lname, dob, email, phone, date):
        self.id = id
        self.fname = fname
        self.lname = lname

#~ class Notification:
    #~ def __init__(self, title, message):
        #~ self.title = title
        #~ self.message = message
        
#INVENTORY CLASS NOT INCLUDED, THE INVENTORY WOULD BE AN SQLLITE FILE RATHER THAN A PYTHON OBJECT
#THE SQLLITE FIEL WOULD STORE ALL ACCOUNTS, NOTIFICATIONS, 



isAdmin = False

def printf(format, *args):
    sys.stdout.write(format % args)
    
    
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
            #print(" "+str(j)+"]  " + i["items"][j]["name"] + "   " + str(i["items"][j]["quantity"]))
        print("\n\n\n")

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
                        continue
                        
                    if(choice == 4):
                        deleteItem(input("\nEnter a substring of the item name: "))
                        
                    if(choice == 5):
                        ####CODE HERE###
                        ####CODE HERE###
                        ####CODE HERE###
                        ####CODE HERE###
                        ####CODE HERE###
                        ####CODE HERE###
                        os.system('reset || cls')
                        
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
                                print("\nEnter a selection shown\n")
                                
                        getInvoices(selection)
                        
                    if(choice == 7):
                        ####CODE HERE###
                        ####CODE HERE###
                        ####CODE HERE###
                        ####CODE HERE###
                        ####CODE HERE###
                        ####CODE HERE###
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
                        search(input("\nEnter the search query :"), 123)
                        
                        
                        
                    if choice == 2:
                        #COMPLETE OPTION 2
                        print()
                    if choice == 3:
                        #COMPLETE OPTION 2
                        print()
        else:
            print("Failed to login\n")
