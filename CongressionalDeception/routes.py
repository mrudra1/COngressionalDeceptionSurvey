from crypt import methods
from datetime import datetime
from forms import IndexForm, SurveyForm, LastForm
from app import app, recaptcha
from flask import render_template, redirect, flash, url_for
import utils

#For the Index Page
@app.route('/index/assignmentId=<assignmentId>&hitId=<hitId>&workerId=<workerId>&turkSubmitTo=https://www.mturk.com', methods=['GET','POST'])
def index(assignmentId=0, hitId=0, workerId = 'AMAC9WOWVCJN'):
    form = IndexForm()
    message = ''
    
    #if returning turker
    if utils.isFinished(workerId):
        return redirect('/ThankYou')

    if utils.checkTurker(workerId):
        return redirect(utils.getPage(workerId))

    #if the guid is None then generate the guid
    guid = form.guid.data

    #Create new survey for new turker
    if form.is_submitted() and recaptcha.verify():
        utils.createSurvey(guid, workerId)
        url = '/definition/guid='+guid
        return redirect(location=url)

    else:
        if form.submit.data and not recaptcha.verify():
            message = 'Please answer the captcha'

    return render_template('index.html', form = form, message=message)

@app.route('/definition/guid=<string:guid>',methods=['GET','POST'])
def definition(guid):
    utils.writeLandingLog(element='landing',guid=guid,page='Definition')
    return render_template('definition.html',guid=guid)


@app.route('/tutorial/id=<int:id>&guid=<string:guid>', methods=['GET', 'POST'])
def tutorial(id,guid):

    if id > utils.getLastConvo(guid):
        return redirect(utils.getPage(utils.getTurker(guid)))

    question, witness = utils.getConvo(guid,id)
    form = SurveyForm()
    message1 = ''
    message2 = ''
    expectedResponses = utils.getExpectedResponse(guid,id)
    
    if not form.deception.data:
        form.setDeceptionChoice(deceptionChoice = utils.getDeception(guid,id))

    if not form.confidence.data:
        form.setConfidenceChoice(confidenceChoice=utils.getConfidence(guid,id))

    if form.validate_on_submit():

        #if previous
        if form.previous.data:
            utils.updateSurvey(guid,id,form.deception.data,form.confidence.data)
            return redirect(url_for('previous', id=id, guid=guid))

        #if next
        if int(form.deception.data) in expectedResponses:
            utils.updateSurvey(guid,id,form.deception.data,form.confidence.data)
            if id < 2 :
                url = '/tutorial/id='+str(id+1)+'&guid='+guid
                return redirect(location=url)
            else:
                return redirect(location='/survey/id='+str(id+1)+'&guid='+guid)
        else:   
            message1 = 'Are you sure you made the right choice? Are you convinced by the response of the witness in the above conversation?'
    
    if form.previous.data:
            #print('\ndetected previous\n')
            utils.updateSurvey(guid,id,form.deception.data,form.confidence.data)
            return redirect(url_for('previous', id=id, guid=guid))
            
    if form.submit.data:
        if not form.deception.data:
            message1 = 'Please ensure you have made a choice'
        if not form.confidence.data:
            message2 = 'Please ensure you have made a choice'

    return render_template('tutorial.html', question=question, witness=witness, form=form, id=id,guid=guid, message1=message1, message2=message2)

@app.route('/previous/<int:id>&guid=<string:guid>', methods = ['GET','POST'])
def previous(id,guid):
    if id > 3: 
        return redirect('/survey/id='+str(id-1)+'&guid='+str(guid))
    elif id > 0 and id<=3 :
        return redirect('/tutorial/id='+str(id-1)+'&guid='+str(guid))
    else:
        return redirect('/definition/guid='+guid)


@app.route('/survey/id=<int:id>&guid=<string:guid>', methods = ['GET','POST'])
def showSurvey(id,guid):

    if id > utils.getLastConvo(guid):
        return redirect(utils.getPage(utils.getTurker(guid)))
    
    question, witness = utils.getConvo(guid,id)
    form = SurveyForm()
    message1 = ''
    message2 = ''
    
    if not form.deception.data:
        form.setDeceptionChoice(deceptionChoice = utils.getDeception(guid,id))

    if not form.confidence.data:
        form.setConfidenceChoice(confidenceChoice=utils.getConfidence(guid,id))

    if form.validate_on_submit():

        utils.updateSurvey(guid,id,form.deception.data,form.confidence.data)
        #if previous
        if form.previous.data:
            #print('\ndetected previous\n')
            #utils.updateSurvey(guid,id,form.deception.data,form.confidence.data)
            return redirect(url_for('previous', id=id, guid=guid))

        if id < 22 :
            url = '/survey/id='+str(id+1)+'&guid='+guid
            return redirect(location=url)
        else:
            return redirect(location='/last/guid='+guid)

    if form.previous.data:
            #print('\ndetected previous\n')
            utils.updateSurvey(guid,id,form.deception.data,form.confidence.data)
            return redirect(url_for('previous', id=id, guid=guid))
    
    if form.submit.data:
        if not form.deception.data:
            message1 = 'Please ensure you have made a choice'
        if not form.confidence.data:
            message2 = 'Please ensure you have made a choice'

    return render_template('survey.html', question=question, witness=witness, form=form, id=id,guid=guid, message1=message1, message2=message2)

@app.route('/ThankYou')
def ThankYou():
    return render_template('Thanks.html')

@app.route('/last/guid=<string:guid>',methods=['GET','POST'])
def showLast(guid):
    form = LastForm()
    message = ''
    if form.is_submitted() and form.feedback.data:
        utils.lastWrite(guid,form.feedback.data)
        return redirect('https://www.mturk.com/mturk/externalSubmit')

    if form.previous.data:
        return redirect(url_for('previous', id=23, guid =guid))

    if form.is_submitted and not form.feedback.data and not form.previous.data:
        message = "Please enter feedback"
    
    #print('not done yet',form.is_submitted(),form.validate(),form.feedback.data)
    
    return render_template('last.html', form=form, id=23, guid=guid, message=message)

@app.route('/log/<string:element>&<string:guid>&<string:page>&<int:id>')
def log(element,guid,page,id):
    #print(id, type(id))
    #log survey page
    if id>=0 and id<=22 :
        #print('here')
        utils.writeLog(element,guid,page,id)
    #log non-survey page
    else:
        #print('there')
        utils.writeLandingLog(element,guid,page)
    return "Something"