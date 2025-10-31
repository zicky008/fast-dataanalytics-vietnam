#!/usr/bin/env python3
"""
Session Resumption Helper
Automatically loads context and displays current status
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

def load_checkpoint() -> Dict[str, Any]:
    """Load current session checkpoint"""
    checkpoint_file = Path(__file__).parent / "SESSION_CHECKPOINT.json"
    
    if not checkpoint_file.exists():
        print("❌ SESSION_CHECKPOINT.json not found!")
        sys.exit(1)
    
    with open(checkpoint_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def display_context(checkpoint: Dict[str, Any]) -> None:
    """Display current project context"""
    
    print("=" * 80)
    print("🧠 SESSION CONTEXT RESUME")
    print("=" * 80)
    print()
    
    # Project Overview
    print("📋 PROJECT OVERVIEW")
    print(f"  Name: {checkpoint['project_name']}")
    print(f"  Owner: {checkpoint['owner']}")
    print(f"  Last Updated: {checkpoint['last_updated']}")
    print()
    
    # Current Status
    status = checkpoint['current_status']
    print("📍 CURRENT STATUS")
    print(f"  Phase: {status['phase']}")
    print(f"  Week: {status['week']}")
    print(f"  Day: {status['day']}")
    print(f"  Task: {status['task']}")
    print(f"  Status: {status['status']}")
    print(f"  Progress: {status['progress_percentage']}%")
    print()
    
    # Core Constraints
    print("⚠️  CORE CONSTRAINTS")
    constraints = checkpoint['core_constraints']
    for key, value in constraints.items():
        print(f"  • {key.replace('_', ' ').title()}: {value}")
    print()
    
    # WrenAI Patterns Status
    print("🎨 WRENAI PATTERNS STATUS")
    patterns = checkpoint['wrenai_patterns_adopted']
    for pattern_name, pattern_info in patterns.items():
        status_emoji = "✅" if pattern_info['status'] == "COMPLETED" else "⏳" if pattern_info['status'] == "IN_PROGRESS" else "⬜"
        priority_emoji = "🔴" if pattern_info['priority'] == "CRITICAL" else "🟡" if pattern_info['priority'] == "HIGH" else "🟢"
        print(f"  {status_emoji} {priority_emoji} {pattern_name.replace('_', ' ').title()}")
        print(f"     Tech: {pattern_info['tech']}")
        print(f"     Week: {pattern_info['week']} | Expected: {pattern_info['expected_outcome']}")
    print()
    
    # Tech Stack Decisions
    print("⚙️  TECH STACK DECISIONS")
    tech_stack = checkpoint['tech_stack_decisions']
    print("  ✅ USE:")
    for tech in tech_stack['use']:
        print(f"     • {tech}")
    print("  ❌ SKIP:")
    for tech in tech_stack['skip']:
        print(f"     • {tech}")
    print("  ⏳ LATER:")
    for tech in tech_stack['later']:
        print(f"     • {tech}")
    print()
    
    # Current Week Tasks
    current_week = f"week_{status['week']}_2" if status['week'] == 1 else f"week_{status['week']}"
    if current_week in checkpoint['roadmap']:
        week_info = checkpoint['roadmap'][current_week]
        print(f"📅 CURRENT WEEK TASKS - {week_info['phase']}")
        print(f"  Investment: {week_info['investment']}")
        print(f"  Expected: {week_info['expected_outcome']}")
        print()
        
        for task in week_info['tasks']:
            status_emoji = "✅" if task['status'] == "COMPLETED" else "🔄" if task['status'] == "IN_PROGRESS" else "⬜"
            print(f"  {status_emoji} Day {task['day']}: {task['name']}")
            print(f"     Hours: {task['hours']} | Deliverable: {task['deliverable']}")
            
            if task['status'] == 'NOT_STARTED' and task['day'] == f"{status['day']}-{status['day']+1}":
                print("     👉 THIS IS YOUR NEXT TASK!")
                print("     Success Criteria:")
                for criterion in task.get('success_criteria', []):
                    print(f"       • {criterion}")
        print()
    
    # ROI Summary
    print("💰 ROI SUMMARY")
    roi = checkpoint['roi_calculation']
    print(f"  Total Investment: {roi['total_investment']}")
    print(f"  3-Month Revenue: {roi['total_3_month_revenue']}")
    print(f"  Net Profit: {roi['net_profit']}")
    print(f"  ROI: {roi['roi_percentage']}")
    print(f"  Annual (with network effects): {roi['with_network_effects']['annual_roi']}")
    print()
    
    # Documents to Read
    print("📚 DOCUMENTS TO READ")
    docs = checkpoint['documents_to_read']
    print("  Priority 1 (Always Read):")
    for doc in docs['priority_1_always_read']:
        print(f"    • {doc}")
    print("  Priority 2 (Strategic):")
    for doc in docs['priority_2_strategic']:
        print(f"    • {doc}")
    print()
    
    # Critical Warnings
    print("🚨 CRITICAL WARNINGS")
    warnings = checkpoint['critical_warnings']
    print("  ❌ DO NOT:")
    for warning in warnings['do_not']:
        print(f"     • {warning}")
    print("  ✅ MUST DO:")
    for must_do in warnings['must_do']:
        print(f"     • {must_do}")
    print()
    
    # Next Session Instructions
    print("🔄 NEXT SESSION INSTRUCTIONS")
    instructions = checkpoint['next_session_instructions']
    for step_key in sorted([k for k in instructions.keys() if k.startswith('step_')]):
        print(f"  {instructions[step_key]}")
    print()
    
    # User Confirmation
    print("=" * 80)
    print("✅ USER CONFIRMATION NEEDED")
    print("=" * 80)
    confirmations = checkpoint['user_confirmation_needed']
    for question_key in sorted([k for k in confirmations.keys() if k.startswith('question_')]):
        print(f"  {confirmations[question_key]}")
    print()
    
    print("=" * 80)
    print("🚀 IF ALL CONFIRMED → READY TO START IMPLEMENTATION!")
    print("=" * 80)

def update_checkpoint(updates: Dict[str, Any]) -> None:
    """Update checkpoint with new status"""
    checkpoint_file = Path(__file__).parent / "SESSION_CHECKPOINT.json"
    
    with open(checkpoint_file, 'r', encoding='utf-8') as f:
        checkpoint = json.load(f)
    
    # Update timestamp
    checkpoint['last_updated'] = datetime.utcnow().isoformat() + 'Z'
    
    # Apply updates
    for key, value in updates.items():
        if '.' in key:  # Nested key (e.g., "current_status.task")
            keys = key.split('.')
            target = checkpoint
            for k in keys[:-1]:
                target = target[k]
            target[keys[-1]] = value
        else:
            checkpoint[key] = value
    
    # Save updated checkpoint
    with open(checkpoint_file, 'w', encoding='utf-8') as f:
        json.dump(checkpoint, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Checkpoint updated: {checkpoint_file}")

def main():
    """Main entry point"""
    
    if len(sys.argv) > 1 and sys.argv[1] == "--update":
        # Update mode
        if len(sys.argv) < 4:
            print("Usage: python resume_session.py --update key value")
            print("Example: python resume_session.py --update current_status.task 'Visual Hierarchy CSS'")
            sys.exit(1)
        
        key = sys.argv[2]
        value = sys.argv[3]
        
        # Try to parse as JSON if it looks like a JSON value
        try:
            if value.lower() in ['true', 'false']:
                value = value.lower() == 'true'
            elif value.isdigit():
                value = int(value)
            elif value.replace('.', '', 1).isdigit():
                value = float(value)
        except:
            pass
        
        update_checkpoint({key: value})
    else:
        # Display mode (default)
        checkpoint = load_checkpoint()
        display_context(checkpoint)

if __name__ == "__main__":
    main()
