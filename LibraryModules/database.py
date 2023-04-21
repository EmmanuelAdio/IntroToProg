#Emmanuel Adio - F229639
#this is the database module that  uses some important functions, that will be used thought my coursework
import sys
sys.path.append("LibraryModules")
from datetime import *

#this is the list of all the books and book information in the book info file.
def SaveFile(filename):
    """
    This is the function that will be used to open the file and return the to the user a 2D array of the file

    filename(String) = this is the name of the file that will be opened
    """
    #create the list that will store all of the lines and values of the file.
    FileList = []
    try:
        File = open(str(filename),"r")
        #add each line in the list to be a seperate record.
        while True:
            row = File.readline()
            if row != "":
                row = row.strip()
                row = row.split("|")
                row.pop()
                #this is to allow the search function to be able to search the upper version of a book
                row[1] = row[1].upper()
                FileList.append(row)
            else:
                break
        File.close()
        return FileList

    except IOError as e:
        ErrorNo,StrError = e.args
        return "I/O error(%d):%s for %s"%(ErrorNo,StrError,filename)

    except:
        return "Error:  " + filename+" File not Found"


#this is a global variable that stores the book data for the log file and the book file.
BookFile = SaveFile("Book_Info.txt")
LogFile = SaveFile("logfile.txt")

def updateLists():
    """
    This file is used to Update the global lists LogFile and BookFile  when used throughout my program.
    """
    global BookFile
    global LogFile
    #updating the global variables LogFile and Bookfile  used throughout the whole program!
    BookFile = SaveFile("Book_Info.txt")
    LogFile = SaveFile("logfile.txt")

def Collect_Book_Title(ID):
    """
    This function takes the ID of a book that has been passed and returns the Title of that book.

    ID(String) = this is the ID of the book that we want the title off
    """
    ID = str(ID)
    #just search through book file until the book with the same ID is reached and return the title of that book.
    for books in BookFile:
        if books[0] == ID:
            Title = books[1]
            return Title

def Today():
    """
    This is a function that returns today's date in a specific format:
    
    no parameters needed.
    """
    #Just create the date in DD/MM/YYYY format like in the files!!
    today = date.today()
    day = today.day
    month = today.month
    year = today.year
    if day < 10:
        day = "0"+str(day)
    if month < 10:
        month = "0"+str(month)
    today = str(day)+"/"+str(month)+"/"+str(year)
    return today

def Collect_BookHistory(BookID):
    """
    This function returns the log history of a book (so all the members that have borrowed the book)

    BookID(string) = two digit string representing the ID of teh book we want the history off
    """
    history = []
    #check through the log file if the record/log has the same Book ID as BookID append that record to the history list.
    for log in LogFile:
        if (log[0] == BookID):
            history.append(log)
    return history

def Check_Valid_BookID(ID):
    """
    This is the function that iw return a boolean value for if the ID the user enters is valid.

    ID(String) = 2 digit string representing the book ID that we are checking
    """
    Found = False
    #chekc through book file untill you find a book with the same ID at the book ID
    for book in BookFile:
        if book[0] == ID:
            Found = True
            break
    return Found

def ReWriteFile(filename,rewrite):
    """
    This is the function that will rewrite the specified file.
    This function should only be called when updating the log file.

    filename(String) =  The name of the file that will be updated
    rewrite(list) = A 2d list of the records that will go into the file
    """
    try:
        f = open(filename,"w")
        f.seek(0)
        #writing each element of the rewrite list line by line to the file
        for element in rewrite:
            line = ""
            for i in range(0,len(element)):
                line = line + str(element[i]) + "|"
            line = line + "\n"
            f.write(line)
        f.close()
        updateLists()
    except IOError as e:
        #display Error Message when the File that is being entered too does not exist
        ErrorNo,StrError = e.args
        return "I/O error(%d):%s for %s"%(ErrorNo,StrError,filename)

    except:
        return "Error:  " + filename+" File not Found"

def AppendFile(filename,record):
    """
    This is the function to append to the end of a file
    Best to use this function in the book checkout option

    Filename(String) = This is the name of the file taht i will be rewriting.
    record(List) = this is the line that will be appended to the file.
    """
    try:
        f = open(filename,"a")
        line = ""
        #appending the valued in the records list too the file after concatinating all of the values together.
        for elements in record:
            line = line + str(elements) + "|"
        line = line + "\n"
        f.write(line)
        f.close()
        updateLists()

    except IOError as e:
        #display Error Message when the File that is being entered too does not exist
        ErrorNo,StrError = e.args
        return "I/O error(%d):%s for %s"%(ErrorNo,StrError,filename)
    except:
        return "Error:  " + filename+" File not Found"
    

def UpdateLogFile(ID,LogUpdate):
    """
    This is the function that will update the log file when a return has been made.
    This function can only work if it is updating not adding.

    ID(String) = This is the book ID of the book that we are updating.
    """
    updated = []
    #go through the log file replacing all the old recorded with the updated records
    for log in LogFile:
        if (log[0] == ID):
            #as you go through it change the element in the logfile to the first element in the LogUpdate
            #then remove the first element in the LopUpdate and append to the updated list
            #change each field data in the log record to the date in the logupdate first record
            for i in range(0,(len(log)-1)):
                log[i] = LogUpdate[0][i]
            updated.append(LogUpdate[0])
            #delete the updated record from the log update file after it has been put into the updated list
            del LogUpdate[0]
    #print("Updating Log file....")
    ReWriteFile("logfile.txt",LogFile)
    updateLists()

def InFile(Title):
    """
    This function will be use to check that the book record is in the file. a boolean Value.

    Title(String)  = the title of the book that that is being searched for.
    """
    Title = str(Title)
    found = False
    #just check each book in the book file until you find a book with the same title, if u do set found to True
    for Book in BookFile:
        if Title == Book[1]:
            found = True
    return found

def BookStatus(ID):
    """
    This is the function that i will use to get the status(book is Available, reserved or unavailable?)

    ID(String) = the ID of the Book that is being checked.
    """
    ID = str(ID)
    #this will be a list that will stor the previous logs of a book to check the books most recent status
    history = Collect_BookHistory(ID)

    #the final log of the book will be the current status of the book.
    if history != []:
        status = history[-1][6]
        return status 
    else:
        #if there is no histoiry for the book then the book is available
        status = "Available"
    return status
    
def DisplayBook(ID):
    """
    This is a function that displays the infomration of one book using that book's ID

    ID(String) = two digit string tat represents the ID of the book we are trying to display
    """
    ID = str(ID)
    Book = ""
    if not Check_Valid_BookID(ID):
        Book = "The ID, %s, you entered is not of a valid book!"%(ID)
    for book in BookFile:
        if book[0] == ID:
            Book += "\n"
            history = Collect_BookHistory(book[0])
            status = BookStatus(book[0])
            #display any extra ststus information.
            if status != "Available" and status != "Unavailable":
                status = "Reserved" + " By member: " + history[-1][2]
            elif status == "Unavailable":
                status = "Borrowed" + " By member: " + history[-1][2]
            else:
                status = history[-1][6]
            Book += book[0]+":"+book[1]+"(by "+book[2]+")"+"\n"+\
                "Genre: "+book[3]+"\n"+\
                "Purchase Price: "+book[4]+"\n"+\
                "Date Purchased: "+book[5]+"\n"+\
                "Status: "+status
    return Book

            

def DisplayBooks(Title):
    """
    this procedure takes the name of  book and displays all the copies of the book in the library an dall of the books information!

    Title(string) =  the title of the book the user is looking for.
    """
    Title = str(Title)
    Title = Title.upper()
    value = ""
    value = value + "****** "+Title+" ******\n"
    if InFile(Title):
        for book in BookFile:
            if book[1] == Title:
                value = value + "\n"
                history = Collect_BookHistory(book[0])
                status = BookStatus(book[0])
                #display extra book status information
                if status != "Available" and status != "Unavailable":
                    status = "Reserved" + " By member - " + history[-1][2]
                elif status == "Unavailable":
                    status = "Borrowed" + " By member -  " + history[-1][2]
                else:
                    #when the status is available.
                    if status == "Available":
                        status = "Available"
                value = value + book[0]+":"+book[1]+"(by "+book[2]+")"+"\n"+\
                    "Genre: "+book[3]+"\n"+\
                    "Purchase Price: "+book[4]+"\n"+\
                    "Date Purchased: "+book[5]+"\n"+\
                    "Status: "+status + "\n"
        return value
    else:
        value = value + "This book cannot be found."
        return value 
    
def BookGenres():
    """
    This is a function just to create a list of all the genres of books the library has. and returns this list sorted in alphebetical order
    """
    genres = []
    #Search through book fil and append every genre that you come accross to the genre list.
    #ignore all already appended genres.
    for Books in BookFile:
        if Books[3] not in genres:
            genres.append(Books[3])
    genres.sort()
    return genres


if __name__ == "__main__":
    #TestingSveFile
    #invalid
    print(SaveFile(98))
    print(SaveFile("NotReal.txt"))
    #valid
    print(SaveFile("Book_Info.txt"))
    print(SaveFile("logfile.txt"))

    #text Collect_Book_title
    #invalid
    print(Collect_Book_Title(12))
    print(Collect_Book_Title("asfs"))
    print(Collect_Book_Title("-1"))
    print(Collect_Book_Title("26"))
    #valid
    print(Collect_Book_Title("00"))
    print(Collect_Book_Title("01"))
    print(Collect_Book_Title("02"))
    print(Collect_Book_Title("23"))
    print(Collect_Book_Title("24"))

    #Test Today
    print(Today())

    #Test Collect_BookHistory
    #invalid
    print(Collect_BookHistory(12))
    print(Collect_BookHistory("asfs"))
    print(Collect_BookHistory("-1"))
    print(Collect_BookHistory("26"))
    #valid
    print(Collect_BookHistory("00"))
    print(Collect_BookHistory("01"))
    print(Collect_BookHistory("02"))
    print(Collect_BookHistory("03"))
    print(Collect_BookHistory("04"))
    print(Collect_BookHistory("22"))
    print(Collect_BookHistory("23"))
    print(Collect_BookHistory("24"))

    #test Check_Valid_BookID
    #false
    print(Check_Valid_BookID(12))
    print(Check_Valid_BookID("25"))
    print(Check_Valid_BookID("-1"))
    print(Check_Valid_BookID("XYZ"))
    #true
    print(Check_Valid_BookID("00"))
    print(Check_Valid_BookID("11"))
    print(Check_Valid_BookID("12"))
    print(Check_Valid_BookID("13"))
    print(Check_Valid_BookID("14"))

    #test RewriteFile - not going to test  directly
    #check the testing of other modules to see results for this one!

    #test AppendFile - not going to test directly
    #check the testing of other modules to see results for this one!

    #Test UpdateLogFile - no going to test directly
    #check the testing of other modules to see results for this one!

    #Test Infile
    #invalid books
    print(InFile(""))
    print(InFile("116809"))
    print(InFile(333))
    print(InFile("rexy"))
    #valid books
    print(InFile("DUNE"))
    print(InFile("CHARLOTTE'S WEB"))
    print(InFile("JAWS"))
    print(InFile("THE CAT IN THE HAT"))
    print(InFile("WONDER"))


    #Test BookStatus
    #invalid
    print(BookStatus(12))
    print(BookStatus("25"))
    print(BookStatus("-1"))
    print(BookStatus("XYZ"))
    #valid
    print(BookStatus("00"))
    print(BookStatus("11"))
    print(BookStatus("12"))
    print(BookStatus("13"))
    print(BookStatus("14"))

    #Test DisplayBook
    #invalid
    print(DisplayBook(12))
    print(DisplayBook("25"))
    print(DisplayBook("-1"))
    print(DisplayBook("XYZ"))
    #valid
    print(DisplayBook("00"))
    print(DisplayBook("11"))
    print(DisplayBook("12"))
    print(DisplayBook("13"))
    print(DisplayBook("14"))

    #Test DisplayBooks
    #invalid books
    print(DisplayBooks(""))
    print(DisplayBooks("116809"))
    print(DisplayBooks(333))
    print(DisplayBooks("rexy"))
    #valid books
    print(DisplayBooks("DUNE"))
    print(DisplayBooks("CHARLOTTE'S WEB"))
    print(DisplayBooks("JAWS"))
    print(DisplayBooks("THE CAT IN THE HAT"))
    print(DisplayBooks("WONDER"))
    

    #Test BookGenres
    print(BookGenres())












