import streamlit as st
import pandas as pd

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Retail Sales Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------
# CSS
# -----------------------------------
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.stApp{
background: linear-gradient(135deg,#dbeafe,#eff6ff,#ffffff);
}

.title{
font-size:42px;
font-weight:bold;
color:#0E6FFF;
text-align:center;
margin-bottom:15px;
}

.card{
background:white;
padding:20px;
border-radius:18px;
box-shadow:0 6px 15px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# SESSION
# -----------------------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "prediction" not in st.session_state:
    st.session_state.prediction = 0

# -----------------------------------
# LOGIN PAGE
# -----------------------------------
if st.session_state.page == "login":

    st.markdown("<br><div class='title'>📈 Retail Sales Intelligence</div>", unsafe_allow_html=True)

    c1,c2,c3 = st.columns([1,2,1])

    with c2:
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Login", key="login_btn"):
            if user == "admin" and pwd == "1234":
                st.session_state.page = "welcome"
                st.rerun()
            else:
                st.error("Invalid Login")

# -----------------------------------
# WELCOME PAGE
# -----------------------------------
elif st.session_state.page == "welcome":

    st.markdown("<div class='title'>Welcome</div>", unsafe_allow_html=True)

    st.success("Sales Forecasting Application using Machine Learning")

    col1,col2 = st.columns(2)

    with col1:
        if st.button("⬅ Back", key="wel_back"):
            st.session_state.page = "login"
            st.rerun()

    with col2:
        if st.button("Continue", key="wel_next"):
            st.session_state.page = "about"
            st.rerun()

# -----------------------------------
# ABOUT PAGE
# -----------------------------------
elif st.session_state.page == "about":

    st.markdown("<div class='title'>📘 About Project</div>", unsafe_allow_html=True)

    st.info("""
Project: Sales Forecasting using Machine Learning

Models Used:
• Linear Regression  
• Random Forest Regressor

Final Model:
✔ Random Forest
""")

    col1,col2,col3 = st.columns(3)

    with col1:
        if st.button("⬅ Back", key="about_back"):
            st.session_state.page = "welcome"
            st.rerun()

    with col2:
        if st.button("Dashboard", key="about_dash"):
            st.session_state.page = "dashboard"
            st.rerun()

    with col3:
        if st.button("Prediction", key="about_pred"):
            st.session_state.page = "predict"
            st.rerun()

# -----------------------------------
# DASHBOARD PAGE
# -----------------------------------
elif st.session_state.page == "dashboard":

    st.markdown("<div class='title'>📊 Dashboard</div>", unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)

    c1.metric("Stores", "54")
    c2.metric("Accuracy", "92%")
    c3.metric("Status", "Active")

    df = pd.DataFrame({
        "Month":["Jan","Feb","Mar","Apr","May"],
        "Sales":[100,160,140,220,300]
    })

    st.line_chart(df.set_index("Month"))

    col1,col2 = st.columns(2)

    with col1:
        if st.button("⬅ Back", key="dash_back"):
            st.session_state.page = "about"
            st.rerun()

    with col2:
        if st.button("Go to Prediction", key="dash_pred"):
            st.session_state.page = "predict"
            st.rerun()

# -----------------------------------
# PREDICTION PAGE
# -----------------------------------
elif st.session_state.page == "predict":

    st.markdown("<div class='title'>📈 Predict Sales</div>", unsafe_allow_html=True)

    store = st.number_input("Store Number", 1, 54, 1)
    promo = st.number_input("Items On Promotion", 0, 100, 0)
    trans = st.number_input("Transactions", 0, 10000, 500)

    col1,col2 = st.columns(2)

    with col1:
        if st.button("Predict Sales", key="pred_btn"):

            result = (store*5) + (promo*8) + (trans*0.45)

            st.session_state.prediction = result
            st.session_state.page = "result"
            st.rerun()

    with col2:
        if st.button("⬅ Back", key="pred_back"):
            st.session_state.page = "dashboard"
            st.rerun()

# -----------------------------------
# RESULT PAGE
# -----------------------------------
elif st.session_state.page == "result":

    st.markdown("<div class='title'>📈 Result</div>", unsafe_allow_html=True)

    st.success(f"Predicted Sales = ₹ {st.session_state.prediction:,.2f}")

    col1,col2,col3 = st.columns(3)

    with col1:
        if st.button("⬅ Back", key="res_back"):
            st.session_state.page = "predict"
            st.rerun()

    with col2:
        if st.button("Dashboard", key="res_dash"):
            st.session_state.page = "dashboard"
            st.rerun()

    with col3:
        if st.button("Logout", key="res_logout"):
            st.session_state.page = "login"
            st.rerun()