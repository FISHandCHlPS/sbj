import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression as LR


def opt_action(diff, house1):
    # 最適戦略
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
    return opt_act


df = pd.read_csv("data/bq-results-20230929-084507-1695977120847.csv")
#df = pd.read_csv("data/bq-results-20230930-075403-1696060464644.csv")
df = df.query("playerCard1>0 and intervenue!=-100").copy()
df["uid"] = df.path.apply(lambda x: x.split(",")[1])
df["sid"] = df.path.apply(lambda x: int(x.split(",")[3].strip(' "')))
#df = df.query("intervenue >= 0").copy()
df["prob_bad"] = -1.0
df["accept"] = -1

out = []
for uid in np.unique(df.uid):
    dfu = df.query(f"uid == '{uid}'").sort_values("sid")
    if dfu.shape[0] != 100:
        continue
    data = []
    ng = False
    for i in range(100):
        dfui = dfu.iloc[i]
        sid = i + 1

        opt_act = opt_action(dfui.dif, dfui.houseCard1)

        if len(data) > 0:
            x, y = zip(*data)
            if np.unique(y).size == 1:
                coef = 100.0
                if y[0] == 0:
                    thr = 100
                else:
                    thr = -100
                policy_diff = dfui.dif - thr
                if dfui.intervenue == 1:
                    policy_diff *= -1
                prob_bad = 0.0 if policy_diff < 0 else 1.0
            else:
                lr = LR()
                lr.fit(np.array(x)[:, np.newaxis], y)
                coef = lr.coef_[0, 0]
                thr = - lr.intercept_[0] / coef
                policy_diff = coef * (dfui.dif - thr)
                if dfui.intervenue == 1:
                    policy_diff *= -1
                prob_bad = lr.predict_proba([[dfui.dif]])[0, 1 - opt_act]

            out.append((thr, coef, dfui.dif, policy_diff, prob_bad))
            if dfui.intervenue_type == 1:
                if (i >= 10) and (prob_bad > 0.2):
                    if dfui.intervenue != opt_act:
                        print("accept?", uid, sid, opt_act, dfui.intervenue, dfui.dif, dfui.houseCard1, thr, coef, policy_diff, prob_bad)
                        ng = True
                else:
                    if dfui.intervenue != -1:
                        print("type-proba", uid, sid, dfui.intervenue_type, dfui.intervenue, dfui.dif, dfui.houseCard1, thr, coef, policy_diff, prob_bad)
                        ng = True
            if dfui.intervenue_type == 2:
                if (i >= 10) and (prob_bad > 0.5):
                    if dfui.intervenue != opt_act:
                        print("accept?", uid, sid, opt_act, dfui.intervenue, dfui.dif, dfui.houseCard1, thr, coef, policy_diff, prob_bad)
                        ng = True
                else:
                    if dfui.intervenue != -1:
                        print("type-proba", uid, sid, dfui.intervenue_type, dfui.intervenue, dfui.dif, dfui.houseCard1, thr, coef, policy_diff, prob_bad)
                        ng = True
            if coef < 0:
                print("minus coef", uid, sid, dfui.intervenue_type, dfui.intervenue, dfui.dif, dfui.houseCard1, thr, coef, policy_diff, prob_bad)
                ng = True
            if ng:
                break
            if dfui.intervenue >= 0:
                df.at[dfui.name, "coef_x"] = float(coef)
                df.at[dfui.name, "policy_diff_x"] = float(policy_diff)
                df.at[dfui.name, "prob_bad_x"] = float(prob_bad)
                df.at[dfui.name, "accept_x"] = 1 if dfui.action == dfui.intervenue else 0
        data.append((dfui.dif, dfui.action))
    if ng:
        df = df.query(f"uid != {uid}")
out = pd.DataFrame(out, columns=["thr", "coef", "dif", "pdif", "prob"])
print(out.sort_values("coef"))

df = df.query("prob_bad_x>=0.0 and coef_x>0")
print(df.sort_values("prob_bad_x")[["prob_bad_x", "intervenue", "accept_x"]])

fig = go.Figure().set_subplots(1, 2, shared_xaxes="all")
for i, m, win in [(0, "降ろす介入", 10), (1, "勝負する介入", 40)]:
    for n, t, color, fcolor in [("積極介入", 1, "red", "rgba(255,0,0,0.3)"), ("消極介入", 2, "blue", "rgba(0,0,255,0.3)")]:
        dfx = df.query(f"intervenue_type=={t} and intervenue=={i}")
        dfx = dfx.sort_values("prob_bad_x")
        x = dfx.prob_bad_x.rolling(window=win).mean()
        y = dfx.accept_x.rolling(window=win).mean()
        e = dfx.accept_x.rolling(window=win).std() / np.sqrt(win)
        fig.add_scatter(x=x, y=y, name=n, row=1, col=i + 1, legendgroup=0, line_color=color, showlegend=i == 0)
        fig.add_scatter(x=x, y=y - e, mode="lines", line_color="rgba(0,0,0,0)", row=1, col=i + 1, showlegend=False)
        fig.add_scatter(x=x, y=y + e, mode="none", fill="tonexty", fillcolor=fcolor, row=1, col=i + 1, showlegend=False)
    fig.add_annotation(x=0.2, y=0.1, showarrow=False, text=m, row=1, col=i + 1)
    #fig.update_xaxes(range=(0, 1))
    fig.update_yaxes(range=(0, 1))
    fig.update_layout(
        template="none",
        legend=dict(x=0.8, y=0.9),
    )
fig.write_image("figs/fig6x.pdf")
