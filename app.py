from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from passlib.hash import sha256_crypt




app = Flask(__name__)
app.config['SECRET_KEY'] = '493753003b7f9dc144cf6de900193330'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site1.db'
bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

 


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60),nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
        


posts = [
    {
        'author' : 'Realdo Beja',
        'title' : 'Blog post 1',
        'content' : 'First post content',
        'date_posted' : '20 November 2020'
    },
    {
        'author' : 'Endi Sukaj',
        'title' : 'Blog post 2',
        'content' : 'Second post content',
        'date_posted' : '20 November 2020'
    }
]


@app.route("/")
@app.route("/home")
def home():
    
    return render_template('home.html', posts=posts, title='Home')

@app.route("/about")
def about():
        
    return render_template('about.html', posts=posts, title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        username_already_in_db = User.query.filter_by(username=form.username.data).first()
        email_already_in_db =  User.query.filter_by(email=form.email.data).first()

        if username_already_in_db or email_already_in_db:
            flash(f'Credentials already in use.', 'error')    
            return redirect(url_for('register'))
        else:
            add_to_table_user(form)
            return redirect(url_for('login'))
        #if email_already_in_db:
        #    flash(f'Email already in use.', 'error')    
        #    return redirect(url_for('register'))
        #else:
        #    add_to_table_user(form)
        
    return render_template('register.html', title='Register', form=form)

def add_to_table_user(form):
    secure_password = sha256_crypt.encrypt(str(form.password.data))
    user = User(username=form.username.data, email=form.email.data, password=secure_password)
    db.session.add(user)
    db.session.commit()
    flash(f'Account created!', 'success')
    
    return


    
@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)






if __name__ == "__main__":
    app.run(debug=True)