from flask import Flask, render_template, url_for, request, g, redirect, session
from database import getDatabase, connect_to_database
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24) # this is for generating the hashed password 


@app.teardown_appcontext
def close_database(error):
    if hasattr(g, "quizapp_db"):
       g.quizapp_db.close() 

"""
Teardown functions in Flask can accept an 'error' parameter, but it's not always needed.
This part of the function 'if hasattr(g, "quizapp_db")' checks if the Flask global object g has an attribute named quizapp_db.
The g object is a place to store and share data during the handling of a request( like a user clicking a link, submitting a form, 
or making an HTTP request using a web browser). If the attribute is present, it assumes it's a database connection (quizapp_db) and closes it.
The purpose is to ensure that database connections are properly closed at the end of each request or when the application context is being torn down. 
This helps prevent potential resource leaks and ensures proper cleanup of database-related resources.
"""


""" Now we are creating this function to be able to use the 'session variable'.
'Sessions' can be used to store form data temporarily as the user navigates between 
different pages or steps of a multi-page form. This ensures that if the user leaves 
the form and returns later, their previously entered data is still available. 

"""
def get_current_user():
    user_result = None # no current user thats why its None
    if 'user' in session: # This checks  if a user is logged in or if certain user-related information is stored in the session.
        user = session['user'] # now we store the user present n session. the user is like a key-value pair
        db = getDatabase()
        user_cursor = db.execute("select * from users where name = ?", [user]) # checking whether this user is already present in the database
        user_result = user_cursor.fetchone()
    return user_result


@app.route('/') # this is to navigate to the first page
def index():
    user = get_current_user()
    db = getDatabase()
    geting_all = db.execute('select questions.question_text, questions.answer_text,\
    askersname.name AS askersname, answeredby.name AS answeredby FROM questions JOIN \
    users AS askersname ON askersname.id = questions.asked_by_id JOIN users AS answeredby \
     ON answeredby.id = questions.teacher_id WHERE questions.answer_text IS NOT NULL')
    fetching_all = geting_all.fetchall()
    
    return render_template('home.html', user = user, fetching_all = fetching_all)


@app.route('/login', methods = ["POsT", "GET"]) 
def login():
    user = get_current_user()
    error = None
    if request.method == "POST":
        db = getDatabase()
        name = request.form["name"]
        password = request.form["password"]
        
        fetched_user_data = db.execute("select * from users where name = ?", [name])
        fetched_user = fetched_user_data.fetchone()
        # checking if fetched_user exists  in the database and if it does, comparing the passwordentered with that of the database
        if fetched_user:
            if check_password_hash(fetched_user['password'], password):
                session['user'] = fetched_user['name'] # this is for all pages to get the current user
                return redirect(url_for('index'))
            else:
                error = "Username or password did not match. Try again"
                #return render_template('login.html', error = error)
        # this else is whem the user name can not be seen
        else:
            error = "Username or password did not match. Try again"
            #return render_template('login.html', error = error)
    
    return render_template('login.html', user = user, error = error)


@app.route('/register', methods = ["POST", "GET"]) 
def register():
    user = get_current_user()
    error = None
    if request.method == "POST":
        db = getDatabase()
        name = request.form["name"]
        password = request.form["password"]
        # this checks if the name already exists in the database i.e someone already has that username
        user_fetching_cursor = db.execute("select * from users where name = ?", [name])
        existing_user = user_fetching_cursor.fetchone() 
        if existing_user:
            error = "Username already taken,please choose a different username"
            return render_template("register.html", error = error)

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        db.execute("insert into users (name, password, teacher, admin) values (?,?,?,?)", [name, hashed_password , '0', '0'])
        db.commit()
        session['user'] = name # storing the current user in session
        return redirect(url_for('index'))

    return render_template('register.html', user = user)

@app.route('/askquestions', methods = ["POST", "GET"])
def askquestions():
    user = get_current_user()
    db = getDatabase()
    # Getting the input from the question and name of teacher and sending them to the database to be stored
    if request.method == "POST":
        question = request.form['question']
        teacher = request.form['teacher']
        db.execute('insert into questions (question_text, asked_by_id, teacher_id) values (?,?,?)', [question, user['id'], teacher])
        db.commit()
        return redirect(url_for('index')) # this is the functions name which will be navigate to and this will take us to the homepage of this application
    # This is getting all from users where teacher = 1 i.e all teachers
    teacher_cursor = db.execute('select * from users where teacher = 1')
    allteachers = teacher_cursor.fetchall()
    return render_template("askquestions.html", user = user, allteachers = allteachers)


@app.route('/unansweredquestions')
def unansweredquestions():
    user = get_current_user()
    db = getDatabase()
    question_cursor = db.execute("select questions.id, questions.question_text,\
    users.name from questions join users on users.id = questions.asked_by_id \
     where questions.answer_text is null and questions.teacher_id = ?", [user['id']]) 
    allquestions = question_cursor.fetchall()
    return render_template("unansweredquestions.html", user = user, allquestions = allquestions)

@app.route('/answerquestions/<question_id>', methods = ["POST", "GET"])
def answerquestions(question_id): # we are taking in a question_id as parameter so that we can receive the actual id of the question when a request or click is made
    user = get_current_user()
    db = getDatabase()
    if request.method == "POST":
        answer = request.form['answer']
        db.execute('update questions set answer_text =? where id = ?', [answer, question_id])
        db.commit()
        return redirect('unansweredquestions')

    question_cursor = db.execute("select id, question_text from questions where id = ?", [question_id])
    question = question_cursor.fetchone()
    return render_template("answerquestions.html", user = user, question = question)


@app.route('/allusers', methods = ["POST", "GET"])
def allusers():
    user = get_current_user()
    db = getDatabase()
    allusers_fetched = db.execute('select * from users')
    allusers = allusers_fetched.fetchall()

    return render_template('allusers.html', user=user, allusers = allusers)

@app.route('/addTeacher/<int:id>', methods=["POST", "GET"])
def addTeacher(id):
    user = get_current_user()
    if request.method == "GET":
        db = getDatabase()
        db.execute("update users set teacher = 1 where id = ? ", [id])
        commit_database = db.commit()
        return redirect(url_for('allusers'))
    return render_template('allusers.html', user = user)



@app.route('/logout') 
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if (__name__) == "__main__": # This checks if name matches the main module of the programme, 
    app.run(debug = True) # and if it does we want it to run true, we can then run the function and also we run the application in debug mode to help us when there is error
