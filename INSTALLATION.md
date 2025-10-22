# DataAnalytics Vietnam - Installation Guide

## 📋 System Requirements

### Python Version
- **Python 3.11+** (recommended)
- Python 3.10+ (minimum)

### Operating System
- ✅ Linux (Ubuntu 20.04+, Debian 11+)
- ✅ macOS (11.0+)
- ✅ Windows 10/11 (with WSL2 recommended)

### Hardware
- **RAM**: Minimum 2GB, Recommended 4GB+
- **Storage**: 500MB free space
- **Internet**: Stable connection for API calls

---

## 🚀 Quick Start (5 minutes)

### Step 1: Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/dataanalytics-vietnam.git
cd dataanalytics-vietnam
```

### Step 2: Create Virtual Environment
```bash
# Using venv (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# OR using conda
conda create -n datavietnam python=3.11
conda activate datavietnam
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure API Key
```bash
# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Get free API key from:
# https://aistudio.google.com/app/apikey
```

### Step 5: Run Application
```bash
streamlit run streamlit_app.py
```

Application will open at: **http://localhost:8501**

---

## 📦 Dependency Details

### Core Dependencies

#### 1. **Streamlit** (v1.31.0+)
- **Purpose**: Web UI framework
- **License**: Apache 2.0
- **Installation**: `pip install streamlit>=1.31.0`
- **Notes**: Provides interactive dashboard interface

#### 2. **Pandas** (v2.0.0+)
- **Purpose**: Data manipulation and analysis
- **License**: BSD 3-Clause
- **Installation**: `pip install pandas>=2.0.0`
- **Notes**: Critical for data cleaning and transformations

#### 3. **NumPy** (v1.24.0+)
- **Purpose**: Numerical computing
- **License**: BSD 3-Clause
- **Installation**: `pip install numpy>=1.24.0`
- **Critical**: Must have proper metadata for dependency chain
- **Known Issue**: If installed with `--no-deps`, can cause Plotly errors
- **Solution**: Always install normally: `pip install numpy>=1.24.0`

#### 4. **Plotly** (v5.18.0+)
- **Purpose**: Interactive visualizations
- **License**: MIT
- **Installation**: `pip install plotly>=5.18.0`
- **Dependencies**: Requires numpy with metadata, xarray, packaging
- **Notes**: Used for all dashboard charts (bar, line, scatter, pie)

#### 5. **Google Generative AI** (v0.3.0+)
- **Purpose**: Gemini API client
- **License**: Apache 2.0
- **Installation**: `pip install google-generativeai>=0.3.0`
- **Model**: Uses `gemini-2.0-flash` (stable, higher quota)
- **Rate Limit**: Free tier = 15 requests/min
- **Notes**: Core AI engine for all analytics

### Supporting Dependencies

#### 6. **OpenPyXL** (v3.1.0+)
- **Purpose**: Excel file (.xlsx) support
- **Installation**: `pip install openpyxl>=3.1.0`
- **Use Case**: Read/write Excel files for data import

#### 7. **Chardet** (v5.2.0+)
- **Purpose**: Character encoding detection
- **Installation**: `pip install chardet>=5.2.0`
- **Use Case**: Auto-detect CSV file encoding (UTF-8, Latin-1, etc.)

#### 8. **Kaleido** (v0.2.1+)
- **Purpose**: Static image export for Plotly
- **Installation**: `pip install kaleido>=0.2.1`
- **Use Case**: Export charts as PNG/SVG (future feature)

#### 9. **Python-dotenv** (v1.0.0+)
- **Purpose**: Environment variable management
- **Installation**: `pip install python-dotenv>=1.0.0`
- **Use Case**: Load `.env` file for API keys

#### 10. **Pydantic** (v2.0.0+)
- **Purpose**: Data validation
- **Installation**: `pip install pydantic>=2.0.0`
- **Use Case**: Validate API responses and configurations

#### 11. **Tenacity** (v8.2.0+)
- **Purpose**: Retry logic with exponential backoff
- **Installation**: `pip install tenacity>=8.2.0`
- **Use Case**: Handle rate limits (2s, 4s, 8s delays)

---

## 🔧 Troubleshooting

### Issue 1: NumPy Metadata Error
**Symptom**: `TypeError: expected str, bytes or os.PathLike object, not NoneType`

**Cause**: NumPy installed with `--no-deps` flag, missing metadata

**Solution**:
```bash
# Remove broken numpy
pip uninstall numpy -y
rm -rf venv/lib/python*/site-packages/numpy*

# Reinstall properly
pip install numpy>=1.24.0
```

### Issue 2: Plotly Import Error
**Symptom**: `ImportError: cannot import name 'packaging' from 'xarray'`

**Cause**: Dependency chain issue (Plotly → xarray → packaging)

**Solution**:
```bash
pip install --upgrade packaging xarray plotly
```

### Issue 3: Gemini API Rate Limit
**Symptom**: `429 Too Many Requests`

**Cause**: Exceeded free tier limit (15 req/min)

**Solution**: Implemented auto-retry with exponential backoff (2s, 4s, 8s)

### Issue 4: Streamlit Context Warnings
**Symptom**: `missing ScriptRunContext! This warning can be ignored`

**Impact**: Harmless warnings when running tests outside Streamlit

**Solution**: Tests check `is_streamlit_context()` before using Streamlit features

---

## 🧪 Verify Installation

### Run Test Suite
```bash
python test_real_api.py
```

**Expected Output**:
```
✅ TEST 1: Gemini Connection - PASSED
✅ TEST 2: Marketing Pipeline - PASSED (13.0s, 100/100 quality)
✅ TEST 3: E-commerce Pipeline - PASSED (22.8s, 100/100 quality)
✅ TEST 4: Rate Limiting - PASSED (5/5 requests)

🎉 ALL TESTS PASSED! Pipeline is ready for deployment.
```

### Test Individual Components
```bash
# Test domain detection
python -c "from src.domain_detection import detect_domain; import pandas as pd; print(detect_domain(pd.DataFrame({'order_id': [1]}), 'Shopify orders'))"

# Test Gemini connection
python -c "import google.generativeai as genai; import os; from dotenv import load_dotenv; load_dotenv(); genai.configure(api_key=os.getenv('GEMINI_API_KEY')); client = genai.GenerativeModel('gemini-2.0-flash'); print(client.generate_content('Test').text)"
```

---

## 🌐 Deployment

### Streamlit Cloud (Recommended)

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy**:
   - Go to https://share.streamlit.io/
   - Connect GitHub repository
   - Select `streamlit_app.py` as main file
   - Add `GEMINI_API_KEY` to Secrets
   - Click Deploy

3. **Configuration**: Streamlit Cloud auto-detects `requirements.txt`

### Manual Deployment (VPS/Cloud)

```bash
# Install system dependencies
sudo apt update
sudo apt install python3.11 python3-pip -y

# Clone and setup
git clone YOUR_REPO
cd dataanalytics-vietnam
pip install -r requirements.txt

# Configure systemd service (optional)
sudo nano /etc/systemd/system/datavietnam.service
```

---

## 📊 Performance Benchmarks

### Pipeline Speed (Gemini 2.0-flash)
- **Domain Detection**: 0.5s (cached: 0.001s)
- **Data Cleaning**: 1-8s (depends on data size)
- **Smart Blueprint**: 7-9s (EDA + Design combined)
- **Dashboard Build**: 0.2-0.4s (pure execution)
- **Domain Insights**: 4-6s (expert analysis)
- **Total**: 13-23s (target: <60s) ✅

### Memory Usage
- **Idle**: ~150MB
- **Processing**: ~300-500MB
- **Peak**: ~600MB (large datasets)

### API Quota Usage (Free Tier)
- **Domain Detection**: 0 requests (cached after first run)
- **Data Cleaning**: 1 request
- **Smart Blueprint**: 1 request
- **Domain Insights**: 1 request
- **Total per pipeline run**: 3 requests
- **Daily limit**: ~50 pipelines (15 req/min × 60 min = 900 req/day ÷ 3 = 300 pipelines)

---

## 🔐 Security Notes

1. **API Key Protection**:
   - NEVER commit `.env` file to git
   - Use Streamlit secrets for cloud deployment
   - Rotate API keys every 90 days

2. **Data Privacy**:
   - All data processed locally before API calls
   - No PII sent to Gemini API
   - Clear session state after analysis

3. **Rate Limiting**:
   - Built-in retry logic with backoff
   - Respects API quota limits
   - Graceful degradation on errors

---

## 📚 Additional Resources

- **Streamlit Documentation**: https://docs.streamlit.io/
- **Gemini API Guide**: https://ai.google.dev/docs
- **Plotly Charts**: https://plotly.com/python/
- **Pandas Tutorial**: https://pandas.pydata.org/docs/

---

## 🤝 Support

For issues or questions:
1. Check this guide first
2. Run test suite: `python test_real_api.py`
3. Check logs in `logs/` directory
4. Create GitHub issue with error details

---

**Version**: 1.0.0  
**Last Updated**: 2025-10-21  
**Maintained by**: DataAnalytics Vietnam Team
