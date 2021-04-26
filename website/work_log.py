# For Work Log(CRUD)
from flask import Blueprint, render_template, request, flash, url_for, redirect, jsonify
from flask_login import login_required, current_user
from .models import User, WorkLog
from . import db
import pandas as pd
from datetime import datetime
import datetime
import json


wlog = Blueprint('wlog', __name__)


# All Work Log Page-----------------------------------------------------------
@wlog.route('/allWorkLog', methods=['GET', 'POST'])
@login_required  # If user logged in, user may access to All Work Log Page.
def log_list():
    get_all_log = WorkLog.query.join(
        User, User.id == WorkLog.user_id).add_entity(User).order_by(
            WorkLog.date.desc(), WorkLog.start_time.desc()).all()

    if request.method == 'POST':
        search_name = request.form.get('search')
        search = "%{}%".format(search_name)

        search_users = WorkLog.query.join(User, User.id == WorkLog.user_id).add_entity(User).filter(
            User.name.like(search)).order_by(WorkLog.date.desc(), WorkLog.start_time.desc()).all()

        if search_users:
            return render_template('work_log/all_log.html', user=current_user, data=search_users)
        else:
            # Show message
            flash('User Not Found!', category='error')
            return render_template('work_log/all_log.html', user=current_user, data=get_all_log)
    else:
        return render_template('work_log/all_log.html', user=current_user, data=get_all_log)
# ----------------------------------------------------------------------------


# My Work Log Page------------------------------------------------------------
@wlog.route('/myWorkLog', methods=['GET', 'POST'])
@login_required  # If user logged in, user may access to My Work Log Page.
def myWorkLog():
    max_date = datetime.date.today()
    get_all_log = WorkLog.query.filter(WorkLog.user_id == current_user.id).order_by(
        WorkLog.date.desc(), WorkLog.start_time.desc()).all()
    if request.method == 'POST':

        # Create Log-----------------------------------
        date = request.form['date']
        start = request.form['startTime']
        end = request.form['endTime']
        content = request.form['content']

        # Change String type to Date type or Time type
        d = pd.to_datetime(date)
        s = pd.to_datetime(start)
        e = pd.to_datetime(end)
        new_date = datetime.date(d.year, d.month, d.day)
        new_start = datetime.time(s.hour, s.minute, s.second)
        new_end = datetime.time(e.hour, e.minute, e.second)

        # Conditions
        if len(content) == 0:
            # Show message
            flash('Content can not be empty.', category='error')
        else:
            # Add new log to database
            new_log = WorkLog(date=new_date, start_time=new_start, end_time=new_end,
                              content=content, user_id=current_user.id)
            db.session.add(new_log)
            db.session.commit()
            # Show message
            flash('Log added!', category='success')

        get_all_log = WorkLog.query.filter(WorkLog.user_id == current_user.id).order_by(
            WorkLog.date.desc(), WorkLog.start_time.desc()).all()

        return render_template('work_log/my_log.html', user=current_user, data=get_all_log, maxDate=max_date)
        # ---------------------------------------------
    else:

        # Search---------------------------------------
        search_date = request.args.get('search')

        if search_date == None or search_date == '':
            return render_template('work_log/my_log.html', user=current_user, data=get_all_log, maxDate=max_date)
        else:
            search_log = WorkLog.query.filter(WorkLog.user_id == current_user.id, WorkLog.date == search_date).order_by(
                WorkLog.date.desc(), WorkLog.start_time.desc()).all()

            if search_log:
                return render_template('work_log/my_log.html', user=current_user, data=search_log, maxDate=max_date)
            else:
                # Show message
                flash('Date Not Found!', category='error')
                return render_template('work_log/my_log.html', user=current_user, data=get_all_log, maxDate=max_date)
        # ---------------------------------------------
# ----------------------------------------------------------------------------


# Edit Work Log--------------------------------------------------------------
@wlog.route('/editLog', methods=['POST'])
def edit_log():
    if request.method == 'POST':
        log_id = request.form['id']
        found = WorkLog.query.get(log_id)

        edit_date = request.form['editDate']
        edit_start = request.form['editStartTime']
        edit_end = request.form['editEndTime']
        edit_content = request.form['editContent']

        # Change String type to Date type or Time type
        d = pd.to_datetime(edit_date)
        s = pd.to_datetime(edit_start)
        e = pd.to_datetime(edit_end)
        new_date = datetime.date(d.year, d.month, d.day)
        new_start = datetime.time(s.hour, s.minute, s.second)
        new_end = datetime.time(e.hour, e.minute, e.second)

   # If the record exist
    if found:
        if found.user_id == current_user.id:

            if len(edit_content) == 0:
                # Show message
                flash('Content can not be empty.', category='error')
            else:
                # Edit
                found.date = new_date
                found.start_time = new_start
                found.end_time = new_end
                found.content = edit_content
                db.session.commit()

                # Show message
                flash('Saved!', category='success')

    return redirect(url_for('.myWorkLog'))
# -----------------------------------------------------------------------------


# Delete Work Log--------------------------------------------------------------
@wlog.route('/deleteLog', methods=['POST'])
def del_log():
    # Get the log that user want to delete.
    # Data is from index.js.
    log = json.loads(request.data)
    # Extract log's id
    log_id = log['logId']
    # Use log's id to find the record
    found = WorkLog.query.get(log_id)

    # If the record exist
    if found:
        if found.user_id == current_user.id:
            # Delete
            db.session.delete(found)
            db.session.commit()

    return jsonify({})
# -----------------------------------------------------------------------------


# Sub Work Log Page------------------------------------------------------------
@wlog.route('/subWorkLog', methods=['GET', 'POST'])
@login_required  # If user logged in, user may access to All Work Log Page.
def subWorkLog():
    get_all_log = WorkLog.query.join(User, User.id == WorkLog.user_id).add_entity(User).filter(
        User.identity == 'subordinate').order_by(WorkLog.date.desc(), WorkLog.start_time.desc()).all()

    if request.method == 'POST':
        search_name = request.form.get('search')
        search = "%{}%".format(search_name)

        search_users = WorkLog.query.join(User, User.id == WorkLog.user_id).add_entity(User).filter(
            User.identity == 'subordinate', User.name.like(search)).order_by(WorkLog.date.desc(), WorkLog.start_time.desc()).all()

        if search_users:
            return render_template('work_log/sub_log.html', user=current_user, data=search_users)
        else:
            # Show message
            flash('User Not Found!', category='error')
            return render_template('work_log/sub_log.html', user=current_user, data=get_all_log)
    else:
        return render_template('work_log/sub_log.html', user=current_user, data=get_all_log)
# -----------------------------------------------------------------------------
