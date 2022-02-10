from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = 'somethingSecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = list()

@app.route('/')
def start_survey_page():
    """Show survey start page """
    return render_template('home.html', survey=survey)



@app.route('/begin', methods=["POST"])
def begin_survey():
    """ Redirect to first question """
    return redirect('/question/0')



@app.route('/question/<int:id>')
def handle_question(id):
    """Show question page"""

  # if no questions are completed, direct to homepage
    if responses is None:
        return redirect('/')
  
  # if all questions are completed, direct to end page
    if len(responses) == len(survey.questions):
        return redirect('/end')

  # if invalid question is accessed, direct to correct question
    if len(responses) != id:
        flash("You are trying to access an invalid question")
        return redirect(f"/question/{len(responses)}")

    current_question = survey.questions[id].question
    choices = survey.questions[id].choices

    return render_template('question.html', choices=choices, current_question=current_question, survey=survey)
    


@app.route('/answer', methods=["POST"])
def save_response():
    """ Save response to list """
    choice = request.form['answer']
    responses.append(choice)

  # if all questions answered end survey, else direct to next question
    if len(responses) == len(survey.questions):
        return redirect('/end')
    else:
        return redirect(f"/question/{len(responses)}")



@app.route('/end')
def show_thankyou_page():
    """Thank user and end survey"""

    return render_template('end.html')

    
        