
# Roll : 71
olympicRecords = [
    # {
    #     "year": 2024,
    #     "winning_country": "United States",
    #     "total_medals_won": "250",
    #     "my_country_played": True, 
    #     "400m_hurdles_game": True,   
    #     "bahrain_won_400m_hurdles": True 
    # },
]

#! CRUD Operations:

#! View all Records
def viewOlympicRecords():
 if(olympicRecords != []):
  for i in range(0, len(olympicRecords)):
     print("Year:",olympicRecords[i]["year"],"\n")
     print("winning country:",olympicRecords[i]["winning_country"],"\n")
     print("total medals won:",olympicRecords[i]["total_medals_won"],"\n\n")
 print("**** Recods not found,you can add a new record by follow option from menu ****")
 

#! Display particular country records 
def displayRecords():
# logic for checking your country won game in that particular year
 if(olympicRecords != []):
  givenYear = int(input("Enter year: \n"))
  for i in range(0,len(olympicRecords)):
    #! First check : if olympic held in given year.   
   if(olympicHeld(givenYear) == True):
    #! Second check : if country played in that year   
    if(olympicRecords[i]["my_country_played"]  == True):
    #! Third check : if 400 m hurdle game played by given country   
     if(olympicRecords[i]["400m_hurdles_game"]==True and olympicRecords[i]["bahrain_won_400m_hurdles"]==True):
        print("**** In Year:",olympicRecords[i]["year"],"Bahrain won 400m hurdles game. **** \n")
        break
     else:
        print("**** Your country not won 400 m hurdles in  year", givenYear," or not played game **** \n")
        break
    else:
        print("***** Bahrain not played in year", givenYear,"**** \n")
        break
  else: 
    print("**** Olympics not held in ",givenYear,"**** \n")
 print("**** Recods not found,you can add a new record by follow option from menu **** \n")
    
#! Helper function to check if the Olympics held in given year
def olympicHeld(year):
    if(year == 2018 or year == 2020 or year == 2022 or year == 2024):
       return True
    elif(year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    else:
       return False

#! Delete Records
def deleteOlympicRecords():
  year = int(input("Enter Year: "))
  if(olympicRecords != []):
    index = getIndexOfOlympicYear(year)
    if index == -1:
        print("**** Olympic records not found,you can also add a new record by follow option from menu for that ****")
    else:
        olympicRecords.pop(index)
        print("**** Olympic record deleted **** \n")
  else:
    print("**** Recods not found,you can add a new record by follow option from menu **** \n")
  

#! Helper function to get index of records 
def getIndexOfOlympicYear(year):
 for i in range(0,len(olympicRecords)): 
     if(olympicRecords[i]["year"] == year):
       return i
 return -1
    

#! Add records
def addOlympicRecords():
    year = int(input("Enter year: \n"))
    winningcountry = input("Enter winning country name: \n")
    totalMedals = int(input("Enter Total Medals won: \n"))
    BahrainPlayed = input("Bahrain played in this Olympics. Type y for yes and n for no: \n")
    if(BahrainPlayed.lower() == "y"):
        BahrainPlayed = True
    BahrainPlayed = False
    
    
    hurdleGame = input("Bahrain played 400 m hurdle game. Type y for yes and n for no: \n")
    if(hurdleGame.lower() == "y"):
        hurdleGame = True
    hurdleGame = False
    
    wonHurdleGame = input("Bahrain won 400 m hurdle game. Type 'y' for yes and 'n' for no: \n")
    if(wonHurdleGame.lower() == "y"):
        wonHurdleGame = True
    wonHurdleGame = False
    
    
    record =  {"year": year,
     "winning_country": winningcountry,
     "total_medals_won": totalMedals,
     "my_country_played": BahrainPlayed,  
     "400m_hurdles_game": hurdleGame,   
     "bahrain_won_400m_hurdles": wonHurdleGame  }
    
    olympicRecords.append(record)
    print("**** Record Added !! **** \n")
    
    


#! Menu 
print("**** Welcome to visiting Olympic Pedia ****")

while True:
  options = int(
input("""
 Select option from given menu:
 Press 1 to add olympic records.
 Press 2 to delete olympic records.
 Press 3 to view all record.
 Press 4 to find your team  record.
 Press 0 to exit.\n
""")
)
  if(options == 1):
      addOlympicRecords()
  elif(options == 2):
      deleteOlympicRecords()
  elif(options == 3):
      viewOlympicRecords()
  elif(options == 4):
      displayRecords()
  elif(options == 0):
      print("Exiting.... ")
      break
  else:
      print("**** Invalid choice **** \n")



#! Olympic record finder:
#! Modules are:
    #! Add records.
    #! Delete records: Using of helper fucntion which will return the index of given year. 
    #! Display records: Here i am checking whether country played in that year or not OR in given year olympic held or not.
    #! View records: User can find last 5 records
    #! Menu of records.
