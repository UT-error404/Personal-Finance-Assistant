"""
FinanceIQ — Personal Finance Assistant
Run  :  streamlit run app.py
Deps :  pip install streamlit pandas matplotlib numpy google-generativeai
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import html as _html
import hashlib
import json
import os
import google.generativeai as genai

# ════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="FinanceIQ",
    page_icon="₹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ════════════════════════════════════════════════════════════════════
#  DESIGN TOKENS
# ════════════════════════════════════════════════════════════════════
N      = "#0A1628"
N2     = "#142238"
N3     = "#1E3352"
ACCENT = "#C8962E"
ACCENT2= "#E8B84B"
SAGE   = "#2E8B6E"
RED    = "#C0392B"
CREAM  = "#F5F4F0"
WHITE  = "#FFFFFF"
TEXT   = "#1C1C2E"
MUTED  = "#5A6B7C"
BORD   = "#DDE3EC"
SIDE_BG= "#0D1E35"
SIDE_T = "#C8D8E8"
SIDE_A = "#E8B84B"

CPAL = [N, ACCENT, SAGE, RED, "#6B48CC", "#0B7D9E", "#C0841A"]

# ════════════════════════════════════════════════════════════════════
#  GEMINI CONFIG  — replace with your key or set env var
# ════════════════════════════════════════════════════════════════════
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6JeQZpyXwU64ROzZ5X8EDJeaOdYPMUHE6VrZJcdcNglyw")

# ════════════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ════════════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&family=Playfair+Display:wght@700&display=swap');

*, body {{ font-family: 'DM Sans', sans-serif; color: {TEXT}; }}
[data-testid="stAppViewContainer"] {{ background: {CREAM}; }}
[data-testid="block-container"] {{ padding-top: 1.8rem; padding-bottom: 3rem; }}
footer {{ display: none; }}
div[data-baseweb="notification"] {{ display: none; }}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {{
    background: {SIDE_BG} !important;
    border-right: 1px solid #1A3050;
}}
[data-testid="stSidebar"] * {{ color: {SIDE_T} !important; }}
[data-testid="stSidebar"] hr {{ border-color: #1A3050 !important; }}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label p {{
    font-size: 1.0rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    color: {SIDE_T} !important;
    letter-spacing: 0.01em;
    padding: 3px 0;
}}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label {{
    padding: 6px 10px !important;
    border-radius: 7px !important;
    transition: background 0.15s;
}}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover {{
    background: #1A3050 !important;
}}

/* ── METRICS ── */
div[data-testid="metric-container"] {{
    background: {WHITE};
    border-radius: 12px;
    padding: 20px 18px;
    border-top: 3px solid {ACCENT};
    box-shadow: 0 2px 10px rgba(10,22,40,0.08);
}}
div[data-testid="metric-container"] label {{
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: {MUTED} !important;
}}
[data-testid="stMetricValue"] > div {{
    font-family: 'DM Mono', monospace !important;
    font-size: 1.5rem !important;
    font-weight: 500 !important;
    color: {N} !important;
}}
[data-testid="stMetricDelta"] {{ font-size: 0.78rem !important; color: {SAGE} !important; }}

h1, h2, h3, h4 {{ font-family: 'DM Sans', sans-serif !important; color: {N}; font-weight: 700; }}
.stProgress > div > div > div > div {{ background: {ACCENT} !important; }}

.stButton > button {{
    background: {N} !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.015em !important;
    padding: 0.55rem 1.4rem !important;
    transition: background .15s, box-shadow .15s !important;
    box-shadow: 0 2px 6px rgba(10,22,40,.15) !important;
}}
.stButton > button:hover {{ background: {N3} !important; box-shadow: 0 4px 12px rgba(10,22,40,.25) !important; }}

.stNumberInput input, .stTextArea textarea, .stTextInput input, .stSelectbox div {{
    border-radius: 8px !important;
    border: 1.5px solid {BORD} !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    background: {WHITE} !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}}

/* ── INPUT TEXT VISIBILITY ── */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea,
[data-baseweb="select"] *,
[data-baseweb="select"] [role="option"] {{
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder,
.stNumberInput input::placeholder {{
    color: #5A6B7C !important;
    -webkit-text-fill-color: #5A6B7C !important;
    opacity: 1 !important;
}}

.stTabs [data-baseweb="tab-list"] {{ border-bottom: 2px solid {BORD}; gap: 0; }}
.stTabs [data-baseweb="tab"] {{
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    padding: 10px 22px;
    color: {MUTED} !important;
    border-radius: 0 !important;
}}
.stTabs [aria-selected="true"] {{
    color: {N} !important;
    border-bottom: 2px solid {ACCENT} !important;
    font-weight: 700 !important;
}}

.stExpander {{ border: 1px solid {BORD} !important; border-radius: 10px !important; }}
.stExpander summary {{ font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important; font-size: 0.95rem !important; }}
.stDataFrame {{ border-radius: 10px !important; overflow: hidden; }}
.stSelectbox label, .stNumberInput label, .stTextInput label, .stSlider label {{
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    color: {N} !important;
    letter-spacing: 0.01em;
}}

/* ── CUSTOM CLASSES ── */
.eyebrow {{
    font-size: 0.68rem; font-weight: 700;
    letter-spacing: 0.16em; text-transform: uppercase;
    color: {ACCENT}; margin-bottom: 4px;
}}
.page-title {{
    font-family: 'DM Sans', sans-serif;
    font-size: 1.85rem; font-weight: 700; color: {N};
    margin-bottom: 0.1rem; letter-spacing: -0.02em;
}}
.page-sub {{
    font-size: 0.92rem; color: {MUTED}; margin-bottom: 1.6rem; line-height: 1.6;
}}
.card {{
    background: {WHITE}; border-radius: 12px;
    padding: 22px 24px; border: 1px solid {BORD};
    box-shadow: 0 2px 10px rgba(10,22,40,.06); margin-bottom: 14px;
}}
.dark-banner {{
    background: {N}; border-radius: 14px;
    padding: 22px 26px; margin-bottom: 18px;
    border-left: 4px solid {ACCENT};
}}
.dark-banner p {{ color: #A8BDD0; font-size: 0.92rem; line-height: 1.7; margin: 0; }}
.dark-banner strong {{ color: {ACCENT2}; }}
.principle-row {{
    display: flex; align-items: flex-start;
    gap: 12px; padding: 12px 0;
    border-bottom: 1px solid {BORD};
}}
.principle-body {{ font-size: 0.9rem; line-height: 1.6; color: {TEXT}; }}
.principle-body b {{ color: {N}; }}
.chat-bubble-user {{
    background: {N}; color: #FAFAF8;
    padding: 11px 15px; border-radius: 12px 12px 4px 12px;
    margin: 7px 0 7px 18%; font-size: 0.88rem; line-height: 1.55;
}}
.chat-bubble-ai {{
    background: {WHITE}; color: {TEXT};
    border: 1px solid {BORD}; border-left: 3px solid {ACCENT};
    padding: 11px 15px; border-radius: 12px 12px 12px 4px;
    margin: 7px 18% 7px 0; font-size: 0.88rem; line-height: 1.7;
    white-space: pre-wrap;
}}
.chat-wrap {{
    max-height: 380px; overflow-y: auto;
    background: #EEF1F7; border-radius: 12px;
    padding: 10px; margin-bottom: 12px;
    border: 1px solid {BORD};
}}
.score-circle {{
    display: flex; align-items: center; justify-content: center;
    width: 136px; height: 136px; border-radius: 50%;
    font-family: 'DM Mono', monospace;
    font-size: 2.8rem; font-weight: 500; border-width: 7px;
    border-style: solid; margin: 0 auto 14px;
}}
.dashboard-chart-title {{
    font-family: 'DM Sans', sans-serif;
    font-size: 0.97rem; font-weight: 700; color: {N};
    margin-bottom: 14px; letter-spacing: -0.01em;
}}
.login-card {{
    max-width: 440px; margin: 60px auto;
    background: {WHITE}; border-radius: 18px;
    padding: 40px 44px;
    border: 1px solid {BORD};
    box-shadow: 0 8px 40px rgba(10,22,40,.12);
}}
.month-pill {{
    display: inline-block;
    background: {ACCENT}22; border: 1px solid {ACCENT};
    border-radius: 20px; padding: 4px 14px;
    font-size: 0.8rem; font-weight: 700; color: {ACCENT};
    letter-spacing: 0.06em; text-transform: uppercase;
    margin-bottom: 14px;
}}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
#  USER STORE  (in-memory for this session; replace with a DB for prod)
# ════════════════════════════════════════════════════════════════════
if "users" not in st.session_state:
    st.session_state.users = {}      # {phone: hashed_password}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None


def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


def validate_phone(ph: str) -> bool:
    digits = ph.replace(" ", "").replace("-", "")
    return digits.isdigit() and 10 <= len(digits) <= 13


# ════════════════════════════════════════════════════════════════════
#  LOGIN / REGISTER PAGE
# ════════════════════════════════════════════════════════════════════
def show_login():
    st.markdown(f"""
<div style='text-align:center;padding:40px 0 10px;'>
    <div style='font-family:DM Sans,sans-serif;font-size:2.2rem;
                font-weight:700;color:{N};letter-spacing:-0.03em;'>FinanceIQ</div>
    <div style='font-size:0.85rem;color:{MUTED};letter-spacing:0.12em;
                text-transform:uppercase;margin-top:4px;'>Personal Finance Platform</div>
</div>
""", unsafe_allow_html=True)

    tab_login, tab_reg = st.tabs(["Sign In", "Create Account"])

    with tab_login:
        st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)
        phone = st.text_input("Mobile Number", placeholder="e.g. 9876543210", key="login_phone")
        pwd   = st.text_input("Password", type="password", key="login_pwd")
        if st.button("Sign In", use_container_width=True, key="btn_login"):
            ph = phone.strip()
            if not ph or not pwd:
                st.error("Please enter your mobile number and password.")
            elif not validate_phone(ph):
                st.error("Enter a valid mobile number (10-13 digits).")
            elif ph not in st.session_state.users:
                st.error("No account found. Please create an account first.")
            elif st.session_state.users[ph] != hash_pw(pwd):
                st.error("Incorrect password.")
            else:
                st.session_state.authenticated = True
                st.session_state.current_user  = ph
                _init_user_state(ph)
                st.rerun()

    with tab_reg:
        st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)
        r_phone = st.text_input("Mobile Number", placeholder="e.g. 9876543210", key="reg_phone")
        r_pwd   = st.text_input("Create Password (min 6 chars)", type="password", key="reg_pwd")
        r_pwd2  = st.text_input("Confirm Password", type="password", key="reg_pwd2")
        if st.button("Create Account", use_container_width=True, key="btn_reg"):
            ph = r_phone.strip()
            if not ph or not r_pwd:
                st.error("All fields are required.")
            elif not validate_phone(ph):
                st.error("Enter a valid mobile number (10-13 digits).")
            elif len(r_pwd) < 6:
                st.error("Password must be at least 6 characters.")
            elif r_pwd != r_pwd2:
                st.error("Passwords do not match.")
            elif ph in st.session_state.users:
                st.error("An account with this number already exists. Please sign in.")
            else:
                st.session_state.users[ph] = hash_pw(r_pwd)
                st.session_state.authenticated = True
                st.session_state.current_user  = ph
                _init_user_state(ph)
                st.success("Account created. Welcome to FinanceIQ.")
                st.rerun()

    st.markdown(f"""
<div style='text-align:center;margin-top:32px;font-size:0.75rem;color:{MUTED};line-height:1.8;'>
    General information only. Consult a SEBI-registered advisor for a personalised plan.
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
#  PER-USER STATE INIT
# ════════════════════════════════════════════════════════════════════
MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

def _init_user_state(ph: str):
    """Initialise session-state keys namespaced to this user."""
    key = f"data_{ph}"
    if key not in st.session_state:
        st.session_state[key] = {
            "global_income":  0.0,
            "qa_log":         [],
            "bp_needs_p":     50,
            "bp_wants_p":     30,
            "selected_month": MONTHS[0],
            # monthly budget data  { "January": {...}, ... }
            "monthly_budget": {},
            "sg_goal":        0.0,
            "sg_current":     0.0,
            "sg_months":      24,
            "sg_rate":        7.0,
            "dm_n_debts":     2,
            "dm_emi":         0.0,
            "dm_debts":       [{"name": f"Loan {i+1}", "amount": 0.0, "rate": 12.0} for i in range(7)],
            "ef_months":      6,
            "ef_current":     0.0,
            "hs_savings":     0.0,
            "hs_emi":         0.0,
            "hs_ef_months":   0.0,
            "hs_has_ins":     False,
            "hs_has_wil":     False,
            "hs_has_sip":     False,
        }


def U() -> dict:
    """Return the current user's data dict."""
    return st.session_state[f"data_{st.session_state.current_user}"]


def US(key, val):
    """Set a value in the current user's data dict."""
    U()[key] = val


def _default_month_data(income: float, needs_p: int, wants_p: int) -> dict:
    return {
        "bp_act_rent":  0.0,
        "bp_act_groc":  0.0,
        "bp_act_util":  0.0,
        "bp_act_trans": 0.0,
        "bp_act_ins":   0.0,
        "bp_act_dining":0.0,
        "bp_act_ent":   0.0,
        "bp_act_shop":  0.0,
        "bp_act_ef":    0.0,
        "bp_act_sip":   0.0,
    }


def get_month_data(month: str) -> dict:
    mb = U()["monthly_budget"]
    if month not in mb:
        mb[month] = _default_month_data(U()["global_income"], U()["bp_needs_p"], U()["bp_wants_p"])
    return mb[month]


def set_month_data(month: str, data: dict):
    U()["monthly_budget"][month] = data


def needs_total_for_month(month: str) -> float:
    d = get_month_data(month)
    return d["bp_act_rent"] + d["bp_act_groc"] + d["bp_act_util"] + d["bp_act_trans"] + d["bp_act_ins"]


# ════════════════════════════════════════════════════════════════════
#  CHART HELPERS
# ════════════════════════════════════════════════════════════════════
def new_fig(w=6.0, h=4.5):
    fig, ax = plt.subplots(figsize=(w, h), facecolor=WHITE)
    ax.set_facecolor(WHITE)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(BORD)
    ax.spines["bottom"].set_color(BORD)
    ax.tick_params(colors=MUTED, labelsize=8)
    return fig, ax


def pie_fig(values, labels, colors=None, w=5.5, h=5.0):
    colors = colors or CPAL
    fig, ax = plt.subplots(figsize=(w, h), facecolor=WHITE)
    wedge_props = {"linewidth": 2.5, "edgecolor": WHITE}
    ax.pie(values, labels=labels, colors=colors,
           autopct="%1.1f%%", startangle=90,
           wedgeprops=wedge_props, pctdistance=0.78,
           textprops={"fontsize": 9.5, "color": TEXT})
    return fig, ax


# ════════════════════════════════════════════════════════════════════
#  INCOME BANNER
# ════════════════════════════════════════════════════════════════════
def income_banner():
    u = U()
    new_val = st.number_input(
        "Monthly Take-Home Income (₹) — shared across all pages",
        min_value=0.0, step=1000.0, format="%.0f",
        value=u["global_income"],
        help="Enter once. Carries across all pages.",
    )
    if new_val != u["global_income"]:
        US("global_income", new_val)
    st.markdown("<hr style='margin:8px 0 18px 0;border-color:#DDE3EC;'>", unsafe_allow_html=True)
    return u["global_income"]


# ════════════════════════════════════════════════════════════════════
#  GEMINI Q&A
# ════════════════════════════════════════════════════════════════════
FINANCE_SYSTEM = (
    "You are FinanceIQ, a professional personal finance advisor for Indian users. "
    "Answer questions about budgeting (50-30-20), savings, debt management, mutual funds, SIPs, "
    "PPF, NPS, ELSS, emergency funds, term and health insurance, tax saving (80C, 80D, HRA), "
    "and retirement planning. Keep answers practical, concise, and specific to India's financial "
    "products and tax laws. Do not discuss topics outside personal finance. "
    "Do not use emojis. Use plain text, avoid markdown symbols like ** or ##."
)

def ask_gemini(question: str, history: list) -> str:
    try:
        genai.configure(api_key="AQ.Ab8RN6Kx914MJBv_2ahVDEEJkBRJmieefHsWhtcNtY5-E3rcAA")
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=FINANCE_SYSTEM,
        )
        chat = model.start_chat(history=[
            {"role": m["role"] if m["role"] == "user" else "model",
             "parts": [m["content"]]}
            for m in history[-8:] if m["role"] in ("user", "advisor")
        ])
        resp = chat.send_message(question)
        return resp.text.strip()
    except Exception as e:
        return (
            f"Unable to reach the AI service right now ({type(e).__name__}). "
            "Please check your Gemini API key or try again shortly.\n\n"
            "Tip: Set the GEMINI_API_KEY environment variable before starting the app."
        )


# ════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════════════════════════════
NAV_ITEMS = [
    "Home",
    "Budget Planner",
    "Savings Goal",
    "Debt Manager",
    "Emergency Fund",
    "Health Score",
    "Finance Q&A",
]

# ════════════════════════════════════════════════════════════════════
#  AUTHENTICATION GATE
# ════════════════════════════════════════════════════════════════════
if not st.session_state.authenticated:
    show_login()
    st.stop()

# ════════════════════════════════════════════════════════════════════
#  MAIN APP (authenticated)
# ════════════════════════════════════════════════════════════════════
u = U()

with st.sidebar:
    st.markdown(f"""
<div style='padding:10px 4px 8px;'>
    <div style='font-family:DM Sans,sans-serif;font-size:1.65rem;
                font-weight:700;color:#FFFFFF;letter-spacing:-0.03em;'>FinanceIQ</div>
    <div style='font-size:0.72rem;color:#5A7A9A;letter-spacing:0.14em;
                text-transform:uppercase;margin-top:4px;'>Personal Finance</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "nav",
        NAV_ITEMS,
        label_visibility="collapsed",
    )

    st.markdown("---")

    if u["global_income"] > 0:
        st.markdown(f"""
<div style='margin-bottom:12px;'>
    <div style='font-size:0.72rem;color:#4A6A88;font-weight:700;
                letter-spacing:0.12em;text-transform:uppercase;margin-bottom:5px;'>Active Income</div>
    <div style='font-size:1.2rem;color:{SIDE_A};font-family:DM Mono,monospace;
                font-weight:500;'>&#8377;{u["global_income"]:,.0f} / mo</div>
</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div style='font-size:0.78rem;color:#3A5A78;line-height:1.75;margin-bottom:18px;'>
    Signed in as<br>
    <span style='color:#8AABB8;font-weight:600;'>{st.session_state.current_user}</span>
</div>
""", unsafe_allow_html=True)

    if st.button("Sign Out", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.current_user  = None
        st.rerun()

    st.markdown(f"""
<div style='font-size:0.72rem;color:#2E4A60;line-height:1.7;margin-top:8px;'>
    General information only.<br>
    Consult a SEBI-registered advisor<br>for personalised advice.
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
#  HOME
# ════════════════════════════════════════════════════════════════════
if page == "Home":
    st.markdown(f"""
<div class='eyebrow'>Personal Finance Assistant</div>
<div class='page-title'>Make every rupee count.</div>
<div class='page-sub'>Your financial summary — fill in the other pages and watch this update.</div>
""", unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Savings Target",      "20%+",     "of take-home pay")
    k2.metric("Emergency Fund",      "6 Months", "essential expenses")
    k3.metric("Healthy Debt Ratio",  "Below 36%","EMI to income")
    k4.metric("Investment Horizon",  "10+ Years","stay invested")

    st.markdown("<br>", unsafe_allow_html=True)

    income   = u["global_income"]
    bp_needs = u["bp_needs_p"]
    bp_wants = u["bp_wants_p"]
    bp_sav   = 100 - bp_needs - bp_wants

    sel_month = u.get("selected_month", MONTHS[0])
    needs_actual = needs_total_for_month(sel_month)

    has_budget_data  = income > 0
    has_savings_data = u["sg_goal"] > 0
    has_ef_data      = needs_actual > 0

    if has_budget_data or has_savings_data or has_ef_data:
        st.markdown(f"""
<div style='background:{N};border-radius:14px;padding:16px 24px;margin-bottom:24px;
            border-left:4px solid {ACCENT};'>
    <div style='font-family:DM Sans,sans-serif;font-size:1.05rem;
                font-weight:700;color:#fff;'>Your Financial Dashboard</div>
    <div style='font-size:0.83rem;color:#7A9BB8;'>Live summary from data across your pages</div>
</div>
""", unsafe_allow_html=True)

        dash_cols = st.columns(3, gap="large")

        if has_budget_data and bp_sav >= 0:
            n_amt = income * bp_needs / 100
            w_amt = income * bp_wants / 100
            s_amt = income * bp_sav   / 100
            with dash_cols[0]:
                st.markdown(f"<div class='dashboard-chart-title'>Budget Split</div>", unsafe_allow_html=True)
                fig_d1, _ = pie_fig(
                    [n_amt, w_amt, s_amt],
                    [f"Needs\n{bp_needs}%", f"Wants\n{bp_wants}%", f"Savings\n{bp_sav}%"],
                    colors=[N, ACCENT, SAGE], w=4.2, h=3.8,
                )
                st.pyplot(fig_d1, use_container_width=True)
                plt.close(fig_d1)
                sr_color = SAGE if bp_sav >= 20 else (ACCENT if bp_sav >= 10 else RED)
                st.markdown(f"""
<div style='background:{sr_color}18;border-left:3px solid {sr_color};
            border-radius:8px;padding:9px 14px;font-size:0.83rem;color:{N};'>
    Saving <b>{bp_sav}%</b> — &#8377;{s_amt:,.0f}/month
    {"   On target" if bp_sav >= 20 else "   Target is 20%"}
</div>""", unsafe_allow_html=True)

        if has_savings_data:
            goal    = u["sg_goal"]
            current = u["sg_current"]
            months  = u["sg_months"]
            rate    = u["sg_rate"]
            remaining = max(goal - current, 0.0)
            r_m = rate / 100 / 12
            if r_m > 0 and remaining > 0:
                sip = remaining * r_m / ((1 + r_m) ** months - 1)
            else:
                sip = remaining / months if months > 0 else 0
            m_arr = list(range(0, months + 1))
            growth = [current * (1+r_m)**m + sip * ((1+r_m)**m - 1) / r_m for m in m_arr] if r_m > 0 else [current + sip * m for m in m_arr]
            with dash_cols[1]:
                st.markdown(f"<div class='dashboard-chart-title'>Savings Goal</div>", unsafe_allow_html=True)
                fig_d2, ax_d2 = new_fig(4.2, 3.8)
                ax_d2.plot(m_arr, [v/1000 for v in growth], color=N, lw=2.5)
                ax_d2.axhline(goal/1000, color=ACCENT, ls=":", lw=2)
                ax_d2.fill_between(m_arr, [v/1000 for v in growth], alpha=0.1, color=N)
                ax_d2.set_xlabel("Month", fontsize=8)
                ax_d2.set_ylabel("Rs thousands", fontsize=8)
                ax_d2.grid(True, alpha=0.15)
                st.pyplot(fig_d2, use_container_width=True)
                plt.close(fig_d2)
                prog = min(current / goal, 1.0) if goal > 0 else 0
                st.progress(prog)
                st.markdown(f"<div style='font-size:0.82rem;color:{MUTED};'>&#8377;{current:,.0f} of &#8377;{goal:,.0f} &nbsp;&middot;&nbsp; SIP needed: <b style='color:{SAGE};'>&#8377;{sip:,.0f}/mo</b></div>", unsafe_allow_html=True)

        if has_ef_data:
            months_ef  = u["ef_months"]
            target_ef  = needs_actual * months_ef
            current_ef = u["ef_current"]
            prog_ef    = min(current_ef / target_ef, 1.0) if target_ef > 0 else 0
            with dash_cols[2]:
                st.markdown(f"<div class='dashboard-chart-title'>Emergency Fund</div>", unsafe_allow_html=True)
                md = get_month_data(sel_month)
                exp_dict = {k: v for k, v in {
                    "Rent/EMI": md["bp_act_rent"], "Groceries": md["bp_act_groc"],
                    "Utilities": md["bp_act_util"], "Transport": md["bp_act_trans"],
                    "Insurance": md["bp_act_ins"],
                }.items() if v > 0}
                if exp_dict:
                    fig_d3, _ = pie_fig(list(exp_dict.values()), list(exp_dict.keys()), colors=CPAL, w=4.2, h=3.8)
                    st.pyplot(fig_d3, use_container_width=True)
                    plt.close(fig_d3)
                gap = max(target_ef - current_ef, 0)
                ef_color = SAGE if prog_ef >= 1.0 else (ACCENT if prog_ef >= 0.5 else RED)
                st.progress(prog_ef)
                st.markdown(f"<div style='background:{ef_color}18;border-left:3px solid {ef_color};border-radius:8px;padding:9px 14px;font-size:0.83rem;color:{N};'><b>{prog_ef*100:.0f}%</b> funded — {'Complete' if gap==0 else f'&#8377;{gap:,.0f} to go'}</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.markdown(f"""
<div class='dark-banner'>
<p><strong>Your dashboard is waiting.</strong><br><br>
Start by entering your monthly income on any calculator page. Charts will appear here automatically.</p>
</div>""", unsafe_allow_html=True)

    left, right = st.columns([1.65, 1], gap="large")
    with left:
        st.markdown("### Core Concepts")
        t1, t2, t3 = st.tabs(["50-30-20 Rule", "Power of Compounding", "Safety Net Order"])
        with t1:
            st.markdown("""
**Split your take-home pay into three purposeful buckets:**

| Category | Share | Examples |
|----------|-------|---------|
| Needs | **50%** | Rent, groceries, EMIs, utilities, transport |
| Wants | **30%** | Dining, OTT, gadgets, leisure travel |
| Savings | **20%** | SIPs, FD, PPF, emergency fund, NPS |

Adjust for your city and life stage — tracking consistently matters more than hitting the exact split.
""")
        with t2:
            st.markdown("""
| Monthly SIP | 10 years | 20 years | 30 years |
|------------|----------|----------|----------|
| Rs 3,000 | Rs 6.97 L | Rs 27.6 L | Rs 1.06 Cr |
| Rs 5,000 | Rs 11.6 L | Rs 46 L | Rs 1.76 Cr |
| Rs 10,000 | Rs 23.2 L | Rs 91.9 L | Rs 3.52 Cr |

*Assumes 12% p.a. (historical long-run equity average). Not guaranteed.*
""")
        with t3:
            st.markdown("""
1. **1-Month Expense Buffer** — cash in savings account, always accessible.
2. **Term + Health Insurance** — protect income and health before investing.
3. **Full Emergency Fund** — grow the buffer to 3-6 months in a liquid fund.
4. **High-Interest Debt Cleared** — credit cards and personal loans at 18%+ gone.
5. **Retirement Contributions** — EPF, PPF, NPS, ELSS with compounding runway.
6. **Goal-Based Investing** — home, education, car — now you can plan these.
""")

    with right:
        st.markdown("### Financial Wellness Principles")
        principles = [
            ("Spend less than you earn", "The foundation of every financial plan. The gap between income and spending is where wealth is built."),
            ("Automate your savings", "Set a transfer to trigger on salary day. Willpower runs out — automation does not."),
            ("Avoid lifestyle inflation", "As income grows, resist the pull to expand spending proportionally. Invest the difference."),
            ("Insure before you invest", "A single medical emergency erases years of savings. Term plus health cover first."),
            ("Stay invested through volatility", "Markets drop. Investors who stay put capture the recovery. Timing the market rarely works."),
        ]
        for headline, detail in principles:
            st.markdown(f"""
<div class='principle-row'>
    <div class='principle-body'><b>{headline}.</b> {detail}</div>
</div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
#  BUDGET PLANNER
# ════════════════════════════════════════════════════════════════════
elif page == "Budget Planner":
    st.markdown(f"""
<div class='eyebrow'>Calculator</div>
<div class='page-title'>Budget Planner</div>
<div class='page-sub'>Select a month, enter your expenses, and see how you track against the 50-30-20 framework. Data is saved per month.</div>
""", unsafe_allow_html=True)

    income = income_banner()

    # Month selector
    col_month, _ = st.columns([1, 2])
    with col_month:
        sel_month = st.selectbox(
            "Select Month",
            MONTHS,
            index=MONTHS.index(u.get("selected_month", MONTHS[0])),
            key="bp_month_select",
        )
        US("selected_month", sel_month)

    st.markdown(f"<div class='month-pill'>{sel_month} Budget</div>", unsafe_allow_html=True)

    # Get or init this month's data
    md = get_month_data(sel_month)

    inp_col, chart_col = st.columns([1, 1.15], gap="large")

    with inp_col:
        st.markdown("#### Allocation")
        needs_p = st.slider("Needs (%)", 20, 70, value=u["bp_needs_p"], step=5, key="bp_needs_slider")
        wants_p = st.slider("Wants (%)", 10, 50, value=u["bp_wants_p"], step=5, key="bp_wants_slider")
        US("bp_needs_p", needs_p)
        US("bp_wants_p", wants_p)
        sav_p = 100 - needs_p - wants_p

        if sav_p < 0:
            st.error("Needs + Wants exceed 100%. Reduce one slider.")
        else:
            color = SAGE if sav_p >= 20 else (ACCENT if sav_p >= 10 else RED)
            st.markdown(f"""
<div style='background:{WHITE};border-left:4px solid {color};border-radius:8px;
            padding:13px 16px;font-family:DM Sans,sans-serif;font-size:1.05rem;
            font-weight:600;color:{N};box-shadow:0 1px 6px rgba(10,22,40,.07);'>
    Savings = {sav_p}% {"  — On target" if sav_p >= 20 else "  — Aim for 20%"}
</div>""", unsafe_allow_html=True)

    if income > 0 and sav_p >= 0:
        n_amt = income * needs_p / 100
        w_amt = income * wants_p / 100
        s_amt = income * sav_p   / 100

        with inp_col:
            st.markdown("#### Monthly Allocation")
            c1, c2, c3 = st.columns(3)
            c1.metric(f"Needs ({needs_p}%)",   f"₹{n_amt:,.0f}")
            c2.metric(f"Wants ({wants_p}%)",   f"₹{w_amt:,.0f}")
            c3.metric(f"Savings ({sav_p}%)",   f"₹{s_amt:,.0f}")

        with chart_col:
            fig, _ = pie_fig(
                [n_amt, w_amt, s_amt],
                [f"Needs\n₹{n_amt/1000:.1f}K", f"Wants\n₹{w_amt/1000:.1f}K", f"Savings\n₹{s_amt/1000:.1f}K"],
                colors=[N, ACCENT, SAGE],
            )
            plt.gca().set_title("Budget Distribution", fontsize=12, fontweight="bold", color=N, pad=14)
            st.pyplot(fig)
            plt.close(fig)
            msg_color = RED if sav_p < 20 else (SAGE if sav_p >= 30 else ACCENT)
            msg = (f"Savings rate is {sav_p}%. Target is 20%. Consider reducing wants by ₹{(income*(20-sav_p)/100):,.0f}/month." if sav_p < 20
                   else (f"Excellent — saving {sav_p}%. Compounding works strongly in your favour." if sav_p >= 30
                         else f"Good start at {sav_p}%. Nudge this to 25-30% as income grows."))
            st.markdown(f"<div style='background:{msg_color}18;border-left:4px solid {msg_color};border-radius:8px;padding:12px 16px;font-size:0.88rem;color:{N};margin-top:8px;'>{msg}</div>", unsafe_allow_html=True)

        # ── EXPENSE TRACKER ──────────────────────────────────
        st.markdown("---")
        st.markdown(f"### Expense Tracker — {sel_month}")
        st.markdown("<p style='font-size:0.86rem;color:#5A6B7C;margin-bottom:18px;'>Enter actual monthly spending. Data is saved for this month automatically.</p>", unsafe_allow_html=True)

        def render_section(title, color, suggested_total, items_def):
            """items_def: list of (label, suggested, key_in_md)"""
            st.markdown(f"""
<div style='background:{color};color:#E8EEF4;font-family:DM Sans,sans-serif;
            font-size:0.78rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;
            padding:10px 16px;border-radius:8px 8px 0 0;'>
    {title} &nbsp;|&nbsp; Suggested: &#8377;{suggested_total:,.0f}
</div>""", unsafe_allow_html=True)

            hc1, hc2, hc3, hc4 = st.columns([2.2, 1.3, 1.8, 1.3])
            for h, t in zip([hc1,hc2,hc3,hc4], ["Category","Suggested (₹)","Your Actual (₹)","Difference"]):
                h.markdown(f"<div style='font-size:0.72rem;font-weight:700;color:{MUTED};text-transform:uppercase;padding:8px 4px 4px;'>{t}</div>", unsafe_allow_html=True)

            actual_total = 0.0
            sugg_total   = 0.0
            new_md = dict(md)
            for label, suggested, mkey in items_def:
                c1, c2, c3, c4 = st.columns([2.2, 1.3, 1.8, 1.3])
                c1.markdown(f"<div style='padding:6px 4px;font-size:0.86rem;color:{N};font-weight:500;'>{label}</div>", unsafe_allow_html=True)
                c2.markdown(f"<div style='padding:6px 4px;font-size:0.86rem;color:{MUTED};'>₹{suggested:,.0f}</div>", unsafe_allow_html=True)
                val = c3.number_input(
                    f"_{mkey}_{sel_month}",
                    min_value=0.0, step=100.0, format="%.0f",
                    value=md.get(mkey, 0.0),
                    label_visibility="collapsed",
                    key=f"input_{mkey}_{sel_month}",
                )
                new_md[mkey] = val
                diff = suggested - val
                dc = SAGE if diff >= 0 else RED
                dp = "+" if diff > 0 else ""
                c4.markdown(f"<div style='padding:6px 4px;font-size:0.86rem;font-weight:600;color:{dc};'>{dp}₹{diff:,.0f}</div>", unsafe_allow_html=True)
                actual_total += val
                sugg_total   += suggested

            set_month_data(sel_month, new_md)
            md.update(new_md)

            td = sugg_total - actual_total
            tc = SAGE if td >= 0 else RED
            tp = "+" if td > 0 else ""
            th1, th2, th3, th4 = st.columns([2.2, 1.3, 1.8, 1.3])
            th1.markdown(f"<div style='font-size:0.86rem;font-weight:700;color:{N};padding:6px 4px;'>{title.split()[0]} Total</div>", unsafe_allow_html=True)
            th2.markdown(f"<div style='font-size:0.86rem;font-weight:700;color:{N};padding:6px 4px;'>₹{sugg_total:,.0f}</div>", unsafe_allow_html=True)
            th3.markdown(f"<div style='font-size:0.86rem;font-weight:700;color:{N};padding:6px 4px;'>₹{actual_total:,.0f}</div>", unsafe_allow_html=True)
            th4.markdown(f"<div style='font-size:0.86rem;font-weight:700;color:{tc};padding:6px 4px;'>{tp}₹{td:,.0f}</div>", unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)
            return actual_total

        needs_actual_total = render_section("NEEDS", N, n_amt, [
            ("Rent / EMI",       income*0.25, "bp_act_rent"),
            ("Groceries",        income*0.10, "bp_act_groc"),
            ("Utilities",        income*0.05, "bp_act_util"),
            ("Transport",        income*0.08, "bp_act_trans"),
            ("Insurance Prem.",  income*0.02, "bp_act_ins"),
        ])
        wants_actual_total = render_section("WANTS", N2, w_amt, [
            ("Dining Out",    income*0.10, "bp_act_dining"),
            ("Entertainment", income*0.08, "bp_act_ent"),
            ("Shopping",      income*0.07, "bp_act_shop"),
        ])
        savings_actual_total = render_section("SAVINGS", SAGE, s_amt, [
            ("Emergency Fund Build", income*0.05, "bp_act_ef"),
            ("SIP / Investment",     income*0.15, "bp_act_sip"),
        ])

        total_spent = needs_actual_total + wants_actual_total + savings_actual_total
        net_saving  = income - total_spent
        st.markdown(f"""
<div style='background:{N};border-radius:12px;padding:22px 26px;'>
    <div style='font-size:0.72rem;font-weight:700;color:#3A5A78;letter-spacing:0.12em;
                text-transform:uppercase;margin-bottom:16px;'>Month-End Summary — {sel_month}</div>
    <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:16px;'>
        <div><div style='font-size:0.72rem;color:#3A5A78;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:5px;'>Income</div>
             <div style='font-family:DM Mono,monospace;font-size:1.25rem;font-weight:500;color:#fff;'>&#8377;{income:,.0f}</div></div>
        <div><div style='font-size:0.72rem;color:#3A5A78;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:5px;'>Total Spent</div>
             <div style='font-family:DM Mono,monospace;font-size:1.25rem;font-weight:500;color:{ACCENT};'>&#8377;{total_spent:,.0f}</div></div>
        <div><div style='font-size:0.72rem;color:#3A5A78;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:5px;'>Net Saved</div>
             <div style='font-family:DM Mono,monospace;font-size:1.25rem;font-weight:500;color:{"#2E8B6E" if net_saving>=0 else "#E87070"};'>&#8377;{net_saving:,.0f}</div></div>
        <div><div style='font-size:0.72rem;color:#3A5A78;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:5px;'>Savings Rate</div>
             <div style='font-family:DM Mono,monospace;font-size:1.25rem;font-weight:500;color:{"#2E8B6E" if (net_saving/income*100 if income>0 else 0)>=20 else ACCENT};'>{(net_saving/income*100) if income>0 else 0:.1f}%</div></div>
    </div>
    <div style='margin-top:16px;font-size:0.83rem;color:{"#2E8B6E" if net_saving>=0 else "#E87070"};'>
        {"Within budget. Good discipline this month." if net_saving>=0 else f"Spending exceeds income by &#8377;{abs(net_saving):,.0f}. Review your Wants category first."}
    </div>
</div>""", unsafe_allow_html=True)

    elif income == 0:
        st.info("Enter your monthly income above to see the full budget breakdown.")

    # ── Monthly comparison (saved months) ───────────────────
    saved_months = [m for m in MONTHS if m in u.get("monthly_budget", {})]
    if len(saved_months) > 1:
        st.markdown("---")
        st.markdown("### Month-over-Month Comparison")
        comp_data = []
        for m in saved_months:
            md_m = u["monthly_budget"][m]
            needs_t = md_m["bp_act_rent"]+md_m["bp_act_groc"]+md_m["bp_act_util"]+md_m["bp_act_trans"]+md_m["bp_act_ins"]
            wants_t = md_m["bp_act_dining"]+md_m["bp_act_ent"]+md_m["bp_act_shop"]
            savgs_t = md_m["bp_act_ef"]+md_m["bp_act_sip"]
            comp_data.append({"Month": m, "Needs": needs_t, "Wants": wants_t, "Savings": savgs_t, "Total": needs_t+wants_t+savgs_t})
        df_comp = pd.DataFrame(comp_data)
        fig_bar, ax_bar = new_fig(8, 4)
        x = range(len(df_comp))
        ax_bar.bar([i-0.25 for i in x], df_comp["Needs"],   0.22, color=N,     label="Needs",   edgecolor=WHITE, linewidth=1.2)
        ax_bar.bar([i-0.0  for i in x], df_comp["Wants"],   0.22, color=ACCENT, label="Wants",   edgecolor=WHITE, linewidth=1.2)
        ax_bar.bar([i+0.25 for i in x], df_comp["Savings"], 0.22, color=SAGE,  label="Savings", edgecolor=WHITE, linewidth=1.2)
        ax_bar.set_xticks(list(x))
        ax_bar.set_xticklabels(df_comp["Month"], fontsize=9)
        ax_bar.set_ylabel("Amount (₹)", fontsize=9)
        ax_bar.legend(fontsize=8.5)
        ax_bar.grid(True, axis="y", alpha=0.2)
        ax_bar.set_title("Monthly Spending Breakdown", fontsize=11, fontweight="bold", color=N, pad=10)
        st.pyplot(fig_bar, use_container_width=True)
        plt.close(fig_bar)


# ════════════════════════════════════════════════════════════════════
#  SAVINGS GOAL
# ════════════════════════════════════════════════════════════════════
elif page == "Savings Goal":
    st.markdown(f"""
<div class='eyebrow'>Calculator</div>
<div class='page-title'>Savings Goal Planner</div>
<div class='page-sub'>Set a goal, see what monthly SIP you need, and get investment suggestions.</div>
""", unsafe_allow_html=True)

    income = income_banner()
    left, right = st.columns(2, gap="large")

    with left:
        goal    = st.number_input("Target Amount (₹)", min_value=0.0, step=5000.0, format="%.0f", value=u["sg_goal"])
        current = st.number_input("Amount Already Saved (₹)", min_value=0.0, step=1000.0, format="%.0f", value=u["sg_current"])
        months  = int(st.number_input("Time Frame (months)", min_value=1, value=u["sg_months"], step=1))
        rate    = st.slider("Expected Annual Return (%)", 0.0, 15.0, u["sg_rate"], 0.5, help="Liquid MF ~7% | Debt fund ~8% | Equity index ~12%")
        US("sg_goal", goal); US("sg_current", current); US("sg_months", months); US("sg_rate", rate)

        if income > 0 and goal > 0:
            sip_20 = income * 0.20
            st.markdown(f"""
<div style='background:{N}0C;border:1px dashed {ACCENT};border-radius:9px;padding:14px 16px;margin-top:10px;'>
    <div style='font-size:0.72rem;font-weight:700;color:{ACCENT};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;'>Income-Based Suggestion</div>
    <div style='font-size:0.88rem;color:{N};line-height:1.6;'>
        20% of income = <b>₹{sip_20:,.0f}/month</b><br>
        At this rate you reach ₹{goal:,.0f} in <b>~{goal/sip_20:.0f} months</b> (simple).
    </div>
</div>""", unsafe_allow_html=True)

    if goal > 0 and months > 0:
        remaining = max(goal - current, 0.0)
        r_m = rate / 100 / 12
        sip = remaining * r_m / ((1+r_m)**months - 1) if r_m > 0 and remaining > 0 else (remaining/months if months>0 else 0)
        progress = min(current/goal, 1.0) if goal > 0 else 0

        with left:
            st.markdown("---")
            st.markdown(f"**Progress toward ₹{goal:,.0f}**")
            st.progress(progress)
            p1, p2 = st.columns(2)
            p1.metric("Completed", f"{progress*100:.1f}%")
            p2.metric("Remaining", f"₹{remaining:,.0f}")
            st.markdown("#### Monthly Savings Required")
            r1, r2 = st.columns(2)
            r1.metric("Without returns", f"₹{remaining/months:,.0f}")
            r2.metric(f"SIP @ {rate}% p.a.", f"₹{sip:,.0f}")

        with right:
            m_arr  = list(range(0, months+1))
            growth = [current*(1+r_m)**m + sip*((1+r_m)**m-1)/r_m for m in m_arr] if r_m > 0 else [current+sip*m for m in m_arr]
            simple = [current + (remaining/months)*m for m in m_arr]
            fig2, ax2 = new_fig(6, 4.2)
            ax2.plot(m_arr, [v/1000 for v in growth], color=N, lw=2.5, label=f"SIP @ {rate}% p.a.")
            ax2.plot(m_arr, [v/1000 for v in simple], color=MUTED, lw=2, ls="--", label="No returns")
            ax2.axhline(goal/1000, color=ACCENT, ls=":", lw=2, label="Target")
            ax2.fill_between(m_arr, [v/1000 for v in growth], alpha=0.08, color=N)
            ax2.set_xlabel("Month", fontsize=9); ax2.set_ylabel("Amount (Rs thousands)", fontsize=9)
            ax2.set_title("Savings Projection", fontsize=12, fontweight="bold", color=N, pad=10)
            ax2.legend(fontsize=8.5); ax2.grid(True, alpha=0.2)
            st.pyplot(fig2); plt.close(fig2)

            st.markdown("#### Suggested Investment Options")
            if months <= 12:
                options = [("Liquid Mutual Fund","5-7%","Withdraw in 1 day. Best for under 1 year.",SAGE),("Ultra Short FD","5-6%","Slightly better than savings account.",ACCENT),("Savings Account","3-4%","Easiest access, lowest return.",MUTED)]
            elif months <= 36:
                options = [("Short-Term Debt MF","6-8%","Low risk, better than FD post-tax.",SAGE),("Fixed Deposit (FD)","6-7%","Guaranteed return, some lock-in.",ACCENT),("Arbitrage Fund","6-7%","Equity taxation, debt-like returns.",N)]
            elif months <= 60:
                options = [("Balanced Advantage Fund","9-11%","Auto-adjusts equity/debt ratio.",SAGE),("Aggressive Hybrid Fund","9-12%","60-80% equity, rest in debt.",ACCENT),("ELSS (tax-saving SIP)","10-14%","80C benefit + equity growth.",N)]
            else:
                options = [("Nifty 50 Index Fund","11-14%","Lowest cost, market returns. Best for 5+ years.",SAGE),("Flexi-cap Fund","11-15%","Fund manager picks across market caps.",ACCENT),("ELSS SIP","10-14%","Tax saving + long-term equity wealth.",N)]

            for name, ret, desc, col in options:
                st.markdown(f"""
<div style='background:{WHITE};border-radius:9px;padding:12px 16px;
            border-left:4px solid {col};border:1px solid {BORD};margin-bottom:10px;
            box-shadow:0 1px 4px rgba(10,22,40,.05);'>
    <div style='display:flex;justify-content:space-between;align-items:center;'>
        <span style='font-family:DM Sans,sans-serif;font-weight:700;font-size:0.9rem;color:{N};'>{name}</span>
        <span style='font-family:DM Mono,monospace;font-weight:500;font-size:0.9rem;color:{col};'>{ret}</span>
    </div>
    <div style='font-size:0.8rem;color:{MUTED};margin-top:4px;'>{desc}</div>
</div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
#  DEBT MANAGER
# ════════════════════════════════════════════════════════════════════
elif page == "Debt Manager":
    st.markdown(f"""
<div class='eyebrow'>Calculator</div>
<div class='page-title'>Debt Manager</div>
<div class='page-sub'>Map your debts, understand your risk, and choose a payoff strategy.</div>
""", unsafe_allow_html=True)

    income = income_banner()
    left, right = st.columns(2, gap="large")

    with left:
        st.markdown("#### Enter Your Debts")
        n_d = int(st.number_input("Number of debts / loans", min_value=1, max_value=7, value=u["dm_n_debts"]))
        US("dm_n_debts", n_d)
        debts = []
        for i in range(n_d):
            with st.expander(f"Debt {i+1}", expanded=(i==0)):
                dc1, dc2, dc3 = st.columns(3)
                saved = u["dm_debts"][i]
                nm = dc1.text_input("Name", value=saved["name"], key=f"dn{i}")
                am = dc2.number_input("Balance (₹)", min_value=0.0, step=1000.0, format="%.0f", value=saved["amount"], key=f"da{i}")
                rt = dc3.number_input("Rate (% p.a.)", min_value=0.0, max_value=60.0, value=saved["rate"], step=0.5, key=f"dr{i}")
                debts.append({"name": nm, "amount": am, "rate": rt})
                u["dm_debts"][i] = {"name": nm, "amount": am, "rate": rt}

        st.markdown("---")
        emi_d = st.number_input("Total Monthly EMI (₹)", min_value=0.0, step=500.0, format="%.0f", value=u["dm_emi"])
        US("dm_emi", emi_d)

    with right:
        active = [d for d in debts if d["amount"] > 0]
        if active:
            total_debt = sum(d["amount"] for d in active)
            st.metric("Total Outstanding", f"₹{total_debt:,.0f}")
            if income > 0 and emi_d > 0:
                dti = emi_d / income * 100
                st.markdown("#### Debt-to-Income Ratio")
                st.progress(min(dti/100, 1.0))
                if dti < 20:    st.success(f"DTI: {dti:.1f}%  — Healthy. Lenders prefer below 36%.")
                elif dti < 36:  st.warning(f"DTI: {dti:.1f}%  — Manageable. Avoid new credit.")
                elif dti < 50:  st.error(f"DTI: {dti:.1f}%  — High. Prioritise debt reduction now.")
                else:           st.error(f"DTI: {dti:.1f}%  — Critical. Consider a debt consolidation plan.")

            sorted_d = sorted(active, key=lambda x: x["rate"], reverse=True)
            names = [d["name"] for d in sorted_d]
            amts  = [d["amount"] for d in sorted_d]
            rates = [d["rate"] for d in sorted_d]
            bar_c = [RED if r>18 else ACCENT if r>12 else N for r in rates]
            fig3, ax3 = new_fig(6, max(2.8, 0.65*len(sorted_d)+1.4))
            bars = ax3.barh(names, amts, color=bar_c, height=0.52, edgecolor=WHITE, linewidth=1.8)
            for bar, r in zip(bars, rates):
                ax3.text(bar.get_width()*1.01, bar.get_y()+bar.get_height()/2, f"{r:.1f}%", va="center", fontsize=8.5, color=MUTED)
            ax3.set_xlabel("Balance (₹)", fontsize=9)
            ax3.set_title("Debts — Sorted by Interest Rate", fontsize=10.5, fontweight="bold", color=N, pad=8)
            ax3.grid(True, axis="x", alpha=0.2)
            st.pyplot(fig3); plt.close(fig3)
            top = sorted_d[0]
            st.markdown(f"""
<div style='background:{N}0F;border-left:4px solid {ACCENT};border-radius:8px;padding:13px 16px;font-size:0.88rem;color:{N};'>
    <b>Avalanche Method:</b> Pay minimums on all debts, then direct every extra rupee to <b>{top['name']}</b> ({top['rate']:.1f}% p.a.) first. This saves the most interest overall.
</div>""", unsafe_allow_html=True)
        else:
            st.info("Enter at least one debt amount above.")

        ref = pd.DataFrame({"Debt Type": ["Credit Card","Personal Loan","Vehicle Loan","Home Loan"], "Typical Rate": ["36-42%","14-24%","8-12%","8-9%"], "Priority": ["Highest","Second","Third","Lowest"]})
        st.markdown("#### Quick Reference")
        st.dataframe(ref, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════════════
#  EMERGENCY FUND
# ════════════════════════════════════════════════════════════════════
elif page == "Emergency Fund":
    st.markdown(f"""
<div class='eyebrow'>Calculator</div>
<div class='page-title'>Emergency Fund</div>
<div class='page-sub'>Your target is calculated from the essential expenses entered in Budget Planner. It also shows how your fund projects across upcoming months.</div>
""", unsafe_allow_html=True)

    sel_month = u.get("selected_month", MONTHS[0])
    needs_from_budget = needs_total_for_month(sel_month)

    if needs_from_budget == 0:
        st.markdown(f"""
<div class='dark-banner'>
<p><strong>No expense data found for {sel_month}.</strong><br><br>
Go to Budget Planner, select a month, and enter your actual essential expenses (Rent, Groceries, Utilities, Transport, Insurance). This page will automatically calculate your emergency fund from those figures.</p>
</div>""", unsafe_allow_html=True)
        current_ef = st.number_input("Current Emergency Fund (₹)", min_value=0.0, step=1000.0, format="%.0f", value=u["ef_current"])
        US("ef_current", current_ef)
    else:
        left, right = st.columns([1, 1.2], gap="large")
        with left:
            st.markdown(f"#### Essential Expenses — {sel_month}")
            md_month = get_month_data(sel_month)
            exp_items = {"Rent / EMI": md_month["bp_act_rent"], "Groceries": md_month["bp_act_groc"], "Utilities": md_month["bp_act_util"], "Transport": md_month["bp_act_trans"], "Insurance": md_month["bp_act_ins"]}
            for label, val in exp_items.items():
                if val > 0:
                    st.markdown(f"<div style='display:flex;justify-content:space-between;padding:8px 12px;border-bottom:1px solid {BORD};font-size:0.88rem;'><span style='color:{MUTED};'>{label}</span><span style='font-weight:600;color:{N};'>₹{val:,.0f}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='display:flex;justify-content:space-between;padding:10px 12px;background:{N}08;border-radius:0 0 8px 8px;font-size:0.92rem;margin-bottom:18px;'><span style='font-weight:700;color:{N};'>Total Monthly Essentials</span><span style='font-weight:700;color:{N};font-family:DM Mono,monospace;'>₹{needs_from_budget:,.0f}</span></div>", unsafe_allow_html=True)

            months_ef = st.slider("Target Coverage (months)", 3, 12, value=u["ef_months"], help="6 months is standard. Use 3 for very stable income, 9-12 if self-employed.")
            US("ef_months", months_ef)
            target_ef = needs_from_budget * months_ef
            st.markdown(f"""
<div style='background:{ACCENT}15;border-left:4px solid {ACCENT};border-radius:8px;padding:14px 16px;margin:12px 0;'>
    <div style='font-size:0.72rem;font-weight:700;color:{ACCENT};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;'>Target Emergency Fund</div>
    <div style='font-family:DM Mono,monospace;font-size:1.6rem;font-weight:500;color:{N};'>₹{target_ef:,.0f}</div>
    <div style='font-size:0.82rem;color:{MUTED};margin-top:4px;'>{months_ef} months × ₹{needs_from_budget:,.0f}/month</div>
</div>""", unsafe_allow_html=True)
            current_ef = st.number_input("Current Emergency Fund (₹)", min_value=0.0, step=1000.0, format="%.0f", value=u["ef_current"])
            US("ef_current", current_ef)

        with right:
            gap_ef  = max(target_ef - current_ef, 0.0)
            prog_ef = min(current_ef/target_ef, 1.0) if target_ef > 0 else 0
            st.markdown("#### Fund Status")
            st.progress(prog_ef)
            ef1, ef2, ef3 = st.columns(3)
            ef1.metric("Monthly Essentials", f"₹{needs_from_budget:,.0f}")
            ef2.metric(f"Target ({months_ef}M)", f"₹{target_ef:,.0f}")
            ef3.metric("Gap Remaining", f"₹{gap_ef:,.0f}" if gap_ef > 0 else "Complete")

            if gap_ef == 0:
                st.success("Emergency fund fully funded. Focus surplus on investing.")
            elif prog_ef >= 0.75:
                st.warning(f"{prog_ef*100:.0f}% funded. Save ₹{needs_from_budget*0.10:,.0f}/mo to complete in ~{gap_ef/(needs_from_budget*0.10):.0f} months.")
            elif prog_ef >= 0.5:
                st.warning(f"Halfway there. Save ₹{needs_from_budget*0.15:,.0f}/month to complete in ~{gap_ef/(needs_from_budget*0.15):.0f} months.")
            else:
                st.error(f"Priority one. Save ₹{needs_from_budget*0.15:,.0f}/month to complete in ~{gap_ef/(needs_from_budget*0.15):.0f} months.")

            # Upcoming months projection
            st.markdown("---")
            st.markdown("#### Upcoming Months Projection")
            st.caption("Assuming you save 15% of monthly essentials each month toward the fund.")
            cur_idx = MONTHS.index(sel_month)
            monthly_save = needs_from_budget * 0.15
            proj_rows = []
            bal = current_ef
            for i in range(1, 7):
                m_idx = (cur_idx + i) % 12
                bal = min(bal + monthly_save, target_ef)
                pct = bal / target_ef * 100 if target_ef > 0 else 0
                proj_rows.append({"Month": MONTHS[m_idx], "Projected Balance": f"₹{bal:,.0f}", "% Funded": f"{pct:.0f}%", "Status": "Complete" if bal >= target_ef else "Building"})
            st.dataframe(pd.DataFrame(proj_rows), use_container_width=True, hide_index=True)

            # Where to keep
            st.markdown("---")
            st.markdown("#### Where to Keep Your Emergency Fund")
            for name, ret, desc, col, badge in [
                ("Liquid Mutual Fund","6-7% p.a.","Redeemable within 1 business day. Best combination of return and accessibility.",SAGE,"Best Choice"),
                ("Sweep-in Fixed Deposit","5-6% p.a.","Bank automatically moves idle savings into an FD. Breaks instantly on withdrawal.",ACCENT,"Convenient"),
                ("High-Yield Savings Account","3-7% p.a.","AU Small Finance, IDFC First offer up to 7%. Instant access, insured up to ₹5 L.",N,"Most Accessible"),
            ]:
                st.markdown(f"""
<div style='background:{WHITE};border-radius:10px;padding:13px 15px;border-left:4px solid {col};border:1px solid {BORD};margin-bottom:10px;'>
    <div style='display:flex;justify-content:space-between;align-items:center;'>
        <span style='font-weight:700;font-size:0.92rem;color:{N};'>{name}
            <span style='background:{col}22;border:1px solid {col}55;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:700;color:{col};margin-left:8px;'>{badge}</span>
        </span>
        <span style='font-family:DM Mono,monospace;font-weight:500;font-size:0.88rem;color:{col};'>{ret}</span>
    </div>
    <div style='font-size:0.8rem;color:{MUTED};margin-top:5px;line-height:1.55;'>{desc}</div>
</div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
#  HEALTH SCORE
# ════════════════════════════════════════════════════════════════════
elif page == "Health Score":
    st.markdown(f"""
<div class='eyebrow'>Assessment</div>
<div class='page-title'>Financial Health Score</div>
<div class='page-sub'>A snapshot of your financial fitness across four key dimensions.</div>
""", unsafe_allow_html=True)

    income = income_banner()
    left, right = st.columns([1, 1.2], gap="large")

    with left:
        st.markdown("#### Your Inputs")
        sav_fh  = st.number_input("Monthly Savings (₹)", min_value=0.0, step=500.0, format="%.0f", value=u["hs_savings"])
        emi_fh  = st.number_input("Monthly EMI Payments (₹)", min_value=0.0, step=500.0, format="%.0f", value=u["hs_emi"])
        ef_mo   = st.number_input("Emergency Fund (months covered)", min_value=0.0, max_value=24.0, value=u["hs_ef_months"], step=0.5)
        has_ins = st.checkbox("Active Term + Health Insurance", value=u["hs_has_ins"])
        has_wil = st.checkbox("Nominees updated / Will in place", value=u["hs_has_wil"])
        has_sip = st.checkbox("Investing regularly (SIP or similar)", value=u["hs_has_sip"])
        US("hs_savings", sav_fh); US("hs_emi", emi_fh); US("hs_ef_months", ef_mo)
        US("hs_has_ins", has_ins); US("hs_has_wil", has_wil); US("hs_has_sip", has_sip)

    if income > 0:
        score = 0; dims = {}
        sr  = sav_fh/income*100
        pts = 25 if sr>=20 else (16 if sr>=10 else (7 if sr>0 else 0))
        score += pts; dims["Savings Rate"] = (pts, 25, f"{sr:.1f}% of income")
        dti = emi_fh/income*100
        pts = 25 if dti<20 else (17 if dti<36 else (7 if dti<50 else 0))
        score += pts; dims["Debt Load"] = (pts, 25, f"EMI = {dti:.1f}% of income")
        pts = 25 if ef_mo>=6 else (17 if ef_mo>=3 else (7 if ef_mo>=1 else 0))
        score += pts; dims["Emergency Fund"] = (pts, 25, f"{ef_mo:.1f} months covered")
        pts = min((11 if has_ins else 0)+(5 if has_wil else 0)+(9 if has_sip else 0), 25)
        score += pts; dims["Protection & Habits"] = (pts, 25, "Insurance / Will / SIP")
        score = min(score, 100)

        with right:
            if   score >= 80: grade, label, col = "A", "Excellent",  SAGE
            elif score >= 60: grade, label, col = "B", "Good",       N
            elif score >= 40: grade, label, col = "C", "Fair",       ACCENT
            else:             grade, label, col = "D", "Needs Work", RED

            st.markdown(f"""
<div style='text-align:center;padding:18px 0 8px;'>
    <div class='score-circle' style='border-color:{col};color:{col};'>{score}</div>
    <div style='font-family:DM Sans,sans-serif;font-size:1.35rem;font-weight:700;color:{col};'>{label}</div>
    <div style='font-size:0.83rem;color:{MUTED};margin-top:3px;'>Financial Health Grade: {grade}</div>
</div>""", unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("#### Score Breakdown")
            for dim, (pts, mx, detail) in dims.items():
                st.markdown(f"**{dim}** — {pts} / {mx} pts — *{detail}*")
                st.progress(pts/mx)

            labels_r = list(dims.keys())
            vals_r   = [v[0]/v[1] for v in dims.values()]
            N_r      = len(labels_r)
            angles   = [n/N_r*2*np.pi for n in range(N_r)]
            angles  += angles[:1]; vals_r += vals_r[:1]
            fig5, ax5 = plt.subplots(figsize=(4.5, 4.5), subplot_kw={"polar": True}, facecolor=WHITE)
            ax5.set_facecolor(WHITE)
            ax5.plot(angles, vals_r, color=N, lw=2.2)
            ax5.fill(angles, vals_r, color=ACCENT, alpha=0.18)
            ax5.set_xticks(angles[:-1]); ax5.set_xticklabels(labels_r, size=7.5, color=N)
            ax5.set_ylim(0, 1); ax5.set_yticks([0.25,0.5,0.75,1.0])
            ax5.set_yticklabels(["25","50","75","100"], size=6, color=MUTED)
            ax5.grid(color=BORD); ax5.set_title("Health Radar", size=11, fontweight="bold", color=N, pad=14)
            st.pyplot(fig5); plt.close(fig5)

            st.markdown("#### Action Plan")
            if sr < 20:  st.warning(f"Increase savings from {sr:.1f}% to 20% of income.")
            if dti >= 36: st.error(f"EMI burden is {dti:.1f}% — target below 36%.")
            if ef_mo < 6: st.warning(f"Build emergency fund to 6 months (currently {ef_mo:.1f}).")
            if not has_ins: st.error("Get term + health insurance — most urgent gap.")
            if not has_sip: st.info("Start a SIP, even ₹500/month. Habit matters more than amount.")
            if score >= 80: st.success("Strong foundations. Explore NPS, ELSS, and long-term equity for wealth building.")
    else:
        st.info("Enter your monthly income above to calculate your health score.")


# ════════════════════════════════════════════════════════════════════
#  FINANCE Q&A — Gemini powered
# ════════════════════════════════════════════════════════════════════
elif page == "Finance Q&A":
    st.markdown(f"""
<div class='eyebrow'>AI Assistant</div>
<div class='page-title'>Ask me anything</div>
<div class='page-sub'>Ask about budgeting, savings, debt, investing, insurance, tax saving, or retirement. Powered by Google Gemini.</div>
""", unsafe_allow_html=True)

    # API key input (optional override)
    with st.expander("Gemini API Key (optional — overrides environment variable)"):
        custom_key = st.text_input("Paste your Gemini API key here", type="password", key="custom_gemini_key")
        if custom_key.strip():
            GEMINI_API_KEY = custom_key.strip()
        st.caption("Get a free key at aistudio.google.com/app/apikey — the free tier includes generous token limits.")

    left, right = st.columns([1, 1.15], gap="large")

    with left:
        st.markdown("#### Quick Topics")
        topic_cols = st.columns(2)
        quick_topics = [
            ("Budgeting",   "How does the 50-30-20 budgeting rule work?"),
            ("Savings",     "Where should I save and how much?"),
            ("Investing",   "How do I start investing in India?"),
            ("Debt",        "How do I pay off debt faster?"),
            ("Emergency",   "How do I build an emergency fund?"),
            ("Insurance",   "What insurance do I actually need?"),
            ("Tax Saving",  "How do I reduce my tax legally in India?"),
            ("Retirement",  "How do I plan for retirement in India?"),
        ]
        for i, (label, question) in enumerate(quick_topics):
            col = topic_cols[i % 2]
            if col.button(label, use_container_width=True, key=f"qt_{i}"):
                u["qa_log"].append({"role": "user", "content": question})
                with st.spinner("Thinking..."):
                    answer = ask_gemini(question, u["qa_log"][:-1])
                u["qa_log"].append({"role": "advisor", "content": answer})
                st.rerun()

        st.markdown("---")
        st.markdown("#### Your Question")
        with st.form("qa_form", clear_on_submit=True):
            user_q = st.text_area(
                "Type your finance question",
                placeholder="e.g. How do I balance saving and paying off a home loan at the same time?",
                height=100,
            )
            fc1, fc2 = st.columns([3, 1])
            submit = fc1.form_submit_button("Ask", use_container_width=True)
            clear  = fc2.form_submit_button("Clear", use_container_width=True)

        if submit and user_q.strip():
            u["qa_log"].append({"role": "user", "content": user_q.strip()})
            with st.spinner("Thinking..."):
                answer = ask_gemini(user_q.strip(), u["qa_log"][:-1])
            u["qa_log"].append({"role": "advisor", "content": answer})
            st.rerun()

        if clear:
            US("qa_log", [])
            st.rerun()

    with right:
        st.markdown("#### Conversation")
        if not u["qa_log"]:
            st.markdown(f"""
<div class='dark-banner' style='margin-top:4px;'>
<p>
    Pick a topic on the left, or type any personal finance question.<br><br>
    <strong>Covered areas:</strong> budgeting &middot; savings &middot; debt &middot; investing &middot;
    emergency funds &middot; insurance &middot; tax saving &middot; retirement
</p>
</div>""", unsafe_allow_html=True)
        else:
            bubbles = ""
            for msg in u["qa_log"][-12:]:
                content = _html.escape(msg["content"]).replace("\n", "<br>")
                if msg["role"] == "user":
                    bubbles += f"<div class='chat-bubble-user'>You<br>{content}</div>"
                else:
                    bubbles += f"<div class='chat-bubble-ai'>FinanceIQ<br><br>{content}</div>"
            st.markdown(f"<div class='chat-wrap'>{bubbles}</div>", unsafe_allow_html=True)

        st.markdown(f"<div style='font-size:0.75rem;color:{MUTED};line-height:2;'>AI responses are for general information only. Consult a SEBI-registered advisor for personalised advice.</div>", unsafe_allow_html=True)
