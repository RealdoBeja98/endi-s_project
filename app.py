from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from forms import RegistrationForm, LoginForm



app = Flask(__name__)
app.config['SECRET_KEY'] = '493753003b7f9dc144cf6de900193330'


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
        flash(f'Account created for { form.username.data }!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)






if __name__ == "__main__":
    app.run(debug=True)