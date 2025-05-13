import responder
import sys
import time

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

from .db import Database


api = responder.API()
db = Database()

# 全部POSTで呼び出される

@api.route('/api/start')
async def start(req, resp):
    data = await req.media()
    user_data = db.get_user_data(data)
    if user_data is None:
        resp.status_code = 400
        return
    if 'result' in user_data:
        resp.status_code = 400
        return
    status = db.get_status()
    assign = status['assign']
    if 'exp_type' in user_data:
        exp_type = user_data['exp_type']
        assign[exp_type] -= 1
    # status に基づいて exp_type を決定
    exp_type = assign.index(min(assign))
    # 必要な情報を記録
    user_data['n_start'] += 1
    user_data['exp_type'] = exp_type
    assign[exp_type] += 1
    db.put_multi([user_data, status])
    resp.media = dict(exp_type=exp_type)


@api.route('/api/finish')
async def finish(req, resp):
    data = await req.media()
    user_data = db.get_user_data(data)
    if user_data is None:
        resp.status_code = 400
        return
    if 'result' in user_data:
        resp.status_code = 400
        return
    exp_type = data['exp_type']
    if user_data['exp_type'] != exp_type:
        resp.status_code = 400
        return
    user_data['result'] = data['result']
    status = db.get_status()
    status['done'][exp_type] += 1
    db.put_multi([user_data, status])
    resp.media = dict(uid=user_data.key.name)
    

@api.route('/api/session')
async def session(req, resp):
    data = await req.media()
    session_data = db.get_session_data(data)
    if session_data is None:
        resp.status_code = 400
        return
    keys = [
        "intervenue_type",
        "houseCard1", "houseCard2",
        "playerCard1", "playerCard2",
        "action", "dif", "point",
    ]
    for k in keys:
        session_data[k] = data[k]
    session_data["time"] = time.time()
    db.put(session_data)
    resp.media = dict(point=session_data['point'])


@api.route('/api/intervenue')
async def intervenue(req,resp):
    data = await req.media()

    # 過去データ取得
    train = db.get_train_data(data)
    # エラー処理
    if type(train)==int:
        resp.media = dict(error_session_id=train)
        return
    if train is None:
        resp.status_code = 400
        return

    # 最適戦略
    diff = data["dif"]
    house1 = data["houseCard1"]
    if diff <= 0:
        p_w = 0
        p_d = 0
    elif diff < house1:
        p_w = 2 * (diff - 1)
        p_d = 2
    elif diff == house1:
        p_w = 2 * (diff - 1)
        p_d = 1
    elif diff <= 9:
        p_w = 2 * (diff - 1) - 1
        p_d = 2
    else:
        p_w = 17
        p_d = 0
    p_l = 17 - p_w - p_d
    e1 = (100 * p_w - 30 * p_d - 70 * p_l) / 17
    e0 = -30
    opt_act = 1 if e1 > e0 else 0

    # 行動予測
    train_dif = train.dif.values
    train_act = train.act.values
    n_act = np.unique(train.act).size
    if n_act == 0:
        thr = -100.0
        coef = -1.0
        pred_act = [-1.0, -1.0]
    elif n_act == 1:
        if train_act[0] == 1:
            thr = -100.0
            coef = -1.0
            pred_act = [0, 1]
        else:
            thr = +100.0
            coef = -1.0
            pred_act = [1, 0]
    else:
        model = LogisticRegression()
        model.fit(train_dif[:, np.newaxis], train_act)
        coef = model.coef_[0, 0]
        thr = - model.intercept_[0] / coef
        pred_act = model.predict_proba([[diff]])[0]
    prob_bad = pred_act[1 - opt_act]
    
    # 介入内容決定
    session_id = int(data["session_id"])
    intervenue_type = int(data['intervenue_type'])
    threshold = [10.0, 0.2, 0.5][intervenue_type]
    if (session_id > 10) and (prob_bad > threshold):
        intervenue = opt_act
    else:
        intervenue = -1

    # DB に書き込み
    session_data = db.get_session_data(data)
    # - エラー処理
    if session_data is None:
        resp.status_code = 400
        return
    # - 書き込み
    session_data["intervenue_type"] = int(intervenue_type)
    session_data["threshold"] = float(thr)
    session_data["thr_scale"] = float(coef)
    session_data["prob_bad"] = float(prob_bad)
    session_data["intervenue"] = int(intervenue)
    session_data["start_time"] = time.time()
    db.put(session_data)

    # クライアントに
    resp.media = dict(intervenue=intervenue, bap=prob_bad)
    return intervenue
