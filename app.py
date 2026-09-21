
import os
import streamlit as st
from google import genai
from google.genai import types

# ---------------------------------------------------------
# STAGE 1 & SETUP: API Configuration & Initialization
# ---------------------------------------------------------
st.set_page_config(
    page_title="Real Estate Micro-Location & Risk Intelligence Agent",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 AI Real Estate Micro-Location & Risk Intelligence Agent")
st.caption("Advanced Agentic Due-Diligence System powered by Gemini 3.8 Flash")

# API Key Handling
api_key = st.sidebar.text_input("Enter Google Gemini API Key:", type="password")

if not api_key:
    st.info("👈 Please enter your Gemini API Key in the sidebar to start the Agent.")
    st.stop()

# Initialize GenAI Client
client = genai.Client(api_key=api_key)

# ---------------------------------------------------------
# STAGE 4: AGENT TOOLS (Custom Python Tools)
# ---------------------------------------------------------
def calculate_financial_metrics(price: float, expected_rent: float) -> dict:
    """Calculates Gross Rental Yield and 5-Year Capital Gain Projection."""
    gross_yield = ((expected_rent * 12) / price) * 100
    five_year_val = price * (1.08 ** 5) # 8% annual inflation/growth estimate
    return {
        "gross_yield_percentage": round(gross_yield, 2),
        "projected_5yr_value": round(five_year_val, 2)
    }

def calculate_risk_score(flood_risk: str, litigation_risk: str, zoning_status: str) -> int:
    """Calculates a weighted safety index out of 100."""
    score = 100
    if flood_risk.lower() == "high": score -= 35
    elif flood_risk.lower() == "medium": score -= 15
    
    if litigation_risk.lower() == "high": score -= 40
    elif litigation_risk.lower() == "medium": score -= 20
    
    if zoning_status.lower() != "commercial/approved": score -= 15
    return max(score, 0)

# ---------------------------------------------------------
# STAGE 1 & 2: USER INPUT & CONTEXT ASSEMBLY
# ---------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    property_title = st.text_input("Property Title/Address:", "DHA Phase 6, Lahore")
    property_price = st.number_input("Asking Price (PKR/USD):", value=45000000, step=500000)
    expected_rent = st.number_input("Estimated Monthly Rent:", value=180000, step=10000)

with col2:
    flood_risk = st.selectbox("Area Flood History / Drainage Risk:", ["Low", "Medium", "High"])
    litigation_risk = st.selectbox("Title / Legal Litigation Risk:", ["Low", "Medium", "High"])
    zoning_status = st.selectbox("Zoning Authority Approval:", ["Commercial/Approved", "Pending", "Unapproved"])

analyze_btn = st.button("🚀 Run Agentic Due-Diligence Analysis")

# ---------------------------------------------------------
# STAGE 3, 5 & 6: REASONING, EVALUATION & RESPONSE
# ---------------------------------------------------------
if analyze_btn:
    with st.spinner("Agent is planning, calculating metrics, and performing risk assessment..."):
        
        # Step 1: Tool Execution
        fin_metrics = calculate_financial_metrics(property_price, expected_rent)
        safety_score = calculate_risk_score(flood_risk, litigation_risk, zoning_status)
        
        # Step 2: System Prompt (Stage 3 - Brain Guidance)
        system_instruction = """
        You are a Senior Real Estate Investment Auditor and Risk Intelligence AI Agent.
        Your job is to generate a highly critical, professional, and actionable due-diligence report.
        
        Structure your response clearly:
        1. Executive Verdict (Buy / Negotiate / Avoid)
        2. Micro-Location & Environmental Risk Breakdown
        3. Financial Analysis & Yield Assessment
        4. Legal & Title Checklist for Buyer
        5. Negotiation Strategy & Recommended Counter-Offer Price
        
        Be direct, analytical, and professional. Avoid generic fluff.
        """
        
        # Step 3: Context Assembly for LLM
        prompt = f"""
        Perform a comprehensive Due-Diligence Audit for the following Property:
        - Location/Title: {property_title}
        - Asking Price: {property_price:,}
        - Expected Monthly Rent: {expected_rent:,}
        - Environmental Flood Risk: {flood_risk}
        - Legal/Litigation Risk: {litigation_risk}
        - Zoning Approval Status: {zoning_status}
        
        Calculated Tool Metrics:
        - Gross Rental Yield: {fin_metrics['gross_yield_percentage']}%
        - Projected 5-Year Asset Value: {fin_metrics['projected_5yr_value']:,}
        - Calculated Safety Index: {safety_score}/100
        
        Analyze these inputs, highlight hidden risks, and provide a strategic investment decision.
        """
        
        try:
            # Stage 3 Call using official google-genai SDK
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.3  # Low temperature for analytical consistency
                )
            )
            
            # Display Metric Dashboards
            st.markdown("---")
            m1, m2, m3 = st.columns(3)
            m1.metric("Safety Index Score", f"{safety_score} / 100")
            m2.metric("Gross Rental Yield", f"{fin_metrics['gross_yield_percentage']}%")
            m3.metric("5-Yr Projected Value", f"{fin_metrics['projected_5yr_value']:,}")
            
            st.markdown("---")
            st.subheader("📋 Comprehensive AI Due-Diligence Report")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Error executing agent task: {e}")
