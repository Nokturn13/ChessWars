from storage import not_allowed
from flask import Flask, Request, Response, redirect, render_template, request
from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import escape

def clean(arg):
    for i in arg:
        clean_object = str(i).replace("(", "").replace(")", "").split(",")
        for i in clean_object:
            clean_object[clean_object.index(i)] = i.removesuffix("'").removeprefix("'").removeprefix(" '")
        return clean_object

app = Flask(__name__)
engine = create_engine("sqlite:///Main.sqlite", echo=True, future=True)


@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":

        Username = request.form.get("Username")
        Email = request.form.get("Email")
        Password = request.form.get("Password")
        HashPassword = generate_password_hash(Password)
        sqlstring = f"""SELECT * FROM Main WHERE "User"='{Username}';"""

        with engine.connect() as conn:
            selected_object = conn.execute(text(sqlstring))
            conn.commit()
            # should use REGEX
            clean_object = clean(selected_object)
            print(clean_object)
            
            try:
                not_allowed.index(clean_object[0])
                return "Username Not valid"
            except:
                if clean_object == None:

                    sqlstring = f"""INSERT INTO Main (User, Email, Passwords) VALUES ('{Username}', '{Email}', '{HashPassword}');"""


                    with engine.connect() as conn:
                        conn.execute(text(sqlstring))
                        conn.commit()
                    Site_url = request.base_url

                    return redirect(f"{Site_url}Users/{Username}")
                else:
                    return "Usename Already Taken"
    else:
        return render_template("Home.html")



@app.route("/login", methods=['POST','GET'])
def login():
    if request.method == "POST":

        Username = request.form.get("Username")
        Email = request.form.get("Email")
        Password = request.form.get("Password")

        sqlstring = f"""SELECT * FROM Main WHERE "User"='{Username}';"""

        with engine.connect() as conn:
            selected_object = conn.execute(text(sqlstring))
            conn.commit()
            # should use REGEX
            clean_object = clean(selected_object)

        if clean_object != None:
            if clean_object[1] == Email:
                if check_password_hash(clean_object[2], Password) == True:
                    return "Loged In"
                else:
                    return render_template('Error.html', error="Password")
            else:
                return render_template('Error.html', error="Email")
        else:
            return render_template("Error.html", error="Account")
        
    else:
        return render_template("login.html")

@app.route("/Users/<name>")
def name(name=None):
    return render_template('Userpage.html', name=name)

@app.route("/Chess")
def chessground():
    return render_template('ChessGround.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)