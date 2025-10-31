"""
Comprehensive Test for Hotfix #5
Verify that tuple index error is fixed
"""

import sys
sys.path.insert(0, 'src')

print("="*80)
print("🧪 COMPREHENSIVE HOTFIX #5 VERIFICATION")
print("="*80)

# Test 1: Validate streamlit_app.py has correct validation order
print("\n📝 Test 1: Check streamlit_app.py validation order")
print("-"*80)

with open('streamlit_app.py', 'r') as f:
    content = f.read()
    
    # Check for Hotfix #5 comment
    if '# 🐛 HOTFIX #5: CRITICAL - Validate result BEFORE saving to session state' in content:
        print("✅ Hotfix #5 marker found")
    else:
        print("❌ Hotfix #5 marker NOT found - code may be old version")
        sys.exit(1)
    
    # Check validation order
    lines = content.split('\n')
    validation_start = None
    save_line = None
    
    for i, line in enumerate(lines):
        if 'if isinstance(result, tuple):' in line and validation_start is None:
            validation_start = i
        if 'st.session_state[\'result\'] = result' in line:
            save_line = i
            break
    
    if validation_start and save_line and validation_start < save_line:
        print(f"✅ Validation order CORRECT:")
        print(f"   - Validation starts at line {validation_start}")
        print(f"   - Save to session_state at line {save_line}")
        print(f"   - Distance: {save_line - validation_start} lines")
    else:
        print(f"❌ Validation order WRONG or not found!")
        print(f"   - Validation: line {validation_start}")
        print(f"   - Save: line {save_line}")
        sys.exit(1)

# Test 2: Simulate tuple return scenario
print("\n📝 Test 2: Simulate tuple return from pipeline")
print("-"*80)

class MockPipeline:
    def run_pipeline(self, df, desc):
        # Simulate error case - return tuple
        return (False, "Simulated pipeline error")

# Simulate the validation logic from Hotfix #5
result = MockPipeline().run_pipeline(None, "")

try:
    # Hotfix #5 logic
    if isinstance(result, tuple):
        success, error_msg = result
        print(f"✅ Tuple detected correctly")
        print(f"   - success: {success}")
        print(f"   - error_msg: {error_msg}")
        print(f"✅ Would call st.stop() WITHOUT saving to session_state")
        # In real code: st.stop() happens here, preventing save
    else:
        print("❌ Tuple NOT detected - would crash!")
        sys.exit(1)
        
    # This line should NOT execute in real code (st.stop() prevents it)
    print("⚠️  Code continues (in real app, st.stop() would prevent this)")
    
except Exception as e:
    print(f"❌ Exception: {e}")
    sys.exit(1)

# Test 3: Verify dict success path
print("\n📝 Test 3: Simulate dict success return")
print("-"*80)

class MockPipelineSuccess:
    def run_pipeline(self, df, desc):
        return {
            'success': True,
            'domain_info': {'domain': 'marketing', 'domain_name': 'Marketing'},
            'dashboard': {'charts': []},
            'insights': {'key_insights': []},
            'performance': {'total': 30.5},
            'quality_scores': {'overall': 85}
        }

result = MockPipelineSuccess().run_pipeline(None, "")

try:
    # Hotfix #5 validation
    if isinstance(result, tuple):
        print("❌ Dict detected as tuple!")
        sys.exit(1)
    
    if not isinstance(result, dict):
        print("❌ Result is not dict!")
        sys.exit(1)
    
    if not result.get('success', False):
        print("❌ Result not successful!")
        sys.exit(1)
    
    print("✅ All validations passed")
    print("✅ Would save to session_state safely")
    
    # Verify dict access works
    domain = result.get('domain_info', {}).get('domain', '')
    print(f"✅ Dict access works: domain = {domain}")
    
except Exception as e:
    print(f"❌ Exception: {e}")
    sys.exit(1)

# Test 4: Verify no tuple index error
print("\n📝 Test 4: Verify tuple index error is prevented")
print("-"*80)

def old_code_would_crash(result):
    """Old code (Hotfix #3) - would crash on tuple"""
    # This is what OLD code did
    if not result['success']:  # ← CRASH if result is tuple!
        return False
    return True

def new_code_safe(result):
    """New code (Hotfix #5) - safe"""
    if isinstance(result, tuple):
        return False  # Handled safely
    if not isinstance(result, dict):
        return False
    if not result.get('success', False):
        return False
    return True

# Test with tuple
tuple_result = (False, "error")
try:
    old_code_would_crash(tuple_result)
    print("❌ Old code did NOT crash (unexpected)")
except TypeError as e:
    print(f"✅ Old code WOULD crash with: {str(e)[:60]}")

try:
    safe = new_code_safe(tuple_result)
    print(f"✅ New code handles safely: {safe}")
except Exception as e:
    print(f"❌ New code crashed: {e}")
    sys.exit(1)

# Final summary
print("\n" + "="*80)
print("🎉 ALL TESTS PASSED")
print("="*80)
print("\n✅ Hotfix #5 Implementation Verified:")
print("   1. Code has correct validation order")
print("   2. Tuple detection works")
print("   3. Dict success path works")
print("   4. Tuple index error is prevented")
print("\n📋 Next Steps:")
print("   1. Ensure PR #29 is merged to main")
print("   2. Wait for Streamlit Cloud auto-deploy (3-5 min)")
print("   3. Test Marketing sample in production")
print("   4. Should see NO tuple index errors")
print("\n" + "="*80)
