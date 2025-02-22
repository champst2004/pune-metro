from flask import Flask, render_template, request, redirect, flash
from db import db, cursor

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/view_cards")
def view_cards():
    cursor.execute("SELECT * FROM cards")
    cards = cursor.fetchall()
    return render_template("view_cards.html", cards=cards)

@app.route("/issue_card", methods=["GET", "POST"])
def issue_card():
    if request.method == "POST":
        name = request.form["name"]
        prn = request.form.get("prn", None)  # If empty, store as NULL
        cardno = request.form["cardno"]

        cursor.execute("SELECT * FROM students WHERE prn = %s", (prn,))
        is_student = cursor.fetchone()

        if is_student:
            cursor.execute("INSERT INTO cards (id, name, cardno, balance) VALUES (%s, %s, %s, 0)",
                           (prn, name, cardno))
        else:
            cursor.execute("INSERT INTO cards (id, name, cardno, balance) VALUES (NULL, %s, %s, 0)",
                           (name, cardno))

        db.commit()
        flash("Metro Card Issued Successfully!", "success")
        return redirect("/view_cards")

    return render_template("issue_card.html")

@app.route("/book_ticket", methods=["GET", "POST"])
def book_ticket():
    cursor.execute("SELECT * FROM stations")
    stations = cursor.fetchall()
    fare = None
    error = None

    if request.method == "POST":
        cardno = request.form.get("cardno", None)
        start_station = int(request.form["start_station"])
        end_station = int(request.form["end_station"])
        discount = 0

        # Check if user has a card and determine discount
        if cardno:
            cursor.execute("SELECT id, balance FROM cards WHERE cardno = %s", (cardno,))
            card = cursor.fetchone()

            if card:
                if card["id"]:  # If PRN exists, it's a student card
                    discount = 25
                else:
                    discount = 10
            else:
                error = "Invalid card number!"
                return render_template("book_ticket.html", stations=stations, error=error)

        # Calculate fare based on number of stations traveled
        station_diff = abs(start_station - end_station)
        fare = min(30, station_diff * 10)
        final_fare = fare - (fare * discount / 100)

        # If user has a card, check balance and deduct fare
        if cardno:
            if card["balance"] < final_fare:
                error = "Insufficient balance! Please recharge your card."
                return render_template("book_ticket.html", stations=stations, error=error)

            # Deduct balance from card
            new_balance = card["balance"] - final_fare
            cursor.execute("UPDATE cards SET balance = %s WHERE cardno = %s", (new_balance, cardno))

            # Insert transaction for fare deduction
            cursor.execute("INSERT INTO transactions (cardno, type, amount) VALUES (%s, 'Fare', %s)", (cardno, final_fare))

        # Insert ride into rides table
        cursor.execute("INSERT INTO rides (cardno, source_station, destination_station, fare) VALUES (%s, %s, %s, %s)", 
                       (cardno, start_station, end_station, final_fare))

        db.commit()

        flash("Ticket booked successfully!", "success")
        return redirect("/ride_history")

    return render_template("book_ticket.html", stations=stations, fare=fare, error=error)


@app.route("/ride_history")
def ride_history():
    cursor.execute("SELECT * FROM rides")
    rides = cursor.fetchall()
    return render_template("ride_history.html", rides=rides)

if __name__ == "__main__":
    app.run(debug=True)
