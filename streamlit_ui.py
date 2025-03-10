import streamlit as st
import requests

API_URL = "http://127.0.0.1:5001"

st.set_page_config(page_title="📚 AI Study Planner", layout="wide")
st.title("📚 AI Study Planner")
st.sidebar.header("✍️ Enter Your Study Goals")

user_id = st.sidebar.text_input("Enter User ID", value="1")
goals = st.sidebar.text_area("Enter your study goals", value="I want to learn AI")
generate_button = st.sidebar.button("Generate Study Plan")

def generate_study_plan():
    payload = {"user_id": int(user_id), "goals": goals}
    response = requests.post(f"{API_URL}/generate_plan/", json=payload)
    return response.json()["plan"] if response.status_code == 200 else None

if generate_button:
    study_plan = generate_study_plan()
    if study_plan:
        st.success("✅ Study Plan Generated Successfully!")
        st.write(f"**Your Plan:** {study_plan}")
    else:
        st.error("❌ Error: Server Issue")

st.header("📊 Existing Study Plans")
response = requests.get(f"{API_URL}/get_plans/")
if response.status_code == 200:
    study_plans = response.json()
    for plan in study_plans:
        st.markdown(f"**User ID {plan['user_id']}**: {plan['goals']}")
        st.write(f"📚 *{plan['plan']}*")
        st.markdown("---")
else:
    st.error("❌ Unable to fetch study plans.")
