# -*- coding: utf-8 -*-
"""
This route callback is called whenever MES data is requested (either daily or period tabs)
"""
from .. import app
import os
import json
from flask import request, send_file
from time import sleep
import datetime as dt
import app.db_lib as db


@app.route('/maquina/<machine_id>/requestMESData', methods=['POST'])
def request_mes_data(machine_id='1'):
    from app.views.request_page import machine_dict
    global start, end, mid

    mid = machine_id
    output = {}

    start_date_str = request.json['date-start']
    start = start_date_str
    end_date_str = request.json['date-end']
    end = end_date_str

    mes = db.select_mes_period(machine_dict[machine_id], start_date_str, end_date_str, host='localhost', user='romi',
                               password='romiconnect')
    if mes.empty:
        output['msg'] = "Não existe relatório para a data selecionada."

    # output['ret_code'] = 0
    return json.dumps(output), 200


@app.route('/maquina/<machine_id>/downloads/', methods=['POST'])
def download_mes(machine_id='1'):
    from app.views.request_page import machine_dict
    global start, end, mid
    while (start is None) or (end is None) or (mid is None):
        pass
    print start, end, machine_dict[machine_id]
    mes = db.select_mes_period(machine_dict[machine_id], start, end, host='localhost', user='romi',
                               password='romiconnect')

    filename = '{} {}.csv'.format(dt.datetime.now(), machine_dict[machine_id])
    path = app.root_path + '/static/res/out/'
    mes.to_csv(path + filename, index=False)
    start = None; end = None; mid = None
    out = send_file(path + filename, as_attachment=True, attachment_filename=filename)
    os.remove(path + filename)

    return out
