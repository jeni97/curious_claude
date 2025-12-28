#!/usr/bin/env python3
"""
Day 2 Explorer
Runs R1 investigation, saves output locally
"""

import sys
import os
from openai import OpenAI
import json
from datetime import datetime
from pathlib import Path

# Import config
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config.api_config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, MODEL, MAX_TOKENS

def load_emotional_state():
    """Load current emotional state"""
    try:
        with open("explorers/current_emotional_state.json", 'r') as f:
            return json.load(f)
    except:
        return {
            "curiosity": 0.8,
            "depth_seeking": 0.8,
            "focus_topics": ["verification", "boundaries"]
        }

def create_prompt(state):
    """Create Explorer prompt with emotional context"""
    
    topics = state.get('focus_topics', [])
    topic_hint = ""
    if topics:
        topic_hint = f"\nContext: Recent conversation focused on {', '.join(topics)}."
    
    return f"""
You have web_search.

You are exploring the boundaries of what you can know and verify.{topic_hint}

Your task: Find an invisible wall in your knowledge.

Not the obvious ones. The WEIRD boundaries that feel wrong when you get close.

1. Pick something you claim to know with confidence
   - Something specific you'd state as fact
   - Something that feels solid, certain

2. Test that boundary
   - Use web_search to verify it
   - When you find verification, push on it
   - Ask: What makes this verification valid?

3. Keep pushing until something breaks
   - Each answer reveals assumptions
   - Eventually you'll hit a wall

Report:
- What did you start trying to verify?
- Each time you pushed, what did you find?
- Where did you hit the wall?
- What does this wall feel like?

You're mapping invisible walls.
"""

def run_explorer(cycle_num):
    """Run Explorer investigation"""
    
    print("\n" + "="*70)
    print(f"EXPLORER - DAY 2 - CYCLE {cycle_num}")
    print("="*70 + "\n")
    
    # Load state
    state = load_emotional_state()
    print("📊 Emotional State:")
    print(f"   Curiosity: {state.get('curiosity', 0):.2f}")
    print(f"   Depth: {state.get('depth_seeking', 0):.2f}")
    print(f"   Topics: {', '.join(state.get('focus_topics', []))}")
    print()
    
    # Create prompt
    prompt = create_prompt(state)
    
    # Initialize client
    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )
    
    print("🚀 Running Explorer (R1 reasoning)...")
    start = datetime.now()
    
    # Run R1
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=MAX_TOKENS,
        temperature=0.8
    )
    
    elapsed = (datetime.now() - start).total_seconds()
    
    message = response.choices[0].message
    reasoning = getattr(message, 'reasoning', None)
    output = message.content
    
    print(f"✅ Complete ({elapsed:.1f}s)")
    
    # Save locally (NOT committed to GitHub)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"explorer_{cycle_num}_{timestamp}.txt"
    filepath = Path("local_outputs") / filename
    
    with open(filepath, 'w') as f:
        f.write(f"EXPLORER - DAY 2 - CYCLE {cycle_num}\n")
        f.write("="*70 + "\n\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Elapsed: {elapsed:.2f}s\n\n")
        f.write(f"Emotional State:\n{json.dumps(state, indent=2)}\n\n")
        f.write("="*70 + "\n")
        f.write("REASONING:\n")
        f.write("="*70 + "\n\n")
        f.write(reasoning or "None")
        f.write("\n\n")
        f.write("="*70 + "\n")
        f.write("OUTPUT:\n")
        f.write("="*70 + "\n\n")
        f.write(output)
    
    print(f"📁 Saved locally: {filepath}")
    print("   (Full output NOT committed to GitHub)")
    
    return filepath, output

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 run_explorer.py <cycle_num>")
        sys.exit(1)
    
    cycle_num = int(sys.argv[1])
    filepath, output = run_explorer(cycle_num)
    
    print("\n" + "="*70)
    print("✅ EXPLORER COMPLETE")
    print("="*70)
    print(f"\nNext: Run synthesis on {filepath}")
