from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd

app = Flask(__name__)
app.secret_key = "dev"          # replace in production

# -------------------------------------------------
# In-memory “database” (one DataFrame for demo)
# -------------------------------------------------
location_df = pd.DataFrame(
    [
        {"id": 1, "name": "Headquarters", "city": "Toronto", "country": "Canada"},
        {"id": 2, "name": "NY Office",     "city": "New York", "country": "USA"},
    ]
)

def next_id(df: pd.DataFrame) -> int:
    return int(df["id"].max()) + 1 if not df.empty else 1
# -------------------------------------------------


# -------------------- Static pages ----------------
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/database")
def database():
    return render_template("database.html")
# --------------------------------------------------


# -------------------- Location CRUD ---------------
@app.route("/database/location")
def location_list():
    rows = location_df.to_dict(orient="records")          # show DataFrame
    return render_template("location_list.html", rows=rows)

@app.route("/database/location/new", methods=["GET", "POST"])
def location_create():
    global location_df
    if request.method == "POST":
        location_df = pd.concat(
            [
                location_df,
                pd.DataFrame(
                    [
                        {
                            "id":      next_id(location_df),
                            "name":    request.form["name"],
                            "city":    request.form["city"],
                            "country": request.form["country"],
                        }
                    ]
                ),
            ],
            ignore_index=True,
        )
        flash("Location created.")
        return redirect(url_for("location_list"))
    return render_template("location_form.html", action="Create", data=None)

@app.route("/database/location/<int:loc_id>/edit", methods=["GET", "POST"])
def location_edit(loc_id):
    global location_df
    if request.method == "POST":
        mask = location_df["id"] == loc_id
        location_df.loc[mask, ["name", "city", "country"]] = [
            request.form["name"],
            request.form["city"],
            request.form["country"],
        ]
        flash("Location updated.")
        return redirect(url_for("location_list"))
    row = location_df[location_df["id"] == loc_id].iloc[0]
    return render_template("location_form.html", action="Edit", data=row)

@app.route("/database/location/<int:loc_id>/delete", methods=["POST"])
def location_delete(loc_id):
    global location_df
    location_df = location_df[location_df["id"] != loc_id].reset_index(drop=True)
    flash("Location deleted.")
    return redirect(url_for("location_list"))
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
