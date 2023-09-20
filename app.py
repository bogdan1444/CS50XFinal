from flask import Flask, redirect, request, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, login_user, LoginManager, logout_user, current_user, UserMixin

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

if __name__=="__main__":
  app.run(debug=True)