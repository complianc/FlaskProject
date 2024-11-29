from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuring SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///equipment.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Database Model
class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration_no = db.Column(db.String(50), nullable=False)
    instrument_name = db.Column(db.String(100), nullable=False)
    maker_manufacturer = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    instrument_sr_no = db.Column(db.String(50), nullable=False)
    range = db.Column(db.String(100), nullable=True)
    resolution_lc = db.Column(db.String(100), nullable=True)
    accuracy = db.Column(db.String(100), nullable=True)
    owner_section_group = db.Column(db.String(100), nullable=True)
    instrument_location = db.Column(db.String(100), nullable=True)
    calibration_due = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False)

# Home Route
@app.route("/")
def home():
    return render_template("home.html")

# Add Equipment Route
@app.route("/add", methods=["GET", "POST"])
def add_equipment():
    if request.method == "POST":
        registration_no = request.form["registration_no"]
        instrument_name = request.form["instrument_name"]
        maker_manufacturer = request.form["maker_manufacturer"]
        model = request.form["model"]
        instrument_sr_no = request.form["instrument_sr_no"]
        range = request.form["range"]
        resolution_lc = request.form["resolution_lc"]
        accuracy = request.form["accuracy"]
        owner_section_group = request.form["owner_section_group"]
        instrument_location = request.form["instrument_location"]
        calibration_due = datetime.strptime(request.form["calibration_due"], "%Y-%m-%d").date()
        status = request.form["status"]

        new_equipment = Equipment(
            registration_no=registration_no,
            instrument_name=instrument_name,
            maker_manufacturer=maker_manufacturer,
            model=model,
            instrument_sr_no=instrument_sr_no,
            range=range,
            resolution_lc=resolution_lc,
            accuracy=accuracy,
            owner_section_group=owner_section_group,
            instrument_location=instrument_location,
            calibration_due=calibration_due,
            status=status
        )

        db.session.add(new_equipment)
        db.session.commit()
        return redirect("/dashboard")

    return render_template("add_equipment.html")

# Dashboard Route
@app.route("/dashboard")
def dashboard():
    equipment = Equipment.query.all()
    return render_template("dashboard.html", equipment=equipment)

# View Equipment List Route
@app.route("/view-list")
def view_list():
    equipment = Equipment.query.all()
    return render_template("view_list.html", equipment=equipment)

# Run the application
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
    
   