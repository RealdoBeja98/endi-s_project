from flask import Flask, render_template, request, url_for, flash, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, CommentForm
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_login import LoginManager, login_required, UserMixin, login_user, current_user, logout_user



app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
app.config['SECRET_KEY'] = '493753003b7f9dc144cf6de900193330'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site1.db'
bcrypt = Bcrypt(app)
login_menager = LoginManager(app)
login_menager.login_view = 'login'
login_menager.login_message_category = 'info'

db = SQLAlchemy(app)

@login_menager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
 


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60),nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    user_comments = db.relationship('Comment', backref='author_comment', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_comments = db.relationship('Comment', backref='title_of_post', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
        
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    comment_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.body}')"


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    form = PostForm()
    comment_form = CommentForm()
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    if comment_form.validate_on_submit():
        id_of_post = get_post_id()
        print(id_of_post)
        reply = Comment(body=comment_form.comment_on_form.data, author_comment=current_user)
        db.session.add(reply)
        db.session.commit()
        
    replies = Comment.query.filter_by(author_comment=current_user).order_by(Comment.timestamp.desc()).all()  
    return render_template('home.html', posts=posts, title='Home', form=form, comment_form=comment_form, replies=replies)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        id_of_post = add_post_in_post_tab(form, current_user)
        def get_post_id(id_of_post):
            return id_of_post
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/about")
def about():
        
    return render_template('about.html', posts=posts, title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        username_already_in_db = User.query.filter_by(username=form.username.data).first()
        email_already_in_db =  User.query.filter_by(email=form.email.data).first()

        if username_already_in_db or email_already_in_db:
            flash(f'Credentials already in use.', 'danger')    
            return redirect(url_for('register'))
        else:
            add_to_table_user(form)
            return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)




    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful', 'danger')    
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():

        username_already_in_db = User.query.filter_by(username=form.username.data).first()
        email_already_in_db = User.query.filter_by(email=form.email.data).first()

        if username_already_in_db or email_already_in_db:
            flash(f'Credentials already in use.', 'danger')    
            return redirect(url_for('account'))
        else:
            update_username_email_on_user_table(form, current_user)
            return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account',
                           form=form)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been update', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
    form.content.data = post.content
    return render_template('create_post.html', title='Update post',
                            form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted", 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>", methods=['GET', 'POST'])
def user_posts(username):
    form = PostForm()
    comment_form = CommentForm()
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).all()
    if comment_form.validate_on_submit():
        reply = Comment(body=comment_form.comment_on_form.data, author_comment=current_user)
        db.session.add(reply)
        db.session.commit()
        
    replies = Comment.query.filter_by(author_comment=current_user).order_by(Comment.timestamp.desc()).all()  
    return render_template('user_post.html', form=form, replies=replies, posts=posts, user=user, comment_form=comment_form)


def add_post_in_post_tab(form, current_user):
    post = Post(title=form.title.data, content=form.content.data, author=current_user)
    db.session.add(post)
    db.session.commit()
    return post.id

def add_to_table_user(form):
    secure_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.username.data, email=form.email.data, password=secure_password)
    db.session.add(user)
    db.session.commit()
    flash(f'Account created!', 'success')
    return

def update_username_email_on_user_table(form, current_user):
    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()
    flash('your account has been updated', 'success')
    return

if __name__ == "__main__":
    app.run(debug=True)
