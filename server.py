import os
import getpass
#import sqlite3
import requests
from flask import Flask, request, jsonify


#VARIABLES
#db = sqlite3.connect("cmac.db").cursor()





#FUNCTIONS
def login(idnum, password):
    global db
    for i in db.tables["accounts"]:
        if dict(i)["id"] == idnum and dict(i)["password"] == password:
            return 1
    return 0

def finditem(query, sorting):
    global db
    results = []
    query = query['query'][0]
    for i in db.tables["items"]:
        if query in dict(i)["name"]:
            results.push(dict(i)["name"])
    if sorting == 123:
        results.sort()
    else:
        results.sort(reverse=True)
    return results




#CLASSES
        
class Database:
    def __init__(self):
        self.tables = {"accounts":[{"id":"admin", "password":"password"}], "invoices":[], "items":[]}
          
    def addItem(self, item):
        self.tables["items"].append(item)
        
    def removeItem(self, itemIndex):
        self.tables["items"][itemIndex] = ""
        
    def searchForItem(self, item):
        results = []
        for i in self.tables["items"]:
            if item in i.name:
                results.append(i)
        return results
        
    def addInvoice(self, invoice):
        self.tables["invoices"].append(invoice)

class Item:
    def __init__(self, id, name, quantity):
        self.id = id
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


#SERVER
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    return "This is the home page"

@app.route('/login', methods=['GET','POST'])
def loginuserin():
    global isLoggedIn
    print(request.form)
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
    query = (dict(request.args))
    print(request.raw._original_response.fp.raw._sock.getpeername()[0])
    result = finditem(query, 123)
    #~ if len(result):
        #~ return "no results found"
    #~ return result
    return "This is the search page"  
    

@app.route('/invoice', methods=['GET','POST'])
def invoice():
    return "This is the invoice page"
    
@app.route('/invoice', methods=['GET','POST'])
def addItem():
    return "This is the invoice page"
    

if __name__ == "__main__":
    db = Database()
    #print(db.__dict__)
    #print(db.tables)
    #db.showdb()
    #print(db.db)
    app.debug = True
    app.run(host='127.0.0.1', port=4000)


    

