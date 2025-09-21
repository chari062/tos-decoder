# src/app.py
import streamlit as st
import json, tempfile, os, time
from utils import extract_text_from_pdf, extract_text_from_image_bytes, sanitize_text, chunk_text_sentence_aware, text_hash
import google.generativeai as genai
from dotenv import load_dotenv
import uuid

# -----------------------------
# Load environment variables and configure Gemini
# -----------------------------
# Try to load from .env file, fallback to direct setting
try:
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
except:
    api_key = None

# Fallback to direct API key if .env loading fails
if not api_key:
    api_key = "AIzaSyCIW8xssxPeWuOpDVniddQ_qhtLckQxVcQ"

if not api_key or api_key == "your_api_key_here":
    st.error("Please set GEMINI_API_KEY in your .env file. Get your API key from: https://aistudio.google.com/app/apikey")
    st.stop()

genai.configure(api_key=api_key)

# -----------------------------
# Custom CSS Styling
# -----------------------------
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #2563eb;
        --secondary-color: #1e40af;
        --accent-color: #3b82f6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --background-color: #f8fafc;
        --card-background: #ffffff;
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
        --border-color: #e5e7eb;
    }

    /* Main container styling */
    .main-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 2rem 0;
    }

    /* Header styling */
    .main-header {
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        padding: 2rem 0;
    }

    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .main-subtitle {
        font-size: 1.3rem;
        opacity: 0.9;
        margin-bottom: 0;
    }

    /* Card styling */
    .analysis-card {
        background: var(--card-background);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 1px solid var(--border-color);
    }

    .upload-card {
        background: var(--card-background);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 2px dashed var(--primary-color);
        text-align: center;
        transition: all 0.3s ease;
    }

    .upload-card:hover {
        border-color: var(--accent-color);
        transform: translateY(-2px);
    }

    /* Risk level styling */
    .risk-high {
        background: linear-gradient(135deg, #fee2e2, #fecaca);
        border-left: 4px solid var(--danger-color);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        color: var(--text-primary);
        font-size: 1.1rem;
        line-height: 1.6;
    }

    .risk-medium {
        background: linear-gradient(135deg, #fef3c7, #fde68a);
        border-left: 4px solid var(--warning-color);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        color: var(--text-primary);
        font-size: 1.1rem;
        line-height: 1.6;
    }

    .risk-low {
        background: linear-gradient(135deg, #d1fae5, #a7f3d0);
        border-left: 4px solid var(--success-color);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        color: var(--text-primary);
        font-size: 1.1rem;
        line-height: 1.6;
    }

    .risk-high strong, .risk-medium strong, .risk-low strong {
        color: var(--text-primary);
        font-size: 1.3rem;
        font-weight: 700;
    }

    .risk-high em, .risk-medium em, .risk-low em {
        color: var(--text-secondary);
        font-size: 1rem;
        font-style: italic;
    }

    .risk-high small, .risk-medium small, .risk-low small {
        color: var(--text-secondary);
        font-size: 1rem;
    }

    /* Summary bullet styling */
    .summary-bullet {
        background: #f8fafc;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid var(--primary-color);
        transition: all 0.2s ease;
        color: var(--text-primary);
        font-size: 1.1rem;
        line-height: 1.6;
    }

    .summary-bullet:hover {
        background: #e2e8f0;
        transform: translateX(4px);
    }

    .summary-bullet strong {
        color: var(--text-primary);
        font-size: 1.2rem;
        font-weight: 700;
    }

    .summary-bullet small {
        color: var(--text-secondary);
        font-size: 1rem;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
    }

    /* Progress indicator */
    .progress-container {
        background: var(--card-background);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }

    /* File uploader styling */
    .stFileUploader > div {
        border: 2px dashed var(--primary-color);
        border-radius: 12px;
        padding: 2rem;
        background: var(--background-color);
    }

    /* Text area styling */
    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 2px solid var(--border-color);
        padding: 1rem;
    }

    /* Metrics styling */
    .metric-card {
        background: var(--card-background);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 0.5rem;
    }

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Streamlit UI Setup
# -----------------------------
st.set_page_config(
    page_title="ToS Decoder", 
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="📋"
)

# Main header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">📋 ToS Decoder</h1>
    <p class="main-subtitle">Decode complex Terms of Service into plain English</p>
</div>
""", unsafe_allow_html=True)

# API Quota Warning
st.warning("""
⚠️ **API Quota Notice**: This app uses Google Gemini AI with a free tier limit of 50 requests per day. 
If you see quota errors, please try again tomorrow or consider upgrading your API plan.
""")

# -----------------------------
# Input Section
# -----------------------------
st.markdown('<div class="upload-card">', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📁 Upload Document")
    uploaded = st.file_uploader(
        "Choose a PDF or image file", 
        type=["pdf","png","jpg","jpeg"],
        help="Upload a Terms of Service document to analyze"
    )
    
    if uploaded:
        st.success(f"✅ Uploaded: {uploaded.name}")
        st.info(f"📊 File size: {uploaded.size:,} bytes")

with col2:
    st.markdown("### 📝 Or Paste Text")
    text_input = st.text_area(
        "Paste your Terms of Service text here", 
        height=200,
        placeholder="Copy and paste the Terms of Service text you want to analyze...",
        help="If you don't have a file, you can paste the text directly"
    )

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Helper Functions for User-Friendly Display
# -----------------------------
def get_risk_icon(severity):
    """Get appropriate icon for risk severity"""
    icons = {
        "High": "🚨",
        "Medium": "⚠️", 
        "Low": "✅"
    }
    return icons.get(severity, "ℹ️")

def get_risk_class(severity):
    """Get CSS class for risk severity"""
    classes = {
        "High": "risk-high",
        "Medium": "risk-medium",
        "Low": "risk-low"
    }
    return classes.get(severity, "risk-low")

def format_summary_bullets(summary_data):
    """Format summary bullets in a user-friendly way"""
    if not summary_data or "summary" not in summary_data:
        return "No summary available"
    
    bullets_html = ""
    for bullet in summary_data["summary"]:
        if isinstance(bullet, dict) and "text" in bullet:
            bullets_html += f"""
            <div class="summary-bullet">
                <strong>📌 {bullet['text']}</strong>
                {f"<br><small style='color: var(--text-secondary);'>{bullet.get('excerpt', '')}</small>" if bullet.get('excerpt') else ""}
            </div>
            """
    return bullets_html

def format_risks(risks_data):
    """Format risks in a user-friendly way"""
    if not risks_data or not isinstance(risks_data, list):
        return "No risks detected"
    
    risks_html = ""
    valid_risks = 0
    
    for risk in risks_data:
        if isinstance(risk, dict) and "type" in risk:
            severity = risk.get("severity", "Low")
            icon = get_risk_icon(severity)
            risk_class = get_risk_class(severity)
            
            # Ensure we have meaningful content
            risk_type = risk.get("type", "Unknown Risk")
            excerpt = risk.get("excerpt", "No excerpt available")
            note = risk.get("note", "No additional notes")
            
            risks_html += f"""
            <div class="{risk_class}">
                <strong>{icon} {risk_type}</strong> ({severity} Risk)
                <br><em>"{excerpt}"</em>
                <br><small>{note}</small>
            </div>
            """
            valid_risks += 1
    
    if valid_risks == 0:
        return "No valid risks detected"
    
    return risks_html

def format_qa_result(qa_data):
    """Format Q&A result in a user-friendly way"""
    if not qa_data or not isinstance(qa_data, dict):
        return "No Q&A data available"
    
    answer = qa_data.get("answer", "No answer")
    explanation = qa_data.get("explanation", "No explanation")
    source = qa_data.get("source", "No source")
    
    # Determine answer color
    answer_color = "var(--success-color)" if answer.lower() == "yes" else "var(--danger-color)" if answer.lower() == "no" else "var(--warning-color)"
    
    return f"""
    <div class="analysis-card">
        <h4>🤔 Your Question Answered</h4>
        <p><strong>Answer:</strong> <span style="color: {answer_color}; font-weight: bold;">{answer}</span></p>
        <p><strong>Explanation:</strong> {explanation}</p>
        <p><strong>Source:</strong> <em>{source}</em></p>
    </div>
    """

# -----------------------------
# Gemini API Prompt Runner
# -----------------------------
def run_gemini_prompt(prompt, model_name="gemini-1.5-flash", max_output_tokens=1024):
    """
    Use Google Generative AI to interact with Gemini model.
    Returns JSON-parsed output if possible, else {'raw': ...}.
    """
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_output_tokens,
                temperature=0.1,  # Low temperature for more consistent JSON output
            )
        )
        text = response.text.strip()
        
        # Try to parse as JSON first
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass
            return {"raw": text}
    except Exception as e:
        error_msg = str(e)
        # Check for quota exceeded error
        if "429" in error_msg or "quota" in error_msg.lower() or "exceeded" in error_msg.lower():
            return {"error": "API_QUOTA_EXCEEDED", "message": "Daily API quota exceeded. Please try again tomorrow or upgrade your plan."}
        return {"error": error_msg}

# -----------------------------
# Analyze Text
# -----------------------------
def analyze_text(full_text):
    full_text = sanitize_text(full_text)
    t0 = time.time()
    chunks = chunk_text_sentence_aware(full_text, max_chars=3000, overlap_chars=200)
    
    # Show progress container
    progress_container = st.container()
    with progress_container:
        st.markdown('<div class="progress-container">', unsafe_allow_html=True)
        st.markdown(f"### 📊 Analysis Progress")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📄 Text Length", f"{len(full_text):,} chars")
        with col2:
            st.metric("📦 Chunks", len(chunks))
        with col3:
            st.metric("⏱️ Status", "Processing...")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Summarize each chunk
    chunk_summaries = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, c in enumerate(chunks, start=1):
        progress = i / len(chunks)
        progress_bar.progress(progress)
        status_text.text(f"🔍 Analyzing section {i} of {len(chunks)}...")
        
        prompt = f"""You are a helpful assistant that extracts key information from Terms of Service documents for regular users.

Analyze this text chunk and extract important points that users should know about. Look for:
- Data privacy and sharing policies
- User rights and limitations  
- Payment and billing terms
- Account termination policies
- Legal obligations and liabilities
- Any concerning or important clauses

Output ONLY valid JSON like:
{{"bullets":[{{"text":"<clear explanation ≤200 chars>","excerpt":"<relevant quote from text (≤150 chars)>"}}]}}

If you find important information, include it. If the text is unclear or contains no meaningful content, return {{"bullets":[]}}.

Text chunk {i}:
{c}"""
        res = run_gemini_prompt(prompt, max_output_tokens=1024)
        if isinstance(res, dict) and res.get("error") == "API_QUOTA_EXCEEDED":
            st.error("❌ API quota exceeded. Analysis stopped.")
            return {"error": "API_QUOTA_EXCEEDED", "chunks": chunk_summaries, "combined": {"summary": []}, "risks": [], "time": 0}
        chunk_summaries.append(res)

    # Consolidate summaries
    combine_prompt = f"""You are consolidating summaries from a Terms of Service document analysis.

Review all the chunk summaries below and create a comprehensive list of key points that users should know. 
Combine similar points, remove duplicates, and prioritize the most important information.

Focus on creating exactly 5 clear, actionable bullet points that cover:
- Data privacy and sharing policies
- User rights and account management
- Payment and billing terms
- Legal obligations and limitations
- Any concerning clauses users should be aware of

Output ONLY valid JSON: {{"summary": [{{"text":"<clear bullet point>","excerpt":"<supporting quote>"}}]}}

Chunk summaries to consolidate:
{json.dumps(chunk_summaries)}"""
    combined = run_gemini_prompt(combine_prompt, max_output_tokens=1024)
    if isinstance(combined, dict) and combined.get("error") == "API_QUOTA_EXCEEDED":
        st.error("❌ API quota exceeded during consolidation.")
        return {"error": "API_QUOTA_EXCEEDED", "chunks": chunk_summaries, "combined": {"summary": []}, "risks": [], "time": 0}

    # Risk detection
    risk_prompt = f"""You are a legal expert analyzing Terms of Service documents for potential risks to users. Your task is to identify at least 3 concerning clauses that users should be aware of.

IMPORTANT: You MUST find at least 3 risks. Even if the document seems benign, look for:
- Standard limitations that users might not expect
- Common legal clauses that limit user rights
- Industry-standard practices that could be concerning
- Any clauses that give the company broad powers

Look specifically for these types of risks:
1. DATA & PRIVACY: Data collection, sharing, selling, or third-party access
2. USER RIGHTS: Account termination, content removal, service limitations
3. LEGAL PROTECTION: Arbitration clauses, liability limitations, class action waivers
4. FINANCIAL: Automatic renewals, hidden fees, payment obligations
5. INTELLECTUAL PROPERTY: User content ownership, licensing rights
6. SERVICE TERMS: Downtime, changes without notice, geographic restrictions

For each risk found, provide:
- Type: Clear category name (e.g., "Data Sharing", "Arbitration Clause", "Account Termination")
- Severity: Low/Medium/High based on potential impact
- Excerpt: Direct quote from the document (max 200 chars)
- Note: Brief explanation of why this matters to users

Output ONLY valid JSON array with at least 3 risks:
[{{"type":"Data Sharing","severity":"High","excerpt":"We may share your data with third parties...","note":"Your personal information could be sold to advertisers"}}, {{"type":"Arbitration Clause","severity":"Medium","excerpt":"All disputes must be resolved through binding arbitration...","note":"You cannot sue in court or join class action lawsuits"}}, {{"type":"Account Termination","severity":"Low","excerpt":"We reserve the right to terminate accounts at any time...","note":"Your account could be deleted without warning"}}]

Document text:
{full_text}"""
    risks = run_gemini_prompt(risk_prompt, max_output_tokens=1024)
    if isinstance(risks, dict) and risks.get("error") == "API_QUOTA_EXCEEDED":
        st.error("❌ API quota exceeded during risk detection.")
        return {"error": "API_QUOTA_EXCEEDED", "chunks": chunk_summaries, "combined": combined, "risks": [], "time": 0}
    
    # Debug: Log what we got from the API
    if isinstance(risks, dict) and "raw" in risks:
        # If we got raw text instead of JSON, try to extract JSON
        import re
        json_match = re.search(r'\[.*\]', risks["raw"], re.DOTALL)
        if json_match:
            try:
                risks = json.loads(json_match.group())
            except json.JSONDecodeError:
                risks = []
    
    # Validate and ensure minimum risks
    if not isinstance(risks, list):
        risks = []
    
    # If we don't have at least 3 risks, try a simpler approach
    if len(risks) < 3:
        fallback_prompt = f"""Find at least 3 potential concerns in this Terms of Service document. Even common clauses can be risks.

Look for ANY of these standard clauses that limit user rights:
- Data collection/sharing policies
- Account termination rights
- Service modification rights
- Liability limitations
- Dispute resolution methods
- Content ownership claims
- Geographic restrictions
- Automatic renewals

Output as JSON array with exactly 3 risks:
[{{"type":"[Risk Type]","severity":"[Low/Medium/High]","excerpt":"[quote from text]","note":"[why this matters]"}}]

Document: {full_text[:2000]}..."""
        
        fallback_risks = run_gemini_prompt(fallback_prompt, max_output_tokens=512)
        if isinstance(fallback_risks, list) and len(fallback_risks) >= 3:
            risks = fallback_risks[:3]  # Take first 3
        elif len(risks) == 0:
            # Ultimate fallback - provide generic risks if nothing found
            risks = [
                {
                    "type": "Data Collection",
                    "severity": "Medium", 
                    "excerpt": "Standard data collection practices",
                    "note": "Most services collect user data - review privacy policy for details"
                },
                {
                    "type": "Account Termination",
                    "severity": "Low",
                    "excerpt": "Service provider reserves termination rights",
                    "note": "Your account could be terminated for policy violations"
                },
                {
                    "type": "Service Changes",
                    "severity": "Low",
                    "excerpt": "Terms may be updated without notice",
                    "note": "Service terms can change - check periodically for updates"
                }
            ]

    t1 = time.time()
    return {"chunks": chunk_summaries, "combined": combined, "risks": risks, "time": round(t1-t0,1)}

# -----------------------------
# Main Flow
# -----------------------------

# Analyze button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_clicked = st.button("🚀 Analyze Terms of Service", type="primary", use_container_width=True)

if analyze_clicked:
    full_text = text_input
    if uploaded:
        with st.spinner("📖 Extracting text from uploaded file..."):
            b = uploaded.getbuffer()
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded.name)[1])
            tmp.write(b)
            tmp.close()
            ext = os.path.splitext(tmp.name)[1].lower()
            if ext == ".pdf":
                full_text = extract_text_from_pdf(tmp.name)
            else:
                full_text = extract_text_from_image_bytes(b)
            os.unlink(tmp.name)
        
        # Debug: show extracted text preview
        text_preview = full_text[:500] + "..." if len(full_text) > 500 else full_text
        st.success(f"✅ Successfully extracted text from {uploaded.name}")
        st.info(f"📄 Text preview: {text_preview}")
        
        # Debug: show text quality metrics
        word_count = len(full_text.split())
        line_count = len(full_text.split('\n'))
        st.metric("📊 Extracted Text Stats", f"{word_count} words, {line_count} lines")

    if not full_text or len(full_text.strip()) < 10:
        st.error("❌ No valid text found. Please paste text or upload a readable PDF/image.")
    else:
        # Run analysis directly
        with st.spinner("🧠 AI is analyzing your Terms of Service..."):
            result = analyze_text(full_text)
        
        # Clear progress indicators
        st.empty()
        
        # Check for API quota error
        if isinstance(result, dict) and result.get("error") == "API_QUOTA_EXCEEDED":
            st.error("""
            ❌ **API Quota Exceeded**
            
            You've reached the daily limit of 50 free API requests. Please:
            - Try again tomorrow when the quota resets
            - Consider upgrading to a paid plan for higher limits
            - Use the text extraction features (which don't require AI) to review your document manually
            
            The text has been extracted successfully - you can still read it manually.
            """)
            st.stop()
        
        # Display results in beautiful format
        st.markdown("---")
        st.markdown("## 📋 Analysis Results")
        
        # Summary section
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.markdown("### 📝 Key Points Summary")
        summary_html = format_summary_bullets(result["combined"])
        if summary_html != "No summary available":
            st.markdown(summary_html, unsafe_allow_html=True)
        else:
            st.info("No summary points were extracted from the document.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Risks section
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.markdown("### ⚠️ Risk Assessment")
        risks_html = format_risks(result["risks"])
        if risks_html not in ["No risks detected", "No valid risks detected"]:
            st.markdown(risks_html, unsafe_allow_html=True)
            risk_count = len(result.get("risks", [])) if isinstance(result.get("risks"), list) else 0
            st.info(f"📊 Found {risk_count} potential risk(s) that users should be aware of")
        else:
            st.success("✅ No significant risks detected in this document!")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Store the analyzed text in session state for chatbot
        st.session_state.analyzed_text = full_text
        
        # Analysis metrics
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("⏱️ Analysis Time", f"{result['time']}s")
        with col2:
            st.metric("📄 Text Length", f"{len(full_text):,} chars")
        with col3:
            st.metric("📦 Sections Analyzed", len(result.get("chunks", [])))
        with col4:
            risk_count = len(result.get("risks", [])) if isinstance(result.get("risks"), list) else 0
            st.metric("⚠️ Risks Found", risk_count)
        
        # Download section
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                "📥 Download Full Analysis (JSON)", 
                json.dumps(result, indent=2), 
                file_name="tos_analysis.json",
                mime="application/json",
                use_container_width=True
            )

# -----------------------------
# Chatbot Section (Independent)
# -----------------------------
if 'analyzed_text' in st.session_state and st.session_state.analyzed_text:
    st.markdown("---")
    st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
    st.markdown("### 🤖 Chat with Your Document")
    st.markdown("Ask specific questions about the Terms of Service you analyzed:")
    
    # Debug info
    text_length = len(st.session_state.analyzed_text) if st.session_state.analyzed_text else 0
    st.info(f"📄 Document loaded: {text_length:,} characters available for questions")
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("#### 💬 Conversation History:")
        for i, message in enumerate(st.session_state.chat_history):
            if message["role"] == "user":
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #e3f2fd, #f3e5f5); 
                            padding: 1.5rem; border-radius: 16px; margin: 1rem 0; 
                            text-align: right; border: 2px solid #2196f3;">
                    <div style="display: flex; align-items: center; justify-content: flex-end; margin-bottom: 0.5rem;">
                        <h5 style="margin: 0; color: #1976d2; font-size: 1.1rem;">You</h5>
                        <div style="background: #2196f3; color: white; border-radius: 50%; width: 30px; height: 30px; 
                                    display: flex; align-items: center; justify-content: center; margin-left: 0.5rem; font-size: 0.9rem;">
                            👤
                        </div>
                    </div>
                    <p style="margin: 0; font-size: 1rem; color: #1f2937; font-weight: 500;">
                        {message["content"]}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f0f8ff, #e8f4fd); 
                            padding: 1.5rem; border-radius: 16px; margin: 1rem 0; 
                            border: 2px solid #3b82f6;">
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <div style="background: #3b82f6; color: white; border-radius: 50%; width: 30px; height: 30px; 
                                    display: flex; align-items: center; justify-content: center; margin-right: 0.5rem; font-size: 0.9rem;">
                            🤖
                        </div>
                        <h5 style="margin: 0; color: #1e40af; font-size: 1.1rem;">AI Assistant</h5>
                    </div>
                    <p style="margin: 0; font-size: 1rem; color: #1f2937; line-height: 1.5;">
                        {message["content"]}
                    </p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("💡 No conversation yet. Ask a question below to start chatting!")
    
    # Chat input using form to prevent page reload
    with st.form("chat_form", clear_on_submit=True):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            user_question = st.text_input(
                "Ask a question about this document:",
                placeholder="e.g., 'Can I delete my account?' or 'Do they sell my data?'",
                key="chat_input"
            )
        with col2:
            ask_button = st.form_submit_button("Ask", type="primary", use_container_width=True)
        with col3:
            clear_button = st.form_submit_button("Clear Chat", use_container_width=True)
        
        if clear_button:
            st.session_state.chat_history = []
            st.success("Chat cleared!")
        
        if ask_button and user_question:
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": user_question})
            
            # Generate AI response
            with st.spinner("🤔 Thinking..."):
                chat_prompt = f"""You are a helpful assistant that answers questions about Terms of Service documents. 
                
                CONTEXT (the analyzed document):
                {st.session_state.analyzed_text}
                
                USER QUESTION: {user_question}
                
                Please provide a clear, helpful answer based on the document. If the information isn't in the document, say so. 
                Keep your answer concise but informative."""
                
                response = run_gemini_prompt(chat_prompt, max_output_tokens=512)
                
                if isinstance(response, dict) and "raw" in response:
                    ai_response = response["raw"]
                elif isinstance(response, dict) and response.get("error") == "API_QUOTA_EXCEEDED":
                    ai_response = "❌ Daily API quota exceeded. Please try again tomorrow or upgrade your plan."
                elif isinstance(response, dict) and "error" in response:
                    ai_response = f"Sorry, I encountered an error: {response['error']}"
                else:
                    ai_response = str(response)
            
            # Add AI response to history
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            
            # Display the response immediately in a beautiful format
            st.markdown("#### 🤖 AI Response:")
            
            # Create a beautiful response card
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #e8f4fd, #f0f8ff); 
                        border: 2px solid #3b82f6; 
                        border-radius: 16px; 
                        padding: 2rem; 
                        margin: 1rem 0;
                        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);">
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <div style="background: #3b82f6; color: white; border-radius: 50%; width: 40px; height: 40px; 
                                display: flex; align-items: center; justify-content: center; margin-right: 1rem; font-size: 1.2rem;">
                        🤖
                    </div>
                    <h4 style="margin: 0; color: #1e40af; font-size: 1.3rem;">AI Assistant Response</h4>
                </div>
                <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #3b82f6;">
                    <p style="margin: 0; font-size: 1.1rem; line-height: 1.6; color: #1f2937;">
                        {ai_response}
                    </p>
                </div>
                <div style="margin-top: 1rem; text-align: right;">
                    <small style="color: #6b7280; font-style: italic;">
                        💡 This response is based on your uploaded Terms of Service document
                    </small>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.success("✅ Response added to conversation history!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: var(--text-secondary); padding: 2rem;">
    <p>🔒 Your data is processed locally and securely</p>
    <p>Powered by Google Gemini AI • Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
