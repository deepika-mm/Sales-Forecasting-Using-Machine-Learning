import streamlit as st
import pandas as pd
import joblib
import os
import time
from sklearn.ensemble import RandomForestRegressor

# -----------------------
# SESSION STATE
# -----------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

# -----------------------
# CSS STYLING
# -----------------------
box_width = "1100px" if st.session_state.page in ["dashboard", "result"] else "850px"

st.markdown(f"""
<style>
[data-testid="stHeader"], [data-testid="stToolbar"] {{ display: none; }}
.stApp {{ background: linear-gradient(135deg, #ede9fe, #ddd6fe); }}
[data-testid="stMainViewContainer"] {{ display: flex !important; align-items: center !important; justify-content: center !important; }}
.block-container {{ max-width: {box_width} !important; padding: 0px !important; margin: auto !important; }}
[data-testid="stVerticalBlockBorderWrapper"] {{
    background-color: white !important;
    border: 2px solid #7c3aed !important;
    border-radius: 15px !important;
    box-shadow: 0px 10px 40px rgba(0,0,0,0.15);
    padding: 0px !important;
}}
.custom-header {{
    background: linear-gradient(180deg, #d8dee9 0%, #e5e9f0 100%);
    padding: 30px; font-size: 34px; font-weight: bold; color: #2e1065;
    border-bottom: 2px solid #7c3aed; border-radius: 13px 13px 0 0;
    text-align: center; margin-bottom: 25px;
}}
.inner-content {{ padding: 20px 50px 50px 50px; font-size: 22px; }}
label p {{ font-size: 24px !important; font-weight: bold !important; color: #1e1b4b !important; }}
.stButton>button {{
    background: #7c3aed !important; color: white !important; font-weight: bold !important;
    font-size: 22px !important; border-radius: 10px !important; width: 100%;
    border: none !important; padding: 12px !important; margin-top: 10px;
}}
.note-box {{
    background-color: #f8fafc;
    border-left: 5px solid #7c3aed;
    padding: 15px;
    margin-top: 20px;
    font-size: 18px;
    color: #475569;
    border-radius: 8px;
}}
</style>
""", unsafe_allow_html=True)

def nav(p):
    st.session_state.page = p
    st.rerun()

# -----------------------
# MODEL HANDLER
# -----------------------
def get_or_train_model():
    model_path = 'best_rf_model_components.pkl'
    if os.path.exists(model_path):
        try:
            return joblib.load(model_path)
        except:
            pass 
    
    train_df = pd.DataFrame({
        'store_nbr': [1, 54, 25, 10, 5, 40],
        'transactions': [1200, 4500, 2100, 3200, 1500, 3800],
        'onpromotion': [5, 45, 12, 20, 8, 30],
        'month': [1, 12, 6, 8, 3, 10],
        'sales': [20000, 58000, 31000, 39000, 24000, 48000]
    })
    model = RandomForestRegressor(n_estimators=50) 
    model.fit(train_df.drop('sales', axis=1), train_df['sales'])
    joblib.dump(model, model_path)
    return model

# -----------------------
# MAIN APP
# -----------------------
with st.container(border=True):
    
    # 1. LOGIN
    if st.session_state.page == "login":
        st.markdown('<div class="custom-header">Sales Forecasting App</div>', unsafe_allow_html=True)
        st.markdown('<div class="inner-content">', unsafe_allow_html=True)
        st.write("### 🔑 Login")
        st.text_input("Username")
        st.text_input("Password", type="password")
        if st.button("Login"): nav("welcome")
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. WELCOME
    elif st.session_state.page == "welcome":
        st.markdown('<div class="custom-header">📈 Welcome User</div>', unsafe_allow_html=True)
        st.markdown('<div class="inner-content">', unsafe_allow_html=True)
        st.success("### Ready to Forecast?")
        st.write("Access your dashboard and prediction tools to optimize retail inventory.")
        c1, c2 = st.columns(2)
        if c1.button("⬅ Back"): nav("login")
        if c2.button("Continue ➡"): nav("about")
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. ABOUT / PROJECT TRAIN (Restored Info)
    elif st.session_state.page == "about":
        st.markdown('<div class="custom-header">📘 Project & Training</div>', unsafe_allow_html=True)
        st.markdown('<div class="inner-content">', unsafe_allow_html=True)
        
        # RESTORED PROJECT INFO
        st.info("""
        **Project:** Sales Forecasting  
        **Models:** Linear Regression, Random Forest  
        **Final Model:** Random Forest
        """)
        
        if st.button("🛠 Train/Reset Model"):
            with st.spinner('Training model...'):
                get_or_train_model()
                time.sleep(1) 
            st.success("Model successfully trained and saved!")

        c1, c2, c3 = st.columns(3)
        if c1.button("⬅ Back"): nav("welcome")
        if c2.button("Dashboard"): nav("dashboard")
        if c3.button("Prediction"): nav("predict")
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. DASHBOARD (Full Note Guide)
    elif st.session_state.page == "dashboard":
        st.markdown('<div class="custom-header">📊 Forecast Dashboard</div>', unsafe_allow_html=True)
        st.markdown('<div class="inner-content">', unsafe_allow_html=True)
        st.write("### Store-wise Sales Analysis")
        data = pd.DataFrame({'Category': ['Dairy', 'Meat', 'Produce', 'Bakery', 'Deli', 'Frozen'], 'Sales': [500, 750, 950, 350, 600, 450]})
        st.bar_chart(data.set_index('Category'))
        
        st.markdown("""
        <div class="note-box">
        <strong>Department Reference Guide:</strong><br>
        • <strong>Dairy:</strong> Milk, butter, cheese, and eggs.<br>
        • <strong>Meat:</strong> Fresh poultry, beef, and pork.<br>
        • <strong>Produce:</strong> Fresh fruits and seasonal vegetables.<br>
        • <strong>Bakery:</strong> Freshly baked bread, cakes, and pastries.<br>
        • <strong>Deli:</strong> Prepared salads, sliced meats, and ready-to-eat meals.<br>
        • <strong>Frozen:</strong> Packaged frozen meals, vegetables, and ice cream.
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        if c1.button("⬅ Back"): nav("about")
        if c2.button("Prediction ➡"): nav("predict")
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. PREDICT (With Back Button)
    elif st.session_state.page == "predict":
        st.markdown('<div class="custom-header">📈 Predict Sales</div>', unsafe_allow_html=True)
        st.markdown('<div class="inner-content">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            s = st.number_input("Store Number", 1, 54, value=1)
            t = st.number_input("Transactions", 1, 10000, value=100)
        with col2:
            p = st.number_input("Items on Promotion", 0, 1000, value=0)
            m = st.number_input("Order Month", 1, 12, value=1)
        
        c1, c2 = st.columns(2)
        if c1.button("⬅ Back"): nav("dashboard") # Back Button Added
        if c2.button("Predict ➡"):
            model = get_or_train_model()
            input_data = pd.DataFrame([[s, t, p, m]], columns=['store_nbr', 'transactions', 'onpromotion', 'month'])
            prediction = model.predict(input_data)[0]
            st.session_state.raw_val = prediction
            st.session_state.final_result = f"$ {prediction:,.2f}"
            nav("result")
        st.markdown('</div>', unsafe_allow_html=True)

    # 6. RESULT (With Back Button)
    elif st.session_state.page == "result":
        st.markdown('<div class="custom-header">📊 Result</div>', unsafe_allow_html=True)
        st.markdown('<div class="inner-content">', unsafe_allow_html=True)
        
        res = st.session_state.get('final_result', 'N/A')
        raw = st.session_state.get('raw_val', 0)
        
        st.metric(label="Predicted Sales Revenue", value=res)
        st.write(f"The model predicts a revenue of **{res}** based on your inputs.")

        # Visual Comparison Chart
        chart_data = pd.DataFrame({
            'Metric': ['Average Sales', 'Your Result', 'Target'],
            'Value': [32000, raw, 48000]
        })
        st.bar_chart(chart_data.set_index('Metric'))
        
        c1, c2 = st.columns(2)
        if c1.button("⬅ Back to Predict"): nav("predict") # Back Button Added
        if c2.button("New Forecast"): nav("predict")
        st.markdown('</div>', unsafe_allow_html=True)
