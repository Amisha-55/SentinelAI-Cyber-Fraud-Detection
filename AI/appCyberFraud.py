# Main application entrypoint for cyber fraud detection
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from PIL import Image
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import io

from modules.scam_detector import detect_scam
from modules.gemini_explainer import get_gemini_response
from modules.ocr_reader import extract_text
from modules.risk_score import calculate_risk
from modules.url_detector import detect_url

# ============================================
# PAGE CONFIG & THEME
# ============================================

st.set_page_config(
    page_title="SentinelAI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for cybersecurity aesthetic
custom_css = """
<style>
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    }
    
    /* Header styling */
    h1 {
        color: #00FF41 !important;
        text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
        font-family: 'Courier New', monospace;
        font-weight: bold;
    }
    
    h2 {
        color: #00FF41 !important;
        border-bottom: 2px solid #00FF41;
        padding-bottom: 10px;
    }
    
    h3 {
        color: #00d4ff !important;
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(0, 255, 65, 0.05);
        border: 2px solid #00FF41;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.2);
    }
    
    /* Risk indicators */
    .risk-high {
        background: rgba(255, 0, 0, 0.1);
        border-left: 4px solid #FF0000;
    }
    
    .risk-medium {
        background: rgba(255, 165, 0, 0.1);
        border-left: 4px solid #FFA500;
    }
    
    .risk-low {
        background: rgba(0, 255, 65, 0.1);
        border-left: 4px solid #00FF41;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #00FF41 0%, #00d4ff 100%);
        color: #000;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.6);
    }
    
    /* Input styling */
    input, textarea {
        background-color: rgba(26, 31, 58, 0.8) !important;
        border: 1px solid #00FF41 !important;
        color: #e0e0e0 !important;
        border-radius: 6px !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        border-right: 2px solid #00FF41;
    }
    
    /* Tab styling */
    .stTabs [role="tablist"] button {
        color: #e0e0e0 !important;
        border-bottom: 2px solid transparent;
    }
    
    .stTabs [role="tablist"] button[aria-selected="true"] {
        color: #00FF41 !important;
        border-bottom: 2px solid #00FF41 !important;
    }
    
    /* Container styling */
    .container {
        background: rgba(26, 31, 58, 0.6);
        border: 1px solid #00FF41;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ============================================
# SESSION STATE
# ============================================

if 'scan_history' not in st.session_state:
    st.session_state.scan_history = []

# ============================================
# NAVIGATION SETUP
# ============================================

# Define pages for navigation
pages = {
    "🏠 Home": "home",
    "📩 SMS/Email Scanner": "sms_scanner",
    "🖼️ Screenshot Scanner": "screenshot_scanner",
    "🌐 URL Detector": "url_detector",
    "📊 Reports & Analytics": "reports",
    "� Cyber Crime Complaint": "complaint_generator",
    "🛡️ Security Tips": "security_tips",
}

# Create navigation
page_names_to_funcs = {
    "🏠 Home": lambda: page_home(),
    "📩 SMS/Email Scanner": lambda: page_sms_scanner(),
    "🖼️ Screenshot Scanner": lambda: page_screenshot_scanner(),
    "🌐 URL Detector": lambda: page_url_detector(),
    "📊 Reports & Analytics": lambda: page_reports(),
    "📄 Cyber Crime Complaint": lambda: page_complaint_generator(),
    "🛡️ Security Tips": lambda: page_security_tips(),
}

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_risk_color(risk_percent):
    """Return color based on risk level"""
    if risk_percent >= 70:
        return "🔴 CRITICAL"
    elif risk_percent >= 50:
        return "🟠 HIGH"
    elif risk_percent >= 30:
        return "🟡 MEDIUM"
    else:
        return "🟢 LOW"

def display_risk_gauge(score, label):
    """Display risk gauge chart"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        title={'text': label},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': "rgba(0, 255, 65, 0.2)"},
                {'range': [30, 60], 'color': "rgba(255, 165, 0, 0.2)"},
                {'range': [60, 100], 'color': "rgba(255, 0, 0, 0.2)"}
            ],
            'threshold': {
                'line': {'color': "#00FF41", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    fig.update_layout(
        font={'color': '#e0e0e0'},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(26, 31, 58, 0.6)',
        margin=dict(l=0, r=0, t=50, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

def log_scan(message, label, score):
    """Log scan to history"""
    st.session_state.scan_history.append({
        'timestamp': datetime.now(),
        'message': message[:100],
        'label': label,
        'score': score
    })

# ============================================
# PAGE: HOME
# ============================================

def page_home():
    st.title("🛡️ SentinelAI - Cyber Fraud Detection")
    
    # Hero section
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### AI-Powered Cyber Security Intelligence
        
        **SentinelAI** is an advanced platform for detecting and analyzing:
        - 📩 Scam SMS and phishing emails
        - 🖼️ Suspicious screenshots and documents
        - 🌐 Malicious and fake URLs
        - 📄 Cyber crime documentation
        
        Use our AI models and expert analysis to stay protected.
        """)
    
    with col2:
        st.info("🚀 **Quick Stats**\n\n"
                f"Total Scans: {len(st.session_state.scan_history)}\n\n"
                f"Threats Detected: 📊")
    
    st.markdown("---")
    
    # Feature cards
    st.subheader("Key Features")
    feat_col1, feat_col2, feat_col3 = st.columns(3)
    
    with feat_col1:
        st.markdown("""
        <div class='container'>
        <h4>🎯 Real-time Detection</h4>
        Instant analysis of threats using advanced ML models
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col2:
        st.markdown("""
        <div class='container'>
        <h4>🤖 AI Explanations</h4>
        Get detailed reasoning for every detection
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col3:
        st.markdown("""
        <div class='container'>
        <h4>📥 Batch Processing</h4>
        Upload CSV for bulk scans and reports
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick start guide
    with st.expander("🚀 Quick Start Guide"):
        st.markdown("""
        1. **SMS/Email Scanner**: Paste text or upload a CSV file for batch analysis
        2. **Screenshot Scanner**: Upload images to extract and analyze text
        3. **URL Detector**: Enter website URLs to check for malicious patterns
        4. **Complaint Generator**: Create formal cyber crime complaints
        5. **Reports**: View analytics and historical scan data
        """)

# ============================================
# PAGE: SMS/EMAIL SCANNER
# ============================================

def page_sms_scanner():
    st.title("📩 SMS & Email Scam Detection")
    
    # Tabs for different input methods
    tab1, tab2 = st.tabs(["Single Message", "Batch Upload"])
    
    with tab1:
        st.subheader("Analyze Individual Message")
        
        message = st.text_area(
            "Paste SMS or Email content",
            height=200,
            placeholder="Enter the suspicious message here..."
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            analyze_btn = st.button("🔍 Analyze Message", use_container_width=True)
        with col2:
            st.write("")  # spacer
        with col3:
            st.write("")  # spacer
        
        if analyze_btn and message:
            with st.spinner("Analyzing message..."):
                label, score = detect_scam(message)
                risk = calculate_risk(score)
                log_scan(message, label, score)
            
            # Display results in columns
            res_col1, res_col2 = st.columns(2)
            
            with res_col1:
                # Risk gauge
                display_risk_gauge(risk, "Risk Score")
            
            with res_col2:
                # Prediction card
                st.markdown(f"""
                <div class='metric-card'>
                <h3>Prediction: {label}</h3>
                <p>Confidence Score: <b>{score:.2%}</b></p>
                <p>Risk Level: <b>{get_risk_color(risk)}</b></p>
                </div>
                """, unsafe_allow_html=True)
            
            # AI Explanation
            st.markdown("---")
            st.subheader("🤖 AI Explanation")
            with st.spinner("Generating AI analysis..."):
                explanation = get_gemini_response(message)
            st.markdown(f"""
            <div class='container'>
            {explanation}
            </div>
            """, unsafe_allow_html=True)
            
            # Download options
            col1, col2 = st.columns(2)
            with col1:
                report_text = f"""SentinelAI Scan Report
Generated: {datetime.now()}

MESSAGE:
{message}

ANALYSIS:
Prediction: {label}
Score: {score:.2%}
Risk Level: {risk}%

EXPLANATION:
{explanation}
"""
                st.download_button(
                    "📥 Download Report",
                    report_text,
                    file_name=f"sentinel_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    
    with tab2:
        st.subheader("Batch Upload CSV")
        
        uploaded_csv = st.file_uploader(
            "Upload CSV file (must contain 'message' column)",
            type=['csv']
        )
        
        explain_batch = st.checkbox("Generate AI explanations for all messages (slower)", value=False)
        
        if uploaded_csv is not None:
            df = pd.read_csv(uploaded_csv)
            
            if 'message' not in df.columns:
                st.error("❌ CSV must contain a 'message' column")
            else:
                if st.button("🔍 Analyze All Messages", use_container_width=True):
                    progress_bar = st.progress(0)
                    results = []
                    
                    for idx, msg in enumerate(df['message'].fillna('').astype(str)):
                        label, score = detect_scam(msg)
                        risk = calculate_risk(score)
                        result = {
                            'message': msg[:100],
                            'label': label,
                            'score': f"{score:.2%}",
                            'risk_percent': risk
                        }
                        
                        if explain_batch:
                            result['explanation'] = get_gemini_response(msg)
                        
                        results.append(result)
                        progress_bar.progress((idx + 1) / len(df))
                    
                    out_df = pd.DataFrame(results)
                    
                    # Display results
                    st.success(f"✅ Analyzed {len(out_df)} messages")
                    st.dataframe(out_df, use_container_width=True)
                    
                    # Statistics
                    stat_col1, stat_col2, stat_col3 = st.columns(3)
                    with stat_col1:
                        st.metric("Total Messages", len(out_df))
                    with stat_col2:
                        scams = (out_df['label'] == 'Scam').sum()
                        st.metric("Scams Detected", scams)
                    with stat_col3:
                        avg_risk = out_df['risk_percent'].mean()
                        st.metric("Avg Risk %", f"{avg_risk:.1f}")
                    
                    # Download
                    csv_bytes = out_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "📥 Download Results CSV",
                        csv_bytes,
                        file_name=f"sentinel_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime='text/csv',
                        use_container_width=True
                    )

# ============================================
# PAGE: SCREENSHOT SCANNER
# ============================================

def page_screenshot_scanner():
    st.title("🖼️ Screenshot Scam Detection")
    
    uploaded_file = st.file_uploader(
        "Upload screenshot (PNG, JPG, JPEG)",
        type=['png', 'jpg', 'jpeg']
    )
    
    if uploaded_file:
        # Display image
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Uploaded Screenshot", use_column_width=True)
        
        with col2:
            st.info(f"**File Info**\n\n"
                   f"Size: {uploaded_file.size / 1024:.1f} KB\n\n"
                   f"Format: {uploaded_file.type}")
        
        # Extract text
        if st.button("🔍 Extract & Analyze", use_container_width=True):
            with st.spinner("Extracting text from image..."):
                with open("temp.png", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                text = extract_text("temp.png")
            
            if not text:
                st.warning("⚠️ No text detected in image")
            else:
                st.subheader("📝 Extracted Text")
                st.text_area("Extracted content:", text, height=150, disabled=True)
                
                # Download extracted text
                st.download_button(
                    "📥 Download Text",
                    text,
                    file_name=f"extracted_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
                st.markdown("---")
                
                # Analyze
                with st.spinner("Analyzing extracted text..."):
                    label, score = detect_scam(text)
                    risk = calculate_risk(score)
                    log_scan(text, label, score)
                
                # Results
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    display_risk_gauge(risk, "Risk Score")
                with res_col2:
                    st.markdown(f"""
                    <div class='metric-card'>
                    <h3>Prediction: {label}</h3>
                    <p>Score: <b>{score:.2%}</b></p>
                    <p>Risk: <b>{get_risk_color(risk)}</b></p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Explanation
                st.subheader("🤖 AI Analysis")
                with st.spinner("Generating analysis..."):
                    explanation = get_gemini_response(text)
                st.markdown(f"<div class='container'>{explanation}</div>", unsafe_allow_html=True)

# ============================================
# PAGE: URL DETECTOR
# ============================================

def page_url_detector():
    st.title("🌐 Fake URL Detection")
    
    url = st.text_input(
        "Enter website URL",
        placeholder="https://example.com"
    )
    
    if st.button("🔍 Check URL", use_container_width=True) and url:
        with st.spinner("Analyzing URL..."):
            suspicious, reasons = detect_url(url)
            explanation = get_gemini_response(url)
        
        # Risk display
        col1, col2 = st.columns(2)
        with col1:
            if suspicious:
                st.error("⚠️ SUSPICIOUS URL DETECTED")
                status = "🔴 MALICIOUS"
                color = "risk-high"
            else:
                st.success("✅ URL APPEARS SAFE")
                status = "🟢 LEGITIMATE"
                color = "risk-low"
        
        with col2:
            st.markdown(f"""
            <div class='metric-card'>
            <h3>Status: {status}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Reasons
        st.subheader("📋 Detection Reasons")
        if reasons:
            for i, reason in enumerate(reasons, 1):
                st.markdown(f"**{i}. {reason}**")
        else:
            st.info("No suspicious patterns detected")
        
        st.markdown("---")
        
        # Analysis
        st.subheader("🤖 Detailed Analysis")
        st.markdown(f"<div class='container'>{explanation}</div>", unsafe_allow_html=True)

# ============================================
# PAGE: REPORTS & ANALYTICS
# ============================================

def page_reports():
    st.title("📊 Reports & Analytics")
    
    if not st.session_state.scan_history:
        st.info("📭 No scans yet. Start by using the scanners above!")
        return
    
    # Convert history to DataFrame
    history_df = pd.DataFrame(st.session_state.scan_history)
    
    # Statistics
    st.subheader("📈 Scan Statistics")
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric("Total Scans", len(history_df))
    with stat_col2:
        scams = (history_df['label'] == 'Scam').sum()
        st.metric("Scams Detected", scams)
    with stat_col3:
        legit = (history_df['label'] == 'Legitimate').sum()
        st.metric("Legitimate", legit)
    with stat_col4:
        avg_score = history_df['score'].mean()
        st.metric("Avg Score", f"{avg_score:.2%}")
    
    st.markdown("---")
    
    # Charts
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Pie chart of scam vs legitimate
        label_counts = history_df['label'].value_counts()
        fig = px.pie(
            values=label_counts.values,
            names=label_counts.index,
            title="Scan Results Distribution",
            color_discrete_map={'Scam': '#FF4444', 'Legitimate': '#00FF41'}
        )
        fig.update_layout(
            font={'color': '#e0e0e0'},
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(26, 31, 58, 0.6)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with chart_col2:
        # Score distribution
        fig = px.histogram(
            history_df,
            x='score',
            nbins=20,
            title="Score Distribution",
            color_discrete_sequence=['#00FF41']
        )
        fig.update_layout(
            font={'color': '#e0e0e0'},
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(26, 31, 58, 0.6)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Recent scans table
    st.subheader("📋 Recent Scans")
    st.dataframe(history_df.sort_values('timestamp', ascending=False), use_container_width=True)
    
    # Download history
    csv_bytes = history_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download Scan History",
        csv_bytes,
        file_name=f"sentinel_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime='text/csv',
        use_container_width=True
    )

# ============================================
# PAGE: COMPLAINT GENERATOR
# ============================================

def page_complaint_generator():
    st.title("📄 Generate Cyber Crime Complaint")

    incident = st.text_area(
        "Describe the incident",
        height=220,
        placeholder="Provide the details of the cyber incident here..."
    )

    if st.button("Generate Complaint"):
        prompt = f"""
Write a formal cyber crime complaint.

Incident:

{incident}

Include:

1 Date

2 Description

3 Request for investigation

4 Polite closing
"""
        with st.spinner("Generating complaint..."):
            complaint = get_gemini_response(prompt)

        st.markdown("---")
        st.subheader("✅ Generated Complaint")
        st.markdown(f"<div class='container'>{complaint}</div>", unsafe_allow_html=True)
        st.download_button(
            "📥 Download Complaint",
            complaint,
            file_name=f"cyber_crime_complaint_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime='text/plain',
            use_container_width=True
        )

# ============================================
# PAGE: SECURITY TIPS
# ============================================

def page_security_tips():
    st.title("🛡️ Cyber Security Tips")
    
    st.markdown("""
    ### Protect Yourself Online
    
    Follow these best practices to stay safe from cyber scams and fraud:
    """)
    
    tips_data = {
        "🔐 Password Security": [
            "Use strong, unique passwords (12+ characters with mixed case, numbers, symbols)",
            "Never share your password with anyone",
            "Use a password manager to store complex passwords",
            "Enable two-factor authentication (2FA) whenever possible"
        ],
        "📱 SMS & Email Safety": [
            "Never share OTP (One-Time Password) with anyone",
            "Be suspicious of urgent messages asking for personal info",
            "Don't click links in unsolicited messages",
            "Verify requests by contacting the organization directly",
            "Check for spelling errors and suspicious sender addresses"
        ],
        "🌐 Web Browsing": [
            "Verify website URLs before entering sensitive information",
            "Look for HTTPS and secure connection indicators",
            "Don't install software from unknown sources",
            "Keep your browser and plugins updated",
            "Use antivirus software"
        ],
        "💳 Financial Safety": [
            "Never share credit/debit card details via email or SMS",
            "Monitor bank statements regularly for suspicious activity",
            "Use virtual card numbers for online shopping",
            "Verify bank messages by calling official numbers",
            "Be wary of 'too good to be true' offers"
        ],
        "🎯 Job Scams": [
            "Beware of fake job offers with unrealistic pay",
            "Never pay upfront fees for job applications",
            "Verify job postings on official company websites",
            "Be suspicious of work-from-home jobs asking for personal details",
            "Research companies before applying"
        ],
        "📧 Email & Phishing": [
            "Don't open attachments from unknown senders",
            "Hover over links to see actual URL before clicking",
            "Check sender email address carefully (spoofing is common)",
            "Be suspicious of requests to 'verify' or 'confirm' information",
            "Report phishing emails to the organization"
        ]
    }
    
    # Display tips in expandable sections
    for category, tips in tips_data.items():
        with st.expander(f"### {category}"):
            for tip in tips:
                st.markdown(f"✓ {tip}")
    
    st.markdown("---")
    
    # Important contacts
    st.subheader("🚨 Important Contacts")
    contact_data = {
        "Organization": ["FBI", "FTC", "IC3 (Internet Crime Complaint Center)", "Local Police"],
        "Contact": [
            "tips.fbi.gov / 1-800-CALL-FBI",
            "reportfraud.ftc.gov",
            "ic3.gov",
            "911 or local non-emergency number"
        ]
    }
    st.dataframe(pd.DataFrame(contact_data), use_container_width=True)

# ============================================
# MAIN APP
# ============================================

def main():
    # Sidebar navigation
    with st.sidebar:
        st.markdown("---")
        selected_page = st.radio(
            "📍 Navigation",
            list(page_names_to_funcs.keys()),
            key="page_selector"
        )
        st.markdown("---")
        
        # Sidebar info
        st.markdown("""
        ### 📊 Quick Stats
        """)
        st.metric("Total Scans", len(st.session_state.scan_history))
        
        st.markdown("---")
        
        st.markdown("""
        ### 🛡️ Security Features
        - ✅ Real-time ML Detection
        - ✅ AI-Powered Analysis  
        - ✅ Batch Processing
        - ✅ Advanced URL Detection
        - ✅ OCR & Image Analysis
        """)
        
        st.markdown("---")
        st.caption("SentinelAI v1.0 | Powered by AI")
    
    # Run selected page
    page_names_to_funcs[selected_page]()
    
    # Footer
    st.markdown("---")
    footer_col1, footer_col2, footer_col3 = st.columns(3)
    with footer_col1:
        st.caption("🛡️ SentinelAI © Cyber Fraud Detection")
    with footer_col2:
        st.caption("AI-Powered Security Intelligence")
    with footer_col3:
        st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

if __name__ == "__main__":
    main()

