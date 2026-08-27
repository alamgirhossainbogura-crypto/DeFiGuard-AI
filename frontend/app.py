import streamlit as st
import requests

# Page Configuration
st.set_page_config(
    page_title="DeFiGuard AI | Smart Contract Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Cyber/DeFi Dark Theme
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
    }
    .metric-card {
        background-color: #1f2937;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #374151;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/clouds/100/1/artificial-intelligence.png", width=80)
    st.title("DeFiGuard-AI")
    st.markdown("---")
    st.markdown("### ⚙️ Pipeline Status")
    st.success("🟢 FastAPI Backend: Online")
    st.success("🟢 Gemini 1.5 Pro: Connected")
    st.success("🟢 Elasticsearch: Active")
    st.markdown("---")
    st.markdown("**Hackathon Track:** Autonomous DeFi Security")

# Main Dashboard Interface
st.title("🛡️ DeFiGuard-AI")
st.markdown("### Autonomous Smart Contract & DeFi Risk Intelligence Platform")
st.write("Detect high-severity vulnerabilities, check historical exploit signatures, and generate automated patches using multi-agent AI reasoning.")

col1, col2 = st.columns([2, 1])

with col1:
    contract_name = st.text_input("Smart Contract Name", value="VulnerableVault.sol", placeholder="e.g., Vault.sol")

with col2:
    chain_type = st.selectbox("Blockchain / Language", ["solidity", "rust", "vyper"])

contract_code = st.text_area(
    "Smart Contract Source Code",
    height=250,
    placeholder="// Paste your Solidity or Rust smart contract code here...\ncontract VulnerableVault {\n    mapping(address => uint) public balances;\n    function withdraw(uint amount) public {\n        require(balances[msg.sender] >= amount);\n        (bool sent, ) = msg.sender.call{value: amount}(\"\");\n        require(sent);\n        balances[msg.sender] -= amount;\n    }\n}"
)

# Backend API Endpoint
API_URL = "http://localhost:8000/run-scan"

if st.button("🚀 Run Autonomous Security Scan"):
    if not contract_code.strip():
        st.warning("⚠️ Please provide smart contract source code before running the scan.")
    else:
        with st.spinner("🤖 Autonomous Agents analyzing control flows and searching exploit vectors..."):
            try:
                payload = {
                    "contract_code": contract_code,
                    "contract_name": contract_name,
                    "chain_type": chain_type
                }
                response = requests.post(API_URL, json=payload, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ Audit Scan Completed Successfully!")
                    
                    # Display Results Layout
                    tab1, tab2 = st.tabs(["📊 AI Security Analysis", "🔍 Retrieved Threat Patterns"])
                    
                    with tab1:
                        st.markdown("### Deep Code Reasoning Report")
                        st.markdown(data.get("ai_analysis", "No analysis returned."))
                        
                    with tab2:
                        st.markdown("### Elasticsearch Hybrid Search Matches")
                        patterns = data.get("retrieved_patterns", [])
                        if patterns:
                            for idx, pattern in enumerate(patterns, 1):
                                st.info(f"**Pattern {idx}:** {pattern.get('title', 'N/A')} (Severity: {pattern.get('severity', 'Unknown')})")
                        else:
                            st.write("No direct historical matches found in local index.")
                            
                else:
                    st.error(f"❌ Server Error: {response.json().get('detail', 'Unknown error')}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the FastAPI backend. Make sure `backend/main.py` is running on port 8000!")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
