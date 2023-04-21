#Emmanuel Adio - F229639
#This is the modue that will be used to select the recommended books
#import the datatbase module
from database import *

#import GUI and Graph libraries(matplotlib and etc)
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plot
import numpy as np

#need to calculate genre budget
#find most popular book
def GenreCounts(year):
    """
    this function collects the occurence of the genres in a given year and returns a list of these occurences.

    year(String) = thsi is the year we want the genre count of  
    """
    year = str(year)
    Genres = BookGenres()
    Counts = []
    for Genres in Genres:
        amount = 0
        #go through the log file collecting book IDs then go through the book file to with those IDs to find the genres of the books with the given book ID
        for logs in LogFile:
            for books in BookFile:
                #if the Book id of the book and the BookID of the log record match and the year in the log records reservation date or teh year in 
                # the log record's chechout date match the year given  increment amount and that will be the genres's count.
                if (logs[0] == books[0]) and (books[3] == Genres) and ((logs[3][6:] == year) or logs[4][6:]== year):
                    amount += 1
        Counts.append(amount)
    return Counts


def collect_GenreInfo(year):
    """
    This is for collect the datat and plotting the graph for the genre information in the file

    year(String) = four didgit string valur representing the year we are collecting the genre information for.
    """
    year = str(year)
    #make a list of all the genres of books that appear in the file.
    Genres = BookGenres()
    Counts = GenreCounts(year)

    #creat plot graph
    GenreGraph = plot.figure(figsize=(8,8), dpi = 100)
    GraphPlotg = GenreGraph.add_subplot(1,1,1)
    GraphPlotg.bar(Genres,Counts)
    GraphPlotg.set_title(year+" Genre Stats")
    GraphPlotg.set_xlabel("Genres")
    GraphPlotg.set_ylabel("No of Activity")

    return GenreGraph

def MonthCount(year,months):
    """
    collects how many times books have been borrowed and/or reserved in a given month to show the activty of books in a month  of a given year

    year(String) = four digit string value representing the year of the data we are looking at.
    month(strig) = two digit string value respresenting months.    
    """
    Counts = []
    for month in months:
        amount = 0
        for logs in LogFile:
            if (logs[3] != "") or (logs[4] != ""):
                #like in the Genrecount function but we want to collect the records with the year and the months in the 
                # reservation date and check out date taht are the same as the montha nd year we are collecting the count off.
                if ((logs[3][6:] == year) and (logs[3][3:5] == month)) or ((logs[4][6:] == year) and (logs[4][3:5] == month)):
                    amount += 1
        Counts.append(amount)
    return Counts
    
def collect_monthlyInfo(Year):
    """
    This function collects all the data for a year in book reservations and book checkouts

    year(String) = a four digit striong representing the year of the data we are looking for.
    """
    Year = str(Year)
    #collect the axis data!
    months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    Counts = MonthCount(Year,months)
    
    #make the graph sub plot values for the graph to be made.
    MGraph = plot.figure(figsize=(8,8), dpi = 100)
    GraphPlotm = MGraph.add_subplot(1,1,1)
    GraphPlotm.plot(months,Counts)
    GraphPlotm.set_title(Year + " Activity")
    GraphPlotm.set_xlabel("Months")
    GraphPlotm.set_ylabel("No of Activity")
    return MGraph


def  Library_book_titles():
    """
    This functions creates a list off all the titles of the books in the library system. and sorts them into alphebetical order!
    """
    BookTitles = []
    #search through the book file appending all new titles tot the list ignoring all already appended list
    for books in BookFile:
        if books[1] not in BookTitles:
            BookTitles.append(books[1])
    BookTitles.sort()
    return BookTitles 



def collect_bookTitle_counts(year):
    """
    this function collects the the number of occurences a book title has in the log file where it has been reserved or checkout
    for a given year. this will be used to calculate the books popularity.

    year(String) = a 4 digit string that will be used to represent 
    """
    counts = []
    BookTitles = Library_book_titles()
    for Title in BookTitles:
        occurence = 0
        for log in LogFile:
            #if it the log recoird has the same book title with the same specfied year number add a increment the occurence
            if (log[1] == Title) and ((log[3][6:] == year) or log[3][6:]== year):
                occurence += 1
        counts.append(occurence)
    return counts


def Get_BookRankings(year):
    """
    this function creates a list of tuples that take two elements the first representing the book number of occurences the book has in the 
    log file and the second element is a string representing the book's title.

    year(string)  = gives us the year we want to know the book rankings of.
    """
    #create a list of book titles parrellel to a list of these book titles occurences
    BookTitles = Library_book_titles()
    BookTitleCounts = collect_bookTitle_counts(year)

    #then zip them up to make a list of tuples
    BookRanking = list(zip(BookTitleCounts, BookTitles))
    BookRanking =sorted(BookRanking,reverse = True)

    return BookRanking
    
def Get_GenreRankings(year):
    """
    This function ranks the genres from most popular to least popular to thn be passed into the distribution of budget calculation.

    year(String) = four digit string that tells us the year we want to collect the genre ranking of.
    """
    #create a list of book titles parrellel to a list of these book titles occurences
    Genres = BookGenres()
    Counts = GenreCounts(year)

    #then zip them up to make a list of tuples
    GenreRanking = list(zip(Counts, Genres))
    GenreRanking =sorted(GenreRanking,reverse = True)

    return GenreRanking


def Most_popular_book_Infocollection(year):
    """
    This is the functiont that i will use to find and return the most popular book's informtation.

    year(String) = four digit string value that tells us the year we want to calculate the distribution of.
    """ 
    BookInfo = ["X","X","X","0","X","X"]
    #get the most populare book
    bookRanking = Get_BookRankings(year)
    (count, Title) = bookRanking[0]
    if count != 0:
        for books in BookFile:
            if books[1] == Title:
                #Book title
                BookInfo[0] = Title
                #Book Author
                BookInfo[1] = books[2]
                #Book Genre
                BookInfo[2] = books[3]
                #Book Price
                BookInfo[3] = books[4]
                #Book occurence
                BookInfo[4] = count
                #new book needed?
                if count >= 5:
                    BookInfo[5] = True
                else:
                    BookInfo[5] = False
    else:
        return BookInfo
    return BookInfo

def calculate_Budget_Distribution(Budget,year):
    """
    This is the function i will be using to calculate how much of the budget will be going to specific genre's of new books

    budget(Real/float) = The amount of money that the librarian has specified as the budget.
    year(String) = a 4 digit string that tells us teh year we want tocalculate the budget distribution off!
    """
    #get the sum of the total activity in the log file for the specified year, i.e get the 
    TotalLogActivity = sum(collect_bookTitle_counts(year))
    #make variable sot stopr the data on ganre's an dtheir amounts
    Genres = []
    amount = []

    #rcoment the most popular books shoudl have another copy bought if teh book activity is higher than 5
    most_popular_book = Most_popular_book_Infocollection(year)
    if most_popular_book[5]:
        Budget = Budget - int(most_popular_book[3])

    #make a variable to stor all the ganre rankings, i.e how mauch activty each ganre has in a given year 
    #sort out this ranking form highest to lowest.
    GenreRankings = Get_GenreRankings(year)


    for elements in GenreRankings:
        (count, Genre) = elements
        if TotalLogActivity != 0:
            #calculate the portion of the Budget that the given genre will have
            GenreBudget = round(((count/TotalLogActivity)*Budget),2)
        else:
            GenreBudget = 0
        Genres.append(Genre)
        amount.append(GenreBudget)

    #distributhion will be a list of tuples
    Distribution = zip(Genres,amount)

    return Distribution

def calculate_Budget_DistributionMessages(Budget,year):
    """
    This is the function i will be using to display if the most popular book needs to have a new copy bought.

    budget(Real/float) = The amount of money that the librarian has specified as the budget.
    year(String) = 4 digit string that represents teh year the user wants teh distribution data of!.
    """
    message = ""

    most_popular_book = Most_popular_book_Infocollection(year)

    #if teh most popular book has more than 5 activity logs then a message needed to be displayed
    if most_popular_book[5]:
        Budget = Budget - int(most_popular_book[3])
        message += "You should buy a new copy of %s which will cost you £%s\n So your remaining budget is : £%r"\
            %(most_popular_book[0],most_popular_book[3],Budget)

    return message

def Get_GenreAverage():
    """
    this gets the mean average price of books in all the genres.
    """
    #stor a list of all genres of books in the library.
    Genres = BookGenres()
    AveragePrices = []
    #take the prices of books in a genre and find the average of those prices
    #by adding up all the prices if books collected and dividing by the number of books in the genre.
    for Genre in Genres:
        count = 0
        TotalPrice = 0
        for book in BookFile:
            if book[3] == Genre:
                TotalPrice = TotalPrice + float(book[4])
                count += 1
        if count != 0:
            mean = TotalPrice / count
        else:
            mean = 0
        mean = round(mean,2)
        AveragePrices.append(mean)
    #make the data from GenreAverage a into dictionary format! 
    GenreAverage = dict(zip(Genres,AveragePrices))
    return GenreAverage

def Get_GenreBookCopies(Budget,year):
    """
    This function gets how many copies of books from each genre should be bought

    budget(Real/float) = The amount of money that the librarian has specified as the budget.
    year(String) = 4 digit string that represents the year
    """
    Genres = BookGenres()
    Budgetdistribution = dict(calculate_Budget_Distribution(Budget,year))
    GenreAverage = Get_GenreAverage()
    copies = []
    for Genre in Genres:
        if GenreAverage[Genre] != 0:
            #do floor division to get the whole number of copies of books in a ganre taht you can buy.
            amount = Budgetdistribution[Genre] // GenreAverage[Genre]
        else:
            amount = 0

        #add the calculated amount and the genres to their respective list.
        amount = round(amount)
        copies.append(amount)
    
    GenreBookCopies = zip(Genres,copies)
    return GenreBookCopies

def Get_remaining(Budget,year):
    """
    Get the remain amount of money from the budget after the recomened copies of books have been bought

    budget(Real/float) = The amount of money that the librarian has specified as the budget.
    year(String) = 4 digit string that represents the year
    """
    Genres = BookGenres()
    Budgetdistribution = dict(calculate_Budget_Distribution(Budget,year))
    GenreAverage = Get_GenreAverage()
    remain = 0
    for Genre in Genres:
        if GenreAverage[Genre] != 0:
            #add the modulous of the values in the Budgetdistributioin and GenreAverage to get the remainder
            remain += (Budgetdistribution[Genre]%GenreAverage[Genre])
    return round(remain,2)


def BookSelect(Budget,year):
    """
    This is the main function for the book select module.
    it just displays the infomations collected from the functions above.

    budget(Real/float) = The amount of money that the librarian has specified as the budget.
    year(String) = 4 digit string that represents the year
    """
    #Genres = BookGenres
    info = ""

    #if the user does not enetr a year use the previous year as year value
    if year == "":
        year = Today()
        year = (int(year[6:]) - 1)
        year = str(year)
        info += "For year "+ year + ":\n"
    else:
        info += "For year "+ year + ":\n"

    if Budget == "":
        Budget = str(0)
    

    #get most popular book display it and some of its information
    Most_popular_book = Most_popular_book_Infocollection(year)
    if Most_popular_book[0] == "X":
        info += "\nNo single most popular book in %s\n\n"%(year)
    else:
        info += "The most popular book is:\n" + \
            Most_popular_book[0] + " by " + Most_popular_book[1]+\
            "\nGenre = " + Most_popular_book[2]+"\n"+\
            "Count = " + str(Most_popular_book[4])+"\n"

    #display if the most populare book should get a new copy
    info += "\n" + calculate_Budget_DistributionMessages(Budget,year) + "\n"

    #display teh money sitribution
    info += "\nYou need to spend:\n"
    Distribution = tuple(calculate_Budget_Distribution(Budget,year))
    for genres in Distribution:
        (Genre, Amount) = genres
        info += "£" + str(Amount) + " on " + Genre + " books\n"     

    #display the coppies needed to be bought
    copies = tuple(Get_GenreBookCopies(Budget,year))
    info += "\nYou should buy:\n"
    for genres in copies:
        (Genre, Amount) = genres
        info += str(Amount) + " copie(s) of new " + Genre + " books \n"
    
    ##display reamaining budget left.
    change = Get_remaining(Budget, year)
    info += "\nYour remaining change will be £" + str(change) + "\n"

    return info

#print(BookSelect(10000,""))

if __name__ == "__main__":
    #Test GenreCount
    #valid
    print(GenreCounts("2021"))
    print(GenreCounts("2020"))
    print(GenreCounts(2022))
    #invalid
    print(GenreCounts(12346))
    print(GenreCounts("123456"))

    #test collect_GenreInfo()
    #valid
    collect_GenreInfo("2021")
    plot.show()
    collect_GenreInfo("2022")
    plot.show()
    collect_GenreInfo("2020")
    plot.show()
    collect_GenreInfo("1234")
    plot.show()
    collect_GenreInfo("asdg")
    plot.show()
    collect_GenreInfo(21)
    plot.show()

    #test Month Counts
    print(MonthCount("2021",["01","02","03","04","05","06","07","08","09","10","11","12"]))
    print(MonthCount("2022",["01","02","03","04","05","06","07","08","09","10","11","12"]))
    print(MonthCount("2020",["01","02","03","04","05","06","07","08","09","10","11","12"]))

    print(MonthCount("1234",["01","02","03","04","05","06","07","08","09","10","11","12"]))
    print(MonthCount("asdf",["01","02","03","04","05","06","07","08","09","10","11","12"]))
    print(MonthCount("",["01","02","03","04","05","06","07","08","09","10","11","12"]))

    #test collect monthly info
    #valid
    collect_monthlyInfo("2021")
    plot.show()
    collect_monthlyInfo("2022")
    plot.show()
    collect_monthlyInfo("2020")
    plot.show()
    collect_monthlyInfo("1234")
    plot.show()
    collect_monthlyInfo("asdg")
    plot.show()
    collect_monthlyInfo(21)
    plot.show()

    #test Library_book_titles
    print(Library_book_titles())

    #test collect_bookTitle_count
    #valid
    print(collect_bookTitle_counts("2021"))
    print(collect_bookTitle_counts("2020"))
    print(collect_bookTitle_counts(2022))
    #invalid
    print(collect_bookTitle_counts(12346))
    print(collect_bookTitle_counts("123456"))

    #test Get_BookRankings
    #valid
    print(Get_BookRankings("2021"))
    print(Get_BookRankings("2020"))
    print(Get_BookRankings(2022))
    #invalid
    print(Get_BookRankings(12346))
    print(Get_BookRankings("123456"))

    #test Get_GenreRankings
    #valid
    print(Get_GenreRankings("2021"))
    print(Get_GenreRankings("2020"))
    print(Get_GenreRankings(2022))
    #invalid
    print(Get_GenreRankings(12346))
    print(Get_GenreRankings("123456"))

    #test most populare book
    #valid
    print(Most_popular_book_Infocollection("2021"))
    print(Most_popular_book_Infocollection("2020"))
    print(Most_popular_book_Infocollection(2022))
    #invalid
    print(Most_popular_book_Infocollection(12346))
    print(Most_popular_book_Infocollection("123456"))

    #test calculate calculate_Budget_Distribution
    #valid
    print(calculate_Budget_Distribution(10000,""))
    print(calculate_Budget_Distribution(10000,"2022"))
    print(calculate_Budget_Distribution(10000,"2020"))
    print(calculate_Budget_Distribution(10000,"2021"))    
    #invalid. the checking for the valid budget number being entered is done before entering this function
    #no need to test it! check GUI results
    print(calculate_Budget_Distribution(10000,"10000"))
    print(calculate_Budget_Distribution(10000,"sdafgt"))
    print(calculate_Budget_Distribution(10000,"aaaaa")) 

    #Test calculate_Budget_DistributionMessages
    #valid
    print(calculate_Budget_DistributionMessages(10000,""))
    print(calculate_Budget_DistributionMessages(10000,"2022"))
    print(calculate_Budget_DistributionMessages(10000,"2020"))
    print(calculate_Budget_DistributionMessages(10000,"2021"))    
    #invalid. the checking for the valid budget number being entered is done before entering this function
    #no need to test it! check GUI results
    print(calculate_Budget_DistributionMessages(10000,"10000"))
    print(calculate_Budget_DistributionMessages(10000,"sdafgt"))
    print(calculate_Budget_DistributionMessages(10000,"aaaaa")) 

    #test Get_GenreAverage
    print(Get_GenreAverage)

    #test Get_GenreBookCopies
    #valid
    print(Get_GenreBookCopies(10000,""))
    print(Get_GenreBookCopies(10000,"2022"))
    print(Get_GenreBookCopies(10000,"2020"))
    print(Get_GenreBookCopies(10000,"2021"))    
    #invalid. the checking for the valid budget number being entered is done before entering this function
    #no need to test it! check GUI results
    print(Get_GenreBookCopies(10000,"10000"))
    print(Get_GenreBookCopies(10000,"sdafgt"))
    print(Get_GenreBookCopies(10000,"aaaaa")) 

    #Test Get_remaining
    #valid
    print(Get_remaining(10000,""))
    print(Get_remaining(10000,"2022"))
    print(Get_remaining(10000,"2020"))
    print(Get_remaining(10000,"2021"))    
    #invalid. the checking for the valid budget number being entered is done before entering this function
    #no need to test it!
    print(Get_remaining(10000,"10000"))
    print(Get_remaining(10000,"sdafgt"))
    print(Get_remaining(10000,"aaaaa")) 

    #Test BookSelect()
    #valid
    print(BookSelect(10000,""))
    print(BookSelect(10000,"2022"))
    print(BookSelect(10000,"2020"))
    print(BookSelect(10000,"2021"))    
    #invalid. the checking for the valid budget number being entered is done before entering this function
    #no need to test it!
    print(BookSelect(10000,"10000"))
    print(BookSelect(10000,"sdafgt"))
    print(BookSelect(10000,"aaaaa")) 
