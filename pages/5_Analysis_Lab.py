import os, numpy as np, pandas as pd, matplotlib.pyplot as plt, streamlit as st
from theme import apply_global_theme, header_with_mascot

st.set_page_config(page_title="Analysis Lab", page_icon="📊", layout="wide")

st.markdown("""
<style>
/* Scale down all content */
.main .block-container {
    zoom: 0.75;
    -moz-transform: scale(0.75);
    -moz-transform-origin: 0 0;
}
/* Adjust max-width to accommodate zoom */
.main .block-container {
    max-width: 1400px;
}
</style>
""", unsafe_allow_html=True)

apply_global_theme()

#headerr
header_with_mascot("CurioLab", "Analysis Lab: Discover patterns and insights from your data!", mascot_path="assets/dr_curio.png", size_px=140)


#style
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@200;400;700;800;900&family=Poppins:wght@200;300;400;600&display=swap');
html, body, [class^="css"], p, li, span, div { 
  font-family: 'Poppins', system-ui, sans-serif; 
  font-weight: 300;
  color: #64748b;
}
h1, h2, h3, h4, .hero h1, .hero h3 { 
  font-family: 'Nunito', system-ui, sans-serif; 
  font-weight: 900;
  color: #334155;
}
/* Fix dataframe font */
.stDataFrame, .stDataFrame * {
  font-family: 'Poppins', system-ui, sans-serif !important;
  font-weight: 300 !important;
  color: #64748b !important;
}
</style>
""", unsafe_allow_html=True)

def cute_box(text: str, bg="#e0f2fe"):
    st.markdown(f"""
    <div style='background:{bg};padding:18px 24px;border-radius:16px;border:1px solid #bfdbfe;line-height:1.7;'>
        {text}
    </div>
    """, unsafe_allow_html=True)

def info_card(title, content, color="#e0f2fe"):
    st.markdown(f"""
    <div style='background:{color};padding:18px;border-radius:12px;border-left:4px solid #3b82f6;margin:12px 0;'>
        <h4 style='color:#1e40af;margin-top:0;font-size:1.1rem;'>{title}</h4>
        <p style='color:#475569;margin-bottom:0;'>{content}</p>
    </div>
    """, unsafe_allow_html=True)

#tip
cute_box("You're about to find connections in your data. Look for correlations and patterns - you're doing real science.", bg="#e0f2fe")

#edu card
st.markdown("### Data Science Basics")
c1, c2, c3 = st.columns(3)
with c1:
    info_card("What is Correlation?", "Correlation shows if two things change together. If one goes up, does the other go up too? That's correlation.", "#e0f2fe")
with c2:
    info_card("Regression Explained", "Regression helps us predict. If we know X, can we guess Y? That's what regression does.", "#fce7f3")
with c3:
    info_card("R² Means What?", "R² tells us how well our line fits the data. Higher is better - it means our prediction is more accurate.", "#ecfccb")

st.markdown("---")

def load_csv(path): 
    return pd.read_csv(path) if os.path.exists(path) else pd.DataFrame()

air = load_csv("data/logs_air.csv")
seeds = load_csv("data/logs_seeds.csv")
poll = load_csv("data/logs_pollinators.csv")

st.markdown("### Choose Your Dataset")
opt = st.selectbox("Which dataset would you like to analyze?", 
                   ["Air & Weather","Seeds & Growth","Pollinator Patrol"],
                   index=0)
df = air if "Air" in opt else (seeds if "Seeds" in opt else poll)

if df.empty:
    cute_box("No data yet. Go collect some observations first in the other modules, then come back here to analyze.", bg="#fef3c7")
else:
    # Dataset stats
    st.markdown("#### Dataset Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Observations", f"{len(df)}")
    with col2:
        st.metric("Columns", f"{len(df.columns)}")
    with col3:
        numeric_cols = len(df.select_dtypes(include=[np.number]).columns)
        st.metric("Numeric Variables", f"{numeric_cols}")
    
    st.markdown("#### Preview Your Data")
    st.dataframe(df.head(20), use_container_width=True, hide_index=True)

    # Basic numeric correlation
    st.markdown("---")
    st.markdown("### Correlations Analysis")
    num = df.select_dtypes(include=[np.number])
    if num.empty:
        cute_box("No numeric columns to analyze. Need numbers to find patterns.", bg="#fef3c7")
    else:
        corr = num.corr()
        
        # Beautiful heatmap
        st.markdown("##### Correlation Matrix")
        fig, ax = plt.subplots(figsize=(10, 8))
        im = ax.imshow(corr, cmap='RdYlBu_r', aspect='auto', vmin=-1, vmax=1)
        ax.set_xticks(range(len(corr.columns)))
        ax.set_yticks(range(len(corr.columns)))
        ax.set_xticklabels(corr.columns, rotation=45, ha='right')
        ax.set_yticklabels(corr.columns)
        ax.set_title("Correlation Heatmap - How Variables Relate", pad=20, fontsize=14, weight='bold')
        
        # Add values to heatmap
        for i in range(len(corr.columns)):
            for j in range(len(corr.columns)):
                text = ax.text(j, i, f'{corr.iloc[i, j]:.2f}',
                             ha="center", va="center", color="black" if abs(corr.iloc[i, j]) < 0.5 else "white",
                             weight='bold', fontsize=9)
        
        plt.colorbar(im, ax=ax, label='Correlation')
        plt.tight_layout()
        st.pyplot(fig)
        
        # Plain-language explanation
        strongest = None; best = 0
        for i in corr.columns:
            for j in corr.columns:
                if i!=j and abs(corr.loc[i,j]) > best:
                    best = abs(corr.loc[i,j]); strongest = (i,j,corr.loc[i,j])
        if strongest:
            i,j,val = strongest
            st.markdown("##### Key Finding")
            if abs(val) > 0.7:
                msg = f"<strong>Very Strong Relationship:</strong> {i} and {j} are tightly connected (r = {val:.2f}). When one changes, the other almost always changes the same way."
            elif abs(val) > 0.5:
                msg = f"<strong>Moderate Relationship:</strong> {i} and {j} tend to change together (r = {val:.2f}). There's definitely a pattern here."
            else:
                msg = f"<strong>Weak Relationship:</strong> {i} and {j} don't change much together (r = {val:.2f}). Keep exploring other pairs."
            cute_box(msg, bg="#ecfccb")

    st.markdown("---")
    st.markdown("### Predict the Future - Simple Regression")
    cols = [c for c in df.columns if c in num.columns]
    if len(cols) >= 2:
        st.markdown("##### Choose Your Variables")
        col1, col2 = st.columns(2)
        with col1:
            xcol = st.selectbox("Predictor Variable (X-axis)", cols, index=0, help="This is the variable you use to make predictions")
        with col2:
            ycol = st.selectbox("Target Variable (Y-axis)", cols, index=1, help="This is what you're trying to predict")
        
        x = df[xcol].astype(float).values
        y = df[ycol].astype(float).values
        
        if len(x) >= 2:
            m, b = np.polyfit(x, y, 1)
            yhat = m*x + b
            
            # Beautiful plot
            fig, ax = plt.subplots(figsize=(10, 7), facecolor='#f9fafb')
            ax.scatter(x, y, s=100, alpha=0.6, color='#6366f1', edgecolors='#4f46e5', linewidth=2, label='Your Data')
            ax.plot(x, yhat, color='#dc2626', linewidth=3, label='Prediction Line')
            ax.set_xlabel(xcol, fontsize=13, color='#4338ca', weight='bold')
            ax.set_ylabel(ycol, fontsize=13, color='#4338ca', weight='bold')
            ax.set_title(f"Prediction Model: How {ycol} relates to {xcol}", fontsize=14, color='#4f46e5', pad=20, weight='bold')
            ax.grid(True, alpha=0.3, linestyle='--', color='#a5b4fc')
            ax.legend(fontsize=11, loc='best')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#a5b4fc')
            ax.spines['bottom'].set_color('#a5b4fc')
            plt.tight_layout()
            st.pyplot(fig)
            
            # r^2 explanation
            r = np.corrcoef(x,y)[0,1] if len(x)>1 else 0
            r2 = r**2
            
            st.markdown("##### Analysis Results")
            direction = "up together" if m > 0 else "opposite directions"
            significance = "Excellent" if r2 > 0.7 else "Pretty good" if r2 > 0.5 else "Getting there" if r2 > 0.3 else "Needs more data"
            
            result_html = f"""
            <div style='background:#e0f2fe;padding:20px;border-radius:12px;border-left:4px solid #3b82f6;'>
                <p style='margin:0 0 12px 0;color:#475569;'><strong>Direction:</strong> When {xcol} goes {'UP' if m > 0 else 'DOWN'}, {ycol} tends to go {direction}</p>
                
                <p style='margin:0 0 12px 0;color:#475569;'><strong>Strength:</strong> r² = {r2:.2f} means the line explains {r2*100:.0f}% of what's happening. {significance}</p>
                
                <p style='margin:0;color:#475569;'><strong>Real Talk:</strong> {'This is a strong pattern you discovered' if r2 > 0.5 else 'Keep collecting more data to see clearer patterns'}</p>
            </div>
            """
            st.markdown(result_html, unsafe_allow_html=True)
            
            # Practical example
            if len(x) > 0:
                x_mean = x.mean()
                y_pred_mean = m * x_mean + b
                st.markdown(f"<br><p style='color:#475569;'>Example Prediction: When {xcol} = {x_mean:.1f}, we'd predict {ycol} ≈ {y_pred_mean:.2f}</p>", unsafe_allow_html=True)
        else:
            cute_box("Need at least 2 data points to make predictions. Keep collecting data.", bg="#fef3c7")
    else:
        cute_box("Pick a dataset with at least two numeric columns to run regression analysis.", bg="#fef3c7")

# Educational section
st.markdown("---")
st.markdown("### Learning Resources")

tab1, tab2, tab3 = st.tabs(["Data Analysis Basics", "Correlation Explained", "Regression & Predictions"])
with tab1:
    st.markdown("""
    <div style='padding:20px;background:#e0f2fe;border-radius:12px;'>
        <h4>What is Data Analysis?</h4>
        <p><strong>Finding Patterns:</strong> Data analysis helps us discover hidden relationships in our data - like whether sunny days have more bees.</p>
        <p><strong>Visualizing Data:</strong> Charts and graphs help us see patterns our eyes might miss. A picture is worth a thousand numbers.</p>
        <p><strong>The Scientific Method:</strong> 1) Observe, 2) Collect data, 3) Analyze, 4) Draw conclusions - that's what you're doing.</p>
        <p><strong>Asking Questions:</strong> Good analysis starts with good questions: "Does X affect Y?" Then we use data to answer.</p>
        <p><strong>Variables Explained:</strong> Variables are the different things we measure - like temperature, height, or number of bees. They're the building blocks of analysis.</p>
        <p><strong>Your Impact:</strong> By analyzing your data, you're doing real science that could help the environment.</p>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div style='padding:20px;background:#fce7f3;border-radius:12px;'>
        <h4>Understanding Correlation</h4>
        <p><strong>What is Correlation?</strong> Correlation measures how two variables change together. Do they go up together? Down together? Or stay independent?</p>
        <p><strong>Positive Correlation:</strong> Both variables increase together. More sun = more butterflies.</p>
        <p><strong>Negative Correlation:</strong> When one goes up, the other goes down. More pollution = fewer bees.</p>
        <p><strong>No Correlation:</strong> Variables change independently. Like the number of birds vs the price of bananas.</p>
        <p><strong>Correlation Values:</strong> Range from -1 (perfect negative) to +1 (perfect positive). 0 means no relationship.</p>
        <p><strong>Don't Confuse with Cause:</strong> Just because two things are related doesn't mean one causes the other. Correlation does not equal causation.</p>
        <p><strong>Why It Matters:</strong> Finding correlations helps us understand our world and make better predictions.</p>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("""
    <div style='padding:20px;background:#ecfccb;border-radius:12px;'>
        <h4>Regression & Making Predictions</h4>
        <p><strong>What is Regression?</strong> Regression helps us predict. If we know one variable, can we predict another? That's regression in action.</p>
        <p><strong>The Best Fit Line:</strong> Regression finds the line that best fits through our data points - minimizing the distance to all points.</p>
        <p><strong>R² Explained:</strong> R² (R-squared) tells us how well our line predicts. R² = 0.8 means the line explains 80% of variation.</p>
        <p><strong>Slope:</strong> The slope tells us the direction and strength of the relationship. Steep slope = strong effect.</p>
        <p><strong>Making Predictions:</strong> Once we have the line, we can predict. "If temperature is 25°C, how many bees might we see?"</p>
        <p><strong>Limits:</strong> Predictions work best for data similar to what we trained on. Don't predict too far outside your data.</p>
        <p><strong>You're a Data Scientist:</strong> By using regression, you're doing the same math that professional scientists use to understand the world.</p>
    </div>
    """, unsafe_allow_html=True)
