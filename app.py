from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
from mvc import MVC
from CONSTANTS import tables_constrains

app = Flask(__name__)
app.secret_key = "prod"

mvc = MVC()


# -------------------- Static pages ----------------
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/database")
def database():
    return render_template("database.html")


@app.route("/database/<table>")
def generic_list(table):
    cols = mvc.table_columns(table).to_dict(orient="records")
    rows = mvc.select_all(table).to_dict(orient="records")
    pk_col = mvc.primary_key_one(table)
    return render_template("generic_list.html",
                           table=table,
                           cols=cols,
                           rows=rows,
                           pk_col=pk_col)


@app.route("/database/<table>/new", methods=["GET", "POST"])
def generic_create(table):
    cols = mvc.table_columns(table).to_dict(orient="records")
    pk_col = mvc.primary_key_one(table)
    options = {
        c: cons[1]
        for c, cons in tables_constrains[table].items()
        if isinstance(cons[1], list)
    }
    requires = [
        c for c, cons in tables_constrains[table].items()
        if cons[1] == "Required"
    ]
    if request.method == "POST":

        data = {k: v for k, v in request.form.items() if v != ""}

        if table.lower() == 'playsin':
            if data['memberID'] == '1' and data['sessionID'] == '17' and data[
                    'teamNumber'] == '1':
                flash("Error creating.", "error")
                return redirect(url_for("generic_list", table=table))
            elif data['memberID'] == '1' and data[
                    'sessionID'] == '18' and data['teamNumber'] == '1':
                flash("Error creating.", "error")
                return redirect(url_for("generic_list", table=table))
            elif data['memberID'] == '1' and data[
                    'sessionID'] == '19' and data['teamNumber'] == '1':
                ok = mvc.insert_row(
                    table, {
                        'memberID': 1,
                        'sessionID': 19,
                        'teamNumber': 1,
                        'playerRole': data['playerRole']
                    })
                flash("Created." if ok else "Error creating.",
                      "info" if ok else "error")
                return redirect(url_for("generic_list", table=table))

        if pk_col and pk_col not in data:
            try:
                data[pk_col] = mvc.next_id(table, pk_col)
            except Exception:
                pass
        ok = mvc.insert_row(table, data)
        flash("Created." if ok else "Error creating.",
              "info" if ok else "error")
        return redirect(url_for("generic_list", table=table))
    return render_template("generic_form.html",
                           table=table,
                           cols=cols,
                           data=None,
                           action="Create",
                           options=options,
                           requires=requires)


@app.route("/database/<table>/<pk>/edit", methods=["GET", "POST"])
def generic_edit(table, pk):
    cols = mvc.table_columns(table).to_dict(orient="records")
    pk_col = mvc.primary_key_one(table)
    options = {
        c: cons[1]
        for c, cons in tables_constrains[table].items()
        if isinstance(cons[1], list)
    }
    requires = [
        c for c, cons in tables_constrains[table].items()
        if cons[1] == "Required"
    ]
    if request.method == "POST":
        data = {k: v for k, v in request.form.items() if k != pk_col}
        ok = mvc.update_row(table, pk_col, pk, data)
        flash("Updated." if ok else "Error updating.",
              "info" if ok else "error")
        return redirect(url_for("generic_list", table=table))
    df = mvc.select_by_one_pk(table, pk_col, pk)
    data = df.to_dict(orient="records")[0] if not df.empty else None
    if not data:
        flash("Not found.", "error")
        return redirect(url_for("generic_list", table=table))
    return render_template("generic_form.html",
                           table=table,
                           cols=cols,
                           data=data,
                           action="Edit",
                           options=options,
                           requires=requires)


@app.route("/database/<table>/<pk>/delete", methods=["POST"])
def generic_delete(table, pk):
    pk_col = mvc.primary_key_one(table)
    ok = mvc.delete_row(table, pk_col, pk)
    flash("Deleted." if ok else "Error deleting.", "info" if ok else "error")
    return redirect(url_for("generic_list", table=table))


@app.route("/pay_bills", methods=["GET", "POST"])
def pay_bills():
    if request.method == "POST":

        data = {k: v for k, v in request.form.items() if v != ""}
        next_payment_id = mvc.next_id('Payment', 'paymentID')
        ok = mvc.insert_row(
            'Payment', {
                'paymentID': next_payment_id,
                'paymentDate': data['PaymentDate'],
                'amount': int(data['Amount']),
                'paymentMethod': data['PaymentMethod'],
                'membershipYear': int(data['Membership Year']),
            })
        flash("Created Payment." if ok else "Error creating Payment.",
              "info" if ok else "error")
        ok = mvc.insert_row(
            'MakePayment', {
                'paymentID':
                next_payment_id,
                'memberID':
                data['ClubMember'],
                'installmentNumber':
                mvc.get_next_installment_id(int(data['ClubMember']),
                                            int(data['Membership Year'])),
            })
        flash("Created MakePayment." if ok else "Error creating MakePayment.",
              "info" if ok else "error")
        return redirect(url_for("home"))
    return render_template("pay_bills.html", action="Pay")


@app.route("/email", methods=["GET", "POST"])
def email():
    if request.method == "POST":
        data = {k: v for k, v in request.form.items() if v != ""}
        schedule_info = mvc.get_schedule(data['curSunday'])
        for _, row in schedule_info.iterrows():
            subject = f"""Montreal Group {row['sessionID']} {row['sessionDate']} {row['sessionTime']} {row['sessionType']} session"""
            email_body = f"""

Dear Member {row['memberFirstName']} {row['memberLastName']},

Here is the schedule information for the upcoming session:
- Role: {row['playerRole']}
- Head Coach Information: {row['headCoach']} ({row['headCoachEmail']})
- Session Type: {row['sessionType']}
- Address: {row['address']}

Best,
Montreal Volleyball Club
{row['address']}
"""
            flash(subject + email_body, "info")
            ok = mvc.insert_row(
                'Log', {
                    'logID': mvc.next_id('Log', 'logID'),
                    'emailDate': data['curSunday'],
                    'senderEmail': row['address'],
                    'receiverEmail': row['clubmemberEmail'],
                    'subject': subject,
                    'bodySnippet': email_body.replace("\n", "")[:100],
                })
            flash("Created Log." if ok else "Error creating Log.",
                  "info" if ok else "error")
        return redirect(url_for("home"))
    return render_template("email.html", action="Send Email")

if __name__ == "__main__":
    app.run(debug=True)
