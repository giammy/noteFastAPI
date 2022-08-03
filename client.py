#!/usr/bin/env python3
import requests
import json
import random
import time

#
# an usage example
#

theUrl = "http://127.0.0.1:8000/note"
numberOfEntities = 10
numberOfGroups = 10

# print a note
def print_note(note):
    print(note)
    # print(note['id'])
    # print(note['rid'])
    # print(note['lid'])
    # print(note['type'])
    # print(note['data'])
    # print("\n")

#
# get list of notes
#
def get_note_list():
    resp = requests.get(url=theUrl)
    # print(resp)
    # print(resp.status_code)
    # print(resp.json())
    if (resp.status_code == 200):
        return resp.json()
    else:
        # TODO - some error handling
        print(resp)
        return []

def get_note_list_with_params(tagName, tagValue):
    resp = requests.get(url=theUrl + "/?type=%s&data=%s" % (tagName, tagValue))
    return resp.json()

def get_note_list_of_attibutes(id):
    resp = requests.get(url=theUrl + "/?rid=%d" % (id))
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

def searchStaffMemberWithGroupNameFetchingAll(groupName):
    startTime = time.time()
    noteList = get_note_list()
    count = 0
    for note in noteList:
        if (note['type'] == "GROUPNAME"):
            if (note['data'] == groupName):
                count = count + 1
                #print_note(note)
                #print("\n")
    print("Searched %d staff members in %s seconds - got %d members" % (len(noteList), time.time() - startTime, count))

def searchStaffMemberWithGroupName(groupName):
    startTime = time.time()
    noteList = get_note_list_with_params("GROUPNAME", groupName)   
    print("Got %d staff members with GROUPNAME=%s in %s seconds" % (len(noteList), groupName, time.time() - startTime))

def searchStaffMemberWithId(id):
    startTime = time.time()
    noteList = get_note_list_of_attibutes(id)   
    print("Got %d notes for staff member %d in %s seconds" % (len(noteList), id, time.time() - startTime))
    
#
# run some tests
#

createManyStaffMembers(numberOfEntities, numberOfGroups)

noteList = get_note_list()
print("Got note list: length=%d" % (len(noteList)))
## iter over the list of notes
#for note in noteList:
#    print_note(note)

searchStaffMemberWithGroupNameFetchingAll("Group3")

searchStaffMemberWithGroupName("Group5")

searchStaffMemberWithId(24)
