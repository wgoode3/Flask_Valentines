from flask import Flask, render_template, request, redirect
from mysqlconnection import MySQLConnector

app = Flask(__name__)
mysql = MySQLConnector(app, "valentines")

@app.route("/")
def index():
	users = mysql.query_db("SELECT * FROM users;")
	return render_template("index.html", users=users)

@app.route("/user", methods=["POST"])
def user():
	query = "INSERT INTO users (name, email, created_at, updated_at) VALUES (:name, :email, NOW(), NOW());"
	mysql.query_db(query, request.form)
	return redirect("/")

@app.route("/user/<id>")
def user_page(id):
	user = mysql.query_db("SELECT * FROM users WHERE id={};".format(id))
	users = mysql.query_db("SELECT * FROM users;")
	sent = mysql.query_db("SELECT message, valentines.created_at, user2s.name AS recipient, users.name AS sender FROM valentines JOIN users ON valentines.sent_id=users.id JOIN users AS user2s ON valentines.received_id=user2s.id WHERE users.id = {};".format(id))
	received = mysql.query_db("SELECT message, valentines.created_at, user2s.name AS recipient, users.name AS sender FROM valentines JOIN users ON valentines.sent_id=users.id JOIN users AS user2s ON valentines.received_id=user2s.id WHERE user2s.id = {};".format(id))
	return render_template("user.html", user=user, users=users, sent=sent, received=received)

@app.route("/valentine/<id>", methods=["POST"])
def valentine(id):
	query = "INSERT INTO valentines (message, created_at, updated_at, sent_id, received_id) VALUES(:message, NOW(), NOW(), {}, :received_id);".format(id)
	mysql.query_db(query, request.form)
	return redirect("/user/{}".format(id))

app.run(debug=True)