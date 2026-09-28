import os
import sys

# Ensure project root is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from src.models import AgentRunTelemetry
from src.circuit_breaker import RunawayLoopCircuitBreaker
from src.finops_tracker import FinOpsTracker

st.set_page_config(page_title="Agent-FinOps | Governance Engine", layout="wide", page_icon="⚡")

st.title("⚡ Agent-FinOps: Token Cost, Latency & Runaway Loop Governor")
st.markdown("**Enterprise AI FinOps | Autonomous Circuit Breakers | Squad Budget Governance** | *100% Free & Open-Source*")

tracker = FinOpsTracker()
circuit_breaker = RunawayLoopCircuitBreaker()

tab1, tab2 = st.tabs(["📊 Executive FinOps & Squad Budgets", "🚨 Autonomous Circuit Breaker Simulator"])

# ----------------- TAB 1: EXECUTIVE FINOPS -----------------
with tab1:
    st.subheader("Executive Telemetry & Financial Health")
    st.caption("Live aggregate governance across 3 engineering divisions and 48 autonomous agent workstreams.")

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric(label="Monthly Token Spend", value="$14,820", delta="-18% vs unmonitored")
    with k2:
        st.metric(label="Avg Cost / Completed Task", value="$0.042", delta="Optimal")
    with k3:
        st.metric(label="P95 Agent Latency", value="2.84s", delta="-0.4s improvement")
    with k4:
        st.metric(label="Runaway Loops Prevented", value="42 Trips", delta="$1,920 Saved", delta_color="normal")

    st.divider()

    st.markdown("### Engineering Division Budget Utilization")
    squad_df = pd.DataFrame({
        "Engineering Division": ["Games Studio Alpha", "Streaming & Playback Squad", "Platform & Core Services"],
        "Allocated Budget ($)": ["$20,000", "$25,000", "$15,000"],
        "Current Month Spend ($)": ["$14,200", "$18,450", "$8,900"],
        "Budget Burn Rate": ["71.0%", "73.8%", "59.3%"],
        "Primary Model Usage": ["Claude 3.5 Sonnet / Llama 3.2", "GPT-4o / FastMCP", "DeepSeek-V3 / Local Ollama"],
        "Governance Status": ["HEALTHY", "HEALTHY", "UNDER BUDGET"]
    })
    st.dataframe(squad_df, use_container_width=True, hide_index=True)

# ----------------- TAB 2: CIRCUIT BREAKER SIMULATOR -----------------
with tab2:
    st.subheader("Autonomous Circuit Breaker Test Harness")
    st.markdown("Simulate agent execution streams to test real-time infinite loop and runaway budget detection.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Configure Simulated Agent Run**")
        scenario = st.selectbox(
            "Select Test Scenario",
            [
                "1. Healthy Autonomous Run (Normal Operation)",
                "2. Runaway Tool Loop (Infinite Retry Trap)",
                "3. Token Budget Explosion (> 25k tokens)"
            ]
        )

        if scenario.startswith("1"):
            default_tools = ["parse_spec", "search_docs", "generate_code", "run_tests"]
            default_tokens = 4500
        elif scenario.startswith("2"):
            default_tools = ["query_endpoint", "query_endpoint", "query_endpoint"]
            default_tokens = 6200
        else:
            default_tools = ["retrieve_context", "summarize_repo"]
            default_tokens = 32000

        run_id = st.text_input("Run Identifier", "RUN-AGENT-8849")
        model = st.selectbox("Model", ["claude-3-5-sonnet", "gpt-4o", "llama3.2 (Local)", "deepseek-v3"])
        tokens = st.slider("Total Tokens (Input + Output)", min_value=1000, max_value=40000, value=default_tokens, step=1000)
        tool_sequence = st.text_input("Tool Sequence (comma-separated)", ", ".join(default_tools))

        simulate_btn = st.button("⚡ Ingest & Evaluate Stream", type="primary")

    with col2:
        if simulate_btn:
            tools_list = [t.strip() for t in tool_sequence.split(",") if t.strip()]
            run_data = AgentRunTelemetry(
                run_id=run_id,
                squad_name="Games Studio Alpha",
                model_name=model,
                input_tokens=int(tokens * 0.7),
                output_tokens=int(tokens * 0.3),
                latency_ms=1850,
                tool_calls_sequence=tools_list
            )

            # Evaluate Circuit Breaker
            alert = circuit_breaker.evaluate_run(run_data)
            cost = tracker.calculate_cost(model, run_data.input_tokens, run_data.output_tokens)

            st.markdown("### Evaluation Verdict")
            if alert.status == "NORMAL_OPERATION":
                st.success("### ✅ STATUS: NORMAL OPERATION")
                st.metric("Incurred Cost", f"${cost:.4f}")
                st.info(f"**Policy Analysis:** {alert.trigger_reason}")
            else:
                st.error("### 🚨 CIRCUIT BREAKER TRIPPED: RUN TERMINATED")
                m_save1, m_save2 = st.columns(2)
                with m_save1:
                    st.metric("Tokens Conserved", f"{alert.saved_tokens_estimate:,} tokens")
                with m_save2:
                    st.metric("Wasted Spend Avoided", f"${alert.financial_cost_avoided_usd:.3f}")
                st.warning(f"**Trigger Reason:** {alert.trigger_reason}")
