# 🌐 GitHub Pages Deployment Guide

Complete guide for hosting your ToS Decoder on GitHub Pages with a beautiful landing page.

## 🎯 **What You'll Get**

- ✅ **Beautiful landing page** on GitHub Pages
- ✅ **Professional presentation** of your project
- ✅ **Easy sharing** with a public URL
- ✅ **No hosting costs** (completely free)
- ✅ **Custom domain** support (optional)
- ✅ **SEO optimized** landing page

## 🚀 **Step-by-Step Deployment**

### **Phase 1: Prepare Your Repository** ⏱️ 5 minutes

#### **Step 1: Create GitHub Repository**
1. **Go to GitHub**: https://github.com/
2. **Click "New Repository"**
3. **Repository name**: `tos-decoder`
4. **Description**: `AI-Powered Terms of Service Analyzer - Decode complex legal documents into plain English`
5. **Make it Public** (required for free GitHub Pages)
6. **Add README**: ✅ Check this box
7. **Click "Create Repository"**

#### **Step 2: Upload Your Files**
Upload these files to your repository:
- `index.html` (landing page)
- `src/app.py` (Streamlit app)
- `src/utils.py` (utility functions)
- `requirements.txt` (dependencies)
- `README.md` (project documentation)

### **Phase 2: Enable GitHub Pages** ⏱️ 3 minutes

#### **Step 3: Enable GitHub Pages**
1. **Go to your repository** on GitHub
2. **Click "Settings"** tab
3. **Scroll down** to "Pages" section
4. **Source**: Select "Deploy from a branch"
5. **Branch**: Select "main" (or "master")
6. **Folder**: Select "/ (root)"
7. **Click "Save"**

#### **Step 4: Wait for Deployment**
- **Wait 2-5 minutes** for GitHub Pages to build
- **Check status** in the "Pages" section
- **Your site will be available** at: `https://yourusername.github.io/tos-decoder`

### **Phase 3: Deploy Streamlit App** ⏱️ 10 minutes

#### **Step 5: Deploy to Streamlit Cloud**
1. **Go to Streamlit Cloud**: https://share.streamlit.io/
2. **Sign in** with your GitHub account
3. **Click "New app"**
4. **Repository**: Select `yourusername/tos-decoder`
5. **Branch**: Select `main`
6. **Main file path**: `src/app.py`
7. **App URL**: `https://yourusername-tos-decoder-src-app-xxxxx.streamlit.app`
8. **Click "Deploy"**

#### **Step 6: Update Landing Page**
1. **Edit `index.html`** in your repository
2. **Find this line**: `const streamlitUrl = 'https://your-streamlit-app-url.streamlit.app';`
3. **Replace** with your actual Streamlit app URL
4. **Commit changes**

### **Phase 4: Customize Your Landing Page** ⏱️ 5 minutes

#### **Step 7: Update Repository Information**
1. **Edit `index.html`**:
   - **Line 8**: Update `og:url` with your GitHub Pages URL
   - **Line 45**: Update GitHub repository link
   - **Line 200**: Update `streamlitUrl` with your Streamlit app URL

#### **Step 8: Add Custom Domain (Optional)**
1. **Go to repository Settings** → **Pages**
2. **Custom domain**: Enter your domain (e.g., `tos-decoder.com`)
3. **Add CNAME file** to repository root with your domain
4. **Update DNS** records to point to GitHub Pages

---

## 🔧 **Configuration Files**

### **Updated `index.html`**
The landing page includes:
- **Responsive design** for all devices
- **SEO optimization** with meta tags
- **Social media** sharing support
- **Professional presentation** of features
- **Call-to-action** buttons
- **Loading animations** and effects

### **Repository Structure**
```
tos-decoder/
├── index.html              # Landing page (GitHub Pages)
├── src/
│   ├── app.py              # Streamlit app
│   └── utils.py            # Utility functions
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
└── CNAME                  # Custom domain (optional)
```

---

## 🎨 **Landing Page Features**

### **Visual Elements:**
- ✅ **Modern gradient background**
- ✅ **Responsive design** (mobile-friendly)
- ✅ **Smooth animations** and hover effects
- ✅ **Professional typography**
- ✅ **Feature showcase** with icons
- ✅ **Step-by-step** usage guide

### **Interactive Elements:**
- ✅ **Launch button** (redirects to Streamlit app)
- ✅ **GitHub repository** link
- ✅ **Loading spinner** with animation
- ✅ **Hover effects** on features
- ✅ **Smooth scrolling** and transitions

### **SEO Optimization:**
- ✅ **Meta tags** for search engines
- ✅ **Open Graph** tags for social sharing
- ✅ **Twitter Card** support
- ✅ **Structured data** for better indexing
- ✅ **Mobile-first** responsive design

---

## 📊 **Deployment Architecture**

```
GitHub Repository
       ↓
   GitHub Pages
       ↓
   Landing Page (index.html)
       ↓
   Streamlit Cloud
       ↓
   Streamlit App (src/app.py)
```

## 💰 **Cost Breakdown**

| Service | Cost | Your Usage |
|---------|------|------------|
| **GitHub Pages** | FREE | ✅ Unlimited |
| **Streamlit Cloud** | FREE | ✅ Unlimited |
| **Custom Domain** | $10-15/year | ✅ Optional |
| **Total** | **$0/month** | ✅ Completely free |

---

## 🔍 **Testing Your Deployment**

### **Step 1: Test Landing Page**
1. **Visit**: `https://yourusername.github.io/tos-decoder`
2. **Check**: All features display correctly
3. **Test**: Responsive design on mobile
4. **Verify**: All links work properly

### **Step 2: Test Streamlit App**
1. **Click "Launch ToS Decoder"** button
2. **Verify**: Redirects to Streamlit app
3. **Test**: All app features work
4. **Check**: File upload and analysis

### **Step 3: Test Integration**
1. **Landing page** loads quickly
2. **Streamlit app** launches properly
3. **Navigation** between pages works
4. **Mobile experience** is smooth

---

## 🚨 **Troubleshooting**

### **Common Issues:**

**Issue 1: "404 Not Found" on GitHub Pages**
- **Solution**: Check repository is public
- **Fix**: Verify Pages is enabled in Settings
- **Check**: Branch and folder settings

**Issue 2: "Streamlit app not loading"**
- **Solution**: Check Streamlit Cloud deployment
- **Fix**: Verify `src/app.py` path is correct
- **Check**: Requirements.txt is in repository root

**Issue 3: "Launch button not working"**
- **Solution**: Update `streamlitUrl` in index.html
- **Fix**: Use correct Streamlit app URL
- **Check**: URL is accessible

**Issue 4: "Page looks broken on mobile"**
- **Solution**: Check responsive design
- **Fix**: Test on different screen sizes
- **Check**: CSS media queries

---

## 🎯 **Customization Options**

### **Branding:**
- **Logo**: Replace emoji with custom logo
- **Colors**: Update CSS color scheme
- **Fonts**: Change typography
- **Images**: Add custom graphics

### **Content:**
- **Features**: Modify feature descriptions
- **Steps**: Update how-it-works section
- **Links**: Add social media links
- **Contact**: Add contact information

### **Functionality:**
- **Analytics**: Add Google Analytics
- **Forms**: Add contact forms
- **Chat**: Add live chat widget
- **Newsletter**: Add email signup

---

## 📈 **SEO Optimization**

### **Meta Tags:**
```html
<title>ToS Decoder - AI-Powered Terms of Service Analyzer</title>
<meta name="description" content="Decode complex Terms of Service documents into plain English using AI.">
<meta name="keywords" content="terms of service, legal documents, AI analysis, PDF analysis">
```

### **Open Graph:**
```html
<meta property="og:title" content="ToS Decoder - AI-Powered Terms of Service Analyzer">
<meta property="og:description" content="Decode complex Terms of Service documents into plain English using AI.">
<meta property="og:image" content="https://yourusername.github.io/tos-decoder/og-image.jpg">
```

### **Structured Data:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "ToS Decoder",
  "description": "AI-Powered Terms of Service Analyzer"
}
</script>
```

---

## 🎉 **Success Checklist**

- [ ] GitHub repository created
- [ ] Files uploaded to repository
- [ ] GitHub Pages enabled
- [ ] Landing page accessible
- [ ] Streamlit app deployed
- [ ] Launch button working
- [ ] Mobile responsive
- [ ] SEO optimized
- [ ] Custom domain (optional)
- [ ] Analytics added (optional)

---

## 🚀 **Quick Commands**

```bash
# Clone your repository
git clone https://github.com/yourusername/tos-decoder.git
cd tos-decoder

# Add files
git add .
git commit -m "Add landing page and Streamlit app"
git push origin main

# Check GitHub Pages status
# Go to: https://github.com/yourusername/tos-decoder/settings/pages
```

---

## 📞 **Support Resources**

- **GitHub Pages Docs**: https://docs.github.com/en/pages
- **Streamlit Cloud**: https://share.streamlit.io/
- **Custom Domains**: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site
- **SEO Guide**: https://developers.google.com/search/docs/beginner/seo-starter-guide

---

**Your ToS Decoder will be live on GitHub Pages with a professional landing page!** 🎉

**Total setup time: ~20 minutes**
**Total cost: $0/month**
**Professional presentation: ✅**
**Global accessibility: ✅**
