# Create website route for Home and Staff List.
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import User, WorkLog
from . import db


views = Blueprint('views', __name__)


# Home Page ------------------------------------------------------------------
@views.route('', methods=['GET'])
@views.route('/', methods=['GET'])
@login_required  # If user logged in, user may access to the Home Page.
def home():
    if current_user.name == 'admin':
        return render_template('index/admin_index.html', user=current_user)
    else:
        if current_user.identity == 'supervisor':
            return render_template('index/super_index.html', user=current_user)
        else:
            return render_template('index/sub_index.html', user=current_user)
# ----------------------------------------------------------------------------


# Staff List Page ------------------------------------------------------------
@views.route('/staffList', methods=['GET', 'POST'])
@login_required  # If user logged in, user may access to Staff List Page.
def staff_list():
    get_all_staff = User.query.order_by(User.identity.desc(), User.name).all()

    if request.method == 'POST':
        search_name = request.form.get('search')
        search = "%{}%".format(search_name)
        search_users = User.query.filter(User.name.like(search)).order_by(
            User.identity.desc(), User.name).all()

        if search_users:
            return render_template('user/staff_list.html', user=current_user, data=search_users)
        else:
            # Show message
            flash('User Not Found!', category='error')
            return render_template('user/staff_list.html', user=current_user, data=get_all_staff)
    else:
        return render_template('user/staff_list.html', user=current_user, data=get_all_staff)
# ----------------------------------------------------------------------------
