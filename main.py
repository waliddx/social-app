import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
from settings.uploads import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from dotenv import load_dotenv


def create_app():
    app = Flask(__name__)
    app.secret_key= os.getenv('SECRET_KEY')
    app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER

    bcrypt = Bcrypt(app)

    @app.route('/')
    def redirected():
        return redirect(url_for('home'))

    @app.route('/home')
    def home():
        if 'logged_in' in session:
            with sqlite3.connect('data.db') as conn:
                cr= conn.cursor()
                cr.execute("SELECT * FROM users WHERE email= ?", (session['email'],))
                data = cr.fetchone()
                fname = data[1]
        else:
            return redirect(url_for('login'))
        return render_template('home.html', title= 'Home', css= 'home', fname= fname)

    @app.route('/Login', methods=['GET', 'POST'])
    def login():
        msg= ""
        if request.method == 'POST':
            email = request.form['Email']
            password = request.form['Password']

            if password:

                with sqlite3.connect("data.db") as conn:
                    cr = conn.cursor()
                    cr.execute("SELECT * FROM users where email= ?", (email,))
                    data = cr.fetchone()
                    if data:
                        email_pass = data[4]
                        if bcrypt.check_password_hash(email_pass, password):
                            session['logged_in']= True
                            session['email']= data[3]
                            session.permanent = True
                            return redirect(url_for('home'))
                        else:
                            msg= "Invalid password"
                    else:
                        msg= 'invalid email, create new account'
                conn.close()

            else:
                msg= "enter your credentials first"

        return render_template('login.html', title= "Login or Signup", css='login', msg=msg)

    @app.route('/signup', methods=["GET", "POST"])
    def signup():

        msg = ""
        passed = ""
        if request.method == 'POST':

            firstname = request.form['firstName']
            lastname = request.form['lastName']
            email = request.form['Email']
            password = request.form['Password']
            cpassword = request.form['cPassword']

            if password:
                if password == cpassword:
                    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                    with sqlite3.connect('data.db') as db:
                        cr = db.cursor()
                        try:
                            cr.execute("INSERT INTO users (firstName, lastName, email, password) VALUES (?, ?, ?, ?)", (firstname, lastname, email, hashed_password,))
                            db.commit()
                            passed = "User registred successfully!"
                            return redirect(url_for('login', ))
                        except db.IntegrityError:
                            db.rollback()
                            passed= "Email already exists, try to login!"
                        except Exception as e:
                            msg = f"an error occured, try again later!"
                    db.close()
                
                else:
                    msg = "passwords doesn't match, try again." 
            else:
                msg= ' please enter a valid credentials'

        return render_template('signup.html', title= "Login or Signup", css='signup', error=msg, passed=passed)
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))

    def allowed_files(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    return app


if __name__ == "__main__":
    app= create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
