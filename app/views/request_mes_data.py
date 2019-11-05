# -*- coding: utf-8 -*-
"""
This route callback is called whenever MES data is requested
"""
from .. import app
import os
import json
from flask import request, send_file
from time import sleep
import datetime as dt
import app.db_lib as db
import stats


@app.route('/maquina/<machine_id>/requestMESData', methods=['POST'])
def request_mes_data(machine_id='1'):
    from app.views.request_page import machine_dict
    global start, end, mid

    mid = machine_id
    out = {'ret_code': 1}

    start_date_str = request.json['date-start']
    start = start_date_str
    end_date_str = request.json['date-end']
    end = end_date_str

    mes = db.select_mes_period(machine_dict[machine_id], start_date_str, end_date_str, host='localhost', user='romi',
                               password='romiconnect')

    if mes.empty:  out['msg'] = "Não existe relatório para a data selecionada."
    else:  out['ret_code'] = 0

    if not request.json['download']:
        df_dict = stats.timebar_enumerate(mes,
            ['alm_list_msg1', 'alm_list_msg2', 'alm_list_msg3', 'alm_stat', 'alm_type1', 'alm_type2', 'alm_type3',
             'auto_stat', 'edit_stat', 'emg_stat', 'motion_stat', 'run_stat', 'pmc_alm1', 'pmc_alm2', 'pmc_alm3',
             'pmc_alm4', 'prgname'])
        out.update(stats.export_figures(stats.plot_timeline(df_dict)))
        return json.dumps(out), 200
    else:
        return out


@app.route('/maquina/<machine_id>/downloads/')
def download_mes(machine_id='1'):
    from app.views.request_page import machine_dict
    global start, end, mid
    while (start is None) or (end is None) or (mid is None):
        pass
    # print start, end, machine_dict[machine_id]
    mes = db.select_mes_period(machine_dict[machine_id], start, end, host='localhost', user='romi',
                               password='romiconnect')

    filename = '{} {}.csv'.format(dt.datetime.now(), machine_dict[machine_id])
    path = app.root_path + '/static/res/out/'
    mes.to_csv(path + filename, index=False)
    start = None; end = None; mid = None
    out = send_file(path + filename, as_attachment=True, attachment_filename=filename, cache_timeout=1)
    os.remove(path+filename)

    return out
