from datetime import datetime
import os
import json
from app import surveys, turkers, conversations, blueprints, logs
from flask import session

#Check for returning Turkers
def checkTurker(turker):
    if turkers.find_one({'turker':turker},{'_id':0,'session':1}):
        return True
    else:
        return False

#Check completion status of Turker
def isFinished(turker):
    details = turkers.find_one({'turker':turker})
    if details:
        return details['isFinished']
    else:
        return False

#get session ID of Turker
def getGUID(turker):
    survey = turkers.find_one({'turker':turker},{})
    return survey['session']

#Returns the Turker ID from existing guid session
def getTurker(guid):
    return turkers.find_one({'session':guid})['turker']

def getLastConvo(guid):
    return surveys.find_one({'turker':getTurker(guid)})['lastConvo']

#Get latest page
def getPage(turker):
    survey = surveys.find_one({'turker':turker},{'_id':0})
    if survey['lastConvo'] == 0:
        return '/definition/guid='+survey['session']
    elif survey['lastConvo'] >0 and survey['lastConvo'] <=2:
        return '/tutorial/id='+str(survey['lastConvo'])+'&guid='+survey['session']
    elif survey['lastConvo'] >=3 and survey['lastConvo'] <=22:
        return '/survey/id='+str(survey['lastConvo'])+'&guid='+survey['session']
    else:
        return '/last/guid='+survey['session']

#Moves Turker from Active to Surveys
def lastWrite(guid,feedback):
    survey = {}
    survey['feedback'] = feedback
    survey['lastConvo'] = 23
    survey['finished'] = 'Yes'
    surveys.update_one({'turker':getTurker(guid)},{'$set':survey})
    turkers.update_one({'session':guid},{'$set':{'isFinished':True}})

#Creates a new survey
def createSurvey(guid,turker):
    
    #choose batch
    batch = 1

    #generate new survey from batch template
    survey = blueprints.find_one({'batch':batch},{'_id':0})
    #populate metadata
    survey['turker'] = turker
    survey['session'] = guid
    survey['lastConvo'] = 0
    #populate log for index
    log = {
        'page' : 'Index',
        'convo' : None,
        'element' : 'next',
        'timestamp' : str(datetime.utcnow().timestamp())
    }
    #create new file for new turker
    surveys.insert_one(survey)
    logs.insert_one(log)

    #create session for new turker
    session = {
        'turker':turker,
        'session':guid,
        'isFinished':False
    }
    turkers.insert_one(session)

#Captures entry for conversation
def updateSurvey(guid,id,choiceD,choiceC):
    survey = surveys.find_one({'turker':getTurker(guid)},{'_id':0})
    survey['convo'][id]['deceptionChoice'] = choiceD
    survey['convo'][id]['confidenceChoice'] = choiceC
    survey['convo'][id]['timestamp'] = str(datetime.utcnow().timestamp())
    surveys.update_one({'turker':survey['turker']},{'$set':{'convo':survey['convo'],'lastConvo':id+1}})

#Getting the Question and witness for a given question 
def getConvo(guid,id):
    survey = surveys.find_one({'turker':getTurker(guid)})
    convID = survey['convo'][id]['convID']
    conversation = conversations.find_one({'convID':convID})
    return conversation['question'],conversation['witness']

#Getting the expected response for a given question 
def getExpectedResponse(guid,id):
    survey = surveys.find_one({'turker':getTurker(guid)})
    return survey['convo'][id]['expectedChoice']

#Getting the deception choice for a given question
def getDeception(guid,id):
    survey = surveys.find_one({'turker':getTurker(guid)})
    return survey['convo'][id]['deceptionChoice']

#Getting the confidence choice for a given question
def getConfidence(guid,id):
    survey = surveys.find_one({'turker':getTurker(guid)})
    return survey['convo'][id]['confidenceChoice']

#for writing logs
def writeLog(element,guid,page,id):
    log = {
        'turker':getTurker(guid),
        'page' : page,
        'convo' : id,
        'element' : element,
        'timestamp' : str(datetime.utcnow().timestamp())
    }
    logs.insert_one(log)

#for writing logs in nonsurvey pages
def writeLandingLog(element,guid,page):
    log = {
        'turker':getTurker(guid),
        'page' : page,
        'convo' : None,
        'element' : element,
        'timestamp' : str(datetime.utcnow().timestamp())
    }
    logs.insert_one(log)