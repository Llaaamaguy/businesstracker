from flask import Flask, request, render_template
from replit import db
import arrow

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")


@app.route("/data", methods=["POST"])
def data():
  if request.method == "POST":
    time = arrow.now("US/Eastern").format("HH:mm")
    if not time in db:
      db[time] = 1
    else:
      newval = db[time] + 1
      db[time] = newval
  return {arrow.now("US/Eastern").format("MM-DD"): dict(db)}


@app.route("/clear", methods=["POST"])
def clear():
  db.clear()
  return "Cleared"


@app.route("/save", methods=["POST"])
def save():
  savedate = arrow.now("US/Eastern").format("MM-DD")
  fname = "saved_data/" + savedate + ".txt"
  with open(fname, "w") as f:
    for k, v in db.items():
      f.write(f"{k}: {v} \n")
  db.clear()
  return "Saved and cleared"

app.run(host="0.0.0.0", port=5000)