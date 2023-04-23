import os
from dotenv import load_dotenv
from datetime import datetime as dt

from flask import abort, Flask, render_template, redirect, url_for, flash, Markup
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import AnonymousUserMixin, UserMixin, login_user, LoginManager, \
    login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

import config
from forms import RegisterForm, CreatePostForm, LogInForm, CommentForm
from safe_html import SafeHtml

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# Setup
app = Flask(__name__)
app.config.from_object(config.Config)
ckeditor = CKEditor(app)
Bootstrap(app)
db = SQLAlchemy(app)

# # Initialize LoginManager.
login_manager = LoginManager()
login_manager.init_app(app)

# # Initialize gravatar
gravatar = Gravatar(app,
                    size=80,           # Default avatar size
                    rating='g',         # Default rating
                    default='retro',    # Default type for unregistered emails
                    force_default=False,    # Build only default avatars (bool)
                    force_lower=False,      # Make email.lower() before build link
                    use_ssl=False,
                    base_url=None
                    )


# # Create tables
class User(db.Model, UserMixin, AnonymousUserMixin):
    """
    User model.

    Columns:, id, email, password_hash, name.

    Children: posts, comments.

    Ignore the warning 'unexpected arguments' when instantiating this class. See
    https://youtrack.jetbrains.com/issue/PY-28663/False-positive-unexpected-arguments-for-the-new-record-if-Flask-SQLAlchemy-is-used
    for more information.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    # Add relationships between the user and their posts (children). This will act like a List of BlogPost
    # objects attached to each User. "author" refers to the author property in the BlogPost class.
    posts = relationship('BlogPost', back_populates='author')
    # Add One-to-Many relationship between User (parent) and Comment (the user's comments = children).
    comments = relationship('Comment', back_populates='author')

    @property
    def is_admin(self):
        if self.get_id() == '1':
            return True
        else:
            return False


class BlogPost(db.Model):
    """
    Blog post model.

    Columns: id, title, subtitle, date, body, img_url.

    Parent: author.

    Child: post_comments.
    """
    __tablename__ = "blogposts"
    id = Column(Integer, primary_key=True)

    # Add relationship to the parent. Author (parent) = User. Foreign key = author_id = 'users.id'.
    # "users" in "users.id" refers to the tablename of User.
    author_id = Column(Integer, ForeignKey("users.id"))
    # "posts" refers to the posts attribute in the User class.
    author = relationship("User", back_populates="posts")

    title = Column(String(250), unique=True, nullable=False)
    subtitle = Column(String(250), nullable=False)
    date = Column(String(250), nullable=False)
    body = Column(db.Text, nullable=False)
    img_url = Column(String(250), nullable=False)

    # Add relationship to children (Comment, blog_post).
    post_comments = relationship('Comment', back_populates='parent_post')


class Comment(db.Model):
    """
    Blogpost-comments model.

    Columns:, id, text, date_time.

    Parents: parent_post, author.
    """
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(String(3000), nullable=False)
    date_time = Column(String(250), nullable=False)

    parent_post_id = Column(Integer, ForeignKey("blogposts.id"))
    parent_post = relationship('BlogPost', back_populates='post_comments')

    # Add relationship to the parent. Author (parent) = User. Foreign key = author_id = 'users.id'.
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship(argument='User', back_populates='comments')


with app.app_context():
    db.create_all()


# --------------------------- Access control --------------------------- #
def admin_only(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            print(f'{current_user.is_admin = }')
        except AttributeError:
            print('admin_only: AttributionError.')
        if current_user.is_anonymous or not current_user.is_admin:
            return abort(403)
        elif current_user.is_admin:
            print('admin_only: Decorator works.')
            return f(*args, **kwargs)
    return wrapper


@login_manager.user_loader
def load_user(user_id: int):
    if user_id is None:
        # print('load_user: no user_id')
        pass
    # print(f"load_user: {user_id = }")
    return db.session.get(entity=User, ident=user_id)


# --------------------------- Make safe HTML --------------------------- #
def mksafe(text: str) -> str:
    """
    Accept a string and remove potentially harmful html-code (tags or attributes) from it.
    Which html tags and attributes that are allowed is defined in the class SafeHtml.
    Use this function for all text that a user has typed in.
    :param text: str:   A string originating from user input.
    """
    sanitizer = SafeHtml()
    safe_text = sanitizer.clean(text)
    return safe_text


# ---------------------------- Routs --------------------------- #
@app.route('/')
def all_posts():
    posts = db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=posts)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    # [POST]
    if form.validate_on_submit():
        # If email in DB -> redirect to 'login' and show a flash-message:
        if db.session.query(User).filter_by(email=mksafe(form.email.data)).first():
            flash(message='You have already signed up with that email. Log in instead.', category='error')
            return redirect(url_for('login'))
        else:   # If email not in DB
            password_hash = generate_password_hash(
                password=mksafe(form.password.data),
                method='pbkdf2:sha256',
                salt_length=10)
            # Add the new_user user to the database:
            new_user = User(
                email=mksafe(form.email.data),
                password_hash=password_hash,
                name=mksafe(form.name.data))
            db.session.add(new_user)
            db.session.commit()
            # Log in new_user:
            login_user(user=new_user, remember=False, force=False, fresh=True)
            return redirect(url_for('all_posts'))
    # [GET]
    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    # [POST]
    if form.validate_on_submit():
        email = mksafe(form.email.data)
        user = db.session.query(User).filter_by(email=email).first()
        if not user:
            flash(Markup(f'{email} does not exist. <br> Please check your spelling and try again or sign up.'))
            return redirect(url_for('login'))
        elif not check_password_hash(user.password_hash, form.password.data):
            flash(Markup('The password is incorrect. <br> Please try again.'))
            return redirect(url_for('login'))
        else:  # If email exist and password is correct:
            login_user(user, remember=False)
            return redirect(url_for('all_posts'))
    # [GET]
    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('all_posts'))


@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def show_post(post_id: int):
    requested_post = db.session.get(entity=BlogPost, ident=post_id)
    comment_form = CommentForm()
    # [POST] Handle the submitted comment:
    if comment_form.validate_on_submit():
        # Not logged-in user -> redirect to login-page and show an appropriate message.
        if not current_user.is_authenticated:
            flash('You need to login or register to comment.')
            return redirect(url_for('login'))

        # Logged-in user -> Add comment to DB. Redirect to the current blogpost.
        new_comment = Comment(text=mksafe(comment_form.comment_text.data),
                              parent_post=requested_post,
                              date_time=dt.now().strftime('%m.%d.%Y %H:%M'),
                              author=current_user)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('show_post', post_id=post_id))

    # [GET]
    return render_template("post.html", post=requested_post, form=comment_form)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/new-post", methods=['GET', 'POST'])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=mksafe(form.title.data),
            subtitle=mksafe(form.subtitle.data),
            body=mksafe(form.body.data),
            img_url=mksafe(form.img_url.data),
            author=current_user,
            date=dt.today().strftime("%B %d, %Y"))
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=['GET', 'POST'])
@admin_only
def edit_post(post_id: int):
    post = db.session.get(BlogPost, ident=post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body)
    if edit_form.validate_on_submit():
        post.title = mksafe(edit_form.title.data)
        post.subtitle = mksafe(edit_form.subtitle.data)
        post.img_url = mksafe(edit_form.img_url.data)
        post.body = mksafe(edit_form.body.data)
        db.session.commit()
        return redirect(url_for("all_posts"))
    return render_template("make-post.html", form=edit_form, is_edit=True)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id: int):
    post_to_delete = db.session.get(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('all_posts'))


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000, debug=True)

# Todo:
#  Show comment field only if user is logged in.
#  Get email to work.
