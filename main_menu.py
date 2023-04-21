#Emmanuel Adio - F229639
#this is my program that will perform the main menu of the library system THE CORE OF THE COURSEWORK!
import sys
sys.path.append("LibraryModules")
from LibraryModules.database import *
from LibraryModules.bookSearch import *
from LibraryModules.bookReturn import *
from LibraryModules.bookCheckout import *
from LibraryModules.bookSelect import *

#import the tkinter modules. that we will need!
from tkinter import *
from tkinter import ttk
import time

def HideGraphButtons():
    """
    this function highes teh buttons that show the graphs
    """
    ShowGenreGraphBtn.pack_forget()
    ShowActivityGraphBtn.pack_forget()
    
def ShowGraphButtons():
    """
    thsi shows teh buttons taht show the graphs
    """
    ShowGenreGraphBtn.pack(padx = 10, pady = 10, side = LEFT)
    ShowActivityGraphBtn.pack(padx = 10, pady = 10, side = LEFT)

def CloseTab(closing):
    """
    This function closes the tab that the program is currently on

    closeing - name of teh fram that is to be closes
    """
    system.hide(closing)

def Check_valid_member(memberID):
    """
    This function just checks that the  memebr ID enters by the user is valid 

    memberID(String)  - representing the ID numebr of a memebr in teh library.
    """
    try:
        if 1000 <= int(memberID) <= 9999:
            errormessage.configure(text = "Welcome "+memberID)
            MainMenuGUI()
            system.hide(memberIDTab)
        else:
            errormessage.configure(text = "ERROR!!! \n please enter a valid ID between 1000 and 9999")
    except:
        errormessage.configure(text = "ERROR!!! \n please enter a valid ID between 1000 and 9999")
        

def configureSearch(value):
    """
    this is what happends when the search book button has been pressed!
    """
    srchResult.delete("1.0",END)
    srchEntry.delete(0,END)

    srchResult.insert("1.0",BookSearch(value))

def BookSearchGUI():
    """
    this what happends when the menu option search book has been picked.
    """
    system.add(searching, text = "Book Search") 
    system.select(searching)


def MakeReservation(MemberID,BookID):
    """
    this is what happend when teh make reservation button has been pressed.
    """
    result = BookReservation(MemberID,BookID)
    checkoutResult.configure(text = result)
    #remove the reservation button to stop people making multiple reservations on the same book.
    reservation.pack_forget()
    CheckoutEntry.delete(0,END)

def configureCheckout(memberID,BookID):
    """
    this is what happens when the check out button has been pressed

    MemberID - the ID of the 
    """
    reservation.pack_forget()
    checkoutText.delete("1.0",END)
    if BookID != "":
        result = BookCheckout(memberID,BookID)
    else:
        result = "That is an invalid book"
        checkoutText.insert("1.0",result)
        checkoutResult.configure(text = "Try again...")

    if result[-1] == "2":
        checkoutText.insert("1.0",result)
        checkoutResult.configure(text = "The book Was sucessfully checked out\nPlease do not try and checkout the same book twice\n it will cause an error")
    elif result[-1] == "0":
        checkoutText.insert("1.0",result)
        checkoutResult.configure(text = "The book is Unavailable, but can be reserved")
        reservation.pack(padx = 10, pady = 10,side = BOTTOM)
    elif result[-1] == "1":
        checkoutText.insert("1.0",result)
        checkoutResult.configure(text = "The book is Unavailable (Cannot be reserved)")
    elif result[-1] == "3":
        checkoutText.insert("1.0",result)
        checkoutResult.configure(text = "Try again...")
    else:
        checkoutResult.configure(text = "Error")


def BookCheckoutGUI():
    """
    this is what happens when teh check out menu option has been chosen
    """
    #system.add(memberIDTab,text = "Member ID")  = this was removed as it leaves code open to being crashed!!
    system.add(checkout, text = "Book Checkout")
    system.select(checkout)


def ConfigureBookReturn(BookID):
    """
    this is what happens when teh return book button has been pressed

    bookID  - 2 digit string of the id of the book the user is trying to return
    """
    returnEntry.delete(0,END)
    result = BookReturn(BookID)
    returnResult.configure(text = result)

def BookReturnGUI():
    """
    this is what happens when the return menu option has been selceted
    """
    #system.add(memberIDTab,text = "Member ID")  = this was removed as it leaves code open to being crashed!!
    system.add(returning, text = "Book Return")
    system.select(returning)

def GetInfo(Budget,year):
    """
    this is what happens when teh get information in the book selct has been pressed
    get the text information of the library stats
    """
    try:
        if year == "":
            year = Today()
            year = (int(year[6:]) - 1)
            year = str(year)
        clearGraphs()
        info = BookSelect(float(Budget),year)
        SelectInfoText.delete("1.0",END)
        SelectInfoText.insert("1.0",info)
        #open up the select graph graph buttons to allow user to have teh graphs displayed to them
        ShowGraphButtons()
    except:

        message = "Please enter a valid Budget"
        SelectInfoText.delete("1.0",END)
        SelectInfoText.insert("1.0",message)

def getGenreGraph(year):
    """
    this is what happens when the get Ganre graph button has been pressed

    year(string) - this is teh year that ahs been specified by the user!
    """
    HideGraphButtons()
    global Graph
    graph = collect_GenreInfo(year)
    Graph = FigureCanvasTkAgg(graph,SelectGraphs)
    Graph.get_tk_widget().pack(padx = 10, pady = 10)


def getYearlyActivityGraph(year):
    """
    this is what happens when the activity graph button is pressed!

    year(string) - this is teh year that ahs been specified by the user!
    """
    if year == "":
        year = Today()
        year = (int(year[6:]) - 1)
        year = str(year)
    HideGraphButtons()
    global Graph
    graph = collect_monthlyInfo(year)
    Graph = FigureCanvasTkAgg(graph,SelectGraphs)
    Graph.get_tk_widget().pack(padx = 10, pady = 10)
    
    
def clearGraphs():
    """
    this is what happens when teh clear graph button it pressed!
    """
    Graph.get_tk_widget().pack_forget()
    HideGraphButtons()



def BookSelectGUI():
    """
    this is shwta happens when the book select option is picked in menu
    """
    system.add(selecting, text = "Book Select")
    system.select(selecting)

def MainMenuGUI():
    """
    thsi is how the menu is Displayed!
    """
    system.add(MainMenu, text = "Main Menu")
    system.select(MainMenu)

def end():
    """
    this is the function that will close teh whole program
    """
    window.destroy()
    exit()
    
    
    


"""
Main GUI CODE!!!
"""
window = Tk()

window.title("Library System")
window.geometry('10000x1600')

system = ttk.Notebook(window)
system.pack(fill = "both", pady = 10, padx = 10, expand = True)

########## Getting the Member ID ##########
memberIDTab = ttk.Frame(system, width = 1000, height = 790)
memberIDTab.pack(fill = "both", expand = True)

errormessage = Label(memberIDTab, text = "please enter a valid Id between 1000 and 9999")
errormessage.pack(padx= 10, pady = 10, expand = True)

memberIDEntry = Entry(memberIDTab, width = 100)
memberIDEntry.pack(padx = 10, pady = 10,expand = True)

memberIDButton = Button(memberIDTab, text = "Submit", command = lambda: Check_valid_member(memberIDEntry.get()))
memberIDButton.pack(padx= 10, pady = 10,)

system.add(memberIDTab,text = "Member ID")

########## Menu System ##########
MainMenu = ttk.Frame(system, width = 1000, height = 790)
MainMenu.pack(fill = "both", expand = True)

MyMenu = Frame(MainMenu)
MyMenu.pack(expand = True)

MenuLbl = Label(MyMenu, text = "Main Menu").pack(padx = 10,pady = 10, side = TOP)

searching = Button(MyMenu, text = "Search", command = lambda:BookSearchGUI(),height = 2, width = 15).pack(padx = 5, pady = 5)

Checkout = Button(MyMenu, text = "Checkout", command = lambda:BookCheckoutGUI(),height = 2, width = 15).pack(padx = 5, pady = 5)

returning = Button(MyMenu, text = "Return", command = lambda:BookReturnGUI(),height = 2, width = 15).pack(padx = 5, pady = 5)

selecting = Button(MyMenu, text = "Select", command = lambda:BookSelectGUI(),height = 2, width = 15).pack(padx = 5, pady = 5)

exiting = Button(MyMenu, text = "Exit", command = lambda:end(),height = 2, width = 15).pack(padx = 5, pady = 5)

system.add(MainMenu,text = "Main Menu")
system.hide(MainMenu)

########## Search System ##########
searching = ttk.Frame(system, width = 1000, height = 790)
searching.pack( expand = True)

srchEntry = Entry(searching,width = 100)
srchEntry.pack(padx = 10, pady = 10)

srchButton = Button(searching, text = "Search Book",  command=lambda: configureSearch(srchEntry.get()))
srchButton.pack(padx = 10,pady = 10)

srchResult = Text(searching)
srchResult.pack(padx = 10,pady = 10)

BackToMenuS = Button(searching, text = "CloseTab", command = lambda: CloseTab(searching))
BackToMenuS.pack(padx = 10,pady = 10, side = BOTTOM)

system.add(searching, text = "Book Search")
system.hide(searching)

########## Checkout System ##########
checkout = ttk.Frame(system, width = 1000, height = 790)
checkout.pack(fill = "both", expand = True)

CheckoutMsg = Label(checkout,text = "What is the book ID of the book you would like to check out?")

CheckoutEntry = Entry(checkout,width = 100)
CheckoutEntry.pack(padx = 10, pady = 10)

CheckoutBtn = Button(checkout, text = "Checkout", command = lambda: configureCheckout(memberIDEntry.get(),CheckoutEntry.get()))
CheckoutBtn.pack(padx = 10, pady = 10)

checkoutResult = Label(checkout, text = "...")
checkoutResult.pack(padx = 10, pady = 10)

checkoutText = Text(checkout)
checkoutText.pack(padx = 10, pady = 10)


reservation = Frame(checkout)
reservation.pack(padx = 10, pady = 10)

RestervationMsg = Label(reservation, text = "If you want to make a reservation for the book Press the button")
RestervationMsg.pack(padx = 10, pady = 10)

ReservationBtn = Button(reservation,text = "Make Reservation", command = lambda: MakeReservation(memberIDEntry.get(),CheckoutEntry.get()))
ReservationBtn.pack(padx = 10, pady = 10)

reservation.pack_forget()

BackToMenuC = Button(checkout, text = "CloseTab", command = lambda: CloseTab(checkout))
BackToMenuC.pack(padx = 10,pady = 10, side = BOTTOM)

system.add(checkout, text = "Book Checkout")
system.hide(checkout)


########## Return System ##########
returning = ttk.Frame(system, width = 1000, height = 790)
returning.pack(fill = "both", expand = True)

returnmsg = Label(returning, text = "Enter the ID of the book you want to return.")
returnmsg.pack(padx = 10, pady = 10)

returnEntry = Entry(returning,width = 100)
returnEntry.pack(padx = 10, pady = 10)

returnBtn = Button(returning, text = "Return Book", command = lambda : ConfigureBookReturn(returnEntry.get()))
returnBtn.pack(padx = 10, pady = 10 )

returnResult = Label(returning, text = "...")
returnResult.pack(padx = 10, pady = 10)

BackToMenuR = Button(returning, text = "CloseTab", command = lambda: CloseTab(returning))
BackToMenuR.pack(padx = 10,pady = 10, side = BOTTOM)

system.add(returning,text = "Book Retun")
system.hide(returning)

########## Select System ##########
selecting = ttk.Frame(system, width = 1000, height = 790)
selecting.pack(fill = "both", expand = True)

SelectInfoCollection = Frame(selecting)
SelectInfoCollection.pack(padx = 10, pady = 10, side = TOP)

selectBudgetlbl = Label(SelectInfoCollection,text = "Enter Budget : £")
selectBudgetlbl.pack(padx = 10, pady = 10, side = LEFT)

selectBudget = Entry(SelectInfoCollection,width = 30)
selectBudget.pack(padx = 10, pady = 10, side = LEFT)

selectyearlbl = Label(SelectInfoCollection, text  = "Enter Year: ")
selectyearlbl.pack(padx = 10, pady = 10, side = LEFT)

selectyear = Entry(SelectInfoCollection,width = 30)
selectyear.pack(padx = 10, pady = 10, side = LEFT)

collectselectInfo = Button(SelectInfoCollection, text =  "Collect Info", command =lambda: GetInfo(selectBudget.get(),selectyear.get()))
collectselectInfo.pack(padx = 10, pady = 10, side = LEFT)

SelectInfo = Frame(selecting)
SelectInfo.pack(padx = 10, pady = 10)

SelectInfolbl = Label(SelectInfo, text = "Book Statistic Infomation")
SelectInfolbl.pack(padx = 10, pady = 10, side = TOP)

SelectInfoText = Text(SelectInfo, height = 10)
SelectInfoText.pack(padx = 10, pady = 10)

ShowGenreGraphBtn = Button(SelectInfo, text = "Show Genres", command = lambda: getGenreGraph(selectyear.get()))
ShowGenreGraphBtn.pack(padx = 10, pady = 10, side = LEFT)

ShowActivityGraphBtn = Button(SelectInfo, text = "Show Activity", command = lambda: getYearlyActivityGraph(selectyear.get()))
ShowActivityGraphBtn.pack(padx = 10, pady = 10, side = LEFT)

HideGraphButtons()

BackToMenuSe = Button(SelectInfo, text = "Close Tab", command = lambda: CloseTab(selecting))
BackToMenuSe.pack(padx = 10,pady = 10, side = LEFT)

clearGraphsBtn = Button(SelectInfo, text = "Clear Graphs", command = lambda: clearGraphs())
clearGraphsBtn.pack(padx = 10,pady = 10, side = LEFT)

SelectGraphs = Frame(selecting)
SelectGraphs.pack(padx = 10 , pady = 10, side = TOP)

graph = plot.figure(figsize = (5,5))
Graph = FigureCanvasTkAgg(graph,SelectGraphs)
Graph.get_tk_widget().pack(padx = 10, pady = 10, side = TOP)
Graph.get_tk_widget().pack_forget()

system.add(selecting,text = "Book Select")
system.hide(selecting)

window.mainloop()

#to allow the user to be able to reenter the memebr Id when checking out a book the program reopens the member ID tab!
#can be closed again by submitting a valid memebr id
#do no try and return book with invalid memebr id - this was removed so do not worry
