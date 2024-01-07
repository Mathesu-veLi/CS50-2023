import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


# Ensure that responses are not cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Route to the "learn" page
@app.route("/learn")
def learn():
    return render_template("learn.html")

# Route to the "mission" page
@app.route("/mission")
def mission():
    return render_template("mission.html")

# Main route for the application, showing the portfolio of stocks
@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Retrieve the stocks and shares associated with the user
    values = db.execute("SELECT stock, shares FROM stocks WHERE user_id = ?", session["user_id"])

    # Retrieve the cash balance of the user
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    print(cash)

    current_prices = []
    holdings = 0

    # Calculate the current prices of the user's stocks and total holdings
    for i in values:
        price = lookup(i["stock"])["price"]
        current_prices.append(price)

        holdings += i["shares"] * price

    net = []
    roi = []

    # Calculate the net gain/loss and ROI for each stock
    for i in range(len(values)):
        hold = db.execute(
            "SELECT price FROM transactions WHERE action = 'buy' OR action = 'short' AND stock = ? AND user_id = ? ORDER BY time DESC LIMIT 1", values[i]["stock"], session["user_id"])
        roi.append(( (current_prices[i] - hold[0]["price"]) / hold[0]["price"]) * 100)
        if values[i]["shares"] > 0:
            net.append((current_prices[i] - hold[0]["price"]) * values[i]["shares"])
        else:
            net.append(-(hold[0]["price"] - current_prices[i]) * values[i]["shares"])

    print(net, roi)

    # Render the "index.html" template with data for display
    return render_template("index.html", values=values, cash=cash[0]["cash"], prices=current_prices, holdings=holdings, net=net, roi=roi)



# Route to buy shares of stock
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        symbol = request.form.get("symbol")
        if not symbol:
            flash("Must provide a stock symbol")
            return redirect("/buy")


        shares = request.form.get("shares")
        if not shares:
            flash("Must provide the number of shares")
            return redirect("/buy")

        symbol = symbol.upper()


        current_price = lookup(symbol)
        if current_price is None:
            flash("Enter a valid stock symbol")
            return redirect("/buy", 400)

        try:
            shares = int(shares)
        except:
            flash("Enter a valid number of shares")
            return redirect("/buy", 400)

        if shares <= 0:
            flash("Enter a valid number of shares")
            return redirect("/buy", 400)

        user_id = session["user_id"]
        current_balance = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        current_price = lookup(symbol)["price"]

        if current_price * shares > current_balance:
            flash("Insufficient funds")
            return redirect("/buy", 400)

        holdings = db.execute("SELECT * FROM stocks WHERE user_id = ?", user_id)
        exist = False

        for i in range(len(holdings)):
            if symbol in holdings[i]["stock"]:
                if holdings[i]["shares"] > 0:
                    x = db.execute("SELECT shares FROM stocks WHERE user_id = ? AND stock = ?", user_id, symbol)[0]["shares"]

                    db.execute("UPDATE stocks SET shares = ? WHERE user_id = ? AND stock = ?", x + shares, user_id, symbol)
                    exist = True
                else:
                    flash("You can't short and own a stock at the same time")
                    return redirect("/buy")

        if exist == False:
            db.execute("INSERT INTO stocks (user_id, stock, shares) VALUES(?, ?, ?)", user_id, symbol, shares)

        db.execute("INSERT INTO transactions (user_id, stock, shares, price, action) VALUES (?, ?, ?, ?, 'buy')", user_id, symbol, shares, current_price)

        db.execute("UPDATE users SET cash = ? WHERE id = ?", current_balance - (current_price * shares), user_id)

        return redirect("/")
    else:
        # Render the "buy.html" template when the HTTP method is GET
        return render_template("buy.html")

# Route to short shares of stock
@app.route("/short", methods=["GET", "POST"])
@login_required
def short():
    """Short shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            flash("Must provide a stock symbol")
            return redirect("/short")

        if not shares:
            flash("Must provide the number of shares")
            return redirect("/short")

        symbol = symbol.upper()

        current_price = lookup(symbol)
        if current_price is None:
            flash("Enter a valid stock symbol")
            return redirect("/short")

        try:
            shares = int(shares)
        except:
            flash("Enter a valid number of shares")
            return redirect("/short")

        if shares <= 0:
            flash("Enter a valid number of shares")
            return redirect("/short")

        user_id = session["user_id"]
        current_balance = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        current_price = lookup(symbol)["price"]

        holdings = db.execute("SELECT * FROM stocks WHERE user_id = ?", user_id)
        exist = False

        for i in range(len(holdings)):
            if symbol in holdings[i]["stock"]:
                if holdings[i]["shares"] < 0:
                    x = db.execute("SELECT shares FROM stocks WHERE user_id = ? AND stock = ?", user_id, symbol)[0]["shares"]

                    db.execute("UPDATE stocks SET shares = ? WHERE user_id = ? AND stock = ?", x - shares, user_id, symbol)
                    exist = True
                else:
                    flash("You can't short and own a stock at the same time")
                    return redirect("/short")

        if exist == False:
            db.execute("INSERT INTO stocks (user_id, stock, shares) VALUES(?, ?, ?)", user_id, symbol, -shares)

        db.execute("UPDATE users SET cash = ? WHERE id=?", current_balance + (current_price * shares), user_id)
        db.execute("INSERT INTO transactions (user_id, stock, shares, price, action) VALUES (?, ?, ?, ?, 'short')", user_id, symbol, shares, current_price)

        return redirect("/")
    else:
        # Render the "short.html" template when the HTTP method is GET
        return render_template("short.html")


# Route to display transaction history
@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Retrieve transaction history for the user from the database
    values = db.execute("SELECT stock, shares, time, action, price FROM transactions WHERE user_id = ? ORDER BY id DESC", session["user_id"])

    # Render the "history.html" template with transaction history data
    return render_template("history.html", values=values)


# Route for user login
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id (clear the session)
    session.clear()

    # Handle user login request via both GET and POST methods
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide a username")
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide a password")
            return redirect("/login")

        # Query the database for the provided username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and the provided password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            flash("Invalid username and/or password")
            return redirect("/login")

        # Remember the user who has logged in by storing their user_id in the session
        session["user_id"] = rows[0]["id"]

        # Redirect the user to the home page
        return redirect("/")

    # Handle GET request by rendering the "login.html" template
    else:
        return render_template("login.html")

# Route to log the user out
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id (clear the session)
    session.clear()

    # Redirect the user to the login form
    return redirect("/")

# Route to get a stock quote
@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        look = lookup(request.form.get("symbol"))
        if look == None:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", quote=look, price=usd(look["price"]))
    else:
        return render_template("quote.html")

# Route for user registration
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    session.clear()

    if request.method == "POST":

        username = request.form.get("username")
        if not username:
            return apology("must provide username", 400)

        password = request.form.get("password")
        if not password:
            return apology("must provide password", 400)

        elif password != request.form.get("confirmation"):
            return apology("password fields don't match")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) > 0:
            return apology("username already registered", 400)

        hashed_password = generate_password_hash(password)

        db.execute("INSERT INTO users (username, hash, cash) VALUES(?, ?, ?)", username, hashed_password, 10000)

        return redirect("/login")

    else:
        return render_template("register.html")

# Route to sell shares of stock
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    user_id = session["user_id"]
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            flash("Must provide a stock symbol")
            return redirect("/sell")

        if not shares:
            flash("Must provide the number of shares")
            return redirect("/sell")

        symbol = symbol.upper()
        shares = int(shares)

        current_price = lookup(symbol)

        if current_price is None:
            flash("Enter a valid stock symbol")
            return redirect("/sell")

        if shares <= 0:
            flash("Enter a valid number of shares")
            return redirect("/sell", 400)

        current_shares = db.execute("SELECT shares FROM stocks WHERE user_id = ? AND stock = ?", user_id, symbol)

        if len(current_shares) == 0:
            flash("You don't own that stock")
            return redirect("/sell", 400)

        current_shares = current_shares[0]["shares"]

        if shares > current_shares:
            flash("You don't own that many shares")
            return redirect("/sell", 400)

        current_balance = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        current_price = lookup(symbol)["price"]

        if current_shares - shares == 0:
            db.execute("DELETE FROM stocks WHERE stock = ? AND user_id = ?", symbol, user_id)

        else:
            db.execute("UPDATE stocks SET shares = ? WHERE user_id = ? AND stock = ?", current_shares - shares, user_id, symbol)

        db.execute("UPDATE users SET cash = ? WHERE id = ?", current_balance + (current_price * shares), user_id)

        db.execute("INSERT INTO transactions (user_id, stock, shares, price, action) VALUES (?, ?, ?, ?, 'sell')", user_id, symbol, shares, current_price)

        return redirect("/")
    else:
        current_stocks = db.execute("SELECT stock FROM stocks WHERE user_id=? AND shares>0", user_id)

        return render_template("sell.html", stocks=current_stocks)

# Route to cover (buy back) short shares of stock
@app.route("/cover", methods=["GET", "POST"])
@login_required
def cover():
    """Cover (buy back) short shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            flash("Must provide a stock symbol")
            return redirect("/cover")

        if not shares:
            flash("Must provide the number of shares")
            return redirect("/cover")

        symbol = symbol.upper()
        shares = int(shares)

        current_price = lookup(symbol)

        if current_price is None:
            flash("Enter a valid stock symbol")
            return redirect("/cover")

        if shares <= 0:
            flash("Enter a valid number of shares")
            return redirect("/cover")

        user_id = session["user_id"]
        current_shares = db.execute("SELECT shares FROM stocks WHERE user_id = ? AND stock = ?", user_id, symbol)

        if len(current_shares) == 0:
            flash("You aren't shorting that stock")
            return redirect("/cover")

        current_shares = current_shares[0]["shares"]

        if -shares < current_shares:
            flash("You aren't shorting that many shares")
            return redirect("/cover")

        current_balance = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        current_price = lookup(symbol)["price"]

        if current_shares + shares == 0:
            db.execute("DELETE FROM stocks WHERE stock = ? AND user_id = ?", symbol, user_id)

        else:
            db.execute("UPDATE stocks SET shares = ? WHERE user_id = ? AND stock = ?", current_shares + shares, user_id, symbol)

        db.execute("UPDATE users SET cash = ? WHERE id = ?", current_balance - (current_price * shares), user_id)

        db.execute("INSERT INTO transactions (user_id, stock, shares, price, action) VALUES (?, ?, ?, ?, 'cover')", user_id, symbol, shares, current_price)
        return redirect("/")
    else:
        # Retrieve the short positions held by the user for display
        current_stocks = db.execute("SELECT stock FROM stocks WHERE user_id = ? AND shares < 0", user_id)

        # Render the "cover.html" template with the list of short positions
        return render_template("cover.html", stocks=current_stocks)
