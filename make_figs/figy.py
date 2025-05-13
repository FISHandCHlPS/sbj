import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression as LR


df = pd.read_csv("data/bq-results-20230929-084507-1695977120847.csv")
df = df.query("playerCard1>0").copy()
df["uid"] = df.path.apply(lambda x: x.split(",")[1])
df["sid"] = df.path.apply(lambda x: int(x.split(",")[3].strip(' "')))

for uid in [
        "9L3LUlN8kAN40D0IRRMg3fOQj6v1",
        "kqKV77R7JXeq2wnKYl0fib9eHtO2",
        "Vj4dGpibdCQFCRIlAsIQxkoqg1s2",
        "ep2tVYB21TgK18QOZTBEFIw9gyI3",
        ]:
    df = df.query(f"uid != '{uid}'")
df = df.copy()

out = []
for uid in np.unique(df.uid):
    dfu = df.query(f"uid == '{uid}'").sort_values("sid")
    if dfu.shape[0] != 100:
        continue
    n_intervenue = 0
    n_accept = 0
    data = []
    for i in range(100):
        dfui = dfu.iloc[i]
        if dfui.intervenue == -1:
            data.append((dfui.dif, dfui.action))
        else:
            n_intervenue += 1
            if dfui.intervenue == dfui.action:
                n_accept += 1
                if n_accept == 1:
                    if len(data) >= 2:
                        x, y = zip(*data)
                        if np.unique(y).size == 2:
                            lr = LR()
                            lr.fit(np.array(x)[:, np.newaxis], y)
                            coef0 = lr.coef_[0, 0]
                            thr0 = - lr.intercept_[0] / coef0
                            thr0 = min(max(-7, thr0), 17)
                            print("thr0", coef0, thr0)
                    data = []
    if n_intervenue > 0:
        if len(data) >= 2:
            x, y = zip(*data)
            if np.unique(y).size == 2:
                lr = LR()
                lr.fit(np.array(x)[:, np.newaxis], y)
                coef1 = lr.coef_[0, 0]
                thr1 = - lr.intercept_[0] / coef1
                thr1 = min(max(-7, thr1), 17)
                print("thr1", coef1, thr1)
                accept = n_accept / n_intervenue
                out.append((dfui.intervenue_type, accept, thr0, coef0, thr1, coef1))
dfx = pd.DataFrame(out, columns=["type", "accept", "thr0", "coef0", "thr1", "coef1"])
dfx["change1"] = dfx.thr0 - dfx.thr1
dfx["change2"] = np.abs(dfx.thr0 - 3) - np.abs(dfx.thr1 - 3)
print(dfx)

dfx = dfx.query("coef0 > 0 and thr0 >= 1 and thr0 <= 9 and coef1 > 0 and thr1 >= 1 and thr1 <= 9")
cond = dfx.type == 1
dfx["weight"] = np.where(cond, 1 / np.count_nonzero(cond), 1 / np.count_nonzero(~cond))
g = sns.jointplot(dfx, x="accept", y="change2", hue="type", palette=["red", "blue"], kind="scatter", marginal_kws=dict(weights=dfx.weight))
#g.plot_joint(sns.relplot)
#sns.move_legend(g, loc="upper right", bbox_to_anchor=(0.8, 0.9))
g.plot_joint(sns.kdeplot, levels=3)
plt.savefig("figs/figy.pdf")
