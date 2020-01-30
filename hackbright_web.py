"""A web application for tracking projects, students, and student grades."""

from flask import Flask, flash, redirect, request, render_template

import hackbright

app = Flask(__name__)
app.secret_key = 'APPSECRETKEY'


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


@app.route("/project-add")
def get_project_add_form():
    """Show form for adding a project."""

    return render_template("project_add.html")


@app.route("/project-added", methods=["POST"])
def project_added():
    """Show information about added project."""

    title = request.form.get("title")
    description = request.form.get("description")
    max_grade = request.form.get("max_grade")

    hackbright.make_new_project(title, description, max_grade)

    return render_template("project_added.html", title=title)


@app.route("/grade-add")
def get_grade_add_form():
    """Show form for adding a student project grade."""
    students = hackbright.get_all_student_names()
    projects = hackbright.get_all_project_names()

    return render_template("assign_grade.html", students=students, projects=projects)


@app.route("/grade-added", methods=["POST"])
def grade_added():
    """Show information about added grade."""
    student = request.form.get("student")
    project = request.form.get("project")
    grade = request.form.get("grade")

    github_tup = hackbright.get_github_by_id(student)
    github = github_tup[0]

    if hackbright.get_grade_by_github_title(github, project):
        hackbright.update_grade_by_github_title(github, project, grade)
        flash('Grade successfully updated.')
    else:
        hackbright.assign_grade(github, project, grade)
        flash('Grade successfully added.')

    return redirect("/grade-add")


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")
