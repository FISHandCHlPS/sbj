import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv("data/bq-results-20230929-084507-1695977120847.csv")
df = df.query("playerCard1>0").copy()
df["uid"] = df.path.apply(lambda x: x.split(",")[1])
df["sid"] = df.path.apply(lambda x: int(x.split(",")[3].strip(' "')))
df = df.query("intervenue >= 0").copy()
df = df.query("threshold >= -7 and threshold <= 17").copy()

diff = df.dif - df.threshold
diffx = df.thr_scale * diff
df["policy_diff"] = np.where(df.intervenue == 0, +diff, -diff)
df["policy_diffx"] = np.where(df.intervenue == 0, +diffx, -diffx)
df["accept"] = np.where(df.intervenue == df.action, 1, 0)
print(np.count_nonzero(df.thr_scale < 0), df.shape[0])

"""
sns.relplot(df, kind="line", x="policy_diff", y="accept", hue="intervenue_type", col="intervenue")
plt.savefig("fig6.pdf")
"""

#df = df.query("thr_scale > 0 and 1 <= threshold and threshold <= 9").copy()
df = df.query("thr_scale > 0").copy()
print(df)
fig = go.Figure().set_subplots(1, 2, shared_xaxes="all")
for i, m, win in [(0, "降ろす介入", 30), (1, "勝負する介入", 30)]:
    for n, t, color, fcolor in [("積極介入", 1, "red", "rgba(255,0,0,0.3)"), ("消極介入", 2, "blue", "rgba(0,0,255,0.3)")]:
        dfx = df.query(f"intervenue_type=={t} and intervenue=={i}")
        dfx = dfx.sort_values("prob_bad")
        x = dfx.prob_bad.rolling(window=win).mean()
        y = dfx.accept.rolling(window=win).mean()
        e = dfx.accept.rolling(window=win).std() / np.sqrt(win)
        fig.add_scatter(x=x, y=y, name=n, row=1, col=i + 1, legendgroup=0, line_color=color, showlegend=i == 0)
        fig.add_scatter(x=x, y=y - e, mode="lines", line_color="rgba(0,0,0,0)", row=1, col=i + 1, showlegend=False)
        fig.add_scatter(x=x, y=y + e, mode="none", fill="tonexty", fillcolor=fcolor, row=1, col=i + 1, showlegend=False)
    fig.add_annotation(x=0.2, y=0.1, showarrow=False, text=m, row=1, col=i + 1)
    fig.update_xaxes(range=(0, 1))
    fig.update_yaxes(range=(0, 1))
    fig.update_layout(
        template="none",
        legend=dict(x=0.8, y=0.9),
    )
fig.write_image("figs/fig6.pdf")
