from datetime import datetime
from markupsafe import Markup
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, HiddenField, StringField, widgets
from wtforms.validators import DataRequired
import uuid

class SurveyForm(FlaskForm):

    def row(field,**kwargs):
        html = []
        for subfield in field:
            if subfield.type in ("HiddenField", "CSRFTokenField"):
                hidden += str(subfield)
            else:
                if '0' in subfield.id:
                    html.append(
                        "<td class=\"greenFeildStrong\">%s%s</td>"
                        % (str(subfield.label),str(subfield))
                    )
                elif '1' in subfield.id:
                    html.append(
                        "<td class=\"greenFeildWeak\">%s%s</td>"
                        % (str(subfield.label),str(subfield))
                    )
                elif '2' in subfield.id:
                    html.append(
                        "<td class=\"yellowFeild\">%s%s</td>"
                        % (str(subfield.label),str(subfield))
                    )
                elif '3' in subfield.id:
                    html.append(
                        "<td class=\"orangeFeild\">%s%s</td>"
                        % (str(subfield.label),str(subfield))
                    )
                else:
                    html.append(
                        "<td class=\"redFeild\">%s%s</td>"
                        % (str(subfield.label),str(subfield))
                    )
        return Markup("".join(html))
    
    logField = HiddenField(id='log')
    deception = RadioField(choices=[(1,'Strongly Agree'),(2,'Agree'),(3,'Neutral'),(4,'Disagree'),(5,'Strongly Disagree')], id='deception', default=None, render_kw = {'onclick':'log(this)'}, widget=row)
    confidence = RadioField(choices=[(1,'Very Confident'),(2,'Confident'),(3,'Somewhat Confident'),(4,'Not Confident'),(5,'Not Confident at All')], id='confidence', default =None, render_kw = {'onclick':'log(this)'}, widget=row)
    submit = SubmitField('Next', render_kw = {'onclick':'log(this)'}, id='next')
    previous = SubmitField('Previous', render_kw = {'onclick':'log(this)'}, id='previous')
    
    def setDeceptionChoice(self,deceptionChoice):
        if deceptionChoice :
            self.deception.data = self.deception.coerce(deceptionChoice)

    def setConfidenceChoice(self,confidenceChoice):
        if confidenceChoice :
            self.confidence.data = self.confidence.coerce(confidenceChoice)

class IndexForm(FlaskForm):
    uuidValue = uuid.uuid4()
    guid = HiddenField(label='guid', default=uuidValue)
    submit = SubmitField('Next')

class LastForm(FlaskForm):
    feedback = StringField(label='Feedback', description='We would like any feedback you might have for us', render_kw={"placeholder": "Feedback"} )
    previous = SubmitField('Previous', render_kw = {'onclick':'log(this)'}, id='previous')
    submit = SubmitField('I am Done', render_kw = {'onclick':'log(this)'}, id='next')