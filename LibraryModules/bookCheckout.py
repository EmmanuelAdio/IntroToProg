#Emmanuel Adio - F229639
#bookcheckout module for checkin gbooks out of the library system.
#import the database module
from database import *
from tkinter import *

def BookReservation(MemberID,BookID):
    """
    This is the function that will be used to reserve books in the library.

    MemberID(String) = four digit string number that represents teh ID of a member
    """
    BookID = str(BookID)
    if Check_Valid_BookID(BookID):
        #collect the history of the book
        history = Collect_BookHistory(BookID)
        #collect the book info to put into the reservation information.
        BookTitle = Collect_Book_Title(BookID)
        date = Today()
        ReservationInfo = [BookID,BookTitle,MemberID,date,"","","Reserved"]
        #make sure the last logging of the Book says unavailable
        if history[-1][6] == "Unavailable":
            AppendFile("Logfile.txt",ReservationInfo)
            return "Making Reservation..."
        else:
            return "Reservation Not Possible, Book (%s)%s already reserved"%(BookID,Collect_Book_Title(BookID))
    else:
        return "Invalid BookID"
        


def MakeCheckout(MemberID,BookID):
    """
    This Function creates a record of a book being checked out, this function assumes that the book is already available.
    or is being checkout out by the first person that reserved it.

    memberID(String) = the four digit striong number that represents the member that is checking out the boko
    BookID(String) = the ID of the book that is being check out
    """
    BookID = str(BookID)
    if Check_Valid_BookID(BookID) == False:
        return "Cannot check out Invalid Book"
    history = Collect_BookHistory(BookID)
    #ReservationList = Collect_Reservations(history)
    BookTitle = Collect_Book_Title(BookID)
    CheckoutInfo = ["","","","","","",""]
    #if the book is available and the member checking out the book did not originally reserved then make a new record for the book.
    if history[-1][6] == "Available" or history == []:
        CheckoutInfo[0] = BookID
        CheckoutInfo[1] = BookTitle
        CheckoutInfo[2] = MemberID
        CheckoutInfo[3] = ""
        CheckoutInfo[4] = Today()
        CheckoutInfo[5] = ""
        CheckoutInfo[6] = "Unavailable"
        AppendFile("Logfile.txt",CheckoutInfo)
    #if the book is reserved and the member checking out the book is the first to reserve the book.
    #change the log in history for the item.
    elif history[-1][6] == "Reserved" and history[-1][2] == MemberID:
        history[-1][4] = Today()
        history[-1][6] = "Unavailable"
        UpdateLogFile(BookID,history)
    else:
        return "Error"

def BookCheckout(MemberID, BookID):
    """
    This is the main function for Checking out books in the system

    MemberID(String) = a four digit string number that represents a member's ID
    BookID(String) = A two digit string number that represents a a Book ID
    """
    #collect the book history, so if book is unavalable we can get the member id.
    history = Collect_BookHistory(BookID)
    #collect a list in chronilogical order if all the people that have reserved the book
    ReservedBy = []#Collect_Reservations(history)
    #display if the book is reserved or currently taken by any members
    message = ""
    for log in history:
        if log[6] == "Reserved":
            message += "This book is reserved by "+log[2]+"\n"
            ReservedBy.append(log[2])
        elif log[6] == "Unavalable":
            message += "This book is currently being borrowed by "+log[2]+"\n"

    if Check_Valid_BookID(BookID):
        #display the book that we are checkingout's information
        message += "\n"
        message += DisplayBook(BookID)
        message += "\n"
        #if book status is already unavailable stop the check out!
        if BookStatus(BookID) == "Unavailable":
            return message + "This book is Unavailable!!\n0"
                
        elif BookStatus(BookID) == "Reserved":
            if MemberID != ReservedBy[0] or (history[-2][6] == "Unavailable" and history[-1][6] == "Reserved"):
                return message + "\nThis book is already Reserved! Sorry!\n1"
            elif (MemberID == ReservedBy[0]):
                update = ["","","","","","","Unavailable"]
                history.append(update)
                MakeCheckout(MemberID,BookID)
                return message + "You resered this book. Checkout Successful\n2"
        elif BookStatus(BookID) == "Available":
            update = ["","","","","","","Unavailable"]
            history.append(update)
            message += "This book is Available. checkout Successful\n2"
            MakeCheckout(MemberID,BookID)
    else:
        message += "The Book you entered is not a valid book\n3"
    return message

#these are what the numbers at teh end mean they are for the GUI when posting messages.
#0 - means book is unavailable but not reserved
#1 - means book is unavailable and book is reserved
#2 - means the checkout was successful
#3 - means the book is invalid

if __name__ == "__main__":
    #only valid memberids will be passed to the functions so no need to test that
    #Test bookReservation
    #valid enrty
    print(BookReservation("1234","01"))
    #invalid entry
    print(BookReservation("1234",46))
    print(BookReservation("1234","46"))

    #test BookCheckout
    #valid enrty
    print(MakeCheckout("1234","01"))
    #invalid entry
    print(MakeCheckout("1234",46))
    print(MakeCheckout("1234","46"))

    #test BookCheckout
    #valid enrty
    print(MakeCheckout("1234","01"))
    #invalid entry
    print(MakeCheckout("1234",46))
    print(MakeCheckout("1234","46"))



