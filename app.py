import streamlit as st
from advisor import get_advice
from analytics import load_all_sessions, summarize_sessions
from image_embedder import classify_image
from datetime import datetime
import base64
import matplotlib.pyplot as plt
import io
import random
import json
import pandas as pd
from portfolio import generate_portfolio
from tax import generate_tax_tips
from budget import generate_budget_plan
from csv_parser import parse_transaction_csv
from assistant_modes import get_advisor_tone
from memory import save_session, load_session
from simplifier import apply_simplifier
from simulation_tools import monte_carlo_simulation
from pdf_export import create_pdf


st.set_page_config(page_title="Financial Advisor", layout="centered")
st.title("Financial Advisor")

# --- Initialize session state ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "advice" not in st.session_state:
    st.session_state.advice = None
if "prompt" not in st.session_state:
    st.session_state.prompt = ""
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []
if "model_version" not in st.session_state:
    st.session_state.model_version = random.choice(["gpt-3.5-turbo", "gpt-4o"])
if "language" not in st.session_state:
    st.session_state.language = "English"

# --- Sidebar Settings ---
selected_model = st.sidebar.selectbox("Choose Model", ["gpt-4o", "mistral"], key="model_choice")

sector_options = ["Tech", "Healthcare", "Energy", "Finance", "Consumer Goods", "ESG"]
selected_sectors = st.sidebar.multiselect("Preferred Sectors", sector_options, default=["Tech", "Finance"])

st.sidebar.markdown("**Adjust Risk Allocation (%)**")
low_risk_pct = st.sidebar.slider("Low Risk", 0, 100, 40)
med_risk_pct = st.sidebar.slider("Medium Risk", 0, 100 - low_risk_pct, 40)
high_risk_pct = 100 - low_risk_pct - med_risk_pct
st.sidebar.markdown(f"High Risk: **{high_risk_pct}%**")
risk_allocation = {"Low Risk": low_risk_pct, "Medium Risk": med_risk_pct, "High Risk": high_risk_pct}
st.sidebar.header("Settings")
advisor_style = st.sidebar.selectbox("Choose advisor persona", [
    "Balanced",
    "Minimalist advisor",
    "Aggressive growth coach",
    "Ethical investor advisor",
    "Luxury lifestyle planner"
])
username = st.sidebar.text_input("Session name (optional)")
elimode = st.sidebar.toggle("Explain Like I'm 5 (ELI5)")
language = st.sidebar.selectbox("Language", ["English", "Spanish", "French", "German", "Russian"])
tax_mode = st.sidebar.toggle("Include tax-saving strategies")
budget_mode = st.sidebar.toggle("Show budget planning")
if username:
    st.sidebar.success(f"Session: {username}")
if not username:
    username = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    st.sidebar.write(f"Session Name: {username}")
# --- Big Five Quiz ---
st.subheader("Personality Estimator (Big Five)")
big_five = {
    "Openness": "I enjoy trying new things and thinking about abstract ideas.",
    "Conscientiousness": "I like to plan and follow a schedule.",
    "Extraversion": "I am outgoing and talkative.",
    "Agreeableness": "I am considerate and kind to almost everyone.",
    "Neuroticism": "I get stressed easily.",
}
personality_scores = {}
with st.form("big_five_form"):
    for trait, question in big_five.items():
        score = st.slider(question, 1, 5, 3)
        personality_scores[trait] = score
    submitted_quiz = st.form_submit_button("Submit Personality Quiz")
if submitted_quiz:
    st.success("Personality traits recorded.")
    st.session_state.personality_scores = personality_scores

# --- User Form ---
st.subheader("Your Financial Profile")
with st.form("user_form"):
    age = st.text_input("Age")
    income = st.text_input("Annual Income (USD)")
    experience = st.selectbox("Investment Experience", ["Beginner", "Intermediate", "Expert"])
    goal = st.text_area("Investment Goal")
    time_horizon = st.slider("Investment Time Horizon (Years)", 1, 30, 5)
    photo = st.file_uploader("Upload a photo of yourself (optional)", type=["jpg", "png"])
    csv_file = st.file_uploader("Upload financial transactions CSV (optional)", type=["csv"])
    submitted = st.form_submit_button("Get Advice")

# --- Advice Generation ---
if submitted:
    profile_text = f"- Age: {age}\n- Income: ${income}\n- Experience: {experience}\n- Goal: {goal}\n- Time Horizon: {time_horizon} years"

    if photo is not None:
        with open("temp_image.jpg", "wb") as f:
            f.write(photo.read())
        image_classification, confidence = classify_image("temp_image.jpg")
        st.success(f"Inferred risk/personality profile: **{image_classification}** ({confidence:.2f} confidence)")
    else:
        fallback_profiles = {
            "Beginner": "a cautious investor",
            "Intermediate": "a balanced investor",
            "Expert": "an aggressive investor"
        }
        image_classification = fallback_profiles[experience]
        st.info(f"Inferred risk profile from text: **{image_classification}**")

    if "personality_scores" in st.session_state:
        traits = st.session_state.personality_scores
        profile_text += f"\nPersonality Traits: {traits}"

    style_prefix = get_advisor_tone(advisor_style)
    if language != "English":
        style_prefix += f" Respond in {language}."

    prompt = f"""
{style_prefix}
You are a professional financial advisor. Here's the user's profile:
{profile_text}
Based on their profile and appearance cues, they are categorized as: '{image_classification}'.

The user has selected the following risk allocation:
- Low Risk: {low_risk_pct}%
- Medium Risk: {med_risk_pct}%
- High Risk: {high_risk_pct}%

Please take their personality, risk tolerance, and goals into account. Detect any potential behavioral finance biases they may be susceptible to. Then provide 5 bullet points of investment advice tailored to them.
"""
    prompt = apply_simplifier(prompt, elimode)

    with st.spinner("Generating your investment advice..."):
        advice = get_advice(prompt, model=st.session_state.model_version)

    st.session_state.advice = advice
    st.session_state.prompt = prompt
    st.session_state.chat_history = []
    st.session_state.chat_log.append({"timestamp": str(datetime.now()), "profile": profile_text, "advice": advice})
    save_session(username, profile_text, advice)

    st.subheader("Personalized Investment Advice")
    st.markdown(advice)

    # Generate PDF
    create_pdf(profile_text, advice)

    # PDF download button
    with open("financial_advice_report.pdf", "rb") as f:
        pdf_ready = f.read()

    st.download_button("Download PDF Report", data=pdf_ready, file_name="financial_advice_report.pdf", mime="application/pdf")


    # Tax tips
    if tax_mode:
        st.subheader("Tax-Saving Strategies")
        tax_tips = generate_tax_tips(income, experience, time_horizon)
        st.markdown(tax_tips)

    # Budget plan
    if budget_mode:
        st.subheader("Suggested Budget Plan")
        df_budget = generate_budget_plan(income)
        st.dataframe(df_budget)

    # CSV Upload + Summary
    if csv_file:
        st.subheader("Your Uploaded Financial Summary")
        error_msg, df_summary = parse_transaction_csv(csv_file)
        if error_msg:
            st.error(error_msg)
        elif df_summary is not None:
            st.dataframe(df_summary)

            # Budget vs. Actual comparison chart
            if budget_mode:
                st.subheader("Budget vs. Actual Spending Comparison")
                df_budget_plot = generate_budget_plan(income).copy()
                df_budget_plot.rename(columns={"Amount (USD)": "Budgeted"}, inplace=True)
                df_compare = pd.merge(df_budget_plot, df_summary, on="Category", how="left")
                df_compare["Total Spent"].fillna(0, inplace=True)
                df_compare.set_index("Category", inplace=True)

                st.bar_chart(df_compare[["Budgeted", "Total Spent"]])

    # Visualization: risk allocation pie chart
    st.subheader("Suggested Risk Allocation")
    labels = ['Low Risk', 'Medium Risk', 'High Risk']
    sizes = [50, 30, 20] if "cautious" in image_classification else [30, 40, 30]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    # Timeline projection: line chart
    st.subheader("Investment Growth Projection")
    start_amount = 10000
    growth_rate = 0.07
    years = list(range(1, time_horizon + 1))
    values = [start_amount * ((1 + growth_rate) ** y) for y in years]
    fig2, ax2 = plt.subplots()
    ax2.plot(years, values, marker='o')
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Projected Value ($)")
    ax2.set_title("Projected Investment Value Over Time")
    st.pyplot(fig2)

    # Simulated portfolio
    st.subheader("Simulated Portfolio")
    df_portfolio = generate_portfolio(image_classification)
    st.dataframe(df_portfolio)

    st.download_button("Download Advice", advice.encode(), file_name="investment_advice.txt")
    score = st.slider("Rate this advice (1 = poor, 5 = excellent)", 1, 5, 3)
    feedback = st.text_input("Optional comments")
    if feedback:
        st.success("Thank you for your feedback!")

#Monte Carlo
if st.session_state.advice:
    st.subheader("Monte Carlo Simulation (500 runs)")
    if st.button("Run Simulation"):
        results = monte_carlo_simulation(start_amount=10000, years=5)
        fig, ax = plt.subplots(figsize=(10, 4))
        for run in results:
            ax.plot(run, color="gray", alpha=0.05)
        ax.set_title("Monte Carlo Portfolio Performance")
        ax.set_xlabel("Years")
        ax.set_ylabel("Portfolio Value ($)")
        st.pyplot(fig)

# --- Chat Interface ---
if st.session_state.advice:
    st.divider()
    st.subheader("Ask a Follow-up Question")
    user_question = st.chat_input("Ask something about your advice...")

    if user_question:
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        full_convo = [
            {"role": "system", "content": "You are a helpful financial assistant continuing a conversation."},
            {"role": "user", "content": st.session_state.prompt},
            {"role": "assistant", "content": st.session_state.advice},
        ] + st.session_state.chat_history

        with st.spinner("Thinking..."):
            response = get_advice(full_convo, model=st.session_state.model_version, mode="chat")
        st.session_state.chat_history.append({"role": "assistant", "content": response})

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- Debug Prompt ---
with st.expander("View AI Prompt"):
    st.code(st.session_state.prompt if st.session_state.prompt else "No prompt yet.")

# --- Log Export ---
with st.expander("Export Chat Log"):
    if st.session_state.chat_log:
        chat_json = json.dumps(st.session_state.chat_log, indent=2)
        st.download_button("Download Full Session Log", chat_json, file_name="session_log.json")

#--- Session Analytics ---
with st.expander("Session Summary Dashboard"):
    df_sessions = load_all_sessions()
    if df_sessions.empty:
        st.info("No session data found yet. Complete a session to view analytics.")
    else:
        summary, traits_df = summarize_sessions(df_sessions)

        if summary:
            st.metric("Total Sessions", summary['num_sessions'])
            st.metric("Avg. Advice Length (words)", summary['avg_length'])
            top_words = ", ".join([kw for kw, _ in summary['top_keywords']])
            st.markdown(f"**Most Common Goal Keywords:** {top_words}")

        if not traits_df.empty:
            st.subheader("Big Five Trait Heatmap")
            st.dataframe(traits_df.describe().transpose())


