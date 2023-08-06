from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from app import db
import json
import csv
from app.models import store_data, Service, Note
import io
import psutil

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash("Note is too short", category="error")
        else:
            # Create note
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note Added", category="success")

    return render_template("notes.html", user=current_user)


@views.route('/deleteNote', methods=['POST'])
def deleteNote():
    data = json.loads(request.data)
    noteId = data['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})


@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = file.filename
            if filename.endswith(".csv"):
                # Process CSV file
                content = file.stream.read().decode("utf-8")
                # Convert string content to file-like object
                csv_file = io.StringIO(content)
                # Use the file-like object with DictReader
                reader = csv.DictReader(csv_file)

                for row in reader:
                    success = store_data(
                        row["LOCATION TYPE"],
                        row["FACILITY TITLE"],
                        row["ADDRESS"],
                        row["PHONE"],
                        row["HOURS OPEN TO PUBLIC"],
                        row["HOURS CLOSED"],
                        row["SERVICE DESCRIPTION"],
                    )

    # Fetch all services from the database
    services = Service.query.all()
    return render_template("search.html", user=current_user, services=services)


@views.route("/monitor")
def monitor():
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    Message = None
    if cpu_percent > 85 or memory_percent > 85:
        Message = f"High CPU{cpu_percent} or memory{memory_percent} utilization detected! Please scale up"
        # flash(f"{message}", category="warning")

    return render_template("monitor.html", user=current_user, monitoring=[cpu_percent, memory_percent], message=Message)
