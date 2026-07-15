from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = []
next_id = 1


@app.route("/")
def index():
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["GET", "POST"])
def add_task():
    global next_id

    if request.method == "POST":
        task = {
            "id": next_id,
            "title": request.form["title"],
            "description": request.form["description"],
            "priority": request.form["priority"],
            "completed": False
        }

        tasks.append(task)
        next_id += 1

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_task(id):

    task = next((t for t in tasks if t["id"] == id), None)

    if task is None:
        return redirect(url_for("index"))

    if request.method == "POST":

        task["title"] = request.form["title"]
        task["description"] = request.form["description"]
        task["priority"] = request.form["priority"]

        return redirect(url_for("index"))

    return render_template("edit.html", task=task)


@app.route("/delete/<int:id>")
def delete_task(id):

    global tasks

    tasks = [t for t in tasks if t["id"] != id]

    return redirect(url_for("index"))


@app.route("/complete/<int:id>")
def complete_task(id):

    task = next((t for t in tasks if t["id"] == id), None)

    if task:
        task["completed"] = True

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)