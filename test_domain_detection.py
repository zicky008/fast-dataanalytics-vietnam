"""Test domain detection after fix"""
import pandas as pd
import sys
sys.path.insert(0, '/home/user/webapp/src')

from domain_detection import detect_domain

# Load Salary data
df = pd.read_csv('sample_data/Salary_Data.csv')

print("=" * 70)
print("🧪 DOMAIN DETECTION TEST")
print("=" * 70)

# Test with Salary data
print(f"\n📊 Dataset: Salary_Data.csv")
print(f"   Rows: {df.shape[0]:,}")
print(f"   Columns: {list(df.columns)}")

result = detect_domain(df, "HR Salary dataset with employee demographics and compensation")

print(f"\n🎯 DETECTION RESULT:")
print(f"   Domain:       {result['domain']}")
print(f"   Domain Name:  {result['domain_name']}")
print(f"   Confidence:   {result['confidence']*100:.1f}%")
print(f"   Expert Role:  {result['expert_role'][:60]}...")
print(f"   Reasoning:    {result['reasoning']}")

# Show all domain keywords
profile = result['profile']
print(f"\n🔑 DOMAIN KEYWORDS ({len(profile['keywords'])} total):")
print(f"   {', '.join(profile['keywords'])}")

# Check which keywords matched
all_text = ' '.join([
    "hr salary dataset employee demographics compensation".lower(),
    ' '.join(df.columns.str.lower())
])
matched = [kw for kw in profile['keywords'] if kw in all_text]
print(f"\n✅ MATCHED KEYWORDS ({len(matched)}/{len(profile['keywords'])}):")
print(f"   {', '.join(matched)}")

print("\n" + "=" * 70)
if result['domain'] == 'hr':
    print("✅ SUCCESS: Correctly detected as HR domain!")
elif result['domain'] == 'general':
    print("⚠️  ISSUE: Still detected as General (not HR)")
    print(f"   Score needed: {len(matched)}/{len(profile['keywords'])} = {len(matched)/len(profile['keywords'])*100:.1f}%")
else:
    print(f"❌ UNEXPECTED: Detected as {result['domain']}")

print("=" * 70)
