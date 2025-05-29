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
from metrics_logger import log_session_metrics
import os
import seaborn as sns
import matplotlib.pyplot as plt



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
if "language" not in st.session_state:
    st.session_state.language = "English"

# --- Sidebar Settings ---
selected_model = st.sidebar.selectbox("Choose Model", ["gpt-4o", "mistral", "gigachat"], key="model_choice")
st.session_state.model_version = selected_model

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
    csv_file = st.file_uploader("Upload financial transactions CSV (optional)", type=["csv"])
    submitted = st.form_submit_button("Get Advice")

# --- Advice Generation ---
if submitted:
    profile_text = f"- Age: {age}\n- Income: ${income}\n- Experience: {experience}\n- Goal: {goal}\n- Time Horizon: {time_horizon} years"

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

The user has selected the following risk allocation:
- Low Risk: {low_risk_pct}%
- Medium Risk: {med_risk_pct}%
- High Risk: {high_risk_pct}%

Preferred sectors: {", ".join(selected_sectors)}
Advisor persona: {advisor_style}
Interface language: {language}

Please take their personality, risk tolerance, investment experience, sector preferences, and advisor style into account. Detect any potential behavioral finance biases they may be susceptible to. Then provide 5 bullet points of investment advice tailored to them.
"""

    prompt = apply_simplifier(prompt, elimode)

    with st.spinner("Generating your investment advice..."):
        advice = get_advice(prompt, model=st.session_state.model_version)

    st.session_state.advice = advice
    st.session_state.prompt = prompt
    st.session_state.chat_history = []
    st.session_state.chat_log.append({"timestamp": str(datetime.now()), "profile": profile_text, "advice": advice})
    save_session(username, profile_text, advice, st.session_state.model_version)
    log_session_metrics(prompt, advice, st.session_state.model_version, username)

    st.subheader("Personalized Investment Advice")
    st.markdown(f"*Модель: `{st.session_state.model_version}`*")
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
    sizes = [risk_allocation["Low Risk"], risk_allocation["Medium Risk"], risk_allocation["High Risk"]]

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
    df_portfolio = generate_portfolio(risk_allocation)
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

#Session Analytics Dashboard
with st.expander("Session Summary Dashboard"):
    df_sessions = load_all_sessions()
    metrics_path = "data/model_metrics.json"
    df_metrics = pd.read_json(metrics_path) if os.path.exists(metrics_path) else pd.DataFrame()

    session_usernames = set(df_sessions["filename"].str.replace(".json", "")) if not df_sessions.empty else set()
    metrics_usernames = set(df_metrics["username"]) if "username" in df_metrics.columns else set()

    all_usernames = session_usernames.union(metrics_usernames)
    total_sessions = len(all_usernames)

    avg_advice_length = int(df_metrics["verbosity"].mean()) if not df_metrics.empty else 0

    if total_sessions == 0:
        st.info("No session data found yet. Complete a session to view analytics.")
    else:
        if not df_sessions.empty:
            summary, traits_df = summarize_sessions(df_sessions)
        else:
            summary, traits_df = {}, pd.DataFrame()

        st.metric("Total Sessions", total_sessions)
        st.metric("Avg. Advice Length (words)", avg_advice_length)

        from collections import Counter
        import re

        text_blob = " ".join(df_sessions["profile"].fillna("").tolist() if not df_sessions.empty else [])
        text_blob += " " + " ".join(df_metrics["prompt_excerpt"].fillna("").tolist() if not df_metrics.empty else [])
        words = re.findall(r'\b[a-z]{4,}\b', text_blob.lower())
        top_keywords = Counter(words).most_common(5)
        top_words = ", ".join([kw for kw, _ in top_keywords])
        st.markdown(f"**Most Common Goal Keywords:** {top_words}")

        if not traits_df.empty:
            st.subheader("Big Five Trait Heatmap")
            heatmap_data = traits_df.describe().transpose()[["mean"]].rename(columns={"mean": "Average Score"})

            fig, ax = plt.subplots(figsize=(6, 3))
            sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", cbar=True, linewidths=0.5, fmt=".2f", ax=ax)
            ax.set_title("Average Big Five Trait Scores")
            st.pyplot(fig)
            
# --- Model Metrics Viewer ---
with st.expander("Model Metrics Overview"):
    if os.path.exists("metrics_log.json"):
        df = pd.read_json("data/model_metrics.json")
        st.dataframe(df)
        #Verbosity
        st.markdown("### Average Verbosity by Model")

        verbosity_avg = df.groupby("model")["verbosity"].mean()

        fig, ax = plt.subplots()
        colors = ["#636EFA"]  
        verbosity_avg.plot(kind="bar", ax=ax, color=colors)
        ax.set_ylabel("Average Word Count")
        ax.set_ylim(0, verbosity_avg.max() * 1.2)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
        st.pyplot(fig)

        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.download_button("Download Verbosity Chart", buf.getvalue(), "verbosity_chart.png", "image/png")

        #Risk Bias
        st.markdown("### Risk Bias Frequency")

        bias_counts = df.groupby(["model", "framing"]).size().unstack(fill_value=0)

        fig1, ax1 = plt.subplots()
        bias_counts.plot(kind="bar", stacked=True, ax=ax1, color=["#636EFA", "#00CC96", "#EF553B", "#AB63FA"])
        ax1.set_ylabel("Count")
        ax1.legend(title="Framing")
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=30, ha="right")
        st.pyplot(fig1)

        buf1 = io.BytesIO()
        fig1.savefig(buf1, format="png")
        st.download_button("Download Risk Bias Chart", buf1.getvalue(), "risk_bias_chart.png", "image/png")

        #Factuality
        st.markdown("### Factuality Mentions")

        fact_counts = df.groupby("model")["factuality"].sum()

        fig2, ax2 = plt.subplots()
        fact_counts.plot(kind="bar", ax=ax2, color="#00CC96")
        ax2.set_ylabel("Mentions")
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=30, ha="right")
        st.pyplot(fig2)

        buf2 = io.BytesIO()
        fig2.savefig(buf2, format="png")
        st.download_button("Download Factuality Chart", buf2.getvalue(), "factuality_chart.png", "image/png")

        #Sentiment
        st.markdown("### Average Sentiment Score by Model")

        df["sentiment_class"] = df["sentiment"].apply(
            lambda s: "negative" if s <= -0.05 else ("neutral" if s < 0.05 else "positive")
        )

        sentiment_binned = df.groupby(["model", "sentiment_class"]).size().unstack(fill_value=0)

        fig, ax = plt.subplots()
        sentiment_binned.plot(kind="bar", stacked=True, ax=ax, color=["#ef7a3b", "#faf063", "#00CC96"])
        ax.set_ylabel("Count")
        ax.legend(title="Sentiment Class")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
        st.pyplot(fig)

        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.download_button("Download Sentiment Chart", buf.getvalue(), "sentiment_score_chart.png", "image/png")

        #Consistency
        st.markdown("### Average Consistency by Model")
        consistency_avg = df.groupby("model")["consistency"].mean()

        fig3, ax3 = plt.subplots()
        consistency_avg.plot(kind="bar", ax=ax3, color="#AB63FA")
        ax3.set_ylabel("Cosine Similarity")
        ax3.set_ylim(0, 1)
        ax3.set_xticklabels(ax3.get_xticklabels(), rotation=30, ha="right")
        st.pyplot(fig3)

        buf3 = io.BytesIO()
        fig3.savefig(buf3, format="png")
        st.download_button("Download Consistency Chart", buf3.getvalue(), "consistency_chart.png", "image/png")
    
    else:
        st.info("No metrics logged yet.")
