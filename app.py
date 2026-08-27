from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3, os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "bloodbridge-demo-secret")
DB = os.path.join(os.path.dirname(__file__), "bloodbridge.db")

def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS donors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        blood_group TEXT NOT NULL,
        city TEXT NOT NULL,
        phone TEXT NOT NULL,
        available INTEGER DEFAULT 1
    );
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT NOT NULL,
        blood_group TEXT NOT NULL,
        city TEXT NOT NULL,
        hospital TEXT NOT NULL,
        units INTEGER NOT NULL,
        contact TEXT NOT NULL,
        status TEXT DEFAULT 'Open'
    );
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    conn=db()
    donors=conn.execute("SELECT * FROM donors WHERE available=1 ORDER BY id DESC LIMIT 6").fetchall()
    requests=conn.execute("SELECT * FROM requests WHERE status='Open' ORDER BY id DESC LIMIT 6").fetchall()
    conn.close()
    return render_template("index.html", donors=donors, requests=requests)

@app.route("/donors")
def donors():
    group=request.args.get("blood_group","").strip()
    city=request.args.get("city","").strip()
    query="SELECT * FROM donors WHERE available=1"
    params=[]
    if group:
        query+=" AND blood_group=?"; params.append(group)
    if city:
        query+=" AND lower(city)=lower(?)"; params.append(city)
    query+=" ORDER BY id DESC"
    conn=db(); rows=conn.execute(query,params).fetchall(); conn.close()
    return render_template("donors.html", donors=rows, group=group, city=city)

@app.route("/add-donor", methods=["GET","POST"])
def add_donor():
    if request.method=="POST":
        data=[request.form.get(k,"").strip() for k in ("name","blood_group","city","phone")]
        if not all(data):
            flash("Please fill all donor details.", "error")
            return redirect(url_for("add_donor"))
        conn=db()
        conn.execute("INSERT INTO donors(name,blood_group,city,phone) VALUES(?,?,?,?)", data)
        conn.commit(); conn.close()
        flash("Donor registered successfully!", "success")
        return redirect(url_for("donors"))
    return render_template("add_donor.html")

@app.route("/request-blood", methods=["GET","POST"])
def request_blood():
    if request.method=="POST":
        fields=("patient_name","blood_group","city","hospital","units","contact")
        data={k:request.form.get(k,"").strip() for k in fields}
        if not all(data.values()) or not data["units"].isdigit() or int(data["units"]) < 1:
            flash("Please enter valid request details.", "error")
            return redirect(url_for("request_blood"))
        conn=db()
        conn.execute("""INSERT INTO requests(patient_name,blood_group,city,hospital,units,contact)
                        VALUES(?,?,?,?,?,?)""",
                     (data["patient_name"],data["blood_group"],data["city"],data["hospital"],int(data["units"]),data["contact"]))
        conn.commit(); conn.close()
        flash("Blood request posted successfully!", "success")
        return redirect(url_for("home"))
    return render_template("request_blood.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

init_db()

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)), debug=False)
