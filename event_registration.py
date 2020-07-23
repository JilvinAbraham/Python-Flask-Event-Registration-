from flask import Flask,render_template,request,session,url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy
import datetime




app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class users(db.Model):

    _id = db.Column("id", db.Integer, primary_key = True)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    mob_number = db.Column(db.Integer) #Integer might not be able to store large numbers
    reg_type = db.Column(db.String(100))
    id_card = db.Column(db.LargeBinary, nullable = True) #have to look how to store images
    num_tickets = db.Column(db.Integer)
    date = db.Column(db.Date)
    reg_num = db.Column(db.Integer)


    num = 11700000
    def __init__(self,full_name,email,mob_number,reg_type,id_card,num_tickets):
        users.num+=1
        self.full_name = full_name
        self.email = email
        self.mob_number = mob_number
        self.reg_type = reg_type
        self.id_card = id_card
        self.num_tickets = num_tickets
        self.date = datetime.datetime.now()
        self.reg_num = users.num



@app.route("/")
@app.route("/register" , methods = ["GET","POST"])
def register():

    if (request.method == "POST"):
        email = request.form.get("email")

        found_user = users.query.filter_by(email = email).first()
        if(found_user):
            flash("You are already registered", "info")
            return render_template("register.html")
        else:
            full_name = request.form.get("full_name")

            mob_number = request.form.get("mob_number")
            reg_type = request.form.get("reg_type")
            id_card = request.files["id_card"]
            num_tickets = request.form.get("num_tickets")

            usr = users(full_name,email,mob_number,reg_type,id_card.read(),num_tickets)

            if(request.form.get("action")=="Preview"):
                params = {

                            "full_name": usr.full_name,
                            "email":usr.email,
                            "mob_number":usr.mob_number,
                            "reg_type":usr.reg_type,
                            # "id_card":usr.id_card,
                            "num_tickets":usr.num_tickets

                }
                return render_template("preview.html", param=params)

            elif(request.form.get("action")=="Submit"):
                db.session.add(usr)
                db.session.commit()
                flash("Your data has been Submitted")



    return render_template("register.html")

@app.route("/admin" , methods = ["GET","POST"])
def admin():

    rows = db.session.query(users).count()
    full_name = [users.query.all()[i].full_name for i in range(rows) ] #list
    email = [users.query.all()[i].email for i in range(rows) ]
    mob_number = [users.query.all()[i].mob_number for i in range(rows) ]
    reg_type = [users.query.all()[i].reg_type for i in range(rows) ]
    num_tickets = [users.query.all()[i].num_tickets for i in range(rows) ]

    params = {

                "full_name": full_name,
                "email":email,
                "mob_number":mob_number,
                "reg_type":reg_type,
                "num_tickets":num_tickets

            }
    return render_template("admin.html",param=params, row = rows)


if __name__== "__main__":
    db.create_all()
    app.run(debug = True)

