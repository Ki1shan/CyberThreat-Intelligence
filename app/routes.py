# app/routes.py

from flask import Blueprint, render_template, request, redirect, url_for
from . import mongo
from .apis.virustotal import check_virustotal
from .apis.abuseipdb import check_abuseipdb
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    iocs = list(mongo.db.iocs.find().sort('timestamp', -1))
    return render_template('dashboard.html', iocs=iocs)

@main.route('/lookup', methods=['POST'])
def lookup():
    input_value = request.form.get('ioc')

    vt_result = check_virustotal(input_value)
    abuse_result = check_abuseipdb(input_value)

    ioc_data = {
        "ioc": input_value,
        "timestamp": datetime.utcnow(),
        "virustotal": vt_result,
        "abuseipdb": abuse_result
    }

    mongo.db.iocs.insert_one(ioc_data)
    return redirect(url_for('main.index'))

