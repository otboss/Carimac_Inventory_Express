import os
import getpass
import requests
from flask import Flask, request, jsonify
import ast



#CLASSES
        
class Database:
    def __init__(self):
        self.tables = {"accounts":[{"id":"admin", "password":"password"}], "invoices":[{"id":1, "items":[{"name": "books", "quantity": 5}, {"name": "staplers", "quantity": 7}], "date":"2018-04-14", "staffIdNum":0, "filled":False}, {"id":2, "items":[{"name": "books", "quantity": 5}, {"name": "staplers", "quantity": 7}], "date":"2018-04-15", "staffIdNum":0, "filled":False}], "items":[{"name": "pen", "quantity": 3}]}
          
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
        
    def getQuantity(self, itemName):
        for i in self.tables["items"]:
            if itemName == i["name"]:
                return i["quantity"]
        return 0


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
    if(login(request.form['id'], request.form['password'])):
        isLoggedIn = True
        return '1'
    else:
        return '0'
 
    
@app.route('/register', methods=['GET','POST'])
def register():
    return "This is the register page"


@app.route('/search', methods=['GET','POST'])
def search():
    global db
    query = dict(request.args)['query'][0]
    result = db.searchForItem(query)
    return result


@app.route('/getaccounts', methods=['GET','POST'])
def getaccounts():
    global db
    accounts = []
    for i in db.tables["accounts"]:
        accounts.append(i["id"])
    return str(accounts)
    
    
@app.route('/getquantity', methods=['GET','POST'])
def getquantity():
    global db
    item = dict(request.args)['name'][0]
    return str(db.getQuantity(item))    
    
@app.route('/addinvoice', methods=['GET','POST'])
def addinvoice():
    global db
    invoice = ast.literal_eval(dict(request.args)['invoice'][0])
    print(invoice)
    db.tables["invoices"].append(invoice)
    return "Invoice added successfully"


@app.route('/addaccount', methods=['GET','POST'])
def addaccount():
    global db
    newUser = UserAccount(dict(request.args)['id'][0], dict(request.args)['password'][0])
    db.tables["accounts"].append(newUser.__dict__)
    return "Account added successfully"
    

@app.route('/deleteaccount', methods=['GET','POST'])
def deleteaccount():
    global db
    index = int(dict(request.args)['id'][0])
    db.tables["accounts"].pop(index)
    return "Account removed successfully"
    

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
        if(len(ast.literal_eval(db.searchForItem(item["name"]))) > 0):
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
    global adm
    try:
        selection = int(dict(request.args)['selection'][0])
        if(selection == 3):
            return str(adm.viewInvoice(3))
        elif(selection == 2):
            return str(adm.viewInvoice(2))
        else:
            return str(adm.viewInvoice(1))
    except:
        return "An error occured while performing this action"
    

if __name__ == "__main__":
    db = Database()
    adm = Administrator("Sheree", "Austin", "admin")
    app.debug = True
    app.run(host='127.0.0.1', port=4000)
    
