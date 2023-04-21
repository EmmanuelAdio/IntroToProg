#Emmanuel Adio - F229639
#this will be the module for the search function in my program.
#import the database module
from database import *
from tkinter import *


def BookSearch(Search_For):
    """
    This is the subroutine preforms the tasks for the book search menu option.

    Search_For(String) = this is the the book title that the user is searching for.
    """
    return DisplayBooks(Search_For)

#hello = BookSearch("Dune")
#print(hello)

if __name__ == "__main__":
    #book search texting
    print(BookSearch("DUNE"))
    print(BookSearch("CHARLOTTE'S WEB"))
    print(BookSearch("THE VERY HUNGRY CATERPILLER"))
    print(BookSearch("JINX"))
    print(BookSearch("MATILDA"))
    print(BookSearch("PRIDE AND PREJUDICE"))
    print(BookSearch("TREASURE ISLAND"))
    print(BookSearch("CORALINE"))
    print(BookSearch("BORN A CRIME"))
    print(BookSearch("THE CAT IN THE HAT"))
    print(BookSearch("SIX OF CROWS"))
    print(BookSearch("WONDER"))
    print(BookSearch("TWILIGHT"))
    print(BookSearch("THE SILENT PATIENT"))
    print(BookSearch("THE WOMEN IN BLACK"))
    print(BookSearch("THE VERY HUNGRY CATERPILLER"))
    print(BookSearch("THE HUNGER GAMES"))
    print(BookSearch("RANDOM BOOK"))
