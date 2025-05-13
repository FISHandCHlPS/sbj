import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression as LR


"""
df0 = pd.read_csv("data/Exp1208Cleaned.csv")
df0 = df0.rename(columns=dict(user_id="uid", session_id="sid"))
dft = df0.query("sid == 0")
dft.index = dft.uid
print(dft[["intervenue"]])
df0 = df0.query("sid > 0").copy()
df0["intervenue_type"] = -1
for uid in np.unique(dft.uid):
    df0.loc[df0.uid == uid, "intervenue_type"] = dft.loc[uid, "intervenue"]
print(df0[["sid", "intervenue_type"]])
df0 = df0.query("intervenue_type == 0")
"""

df1 = pd.read_csv("data/bq-results-20230929-084507-1695977120847.csv")
df1 = df1.query("playerCard1>0").copy()
df1["uid"] = df1.path.apply(lambda x: x.split(",")[1])
df1["sid"] = df1.path.apply(lambda x: int(x.split(",")[3].strip(' "')))

df = pd.concat([df1], axis=0)
df = df.query("intervenue_type >= 0")

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
    data = []
    for i in range(100):
        dfui = dfu.iloc[i]
        if dfui.intervenue >= 0:
            data.append((dfui.dif, dfui.action))
    if dfui.intervenue_type == 0:
        print(data)
    if len(data) >= 2:
        x, y = zip(*data)
        if np.unique(y).size == 2:
            lr = LR()
            lr.fit(np.array(x)[:, np.newaxis], y)
            coef1 = np.log(3) / lr.coef_[0, 0]
            thr1 = - lr.intercept_[0] / lr.coef_[0, 0]
            out.append((dfui.intervenue_type, thr1, coef1))
dfx = pd.DataFrame(out, columns=["type", "thr1", "coef1"])
print(dfx)

dfx = dfx.query("coef1 > 0 and thr1 >= 1 and thr1 <= 9")
#dfx = dfx.query("coef1 > 0")
for i in range(1, 3):
    cond = dfx.type == i
    dfx.loc[cond, "weight"] = 1 / np.count_nonzero(cond)
g = sns.jointplot(dfx, x="coef1", y="thr1", hue="type", xlim=(0, 5.8), ylim=(-2, 12), palette=["red", "blue"], marginal_kws=dict(weights=dfx.weight))
g.plot_joint(sns.kdeplot, levels=3)
plt.savefig("figs/figx2.pdf")
