import os
import getpass
#import sqlite3
import requests
from flask import Flask, request, jsonify
import ast


#VARIABLES
#db = sqlite3.connect("cmac.db").cursor()




#CLASSES
        
class Database:
    def __init__(self):
        self.tables = {"accounts":[{"id":"admin", "password":"password"}], "invoices":[], "items":[{"name": "pen", "quantity": 3}]}
          
    def addItem(self, item):
        self.tables["items"].append(item)
        return True
        
    def removeItem(self, itemName):
        for i in range(len(self.tables["items"])):
            if self.tables["items"][i]["name"] == itemName:
                self.tables["items"].pop(i)
                return True
        return False
        
    def searchForItem(self, item):
        item = item.lower()
        results = []
        for i in self.tables["items"]:
            if item in i["name"].lower():
                results.append(i["name"])
        results.sort()
        return str(results)
    
    def addInvoice(self, invoice):
        self.tables["invoices"].append(invoice)
        return True



class Item:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity
    
    def editItemName(self, name):
        self.name = name
        
    def editItemQuantity(self, quantity):
        self.quantity = quantity


class UserAccount:
    def __init__(self, id, password):
        self.id = id
        self.password = password



class Employee:
    def __init__(self, firstname, lastname, id):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname



class Administrator(Employee):
    pass
    def viewInvoice(self, selection):
        global db
        unfilledInvoices = []
        filledInvoices = []
        for i in db.tables["invoices"]:
            if(i["filled"] == False):
                unfilledInvoices.append(i)
            else:
                filledInvoices.append(i)    
        if(selection == 1 or selection > 3):
            #SELECTION 1 IS THE DEFAULT SELECTION, RETURN ALL UNFILLED INVOICES
            return str(unfilledInvoices)
        if(selection == 2):
            #SELECTION 2 RETURNS ALL FILLED INVOICES
            return str(filledInvoices)
        if(selection == 3):
            #SELECTION 3 RETURNS ALL INVOICES
            return str(unfilledInvoices + filledInvoices)
    
    def removeAccount(self, accountId):
        global db
        for i in range(len(db.tables["accounts"])):
            if(db.tables["accounts"][i]["id"] == accountId):
                db.tables["accounts"].pop(i)
                return True
        return False
                
                
        
    def addAccount(self, accountId):
        global db
        accountId = accountId.lower()
        for i in db.tables["accounts"]:
            if i["id"].lower() == accountId:
                return False
        db.tables["accounts"].append(accountId)
        return True
        
        
        
        
        
    



#FUNCTIONS
def login(idnum, password):
    global db
    for i in db.tables["accounts"]:
        if dict(i)["id"] == idnum and dict(i)["password"] == password:
            return 1
    return 0

    
    
    
    
    
#SERVER
app = Flask(__name__)



@app.route('/', methods=['GET','POST'])
def index():
    return "This is the home page"





@app.route('/login', methods=['GET','POST'])
def loginuserin():
    global isLoggedIn
    #print(request.form)
    if(login(request.form['id'], request.form['password'])):
        isLoggedIn = True
        return '1'
    else:
        return '0'
    #URL
    #http://127.0.0.1:4000/?login=username&password=password
    #FOR GET REQUESTS
    #~ print (dict(request.args))
    #~ #FOR POST REQUESTS
    #~ print (dict(request.form))     
    #~ return "This is the login page"
    
 
 
 
    
@app.route('/register', methods=['GET','POST'])
def register():
    return "This is the register page"
    





@app.route('/search', methods=['GET','POST'])
def search():
    query = dict(request.args)['query'][0]
    result = db.searchForItem(query)
    return result
    
    
    
    
    

@app.route('/additem', methods=['GET','POST'])
def additem():
    global db
    r = dict(request.args)['item']
    item = ""
    if len(r) == 0:
        return "no items provided"
    for i in r:
        item = ast.literal_eval(i)
        print(item["name"])
        if(len(ast.literal_eval(finditem(item["name"]))) > 0):
            return "Item not added. It already exists!"
        else:
            db.addItem(item)
    return "Item added successfully"



@app.route('/deleteitem', methods=['GET','POST'])
def deleteitem():
    global db
    try:
        print(dict(request.args)['item'][0])
        db.removeItem(dict(request.args)['item'][0])
        return "The item has successfully been removed"
    except Exception as exp:
        print(exp)
        return "An error occurred during the deletion process"



@app.route('/viewinvoices', methods=['GET','POST'])
def viewinvoices():
    try:
        r = dict(request.args)['choice']
        if(choice == 3):
            return adm.viewInvoice(3)
        elif(choice == 2):
            return adm.viewInvoice(2)
        else:
            return adm.viewInvoice(1)
    except:
        return "An error occured while performing this action"






    

if __name__ == "__main__":
    db = Database()
    adm = Administrator("Sheree", "Austin", "admin")
    item = Item("pen", 3)   
    #~ print(item.__dict__)
    #print(db.__dict__)
    #print(db.tables)
    #db.showdb()
    #print(db.db)
    app.debug = True
    app.run(host='127.0.0.1', port=4000)


    

