# A Blog built with Flask

THe blog is deployed here https://elisabeth.onrender.com. It loads very slowly. I don't know if 
it's my fault, or if it's because I'm using render's free solution.

My solution on day 69 of "100 Days of Code: The Complete Python Pro Bootcamp for 2023", 
a course made by Dr. Angela Yu. https://www.udemy.com/course/100-days-of-code/

---

### Through this project I have gained some knowledge and experience with:

- Flask - a micro web framework written in Python.
- SQLAlchemy, SQLite3 relational databases.
- User authentication with Flask-Login.
- Password salting and hashing, to store passwords in a secure way.
- Flask-WTF (WTForms) - a library that provides flexible web form validation and rendering.
- RESTful routing.
- HTML and Jinja2 templating.
- Bootstrap - a CSS framework for making responsive websites.

---

### Overview
- **On all pages:** A header with navigation bar, and a footer.
- **Home Page:** For each blog pos, the title, subtitle, author and publication date is shown.
- **Register page:** 
  - Form made with Flask-WTF, styled with the help of Flask-Bootstrap.
  - Password is salted and hashed before the user data is stored in the database.
- **Comment feature:** 
  - There is a comment field under each blog post. The comment text-field is made with Flask-CKEditor.
  - Implementation of Flask-Gravatar allows users who have a "gravatar"* to use this as their profile picture. Anonymous users get a random gravatar.
 
 *Gravatar images are used across the internet to provide an avatar image for blog commenters. Gravatar allows 
  you to change the image you use across the blog websites that use Gravatar http://gravatar.com/.
