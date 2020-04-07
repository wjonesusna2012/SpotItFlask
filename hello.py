from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from flask_bootstrap import Bootstrap
app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
bootstrap = Bootstrap(app)


class NameForm(FlaskForm):
    name = StringField('Enter your name:', validators=[DataRequired()])
    numPictures = IntegerField('Number of Pictures', validators=[NumberRange(min=1, max=100, message="Enter a number 1-100")])
    symbolsPerCard = IntegerField('Number of Symbols per card', validators=[NumberRange(min=1, max=10, message="Enter a number 1-10")])
    submit = SubmitField('Calculate')

def validateNumberOfOneBits(testNumber, numberOfOnes):
    test = testNumber
    oneCount = 0
    while test > 0:
        if test % 2 == 1:
            oneCount += 1
        test = test >> 1
    return oneCount == numberOfOnes

def checkOneBitInCommon(a, b):
    return validateNumberOfOneBits(a & b, 1)

def checkNumberAgainstList(listOfNumbers, testNumber):
    for l in listOfNumbers:
        if not checkOneBitInCommon(l, testNumber):
            return False
    return True

def generateSymbolList(numberOfSymbols, symbolsPerCard):
    allValidSymbols = []
    maxNumber = 2 ** (symbolsPerCard + 1) - 1 # for example 7 yields 2^8 - 1 or 0b1111111
    maxNumber = maxNumber << (numberOfSymbols - symbolsPerCard)
    for i in range(0, maxNumber):
        if validateNumberOfOneBits(i, symbolsPerCard) and checkNumberAgainstList(allValidSymbols, i):
            allValidSymbols.append(i)
    return allValidSymbols

@app.route('/', methods=['POST', 'GET'])
def index():
    testForm = NameForm()
    name = 'William'
    numberOfSymbols = 0
    numberOfSymbols = 0
    symbols = []

    if testForm.validate_on_submit():
        numberOfSymbols = testForm.numPictures.data
        numberOfSymbolsPerCard = testForm.symbolsPerCard.data
        name = testForm.name.data
        symbols=generateSymbolList(numberOfSymbols, numberOfSymbolsPerCard)

    return render_template('test.html', form=testForm, name=name, symbolData=symbols)

