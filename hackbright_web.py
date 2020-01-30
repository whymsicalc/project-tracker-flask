"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/")
def get_homepage():
    """Show list of students and projects on homepage."""
    students = hackbright.get_all_student_names()
    projects = hackbright.get_all_project_names()

    return render_template("homepage.html", students=students, projects=projects)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    grades = hackbright.get_grades_by_github(github)

    return render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           grades=grades)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-add")
def get_add_form():
    """Show form for adding a student."""

    return render_template("student_add.html")


@app.route("/student-added", methods=['POST'])
def student_added():
    """Show information about added student."""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    github = request.form.get("github")

    hackbright.make_new_student(first_name, last_name, github)

    return render_template("student_added.html", first=first_name,
                           last=last_name, github=github)


@app.route("/project")
def get_project_info():
    """Show project information."""

    project = request.args.get("title")
    title, description, max_grade = hackbright.get_project_by_title(project)
    grades_by_github = hackbright.get_grades_by_title(project)

    return render_template("project_info.html", title=title,
                           description=description, max_grade=max_grade,
                           grades=grades_by_github)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")
