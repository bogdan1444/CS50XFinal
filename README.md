# YOUR PROJECT TITLE
#### Video Demo:  <URL https://youtu.be/vn-2h8E3Mnk>
#### Description:
This is prototype of a MAIL APP constructed using pyton, flask, flask_sqlalchemy
- Starting with register form with server validation for duplication user, null password, null username and email, password match, and client side validation for email input i.e. should contain @somethig;
      register form submits data via post method; function user_  create is called: after checking the content, in database is added the new user - this is done by creating a new instance of User class. this function returns a flash with "User created succesfull" if is okay.

- Log in form - contains server validation for not submitting and emy user fiedl or password fiel. This was constructed using logic expression in python

After submitting loging user is redirected to a index page where is greeted, the navbar shows now some new options availible for the curent_user: inbox, sent, change password, logout
   by clicking on the Mail app logo user is redirected to a page where user details are shown: username and email
   Mail imbox shows all the mail received/ sended in with last mails showed first on list. user has two filters tho show either sended , receiver or both types of mails at the same time
   this is done by accesing all the clss Mail objects filtering by receiver/sender to be current_user than displayng the contend in a html table; content is ordered by timestamp in decreasing order as so the last sended/received is first shown
   by clicking on see content on an email row user is redirected to a page where it can be seen the email content and can be sended a reply

   sent  - contains a form where user submits receiver email, subject and email content. submitting this form creates "under the hood" a new instance of Mail class which can be seen in inbox selecting the sended emails filter

   Change password - this page contains a form with old password, and a new password, new password confirmation. in back-end there are some logic code in python that is checkin for: correnctness od old password, and match between new password and new password confirmatio, also cheking that new password should not be empty string

this aplications is using flask_login log fuction to:
   -remember the current_user
   - acces some function only of the currend user is logged in by usend @login_required decorator on those specific functions

all the templates use the "layout.html" base. the mail ones are:
- create.html - form for submitting user credentials
- login.html - submitting login form
- index.html, detail.html - main page - with user details
- inbox.html, inbox_2.html - list all emails, list specific email content
- sent.html form for submitting sent email
- chpass - change the password form
some other like list.html, dashboard.html, delete.html are not necesarely part of the project, it is more for testing the app, and see what is going on;

All the python code is written in app.py with all the imported libraries, routes, and axiliary functions.
During constructing the app I use printing statemets to see what code, more of those remain there for debugging purposes
This project was build on the fundation of Finance Problem set frame but changeing entirely  the LoginManager, aand database, as i use flask_sqlaclemy and flask_login features instead of sessions and CS50 library. I chose to use these features for making for better understanding of login management
Flask Sqlalchemy documentation and stackoverflow.com where the main inspirations sources for writing the code for this project.

