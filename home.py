from flask import Flask, render_template,request, redirect, url_for, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
app = Flask(__name__)
PASSWORD = os.environ.get('PASSWORD')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:'+PASSWORD+'@localhost/incogmaths'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY']='secret'

db = SQLAlchemy(app)

class Problems(db.Model):
    '''
    sno, name phone_num, msg, date, email
    '''
    Serial_no = db.Column(db.Integer, primary_key=True)
    Question = db.Column(db.String(120), nullable=False)
    image= db.Column(db.LargeBinary)
    Mobile = db.Column(db.String(12), nullable=False)
    Date = db.Column(db.Date, nullable=True)
    Email = db.Column(db.String(50), nullable=False)

class Contact(db.Model):
    '''
    sno, name phone_num, msg, date, email
    '''
    sno = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.String(120), nullable=False)
    mobile = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date)
    email = db.Column(db.String(50), nullable=False)



@app.route("/")
def home():
    return render_template('inc.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/post", methods = ['GET', 'POST'])
def post():
    if(request.method=='POST'):
        '''Add entry to the database'''
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        ques= request.form.get('ques')
        f=request.files['img']
        entry = Problems(Mobile = mobile, Question=ques, Date= datetime.now(),Email = email ,image=f.read())
        db.session.add(entry)
        db.session.commit()
        flash('Thankyou! we will contact you soon.')
        return redirect(url_for('post'))

    return render_template('questions.html')

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        '''Add entry to the database'''
        msg = request.form.get('message')
        email = request.form.get('email')
        mobile = request.form.get('phone')
        entry = Contact(mobile = mobile, msg=msg, date= datetime.now(),email = email)
        db.session.add(entry)
        db.session.commit()
        flash('Thankyou! we will contact you soon.')
        return redirect(url_for('contact'))

    return render_template('contact.html')

@app.route('/solution')
def solution():
    return render_template('solution1.html')

@app.route('/solution2')
def solution2():
    return render_template('solution2.html')

if __name__ == "__main__":
    app.run(debug=True)
