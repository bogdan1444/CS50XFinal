from flask import Flask, redirect, request, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, login_user, LoginManager, logout_user, current_user, UserMixin
from sqlalchemy.sql import func
from datetime import datetime

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
app.config['SECRET_KEY'] = 'Secret'

# initialize the app with the extension
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String, nullable=False)
    def is_authenticated(self):
        return True 
class Mail(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sender: Mapped[str] = mapped_column(String)
    receiver: Mapped[str] = mapped_column(String)
    subject : Mapped[str] = mapped_column(String)
    message: Mapped[str] = mapped_column(String)
    timestamp: Mapped[timestamp] = mapped_column(DateTime, default= datetime.now())
    


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#create db - DATABASE
with app.app_context():
    db.create_all()
  

@app.route("/")
def index():
    return render_template("user/index.html")

@app.route("/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return render_template("user/list.html", users=users)

@app.route("/users/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        if( not request.form["username"] or not request.form["password"]):
            return render_template("user/create.html", message = "insert username or password")
        if ((request.form["password"]) != (request.form["confirm"])):
            return render_template("user/create.html", message="password do not match")
        try:
            if User.query.filter_by(username =request.form["username"]).first() :
                return render_template("user/create.html", message="username already exists")
            user = User(
                username=request.form["username"],
                email=request.form["email"],
                password = generate_password_hash(request.form["password"])
            )
        except:
            return render_template("user/create.html", message="username already exists")
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user_detail", id=user.id))

    return render_template("user/create.html")

@app.route("/user/<int:id>")
def user_detail(id):
    user = db.get_or_404(User, id)
    # print(type(user))
    # print(user.username)
    # usr = User.query.filter_by(username=user.username).first()
    # print(usr.password)
    # print(check_password_hash(User.query.filter_by(username=user.username).first().password ,"qw") )
    return render_template("user/detail.html", user=user)

@app.route("/user/<int:id>/delete", methods=["GET", "POST"])
def user_delete(id):
    user = db.get_or_404(User, id)

    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("user_list"))

    return render_template("user/delete.html", user=user)


@app.route("/login", methods=["POST","GET"])
def login():
    if(request.method == "GET"):
        return render_template("user/login.html")
    else:
        try:
            username = request.form["username"]
            password = request.form["password"]
            # print(username) # print username, password
            # print(password)
            if(not username or not password):
                return render_template("user/login.html")
            #check password and username 
            if(( not username==User.query.filter_by(username=username).first().username) or (not check_password_hash( User.query.filter_by(username=username).first().password,password))):
                print("EROR username incorect or  password incorect")
                return render_template("user/login.html")
            # user = User.query.filter_by
        except:
            print("Error")
            return render_template("user/login.html")
        
        user = User.query.filter_by(username=username).first()
        # print(user)
        login_user(user, remember=True)
        # print(current_user)
        return render_template("user/dashboard.html", user = current_user)
        

@app.route("/logout", methods = ["GET","POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if(current_user):
        user = current_user
    return render_template("user/dashboard.html", user= user)


@app.route('/sent', methods=["GET", "POST"])
@login_required
def sent():
    if request.method=="GET":
        sender_email = current_user.email
        print(Mail.query.all())
        return render_template("user/sent.html")
    else:
        email_to = request.form.get("email_to")
       
        senders_emails = []
        for user in User.query.all():
            senders_emails.append(user.email)
        print(senders_emails) 
        #check the reciveiever
        if  not email_to in senders_emails:
            Erormsg = "Receiver email not found "
            print(Erormsg)
            return render_template("user/sent.html", error=Erormsg)

        subject = request.form.get("subject")
        message = request.form.get("message")
        print(email_to, subject,message)
        mail = Mail(
            sender = current_user.email,
            receiver = email_to,
            subject = subject,
            message = message,
            timestamp = datetime.now()
        )
        db.session.add(mail)
        db.session.commit()
        return render_template("user/sent.html")
    

@app.route("/inbox", methods=["GET", "POST"])
@login_required
def inbox():
    user = current_user.username
    if(request.method=="GET"):
        return render_template("user/inbox.html", user= user)
    else:
        # types_email = ["sended", "received", "all"]
        print(request.form.get("sent"))
        print(request.form.get("received"))
        mails = []
        if( request.form.get("sent") and request.form.get("received")):
            print("show all emails")
            mails = show_emails("all")
            # return render_template("user/inbox_2.html",mails=mails)
        elif(request.form.get("received")):
            print("show all emails received")
            mails = show_emails("received")
        elif(request.form.get("sent")):
            # print("show sended emails")
            mails = show_emails("sent")
        else:
            print("Select what email you want to see")
        # show_emails("sent")
        
        return render_template("user/inbox.html", mails=mails)
    



@login_required
def show_emails(type_of_mail):
    # print(Mail.query.order_by(Mail.timestamp.desc()).all())
    if(type_of_mail=="sent"):
        mails = Mail.query.filter_by(sender=current_user.email).order_by(Mail.timestamp.desc()).all()
    # print(mails)
    # print(type(mails)
            
        for mail in mails:
            mail.sender = "you"
            mail.receiver_name = User.query.filter_by(email=mail.receiver).first().username
        # print(mail.sender)
    # print(len(mails))
    elif(type_of_mail=="received"):
        mails = Mail.query.filter_by(receiver=current_user.email).order_by(Mail.timestamp.desc()).all()
        for mail in mails:
            mail.receiver = "you"
            mail.sender_name = User.query.filter_by(email=mail.sender).first().username
        print(mails)
    elif(type_of_mail=="all"):
        mails_s = Mail.query.filter_by(sender=current_user.email).order_by(Mail.timestamp.desc()).all()
        for mail in mails_s:
            mail.sender = "you"
        mails_r = Mail.query.filter_by(receiver=current_user.email).order_by(Mail.timestamp.desc()).all()
        for mail in mails_r:
            mail.sender = "you"
        mails = mails_s + mails_r
        
    indexes = []
    for i in range(len(mails)):
        indexes.append(i+1)
    for i in range(len(indexes)):
        mails[i].index = indexes[i]
    # for mail in mails:
        # print(mail.index)
    
    return mails



if __name__=="__main__":
  app.run(debug=True)