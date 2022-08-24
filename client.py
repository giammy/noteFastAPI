#!/usr/bin/env python3
import requests
import json
import random
import time
import argparse
import datetime

#
# a command line interface to REST API of notes
# to get help use: ./client.py --help
#
# some usage examples:
# ./client.py --createEntity '{"__ENT__":"PC", "OWNER":"name1", "LOCATION":"office1"}'
# ./client.py --listEntities STAFFMEMBER   
# ./client.py --searchEntity '{"__ENT__":"PC", "OWNER":"name1"}'     
# ./client.py --searchEntity '{"__ENT__":"STAFFMEMBER", "GROUPNAME":"Group2"}'
# ./client.py --getEntity 6 

theUrl = "http://127.0.0.1:8000/note"

#
# the following 2 functions create an example entity called STAFFMEMBER, 
# they are invoked by the option --createManyStaffMembers NUM
# to fill the database for testing purposes
#
def createStaffMember(username, email, secondaryEmail, name, surname, groupName, leaderOfGroup, qualification, organization, totalHoursPerYear, totalContractualHoursPerYear, parttimePercent, isTimeSheetEnabled, created, validFrom, validTo, note, officePhone, officeLocation, internalNote, lastChangeAuthor, lastChangeDate):
    rid = createNote(rid=0, type="STAFFMEMBER", data="")
    createNote(rid=rid, type="USERNAME", data=username)
    createNote(rid=rid, type="EMAIL", data=email)
    createNote(rid=rid, type="SECONDARYEMAIL", data=secondaryEmail)
    createNote(rid=rid, type="NAME", data=name)
    createNote(rid=rid, type="SURNAME", data=surname)
    createNote(rid=rid, type="GROUPNAME", data=groupName)
    createNote(rid=rid, type="LEADEROFGROUP", data=leaderOfGroup)
    createNote(rid=rid, type="QUALIFICATION", data=qualification)
    createNote(rid=rid, type="ORGANIZATION", data=organization)
    createNote(rid=rid, type="TOTALHOURSPERYEAR", data=totalHoursPerYear)
    createNote(rid=rid, type="TOTALCONTRACTUALHOURSPERYEAR", data=totalContractualHoursPerYear)
    createNote(rid=rid, type="PARTTIMEPERCENT", data=parttimePercent)
    createNote(rid=rid, type="ISTIMESHEETENABLED", data=isTimeSheetEnabled)
    createNote(rid=rid, type="CREATED", data=created)
    createNote(rid=rid, type="VALIDFROM", data=validFrom)
    createNote(rid=rid, type="VALIDTO", data=validTo)
    createNote(rid=rid, type="NOTE", data=note)
    createNote(rid=rid, type="OFFICEPHONE", data=officePhone)
    createNote(rid=rid, type="OFFICELOCATION", data=officeLocation)
    createNote(rid=rid, type="INTERNALNOTE", data=internalNote)
    createNote(rid=rid, type="LASTCHANGEAUTHOR", data=lastChangeAuthor)
    createNote(rid=rid, type="LASTCHANGEDATE", data=lastChangeDate)
    return rid

def createManyStaffMembers(num, numberOfGroups):
    startTime = time.time()
    for i in range(0, num):
        createStaffMember(username="username%d" % (i), email="email%d@email.it" % (i), secondaryEmail="email%d@email.it" % (i), name="name%d" % (i), surname="surname%d" % (i), groupName="Group%d"%(random.randint(1, numberOfGroups)), leaderOfGroup="leaderOfGroup%d" % (i), qualification="qualification%d" % (i), organization="organization%d" % (i), totalHoursPerYear="totalHoursPerYear%d" % (i), totalContractualHoursPerYear="totalContractualHoursPerYear%d" % (i), parttimePercent="parttimePercent%d" % (i), isTimeSheetEnabled="isTimeSheetEnabled%d" % (i), created="created%d" % (i), validFrom="validFrom%d" % (i), validTo="validTo%d" % (i), note="note%d" % (i), officePhone="officePhone%d" % (i), officeLocation="officeLocation%d" % (i), internalNote="internalNote%d" % (i), lastChangeAuthor="lastChangeAuthor%d" % (i), lastChangeDate="lastChangeDate%d" % (i))
    print("Created %d staff members in %s seconds" % (num, time.time() - startTime))

#
# general functions
#

def getCurrentDate():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+0000")

def printNote(note):
    print(note)
    # print("%i,%i,%i,%s,%s\n" % (note['id'],note['rid'],note['lid'],note['type'],note['data']))

def auxGetAndReturnList(url):
    resp = requests.get(url=url)
    if (resp.status_code == 200):
        return resp.json()
    else:
        return []

def getAllNotes():
    return auxGetAndReturnList(theUrl)

def getNote(id):
    return auxGetAndReturnList(theUrl + "/?id=%s" % (id))

def getNotesWithType(tagName):
    return auxGetAndReturnList(theUrl + "/?type=%s" % (tagName))

def getAttributesOfNote(id):
    return auxGetAndReturnList(theUrl + "/?rid=%d" % (id))

def getEntities(whichType):
    return auxGetAndReturnList(theUrl + "/?type=%s&rid=0" % (whichType))

# create a new note with a POST request
def createNote(rid, type, data):
    resp = requests.post(url=theUrl, json={"rid": rid, "lid": 1, "type": type, "data": data})
    return(resp.json()['id'])

def createEntity(jsonInfo):
    entityType = jsonInfo['__ENT__']
    rid = createNote(rid=0, type=entityType, data="")
    for key in jsonInfo:
        if (key != '__ENT__'):
            createNote(rid=rid, type=key, data=jsonInfo[key])

def checkType(thisType, noteList):
    if len(noteList)<1:
        return False
    return noteList[0]['type'] == thisType

def searchEntity(jsonInfo):
    entityType = jsonInfo['__ENT__']
    del jsonInfo['__ENT__']
    firstKey = list(jsonInfo.keys())[0]
    firstValue = jsonInfo[firstKey]
    noteList = auxGetAndReturnList(theUrl + "/?type=%s&data=%s" % (firstKey, firstValue))
    idList = list(map(lambda x: x['rid'], noteList))
    resList = list(filter(lambda x: checkType(entityType, getNote(x)), idList))
    return resList

#
# Available operations
#         

def infoDb():
    note = getNotesWithType("__SYSTEM__")
    if len(note) == 0:
        return []
    else:  
        note = getAttributesOfNote(note[0]['id']) 
        return note

def initDb():
    if len(infoDb()) > 0:
        return False
    rid = createNote(rid=0, type="__SYSTEM__", data="")
    createNote(rid=rid, type="CREATED", data=getCurrentDate())
    return True

def deleteNote(id):
    resp = requests.delete(url=theUrl + "/" + str(id))
    return(resp)

def resetDb():
    noteList = getAllNotes()
    for note in noteList:
        deleteNote(note['id'])

def countNotes():
    noteList = getAllNotes()
    return len(noteList)

def countEntities():
    noteList = getAttributesOfNote(0) 
    typeList = list(map(lambda x: x['type'], noteList))
    counted = {i:typeList.count(i) for i in typeList}
    return counted 

def printNotes():
    noteList = getAllNotes()
    for note in noteList:
        printNote(note)

def listEntities(whichType):
    noteList = getEntities(whichType)
    idList = list(map(lambda x: x['id'], noteList))
    return idList

def getEntity(id):
    noteList = getAttributesOfNote(id)
    return noteList


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--initDb', help='Initialize the database', action='store_true')
    parser.add_argument('--resetDb', help='Reset the database. WARNING: ALL DATA WILL BE DELETED', action='store_true')
    parser.add_argument('--infoDb', help='Show some info on the database', action='store_true')
    parser.add_argument('--countNotes', help='Count all the notes present in the database', action='store_true') 
    parser.add_argument('--countEntities', help='Count all the entities present in the database', action='store_true')
    parser.add_argument('--listEntities', help='List all the entities of given type', metavar='TYPE')  
    parser.add_argument('--printNotes', help='Print all the notes present in the database', action='store_true')
    parser.add_argument('--createEntity', help='Create a new entity from the given JSON', 
                        metavar='{"__ENT__":"PC", "OWNER":"name1", "LOCATION":"office1"}')
    parser.add_argument('--searchEntity', help='Search an entity from the given JSON (search on 1 property only)', 
                        metavar='{"__ENT__":"PC", "OWNER":"name1"}')
    parser.add_argument('--getEntity', help='Get an entity', type=int, metavar='ID')
    parser.add_argument('--createManyStaffMembers', help='Create may staff members', type=int, metavar='NUM')

    args = parser.parse_args()
    for k, arg in args.__dict__.items():
        match k:
            case 'infoDb':
                if arg:
                    print("Show info about the database:")
                    res = infoDb()
                    if len(res) > 0:
                        print(res)
                    else:
                        print("Database not initialized.")  
                    continue
            case 'initDb':
                if arg:
                    print("Initializing the database")
                    if initDb():
                        print("Database initialized")
                    else:
                        print("Database already initialized")
                    continue
            case 'resetDb':
                if arg:
                    print("Resetting the database")
                    resetDb()
                    continue
            case 'countNotes':
                if arg:
                    print("Counting the notes in the database: %d" % (countNotes()))
                continue
            case 'countEntities':
                if arg:
                    print("Counting the entities in the database: %s" % (countEntities()))
                continue
            case 'listEntities':
                if arg != None:
                    print("List the entities in the database: %s" % (listEntities(arg)))
                continue
            case 'printNotes':
                if arg:
                    print("Printing the notes in the database:")
                    printNotes()
                continue
            case 'createEntity':
                if arg != None:
                    print("Creating entity: %s" % (arg))
                    convertedArg = json.loads(arg)
                    createEntity(convertedArg)
                continue
            case 'searchEntity':
                if arg != None:
                    print("Searching entity: %s" % (arg))
                    convertedArg = json.loads(arg)
                    res = searchEntity(convertedArg)
                    print(res)
                continue
            case 'getEntity':
                if arg != None:
                    print("Getting entity: %s" % (arg))
                    res = getEntity(arg)
                    print(res)
            case 'createManyStaffMembers':
                if arg != None:
                    print("Creating %d staff members" % (arg))
                    createManyStaffMembers(arg, 10)
            case _:
                print("Unmanaged flag: %s" % (k))

main()
