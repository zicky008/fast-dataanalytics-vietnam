# Font Setup for PDF Export

## Vietnamese Font Support

The PDF export feature requires **DejaVu Sans** fonts to properly display Vietnamese characters with diacritics.

## Installation

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install fonts-dejavu fonts-dejavu-core fonts-dejavu-extra
```

### Linux (CentOS/RHEL)
```bash
sudo yum install dejavu-sans-fonts dejavu-serif-fonts
```

### macOS
DejaVu fonts are usually available via Homebrew:
```bash
brew tap homebrew/cask-fonts
brew install --cask font-dejavu
```

### Windows
Download DejaVu fonts from: https://dejavu-fonts.github.io/
Extract and install the .ttf files to `C:\Windows\Fonts\`

## Docker/Cloud Deployment

If deploying via Docker, add this to your Dockerfile:

```dockerfile
# Install Vietnamese fonts
RUN apt-get update && \
    apt-get install -y fonts-dejavu fonts-dejavu-core fonts-dejavu-extra && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

## Verification

The application will automatically detect and use DejaVu fonts. You'll see one of these messages:

✅ **Success**: "Vietnamese fonts loaded successfully"
⚠️ **Warning**: "DejaVu fonts not found. Vietnamese characters may not display correctly."

If you see the warning, install the fonts using the instructions above.

## Alternative Fonts

If DejaVu is not available, the system falls back to Helvetica, which **does not support Vietnamese diacritics**.

For other Unicode fonts that support Vietnamese:
- **Noto Sans** (Google Fonts)
- **Arial Unicode MS**
- **Times New Roman** (limited support)

## Troubleshooting

### Charts Not Appearing in PDF

If charts are not showing in exported PDFs:

1. Ensure `kaleido` is installed: `pip install kaleido>=0.2.1`
2. Check the console for error messages during export
3. Verify Plotly version: `pip install plotly>=5.18.0`

### Font Path Issues

If fonts are installed but not detected, manually specify the path in `/src/utils/export_utils.py`:

```python
dejavu_paths = [
    '/your/custom/path/DejaVuSans.ttf',
    '/your/custom/path/DejaVuSans-Bold.ttf'
]
```

## Support

For issues, please check:
- System fonts: `fc-list | grep -i dejavu`
- Python packages: `pip list | grep -E "reportlab|kaleido|plotly"`
