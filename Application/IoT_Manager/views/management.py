from flask import Blueprint, request, render_template, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, current_user, login_required

from IoT_Manager import app, db_session

from IoT_Manager.sql_models import (
    User,
    Device,
    Trigger,
    Event,
    Trigger_Types
)
from IoT_Manager.forms import LoginForm, SignUpForm, CreateDeviceForm, CreateTriggerForm

Management_Blueprint = Blueprint('management', __name__)

@Management_Blueprint.route('/panel', methods=['GET', 'POST'])
@login_required
def gen_panel():
    # CREATE DEVICE CREATE FORM
    form = CreateDeviceForm()
    # CHECK IF VALID DEVICE CREATE REQUEST
    if request.method == 'POST' and form.validate_on_submit():
        # CREATE NEW DEVICE
        new_device = Device(
            user=current_user,
            device_code=form.device_code.data,
            name=form.name.data,
            desc=form.desc.data
        )
        db_session.add(new_device)
        db_session.commit()
        return redirect(url_for('management.gen_panel'))
    return render_template('panel.html', form=form)

@Management_Blueprint.route('/device/<device_id>/delete', methods=['GET'])
@login_required
def device_delete(device_id):
    # GET THE DEVICE REQUESTED
    device = db_session.query(Device).get(device_id)
    # CHECK IF CURRENT USER IS OWNER
    if device == None or device.user != current_user:
        return abort(401)
    # DELETE THE DEVICE
    db_session.delete(device)
    db_session.commit()
    return redirect(url_for('management.gen_panel'))

@Management_Blueprint.route('/panel/<device_id>', methods=['GET', 'POST'])
@login_required
def device_panel(device_id):
    # GET THE DEVICE REQUESTED
    device = db_session.query(Device).get(device_id)
    # CHECK IF CURRENT USER IS OWNER
    if device == None or device.user != current_user:
        return abort(401)
    # CREATE FORM FOR CREATING TRIGGER
    form = CreateTriggerForm()
    # CHECK IF VALID TIRGGER CREATION REQUEST
    if request.method == 'POST' and form.validate_on_submit():
        # CREATE NEW TRIGGER
        new_trigger = Trigger(
            device=device,
            trigger_type=Trigger_Types(int(form.trigger_type.data)).name,
            name=form.name.data,
            desc=form.desc.data
        )
        db_session.add(new_trigger)
        db_session.commit()
        return redirect(url_for('management.device_panel', device_id=device_id))
    return render_template('device_panel.html', form=form, device=device)

@Management_Blueprint.route('/trigger/<trigger_id>/delete', methods=['GET'])
@login_required
def trigger_delete(trigger_id):
    # GET THE TRIGGER REQUESTED
    trigger = db_session.query(Trigger).get(trigger_id)
    # CHECK IF THE CURRENT USER IS THE OWNER OF THE TRIGGER/DEVICE
    if trigger == None or trigger.device.user != current_user:
        return abort(401)
    # DELETE THE TRIGGER
    db_session.delete(trigger)
    db_session.commit()
    return redirect(url_for('management.device_panel', device_id=trigger.device.id))