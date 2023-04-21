#Emmanuel Adio - F229639
#this is the book return module that ask the librarian for the books being returned
#import the database module!!!
from database import *
from tkinter import *
    

def BookReturn(BookID):
    """
    the main function for the book return module, this function will be used ot make the changes to the logFile when a book has been returned.
    no need for memebr ID be cause it does not matter who returned the book just as long as a valid book with a valid book ID has been returned.

    BookID(String) = two digit number representing a book
    """
    message = ""
    #this is how the day the book is returned will be saved.
    today = Today()
    #check if the book ID is valid before continuing
    if Check_Valid_BookID(BookID):
        #collect the log history of the member and if the last book 
        BookHistory = Collect_BookHistory(BookID)
        #if the book is already available
        if BookHistory == [] or BookHistory[-1][6] == "Available" or (BookHistory[-1][6] == "Reserved" and BookHistory[-2][6] == "Available"):
            message += "Return Failed\n"
            message += "This Book is already available in the building\n"


        if BookHistory != []:    
            #if this book is reserved change the previous log to available and display who the book is reserved too.
            if BookHistory[-1][6] == "Reserved":
                #display who has the book reserved
                message += "This book is reserved by "+ BookHistory[-1][2]+"\n"
                #make changes to file if book is currently being borrowed
                if BookHistory[-2][6] == "Unavailable":
                    message += "Return Successful\n"
                    BookHistory[-2][6] = "Available"
                    BookHistory[-2][5] = today
                    UpdateLogFile(BookID,BookHistory)
                
            #if the book has been borrowed make it available and set the date to today.
            elif BookHistory[-1][6] == "Unavailable":
                message += "Return Successful\n"
                BookHistory[-1][6] = "Available"
                BookHistory[-1][5] = today
                UpdateLogFile(BookID,BookHistory)
        else:
            message += "ERROR : This book has No History!\n"
    else:
        message += "The book ID is invalid Please Reenter\n"

    return message


if __name__ == "__main__":
    #test bookReturn
    #invalid
    print(BookReturn(12))
    print(BookReturn("asfs"))
    print(BookReturn("-1"))
    print(BookReturn("26"))
    #valid
    print(BookReturn("00"))
    print(BookReturn("01"))
    print(BookReturn("02"))
    print(BookReturn("03"))
    print(BookReturn("04"))
    print(BookReturn("22"))
    print(BookReturn("23"))
    print(BookReturn("24"))