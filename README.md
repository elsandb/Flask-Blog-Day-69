# A Blog built with Flask
#### Jinja templates, Bootstrap, SQLAlchemy, 

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

### A few words and screenshots
  On all pages: A header with navigation bar, and a footer.
  
  #### Home Page
  For each blog pos, the title, subtitle, author and publication date is shown.
  
  <details>
    <summary> Screenshot</summary>
    
  ![Screenshot of the Home page.](/screenshot/21.04.2023%20Home.png)
    
  </details>
  
  
  #### Register page
  Form made with Flask-WTF, styled with the help of Flask-Bootstrap.
  Password is salted and hashed before the user data is stored in the database.
  
  <details>
    <summary>Screenshot</summary>
    
  ![Screenshot of the Register page](/screenshot/21.04.2023%20Register.png)
    
  </details>
  
  
  #### Comment feature
  There is a comment field under each blog post. The comment text-field is made with Flask-CKEditor.
  
  Implementation of Flask-Gravatar allows users who have a "gravatar"* to use this as their profile picture.
  Anonymous users get a random gravatar. On the screenshot below, _Anonymous_ and _qwe_ have written some nonsense.
  
  *Gravatar images are used across the internet to provide an avatar image for blog commenters. Gravatar allows 
  you to change the image you use across the blog websites that use Gravatar http://gravatar.com/.
  
  <details>
    <summary>Screenshot</summary>
  
  ![Screenshot of the comments-feature.](/screenshot/21.04.2023%20Comment.png)
  
  </details>
  
  More screenshots in https://github.com/elsandb/Flask-Blog-Day-69/tree/main/screenshot
