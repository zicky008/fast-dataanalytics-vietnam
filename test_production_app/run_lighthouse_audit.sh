#!/bin/bash
# Lighthouse Performance Audit for Production App
# Usage: cd /home/user/webapp && bash test_production_app/run_lighthouse_audit.sh

echo "🚀 Starting Lighthouse Performance Audit..."
echo "=========================================="

PROD_URL="https://fast-nicedashboard.streamlit.app/"
OUTPUT_DIR="/home/user/webapp/test_production_app"

# Desktop Audit
echo ""
echo "📊 Running Desktop Performance Audit..."
npx lighthouse "$PROD_URL" \
  --output=html \
  --output=json \
  --output-path="$OUTPUT_DIR/lighthouse_desktop" \
  --preset=desktop \
  --only-categories=performance,accessibility,best-practices,seo \
  --quiet

# Mobile Audit
echo ""
echo "📱 Running Mobile Performance Audit..."
npx lighthouse "$PROD_URL" \
  --output=html \
  --output=json \
  --output-path="$OUTPUT_DIR/lighthouse_mobile" \
  --preset=mobile \
  --only-categories=performance,accessibility,best-practices,seo \
  --quiet

echo ""
echo "✅ Lighthouse audits complete!"
echo ""
echo "📄 Reports generated:"
echo "   - Desktop HTML: $OUTPUT_DIR/lighthouse_desktop.report.html"
echo "   - Mobile HTML: $OUTPUT_DIR/lighthouse_mobile.report.html"
echo ""
echo "🎯 Performance Targets:"
echo "   - Performance Score: ≥90/100"
echo "   - First Contentful Paint: <1.8s"
echo "   - Largest Contentful Paint: <2.5s"
echo "   - Time to Interactive: <3.8s"
echo ""
echo "Open HTML reports to see detailed results!"
