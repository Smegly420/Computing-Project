#devil in i syn flip


import sys, uuid, hashlib, re, sqlite3 #imports python modules
from PyQt5 import QtCore, QtGui, uic #imports modules from pyqt5
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5 import QtWidgets 
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QComboBox, QTextEdit 



mainWin = uic.loadUiType("mainScreen.ui")[0]
loginWin = uic.loadUiType("loginScreen.ui")[0]
signWin = uic.loadUiType("signupScreen.ui")[0]
dbWin = uic.loadUiType("dbScreen.ui")[0]
popupWin1 = uic.loadUiType("popupScreen1.ui")[0]
popupWin2 = uic.loadUiType("popupScreen2.ui")[0]
popupWin3 = uic.loadUiType("popupScreen3.ui")[0]


class PopUpWindow1(QtWidgets.QMainWindow, popupWin1):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)

class PopUpWindow2(QtWidgets.QMainWindow, popupWin2):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)

class PopUpWindow3(QtWidgets.QMainWindow, popupWin3):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
    

class LogInWindow(QtWidgets.QMainWindow, loginWin):
    
    def __init__(self): #constructor for window class
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self) #initiates UI using UI file
        self.loginBtn.clicked.connect(self.login) #when login button is clicked, login function runs
        self.backBtn.clicked.connect(self.back) #when back button is clicked, back function runs

    def login(self):
        enteredUsername = self.userNameTxt.toPlainText() #these take the text entered into the username and password boxes
        enteredPassword = self.passwordTxt.toPlainText() #and store them in variables
        passwordRegEx = re.search(r'''[!"£$%^&*():@~;'#\[\]{}<>?,.\\\/¬`]''',enteredPassword) #searches enteredPassword for
                                                                                              #special symnbols that I dont want
        #if passwordRegEx: #if special symbols are found in the variable
            #print("1")

       # else: #anything else
        conn = sqlite3.connect("Main_Program_Database.db") #connects to database
        cur = conn.cursor() #combines connection with cursor function
        sqlSearchUserStatemnet = "SELECT Username FROM UserInfo WHERE Username = :enteredUsername" #stores sql statement in variable
        cur.execute(sqlSearchUserStatemnet, {"enteredUsername": enteredUsername}) #executes the statement
        usernameInDatabase = cur.fetchone() #fetches username from database if it exists

        if usernameInDatabase:
            sqlSearchSaltStatement = "SELECT Salt FROM UserInfo WHERE Username = :enteredUsername" #stores sql statement in a variable
            cur.execute(sqlSearchSaltStatement, {"enteredUsername": enteredUsername}) #executes the statement using enteredUsername variable
            salt = cur.fetchone()[0] #finds salt in the database that matches the user
            hashedPassword = hashlib.sha256(salt.encode()+enteredPassword.encode()).hexdigest() #combines the salt and password and hashes it
            sqlSearchPassStatement = "SELECT HashedPassword FROM UserInfo WHERE Username = :enteredUsername" #stores sql statement in a variable
            cur.execute(sqlSearchPassStatement, {"enteredUsername": enteredUsername}) #executes the statement using enteredUsername variable
            hashedDBPassword = cur.fetchone()[0] #retrieves hashed password from database
                
            if hashedDBPassword == hashedPassword: #compares the passwords, if they match, runs if statement
                self.hide()
                self.newWindow = MainMenuWindow()
                self.newWindow.show()
            else: #if anything else, runs else
                self.newWindow = PopUpWindow1()
                self.newWindow.show()

        else: #if anything else, runs else
            self.newWindow = PopUpWindow1()
            self.newWindow.show()

    def back(self): #function for back button
        self.hide() #closes current login window
        self.newWindow = MainMenuWindow() #assigns class to an attribute
        self.newWindow.show() #opens mainmenu window
    


class SignUpWindow(QtWidgets.QMainWindow, signWin):

    def __init__(self): #contructor for window class
        QtWidgets.QMainWindow.__init__(self) 
        self.setupUi(self) #initiates UI using UI file
        self.signBtn.clicked.connect(self.signUp) #when signup button is clicked, sigUp function runs
        self.backBtn.clicked.connect(self.back) #when back button is clicked, back function runs

    def signUp(self):
        enteredUsername = self.userNameTxt.toPlainText()            #
        enteredPassword = self.enteredPasswordTxt.toPlainText()     #stores user input in variables
        reEnteredPassword = self.reEnteredPasswordTxt.toPlainText() #
        userNameRegEx = re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$",enteredUsername) 
        #compares enteredUsername to the regular expression

        if not userNameRegEx: #compares enteredUsername to the regualar expression
            self.newWindow = PopUpWindow2()
            self.newWindow.show()

        else: #anything else
            conn = sqlite3.connect("Main_Program_Database.db") #connects to the database
            cur = conn.cursor() #combines connection with cursor function
            sqlSearchUserStatemnet = "SELECT Username FROM UserInfo WHERE Username = :enteredUsername" #stores sql statement in a variable
            cur.execute(sqlSearchUserStatemnet, {"enteredUsername": enteredUsername}) #executes sql statement using variable enteredUsername
            usernameInDatabase = cur.fetchone() #contains the result in a variable

            if not usernameInDatabase: #if the username isnt in the database
                salt = uuid.uuid4().hex #stores uuid in a variable
                hashedP = hashlib.sha256(salt.encode()+enteredPassword.encode()).hexdigest() #sets value of hashedP to the salt hashed password    
                sqlInsertStatement = "INSERT INTO UserInfo VALUES (:Username, :HashedPassword, :Salt)" #stores sql statement in a variable

                cur.execute(sqlInsertStatement, {"Username": enteredUsername, "HashedPassword": hashedP, "Salt": salt}) #executes sql statemnet using variables
                conn.commit() #commit
                self.newWindow = MainMenuWindow()
                self.newWindow.show()

            else: #anything else
                self.newWindow = PopUpWindow3()
                self.newWindow.show()

    def back(self):
        self.hide()
        self.newWindow = MainMenuWindow()
        self.newWindow.show()

class DbWindow(QtWidgets.QMainWindow, dbWin):

    def __init__(self): #constructor
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self) #initiates UI using UI file
        self.backBtn.clicked.connect(self.back) #when back button is clicked, run back function
        self.customerInfoBtn.clicked.connect(self.customerInfo) #when customerInfo  buutton is clicked, run customerInfo function
        self.productInfoBtn.clicked.connect(self.productInfo) #when productInfo button is clicked, run productInfo funtion
        self.errorInfoBtn.clicked.connect(self.errorInfo) #when errorInfo button is clicked, run errorInfo function
        self.createReportBtn.clicked.connect(self.createReport) #when create report button is clicked, run createReport function
        self.col1Lbl.adjustSize()
        self.col2Lbl.adjustSize()
        self.col3Lbl.adjustSize()
        self.col4Lbl.adjustSize()
        self.col5Lbl.adjustSize()
        self.col6Lbl.adjustSize()
        self.backBtn.adjustSize()
        self.customerInfoBtn.adjustSize()
        self.productInfoBtn.adjustSize()
        self.errorInfoBtn.adjustSize()
        self.createReportBtn.adjustSize()
       

   
    def customerInfo(self):
        self.col1Lbl.setText("Customer ID") #
        self.col2Lbl.setText("First Name")  #
        self.col3Lbl.setText("Last Name")   #prints the column names in labels
        self.col4Lbl.setText("Address")     #
        self.col5Lbl.setText("Post Code")   #
        self.col6Lbl.setText("Return ID")   #

        conn = sqlite3.connect("Main_Program_Database.db") #connects to the database
        cur = conn.cursor() #combines connection with cursor function

        sqlDisplayStatement = "SELECT * FROM CustomerInfo" #stores sql statement in variable
        cur.execute(sqlDisplayStatement) #executes sql statement

        columnResults = cur.fetchall() #stores results from sql statement in variable columnResults


        finalString = "" #is the variable that gets printed into the text box
        for x in range(len(columnResults)): #creates a for loop the lenght of the amount of items from the sql statement
            string1 = str(columnResults[x][0]) #takes the item from the first set of data in columnResults
            finalString = finalString + string1 +"\n" #combines string 1 with finalString with a line space

            self.col1Txt.setPlainText(finalString) #prints finalString into the column on the GUI

        finalString = ""
        for x in range(len(columnResults)):
            string1 = str(columnResults[x][1])
            finalString = finalString + string1 +"\n"

            self.col2Txt.setPlainText(finalString)

        finalString = ""
        for x in range(len(columnResults)):
            string1 = str(columnResults[x][2])
            finalString = finalString + string1 +"\n"

            self.col3Txt.setPlainText(finalString)

        finalString = ""
        for x in range(len(columnResults)):
            string1 = str(columnResults[x][3])
            finalString = finalString + string1 +"\n"

            self.col4Txt.setPlainText(finalString)

        finalString = ""
        for x in range(len(columnResults)):
            string1 = str(columnResults[x][4])
            finalString = finalString + string1 +"\n"

            self.col5Txt.setPlainText(finalString)

        finalString = ""
        for x in range(len(columnResults)):
            string1 = str(columnResults[x][5])
            finalString = finalString + string1 +"\n"

            self.col6Txt.setPlainText(finalString)
        

    def productInfo(self):
        self.col1Lbl.setText("SKU")
        self.col2Lbl.setText("Name")
        self.col3Lbl.setText("Quantity") 
        self.col4Lbl.setText("Price")
        self.col5Lbl.setText("Description")
        self.col6Lbl.setText("")

        conn = sqlite3.connect("Main_Program_Database.db")
        cur = conn.cursor() 

        sqlDisplayStatement = "SELECT * FROM ProductInfo"
        cur.execute(sqlDisplayStatement)

        columnResults = cur.fetchall() 
        print(columnResults)

        finalString = ""
        for x in range(len(columnResults)):
            string1 = str(columnResults[x][0])
            finalString = finalString + string1 +"\n"

            self.col1Txt.setPlainText(finalString)

        finalString = ""
        for x in range(len(columnResults)):
            string1 = columnResults[x][1]
            string2 ="""%s"""%(string1)
            finalString = finalString + string2 +"\n"

            self.col2Txt.setPlainText(finalString)

        finalString = ""
        for x in range(len(columnResults)):
            string1 = columnResults[x][2]
            string2 ="""%s"""%(string1)
            finalString = finalString + string2 +"\n"

            self.col3Txt.setPlainText(finalString)

        finalString = ""
        for x in range(len(columnResults)):
            string1 = columnResults[x][3]
            string2 ="""%s"""%(string1)
            finalString = finalString + string2 +"\n"

            self.col4Txt.setPlainText(finalString)

        finalString = ""
        for x in range(len(columnResults)):
            string1 = str(columnResults[x][4])
            finalString = finalString + string1 +"\n"

            self.col5Txt.setPlainText(finalString)
       
    def errorInfo(self):
        self.col1Lbl.setText("Return ID") 
        self.col2Lbl.setText("SKU") 
        self.col3Lbl.setText("Customer ID") 
        self.col4Lbl.setText("Type of Error") 
        self.col5Lbl.setText("Date of Return") 
        self.col6Lbl.setText("")

        conn = sqlite3.connect("Main_Program_Database.db")
        cur = conn.cursor() 

        sqlDisplayStatement = "SELECT * FROM ErrorInfo"
        cur.execute(sqlDisplayStatement)

        columnResults = cur.fetchall() 
        print(columnResults)

        finalString = ""
        for x in range(len(columnResults)):
            string1 = str(columnResults[x][0])
            finalString = finalString + string1 +"\n"

            self.col1Txt.setPlainText(finalString)

        finalString = ""
        for x in range(len(columnResults)):
            string1 = str(columnResults[x][1])
            finalString = finalString + string1 +"\n"

            self.col2Txt.setPlainText(finalString)

        finalString = ""
        for x in range(len(columnResults)):
            string1 = str(columnResults[x][2])
            finalString = finalString + string1 +"\n"

            self.col3Txt.setPlainText(finalString)

        finalString = ""
        for x in range(len(columnResults)):
            string1 = str(columnResults[x][3])
            finalString = finalString + string1 +"\n"

            self.col4Txt.setPlainText(finalString)

        finalString = ""
        for x in range(len(columnResults)):
            string1 = str(columnResults[x][4])
            finalString = finalString + string1 +"\n"

            self.col5Txt.setPlainText(finalString)
       
    def createReport(self):
        pass

    def back(self):
        self.hide()
        self.newWindow = MainMenuWindow()
        self.newWindow.show()


class MainMenuWindow(QtWidgets.QMainWindow, mainWin):

    def __init__(self): #constructor for window class
        QtWidgets.QMainWindow.__init__(self) 
        self.setupUi(self) #initiates UI using UI file
        self.loginBtn.clicked.connect(self.logIn) #when logIn button is clicked, logIn functino runs
        self.signUpBtn.clicked.connect(self.signUp) #when signUp button is clicked, signUp function runs
        self.databaseBtn.clicked.connect(self.database) #when database button is clicked, database function runs
        self.exitBtn.clicked.connect(self.exit) #when exit button is clicked, exit function runs
        self.statusLbl = self.statusLbl.text() #displays login status as a label

    def logIn(self): #logIn function
        self.hide() #hides mainmenu window
        self.newWindow = LogInWindow() 
        self.newWindow.show() #runs code for logIn screen

    def signUp(self): #signUp function
        self.hide() #hides mainmenu window
        self.newWindow = SignUpWindow()
        self.newWindow.show() #runs code for signUp screen

    def database(self):
        self.hide() #hides mainmenu window
        self.newWindow = DbWindow()
        self.newWindow.show() #runs code for database screen 
          
    def exit(self): #exit function
        self.hide() #hides mainmenu window
        sys.exit() #exits program

class User():

    def __init__(self):
        self.loginStatus = ""
        self.allowAccess = False

    def userClear(self):
        self.loginStatus = ""
        self.allowAccess = False





app = QtWidgets.QApplication(sys.argv)

mainWin = MainMenuWindow()
mainWin.show()

#signupWin = SignUpWindow()
#signupWin.show()

#loginWin = LogInWindow()
#loginWin.show()

#dbWin = DbWindow()
#dbWin.show()

app.exec_()


        