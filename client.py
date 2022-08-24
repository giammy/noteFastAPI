#!/usr/bin/env python3
import requests
import json
import random
import time
import argparse
import datetime

#
# a command line interface to REST API of notes
#

theUrl = "http://127.0.0.1:8000/note"
numberOfEntities = 10
numberOfGroups = 10

def get_note_list_with_params(tagName, tagValue):
    resp = requests.get(url=theUrl + "/?type=%s&data=%s" % (tagName, tagValue))
    if "detail" in resp.json():
        return []
    else:   
        return resp.json()


#
# create a new note with a POST request
#
def createNote(rid, type, data):
    resp = requests.post(url=theUrl, json={"rid": rid, "lid": 1, "type": type, "data": data})
    return(resp.json()['id'])

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
    

def getRandomGroup(numberOfGroups):
    return "Group%d" % (random.randint(1, numberOfGroups))

def createManyStaffMembers(num, numberOfGroups):
    startTime = time.time()
    for i in range(0, num):
        createStaffMember(username="username%d" % (i), email="email%d@email.it" % (i), secondaryEmail="email%d@email.it" % (i), name="name%d" % (i), surname="surname%d" % (i), groupName=getRandomGroup(numberOfGroups), leaderOfGroup="leaderOfGroup%d" % (i), qualification="qualification%d" % (i), organization="organization%d" % (i), totalHoursPerYear="totalHoursPerYear%d" % (i), totalContractualHoursPerYear="totalContractualHoursPerYear%d" % (i), parttimePercent="parttimePercent%d" % (i), isTimeSheetEnabled="isTimeSheetEnabled%d" % (i), created="created%d" % (i), validFrom="validFrom%d" % (i), validTo="validTo%d" % (i), note="note%d" % (i), officePhone="officePhone%d" % (i), officeLocation="officeLocation%d" % (i), internalNote="internalNote%d" % (i), lastChangeAuthor="lastChangeAuthor%d" % (i), lastChangeDate="lastChangeDate%d" % (i))
    print("Created %d staff members in %s seconds" % (num, time.time() - startTime))

def searchStaffMemberWithGroupName(groupName):
    startTime = time.time()
    noteList = get_note_list_with_params("GROUPNAME", groupName)   
    print("Got %d staff members with GROUPNAME=%s in %s seconds" % (len(noteList), groupName, time.time() - startTime))

def getStaffMemberWithId(id):
    startTime = time.time()
    noteList = getAttributesNotesOf(id)  
    # print(noteList) 
    # print("Got %d notes for staff member %d in %s seconds" % (len(noteList), id, time.time() - startTime))
    return noteList



# createManyStaffMembers(numberOfEntities, numberOfGroups)
# searchStaffMemberWithGroupNameFetchingAll("Group3")
# searchStaffMemberWithGroupName("Group5")
# res = getStaffMemberWithId(24)
# print("Got %d notes for staff member %d" % (len(
#   res), 24))

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

def getNotesWithType(tagName):
    return auxGetAndReturnList(theUrl + "/?type=%s" % (tagName))

def getAttributesOfNote(id):
    return auxGetAndReturnList(theUrl + "/?rid=%d" % (id))

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

def printNotes():
    noteList = getAllNotes()
    for note in noteList:
        printNote(note)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--initDb', help='Initialize the database', action='store_true')
    parser.add_argument('--resetDb', help='Reset the database. WARNING: ALL DATA WILL BE DELETED', action='store_true')
    parser.add_argument('--infoDb', help='Show some info on the database', action='store_true')
    parser.add_argument('--countNotes', help='Count all the notes present in the database', action='store_true')  
    parser.add_argument('--printNotes', help='Print all the notes present in the database', action='store_true')
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
            case 'initDb':
                if arg:
                    print("Initializing the database")
                    if initDb():
                        print("Database initialized")
                    else:
                        print("Database already initialized")
            case 'resetDb':
                if arg:
                    print("Resetting the database")
                    resetDb()
            case 'countNotes':
                if arg:
                    print("Counting the notes in the database: %d" % (countNotes()))
            case 'printNotes':
                if arg:
                    print("Printing the notes in the database:")
                    printNotes()
            case _:
                print("Unmanaged flag: %s" % (k))

main()
