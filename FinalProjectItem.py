import csv
from datetime import date

#Carlos Carbajal
#Final Project CIS 2348
#08/11/2024
#fields = ['ID', 'Manufacturer', 'Item Type', 'Price', 'Service Date', 'Damage']
listOfItems = []



class Item(object):
#Item class has attributes ID, Manufacturer, item type, price, service date, and damage notifier
    def __init__(self):
        self.itemID = 0
        self.manufact = ""
        self.itemType = ""
        self.itemPrice = 0
        self.servDate = ""
        self.itemDamaged = ""
        #info = {}
#Provided methods to make it easier to sort based on what file the program will be writing to
    def sortByManufacture(self):
        return self.manufact
    
    def sortByPrice(self):
        return self.itemPrice

    def sortByItemID(self):
        return self.itemID
    
    def sortByServiceDate(self):
        return self.servDate
    
    def sortByItemType(self):
        return self.itemType

    def __str__(self):
        return "" + str(self.itemID) + " " + str(self.manufact) + " " + str(self.itemType) + " " + str(self.itemPrice) + " " + str(self.servDate) + " " + str(self.itemDamaged) + "\n"
 
 #Setter methods for Item objects used when program is reading input from csv file   
    def setID(self, id):
        self.itemID = id

    def setManufacturer(self, manufacturer):
        self.manufact = manufacturer

    def setItemType(self, type):
        self.itemType = type

    def setPrice(self, price):
        self.itemPrice = price
    
    def setServiceDate(self, date):
        self.servDate = date

    def setItemDamage(self, dmg):
        if not(dmg == ""):
            self.itemDamaged = "Damaged"

        else:
            self.itemDamaged = ""




def checkItemExistence(itemIden):
    #checks if item exists in list already
    for items in listOfItems:
        if itemIden == items.itemID:
            return True
    return False

def checkListType(fileName, file, inventoryList):
    #Checks if the list is a manufacturer, service date, or price list
    if "ManufacturerList" in fileName:
            manufacturerList(file, inventoryList)
    elif "ServiceDatesList" in fileName:
            serviceDatesList(file, inventoryList)
    elif "PriceList" in fileName:
            priceList(file, inventoryList)


def listOfDamaged(list):
    #checks if the item is marked as damaged and is appended to a list that is returned
    dummyList = []
    for each in list:
        if not(each.itemDamaged == ""):
            dummyList.append(each)
    return dummyList


def filesByType(list, itemType, indexL):
    newList = []
    for item in list[indexL:]:
        if item.itemType == itemType:
            newList.append(item)
            indexL+=1
    newList = sorted(newList, key=Item.sortByItemID)
    createNewFile = ""+itemType+".csv"
    writer = open(createNewFile, 'w')
    for each in newList:
        writer.write("" + str(each.itemID) + " " + str(each.manufact) + " " + str(each.itemType) + " " + str(each.itemPrice) + " " + str(each.servDate) + "\n")
    if indexL<len(list):
        filesByType(list, str(list[indexL].itemType), indexL)
    


def main():
    #main function that inputs the file names of csv's to be read from and opens files to write to
    #input file names are already taken care of
    


    inputFileNameOne = "ManufacturerList.csv" #input("Please enter a file name: ")
    fileOne = open(inputFileNameOne, 'r')
    checkListType(inputFileNameOne, fileOne, listOfItems)

    inputFileNameTwo = "PriceList.csv"
    fileTwo = open(inputFileNameTwo, 'r')
    checkListType(inputFileNameTwo, fileTwo, listOfItems)

    inputFileNameThree = "ServiceDatesList.csv"
    fileThree = open(inputFileNameThree, 'r')
    checkListType(inputFileNameThree, fileThree, listOfItems)
    fileOne.close()
    fileTwo.close()
    fileThree.close()


    fullInvOPFileName = "FullInventory.csv"
    fullInventoryFile = open(fullInvOPFileName, 'w')
    fullInventoryReport(listOfItems, fullInventoryFile)

    dmgInvOPFileName = "DamagedInventory.csv"
    dmgInventoryFile = open(dmgInvOPFileName, 'w')
    damagedInventoryReport(listOfItems, dmgInventoryFile)

    pastServiceInvOPFileName = "PastServiceDateInventory.csv"
    pastServiceInventoryFile = open(pastServiceInvOPFileName, 'w')
    pastServiceDateInventoryReport(listOfItems, pastServiceInventoryFile)

    
    indexL=0
    filesByType(listOfItems, str(listOfItems[indexL].itemType), indexL)
        

def fullInventoryReport(listOfItems, fullInventoryFile):
    #Creates a list sorted by the manufacturer name in ascending order and returns a string concatenation to write to file
    maybe1= listOfItems
    maybe1 = sorted(listOfItems, key=Item.sortByManufacture)
    for each in maybe1:
        fullInventoryFile.write("" + str(each.itemID) + " " + str(each.manufact) + " " + str(each.itemType) + " " + str(each.itemPrice) + " " + str(each.servDate) + "\n")


def damagedInventoryReport(listOfItems, dmgInventoryFile):
    #Creates a list sorted by the item price in descending order and returns a string concatenation to write to file
    maybe2= listOfItems
    maybe2 = sorted(listOfDamaged(listOfItems), key=Item.sortByPrice, reverse= True)
    for each in maybe2:
        dmgInventoryFile.write("" + str(each.itemID) + " " + str(each.manufact) + " " + str(each.itemType) + " " + str(each.itemPrice) + " " + str(each.servDate) + "\n")


def pastServiceDateInventoryReport(listOfItems, pastServiceInventoryFile):
    #Creates a list sorted by the service date in descending order and returns a string concatenation to write to file
    maybe3= listOfItems
    maybe3 = sorted(listOfItems, key=Item.sortByServiceDate)
    currentDate = date.today()
    for each in maybe3:
        tempTime = str(each.servDate).split('/')
        tempMonth = tempTime[0]
        tempDay = tempTime[1]
        tempYear = tempTime[2]
        testDate = date(int(tempYear), int(tempMonth), int(tempDay))
        if testDate < currentDate:
            pastServiceInventoryFile.write("" + str(each.itemID) + " " + str(each.manufact) + " " + str(each.itemType) + " " + str(each.itemPrice) + " " + str(each.servDate) + "\n")




def manufacturerList(file, listOfItems):
    #Reads the csv file and checks if the csv file is a ManufacturerList, checks if the item is new or already on the list and adds its attributes accordingly.
    csvreader = csv.reader(file)
    for row in csvreader:
        for item in listOfItems:
            if item.itemID in row[0]:
                item.setManufacturer(row[1])
                item.setItemType(row[2])
                item.setItemDamage(row[3])
        if not(checkItemExistence(row[0])):
            newItem = Item()
            newItem.setID(row[0])
            newItem.setManufacturer(row[1])
            newItem.setItemType(row[2])
            newItem.setItemDamage(row[3])
            listOfItems.append(newItem)

def priceList(file, listOfItems):
    #Reads the csv file and checks if the csv file is a PriceList, checks if the item is new or already on the list and adds its attributes accordingly.
    csvreader = csv.reader(file)
    for row in csvreader:
        for item in listOfItems:
            if item.itemID in row[0]:
                item.setPrice(row[1])
        if not(checkItemExistence(row[0])):
            newItem = Item()
            newItem.setID(row[0])
            newItem.setPrice(row[1])
            listOfItems.append(newItem)


def serviceDatesList(file, listOfItems):
    #Reads the csv file and checks if the csv file is a ServiceDatesList, checks if the item is new or already on the list and adds its attributes accordingly.
    csvreader = csv.reader(file)
    for row in csvreader:
        for item in listOfItems:
            if item.itemID in row[0]:
                item.setServiceDate(row[1])
        if not(checkItemExistence(row[0])):
            newItem = Item()
            newItem.setID(row[0])
            newItem.setServiceDate(row[1])
            listOfItems.append(newItem)


if __name__ == "__main__":
    main()