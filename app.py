from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None

    if request.method == "POST":
        try:
            student_name = request.form["student_name"].strip()
            subject_names = request.form.getlist("subject_name")
            mark_values = request.form.getlist("marks")

            if not student_name:
                raise ValueError

            subjects = {}

            for subject, mark in zip(subject_names, mark_values):
                subject = subject.strip()

                if not subject:
                    continue

                mark = float(mark)

                if mark < 0 or mark > 100:
                    raise ValueError

                subjects[subject] = mark

            if not subjects:
                raise ValueError

            total = sum(subjects.values())
            maximum = len(subjects) * 100
            percentage = (total / maximum) * 100

            passed = all(mark >= 33 for mark in subjects.values())

            if not passed:
                grade = "F"
                status = "FAIL"
            elif percentage >= 90:
                grade = "A+"
                status = "PASS"
            elif percentage >= 80:
                grade = "A"
                status = "PASS"
            elif percentage >= 70:
                grade = "B"
                status = "PASS"
            elif percentage >= 60:
                grade = "C"
                status = "PASS"
            elif percentage >= 50:
                grade = "D"
                status = "PASS"
            else:
                grade = "E"
                status = "PASS"

            result = {
                "name": student_name,
                "subjects": subjects,
                "total": total,
                "maximum": maximum,
                "percentage": percentage,
                "grade": grade,
                "status": status
            }

        except (ValueError, TypeError):
            error = "Please enter a valid name, subject and marks between 0 and 100."

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True)
