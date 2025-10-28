import os, numpy as np, pandas as pd, matplotlib.pyplot as plt, streamlit as st

st.set_page_config(page_title="Analysis Lab — LearnLab", page_icon="📊", layout="wide")

st.markdown("## 📊 Analysis Lab")
st.caption("Explore relationships between variables with simple statistics and friendly explanations.")

def load_csv(path): 
    return pd.read_csv(path) if os.path.exists(path) else pd.DataFrame()

air = load_csv("data/logs_air.csv")
seeds = load_csv("data/logs_seeds.csv")
poll = load_csv("data/logs_pollinators.csv")

st.markdown("### Pick a dataset")
opt = st.selectbox("Dataset", ["Air & Weather","Seeds & Growth","Pollinator Patrol"])
df = air if opt=="Air & Weather" else (seeds if opt=="Seeds & Growth" else poll)
if df.empty:
    st.info("No data yet. Add entries in Missions first.")
else:
    st.dataframe(df.head(50), use_container_width=True)

    # Basic numeric correlation
    st.markdown("### Correlations")
    num = df.select_dtypes(include=[np.number])
    if num.empty:
        st.info("No numeric columns found.")
    else:
        corr = num.corr()
        st.dataframe(corr.style.format("{:.2f}"))
        # plain-language
        strongest = None; best = 0
        for i in corr.columns:
            for j in corr.columns:
                if i!=j and abs(corr.loc[i,j]) > best:
                    best = abs(corr.loc[i,j]); strongest = (i,j,corr.loc[i,j])
        if strongest:
            i,j,val = strongest
            msg = f"**Strongest relationship:** {i} ↔ {j} (r = {val:.2f}). "
            if abs(val) > 0.7: msg += "Very strong."
            elif abs(val) > 0.5: msg += "Moderate."
            else: msg += "Weak."
            st.markdown(msg)

    st.markdown("### Try a simple prediction")
    cols = [c for c in df.columns if c in num.columns]
    if len(cols) >= 2:
        xcol = st.selectbox("Predictor (x)", cols, index=0)
        ycol = st.selectbox("Target (y)", cols, index=1)
        x = df[xcol].astype(float).values
        y = df[ycol].astype(float).values
        if len(x) >= 2:
            m,b = np.polyfit(x, y, 1)
            yhat = m*x + b
            # plot
            fig, ax = plt.subplots()
            ax.scatter(x, y)
            ax.plot(x, yhat)
            ax.set_xlabel(xcol); ax.set_ylabel(ycol); ax.set_title(f"Regression: {ycol} ~ {xcol}")
            st.pyplot(fig)
            # r^2
            r = np.corrcoef(x,y)[0,1] if len(x)>1 else 0
            r2 = r**2
            st.markdown(f"**Plain language:** When `{xcol}` changes, `{ycol}` tends to change in the same direction (if slope {m:.2f} positive) or opposite (if negative). r² = {r2:.2f} means this line explains about {r2*100:.0f}% of the variation.")
        else:
            st.info("Need at least 2 data points.")
    else:
        st.info("Pick a dataset with at least two numeric columns to run regression.")
