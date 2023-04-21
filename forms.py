"""Module containing the forms used in this project."""
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, HiddenField
from wtforms.validators import URL, InputRequired


# # WTForm
class CreatePostForm(FlaskForm):
    """Form for creating og editing a blog post. Fields: title, subtitle, img_url, body, preview, submit."""
    # The form.hidden_tag() template argument generates a hidden field that
    # includes a token that is used to protect the form against CSRF attacks...?
    # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
    hidden_field = HiddenField()
    title = StringField("Blog Post Title", validators=[InputRequired()])
    subtitle = StringField("Subtitle", validators=[InputRequired()])
    img_url = StringField("Blog Image URL", validators=[InputRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[InputRequired()])
    # preview = SubmitField("Preview")
    submit = SubmitField("Submit Post")


class RegisterForm(FlaskForm):
    """Register form (to register a new user). Fields: email, password, name, submit."""
    email = StringField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    name = StringField("Name", validators=[InputRequired()])
    submit = SubmitField("Sign me up!")


class LogInForm(FlaskForm):
    """Log-in form. Fields: email, password, submit."""
    email = StringField("Email", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])
    submit = SubmitField("Log in")


class CommentForm(FlaskForm):
    """Comment form (to make a comment on a blog posts). Fields:, comment_text, submit."""
    comment_text = CKEditorField("Comment", validators=[InputRequired()])
    submit = SubmitField('Submit comment')
