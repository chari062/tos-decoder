# 📋 ToS Decoder

A beautiful, user-friendly web application that decodes complex Terms of Service documents into plain English using AI. Upload PDFs, images, or paste text to get an easy-to-understand analysis of legal documents.

**🌐 Live Demo**: [https://yourusername.github.io/tos-decoder](https://yourusername.github.io/tos-decoder)

## ✨ Features

- **📁 Multiple Input Methods**: Upload PDF files, images, or paste text directly
- **🎨 Beautiful UI**: Modern, aesthetic interface with intuitive design
- **📝 Plain English Summaries**: Convert legal jargon into 5 key points
- **⚠️ Risk Assessment**: Identify at least 3 potential risks with color-coded severity levels
- **🤔 Q&A**: Ask specific questions about the Terms of Service
- **📊 Progress Tracking**: Real-time analysis progress with metrics
- **📥 Export Results**: Download analysis results as JSON

## 🚀 Quick Start

### **Option 1: Use Live Demo**
1. **Visit**: [https://yourusername.github.io/tos-decoder](https://yourusername.github.io/tos-decoder)
2. **Click "Launch ToS Decoder"** button
3. **Start analyzing** Terms of Service documents

### **Option 2: Run Locally**
1. **Clone repository**:
   ```bash
   git clone https://github.com/yourusername/tos-decoder.git
   cd tos-decoder
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API key**:
   ```bash
   export GEMINI_API_KEY=your_api_key_here
   ```

4. **Run the application**:
   ```bash
   streamlit run src/app.py
   ```

5. **Open in browser**: http://localhost:8501

## 📁 Project Structure

```
tos-decoder/
├── index.html              # Landing page (GitHub Pages)
├── src/
│   ├── app.py              # Main Streamlit application
│   └── utils.py            # Utility functions
├── requirements.txt        # Python dependencies
├── GITHUB_PAGES_DEPLOYMENT.md  # Deployment guide
└── readme.md              # This file
```

## 🎯 How to Use

1. **Upload or Paste**: Choose to upload a PDF/image file or paste Terms of Service text
2. **Ask Questions** (Optional): Ask specific questions like "Can I delete my account?"
3. **Analyze**: Click "🚀 Analyze Terms of Service" to start the AI analysis
4. **Review Results**: View the 5 key points, 3+ risk assessments, and Q&A results
5. **Download**: Save the full analysis as JSON for your records

## 🎨 UI Features

- **Modern Design**: Clean, professional interface with gradient backgrounds
- **Color-Coded Risks**: 
  - 🚨 High Risk (Red)
  - ⚠️ Medium Risk (Yellow) 
  - ✅ Low Risk (Green)
- **Interactive Elements**: Hover effects and smooth transitions
- **Responsive Layout**: Works on desktop and mobile devices
- **Progress Indicators**: Real-time feedback during analysis

## 🔧 Technical Details

- **Frontend**: Streamlit with custom CSS
- **AI Model**: Google Gemini 1.5 Flash
- **Text Processing**: PDF extraction, OCR for images
- **Hosting**: GitHub Pages + Streamlit Cloud
- **Styling**: Custom CSS with modern design principles

## 📋 Requirements

- Python 3.7+
- Google Gemini API key
- Required packages listed in `requirements.txt`

## 💰 Cost

- **GitHub Pages**: FREE (unlimited hosting)
- **Streamlit Cloud**: FREE (unlimited hosting)
- **Total Cost**: $0/month

## 🔒 Privacy & Security

- Your data is processed securely
- No Terms of Service content is stored permanently
- Secure API communication with Google Gemini
- Professional hosting on GitHub and Streamlit Cloud

## 📞 Support

- **Deployment Guide**: `GITHUB_PAGES_DEPLOYMENT.md`
- **Live Demo**: [https://yourusername.github.io/tos-decoder](https://yourusername.github.io/tos-decoder)
- **GitHub Repository**: [https://github.com/yourusername/tos-decoder](https://github.com/yourusername/tos-decoder)

---

**Built with ❤️ using Streamlit, Google Gemini AI, and GitHub Pages**