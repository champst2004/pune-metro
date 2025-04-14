from flask import Flask, render_template, request, redirect, flash, session
from db import get_db
import mysql.connector

app = Flask(__name__)
app.secret_key = "hehedbms"

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login2", methods=["GET", "POST"])
def login2():
    db, cursor = get_db()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        cursor.execute("SELECT * FROM users WHERE name=%s AND email=%s", (name, email))
        user_data = cursor.fetchone()

        if user_data:
            userid = user_data["userID"]
            session["userid"] = userid
            flash("Login successful!", "success")
            return redirect("/user")
        else:
            flash("Credentials do not match", "warning")

    return render_template("login2.html")

@app.route("/user")
def user():
    if "userid" not in session:
        flash("Please login first", "warning")
        return redirect("/login2")

    return render_template("user.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    db, cursor = get_db()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        usertype = request.form['usertype']

        try:
            if usertype == "Student":
                cursor.execute("SELECT * FROM students WHERE email = %s", (email,))
                student = cursor.fetchone()
                if not student:
                    flash("Email not found in MITWPU student database!", "danger")
                    return render_template("signup.html")

            cursor.execute("INSERT INTO users (name, email, usertype) VALUES (%s, %s, %s)",
                           (name, email, usertype))
            db.commit()
            flash("User registered successfully!", "success")
            return redirect('/login')

        except mysql.connector.IntegrityError:
            flash("Email already exists or is invalid!", "danger")
        finally:
            cursor.close()
            db.close()

    return render_template("signup.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    db, cursor = get_db()
    if request.method == "POST":
        id = request.form["id"]
        passw = request.form["passw"]

        cursor.execute("SELECT * FROM admin WHERE adminid=%s AND password=%s", (id, passw))
        admin_data = cursor.fetchone()

        if admin_data:
            session["admin"] = id
            flash("Login successful!", "success")
            return redirect("/admin_dashboard")
        else:
            flash("Invalid credentials!", "danger")

    return render_template("admin.html")

@app.route("/admin_dashboard")
def admin_dashboard():
    db, cursor = get_db()
    if "admin" not in session:
        flash("Please log in as admin first!", "warning")
        return redirect("/admin")

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    cursor.execute("SELECT * FROM cards")
    cards = cursor.fetchall()

    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()

    return render_template("admin_dashboard.html", users=users, cards=cards, transactions=transactions)


@app.route("/delete/<int:no>")
def delete(no):
    db, cursor = get_db()
    try:
        cursor.execute("DELETE FROM users WHERE userid = %s", (no,))
        db.commit()
        flash("Account deleted successfully!", "success")
    except mysql.connector.Error as e:
        db.rollback()
        flash(f"Failed to delete user: {str(e)}", "danger")
    return redirect("/admin_dashboard")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    flash("Logged out successfully.", "info")
    return redirect("/admin")

@app.route("/booking", methods=["GET", "POST"])
def booking():
    db, cursor = get_db()
    cursor.execute("SELECT stationID, name FROM stations")
    stations = cursor.fetchall()

    if request.method == "POST":
        depart_id = int(request.form["departure"])
        arrival_id = int(request.form["arrival"])
        card_id = request.form.get("cardID")

        # Fare calculation (simple version, adjust as needed)
        distance = abs(depart_id - arrival_id)
        amount = 10 + distance * 2  # Example: base fare + per-station

        try:
            cursor.execute("""
                INSERT INTO transactions (cardID, departID, arrivalID, amount)
                VALUES (%s, %s, %s, %s)
            """, (card_id if card_id else None, depart_id, arrival_id, amount))
            db.commit()
            flash("Ticket booked successfully!", "success")
        except Exception as e:
            db.rollback()
            flash(f"Booking failed: {str(e)}", "danger")

    return render_template("booking.html", stations=stations)

@app.route("/issue_card", methods=["GET", "POST"])
def issue_card():
    db, cursor = get_db()

    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            dep = request.form["dep"]

            cursor.execute("SELECT userid FROM users WHERE email = %s", (email,))
            user_row = cursor.fetchone()

            cursor.execute("SELECT usertype FROM users WHERE email = %s", (email,))
            type_row = cursor.fetchone()

            if not user_row or not type_row:
                flash("User not found!", "danger")
                return render_template("issue_card.html")

            userid = user_row["userid"]
            cardtype = type_row["usertype"]

            cursor.execute(
                "INSERT INTO cards (userid, cardtype, balance) VALUES (%s, %s, %s)",
                (userid, cardtype, dep)
            )
            db.commit()
            flash("Card issued successfully!", "success")

        except mysql.connector.Error as e:
            db.rollback()
            flash(f"Database Error: {e}", "danger")

        finally:
            cursor.close()
            db.close()

    return render_template("issue_card.html")

@app.route("/balance")
def balance():
    db, cursor = get_db()
    userid = session["userid"]

    cursor.execute("call get_balance(%s)", (userid, ))
    remainBal = cursor.fetchone()

    return render_template("balance.html", bal = remainBal)

@app.route("/topup", methods=["GET", "POST"])
def topup():
    db, cursor = get_db()

    if request.method == "POST":
        cardid = request.form["cardid"]
        amount = request.form["amount"]

        try:
            cursor.execute("SELECT balance FROM cards WHERE cardID = %s", (cardid,))
            card = cursor.fetchone()
            if not card:
                flash("Card ID not found!", "danger")
            else:
                cursor.execute("UPDATE cards SET balance = balance + %s WHERE cardID = %s", (amount, cardid))
                db.commit()
                flash("Balance successfully added!", "success")
        except Exception as e:
            db.rollback()
            flash(f"Error: {e}", "danger")

    return render_template("topup.html")

@app.route("/user_trans")
def user_trans():
    db, cursor = get_db()

    if "userid" not in session:
        flash("Please log in first.", "warning")
        return redirect("/login2")

    userid = session["userid"]
    cursor.execute("SELECT cardID FROM cards WHERE userID = %s", (userid,))
    card = cursor.fetchone()

    if not card:
        flash("No card found for this user.", "warning")
        return render_template("user_trans.html", transactions=[])

    cardid = card["cardID"]
    cursor.execute("""
        SELECT t.transID, t.cardID, s1.name AS depart_station, s2.name AS arrival_station,
               t.amount, t.timed
        FROM transactions t
        JOIN stations s1 ON t.departID = s1.stationID
        JOIN stations s2 ON t.arrivalID = s2.stationID
        WHERE t.cardID = %s
        ORDER BY t.timed DESC
    """, (cardid,))
    transactions = cursor.fetchall()

    return render_template("user_trans.html", transactions=transactions)

if __name__ == "__main__":
    app.run(debug=True)