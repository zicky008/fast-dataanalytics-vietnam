# Dependency Management Guide

## 📦 Critical Dependency Information

This document provides detailed information about the dependency chain, known issues, and troubleshooting steps for **DataAnalytics Vietnam**.

---

## 🔗 Dependency Chain

### Primary Dependencies

```
DataAnalytics Vietnam (app)
├── streamlit (Web Framework)
│   ├── pandas
│   ├── numpy
│   └── altair
├── pandas (Data Processing)
│   └── numpy
├── plotly (Visualization) ⚠️ CRITICAL PATH
│   ├── tenacity
│   ├── packaging
│   └── numpy (with metadata) ⚠️ MUST HAVE METADATA
├── google-generativeai (AI Engine)
│   ├── google-ai-generativelanguage
│   └── google-api-core
└── python-dotenv (Configuration)
```

### Critical Path: NumPy Metadata

**Why Critical**: Plotly requires NumPy with proper metadata for version detection.

**Dependency Flow**:
```
plotly
  → imports xarray (optional dependency)
    → imports packaging.version
      → calls importlib.metadata.version('numpy')
        → MUST RETURN version string (e.g., "1.24.3")
        → If returns None → TypeError crash
```

**When This Breaks**:
- Installing NumPy with `pip install --no-deps numpy`
- Installing NumPy with `--ignore-installed` incorrectly
- Corrupted NumPy installation
- Multiple NumPy versions installed

---

## ⚠️ Known Issues & Solutions

### Issue #1: NumPy Metadata Corruption

**Symptom**:
```python
TypeError: expected str, bytes or os.PathLike object, not NoneType
```

**Root Cause**:
NumPy installed without metadata files (`*.dist-info/` directory missing).

**How It Happens**:
```bash
# ❌ WRONG: This breaks metadata
pip install --no-deps numpy
pip install --ignore-installed --no-deps numpy

# ✅ CORRECT: This preserves metadata
pip install numpy>=1.24.0
```

**Detection**:
```python
import importlib.metadata
version = importlib.metadata.version('numpy')
print(version)  # Should print "1.24.3", not None
```

**Solution 1 (Quick Fix)**:
```bash
# Uninstall completely
pip uninstall numpy -y

# Remove all numpy files
rm -rf venv/lib/python*/site-packages/numpy*
rm -rf venv/lib/python*/site-packages/numpy-*.dist-info

# Reinstall properly
pip install numpy>=1.24.0
```

**Solution 2 (Nuclear Option)**:
```bash
# Recreate entire virtual environment
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Prevention**:
- ✅ Always use `pip install numpy` (no flags)
- ✅ Use `requirements.txt` for consistent installs
- ❌ Never use `--no-deps` with NumPy
- ❌ Never manually copy NumPy files

---

### Issue #2: Plotly Import Error

**Symptom**:
```python
ImportError: cannot import name 'packaging' from 'xarray'
```

**Root Cause**:
Xarray expects `packaging` module but it's not installed or version mismatch.

**Solution**:
```bash
# Install/upgrade packaging
pip install --upgrade packaging

# If still fails, reinstall xarray
pip install --upgrade xarray

# If still fails, reinstall plotly
pip install --upgrade plotly
```

**Verification**:
```python
import plotly.express as px
print("Plotly working!")
```

---

### Issue #3: Streamlit Context Warnings

**Symptom**:
```
WARNING streamlit.runtime.scriptrunner_utils.script_run_context: 
Thread 'MainThread': missing ScriptRunContext! 
This warning can be ignored when running in bare mode.
```

**Root Cause**:
Code uses Streamlit features (st.metric, st.info, etc.) outside Streamlit app context (e.g., during testing).

**Impact**: 
- Harmless warnings
- Does not affect functionality
- Only appears in test logs

**Already Fixed**:
```python
def is_streamlit_context():
    """Check if running in Streamlit context"""
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        return get_script_run_ctx() is not None
    except:
        return False

# Usage
if is_streamlit_context():
    st.info("Processing...")  # Only runs in Streamlit
```

**No Action Needed**: Pipeline already handles this correctly.

---

### Issue #4: Gemini API Rate Limits

**Symptom**:
```
google.api_core.exceptions.ResourceExhausted: 429 RESOURCE_EXHAUSTED
```

**Root Cause**:
Free tier limit: 15 requests/minute

**Already Fixed**:
```python
@rate_limit_handler(max_retries=3, backoff_base=2)
def api_call():
    # Automatically retries with delays: 2s, 4s, 8s
    pass
```

**Manual Override** (if needed):
```python
import time

def manual_retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if '429' in str(e) and attempt < max_retries - 1:
                delay = 2 ** (attempt + 1)  # 2s, 4s, 8s
                print(f"Rate limited. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise
```

---

## 🔍 Diagnostic Commands

### Check Dependency Versions

```bash
# List all installed packages
pip list

# Check specific versions
pip show streamlit pandas numpy plotly google-generativeai

# Check for outdated packages
pip list --outdated
```

### Verify NumPy Metadata

```python
# Test NumPy metadata
import importlib.metadata
try:
    version = importlib.metadata.version('numpy')
    print(f"✅ NumPy version: {version}")
except Exception as e:
    print(f"❌ NumPy metadata error: {e}")
```

### Verify Plotly

```python
# Test Plotly import
try:
    import plotly.express as px
    import pandas as pd
    df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    fig = px.bar(df, x='x', y='y')
    print("✅ Plotly working!")
except Exception as e:
    print(f"❌ Plotly error: {e}")
```

### Verify Gemini API

```python
# Test Gemini connection
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

try:
    client = genai.GenerativeModel('gemini-2.0-flash')
    response = client.generate_content("Test")
    print(f"✅ Gemini API working: {response.text[:50]}...")
except Exception as e:
    print(f"❌ Gemini API error: {e}")
```

---

## 📋 Version Compatibility Matrix

| Package | Min Version | Tested Version | Max Version | Notes |
|---------|-------------|----------------|-------------|-------|
| Python | 3.10 | 3.11 | 3.12 | 3.11+ recommended |
| streamlit | 1.31.0 | 1.31.0 | latest | Web framework |
| pandas | 2.0.0 | 2.2.0 | latest | Data processing |
| numpy | 1.24.0 | 1.24.3 | <2.0 | CRITICAL: Must have metadata |
| plotly | 5.18.0 | 5.18.0 | latest | Visualization |
| google-generativeai | 0.3.0 | 0.8.0 | latest | AI engine |
| openpyxl | 3.1.0 | 3.1.2 | latest | Excel support |
| chardet | 5.2.0 | 5.2.0 | latest | Encoding detection |
| kaleido | 0.2.1 | 0.2.1 | latest | Image export |
| python-dotenv | 1.0.0 | 1.0.0 | latest | Config management |
| pydantic | 2.0.0 | 2.5.0 | latest | Data validation |
| tenacity | 8.2.0 | 8.2.0 | latest | Retry logic |

---

## 🔄 Update Strategy

### When to Update

**Security Updates**: Immediately
```bash
pip install --upgrade PACKAGE
```

**Feature Updates**: Review changelog first
```bash
pip show PACKAGE  # Check current version
pip install --upgrade PACKAGE
python test_real_api.py  # Run tests
```

**Major Version Updates**: Test in separate environment
```bash
# Create test environment
python3 -m venv test_env
source test_env/bin/activate
pip install PACKAGE==NEW_VERSION
# Test thoroughly before updating production
```

### Update Workflow

1. **Check for updates**:
   ```bash
   pip list --outdated
   ```

2. **Update one package at a time**:
   ```bash
   pip install --upgrade PACKAGE
   ```

3. **Run tests**:
   ```bash
   python test_real_api.py
   ```

4. **Update requirements.txt**:
   ```bash
   pip freeze > requirements.txt
   ```

5. **Commit changes**:
   ```bash
   git add requirements.txt
   git commit -m "Update PACKAGE to vX.Y.Z"
   ```

---

## 🛡️ Dependency Pinning

### Current Strategy

**requirements.txt** uses minimum version pinning:
```
# ✅ Allows upgrades within major version
pandas>=2.0.0

# ❌ Too restrictive (avoid)
pandas==2.2.0

# ❌ Too loose (avoid)
pandas
```

### When to Use Exact Pinning

Use `==X.Y.Z` for:
- Known breaking changes in newer versions
- Production deployments (for stability)
- Reproducible environments

**Example**:
```
# Lock down for production
pandas==2.2.0
numpy==1.24.3
plotly==5.18.0
```

### Lock File Strategy

For production, consider using `pip freeze`:
```bash
# Generate exact versions
pip freeze > requirements-lock.txt

# Install from lock file
pip install -r requirements-lock.txt
```

---

## 🧪 Testing Dependencies

### Run Full Test Suite

```bash
# Test all components
python test_real_api.py

# Expected output:
# ✅ TEST 1: Gemini Connection - PASSED
# ✅ TEST 2: Marketing Pipeline - PASSED
# ✅ TEST 3: E-commerce Pipeline - PASSED
# ✅ TEST 4: Rate Limiting - PASSED
```

### Test Individual Dependencies

```bash
# Test NumPy
python -c "import numpy; print(numpy.__version__)"

# Test Pandas
python -c "import pandas; print(pandas.__version__)"

# Test Plotly
python -c "import plotly; print(plotly.__version__)"

# Test Gemini
python -c "import google.generativeai; print('OK')"
```

---

## 📞 Support

**Dependency Issues**:
1. Check this guide first
2. Run diagnostic commands above
3. Try clean reinstall (remove venv + recreate)
4. Create GitHub issue with full error trace

**Useful Commands**:
```bash
# Show dependency tree
pip install pipdeptree
pipdeptree -p plotly

# Show package info
pip show --verbose numpy

# Check for conflicts
pip check
```

---

**Last Updated**: 2025-10-21  
**Maintained by**: DataAnalytics Vietnam Team
