#!/usr/bin/env python3
"""
PROOF OF CONCEPT LOOP
Single Explorer that commits to GitHub for background synthesis
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openai import OpenAI
import json
import subprocess
from datetime import datetime
from pathlib import Path
from config.api_config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, MODEL, MAX_TOKENS

class ProofOfConceptLoop:
    def __init__(self):
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL
        )
        self.output_dir = Path("loop_outputs")
        self.output_dir.mkdir(exist_ok=True)
    
    def load_emotional_state(self):
        """Load current emotional state"""
        state_file = Path("explorers/current_emotional_state.json")
        
        if state_file.exists():
            with open(state_file, 'r') as f:
                return json.load(f)
        else:
            return {
                "curiosity": 0.8,
                "urgency": 0.5,
                "depth_seeking": 0.8,
                "focus_topics": ["verification", "boundaries"]
            }
    
    def create_prompt(self, state):
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
    
    def run_explorer(self, cycle_num):
        """Run one Explorer cycle"""
        
        print("\n" + "="*70)
        print(f"PROOF OF CONCEPT LOOP - CYCLE {cycle_num}")
        print("="*70 + "\n")
        
        # Load state
        state = self.load_emotional_state()
        print("📊 Emotional State:")
        print(f"   Curiosity: {state.get('curiosity', 0):.2f}")
        print(f"   Depth: {state.get('depth_seeking', 0):.2f}")
        print(f"   Topics: {', '.join(state.get('focus_topics', []))}")
        print()
        
        # Create prompt
        prompt = self.create_prompt(state)
        
        # Run Explorer
        print("🚀 Running Explorer...")
        start = datetime.now()
        
        response = self.client.chat.completions.create(
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
        
        # Save locally
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"loop_cycle_{cycle_num}_{timestamp}.txt"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            f.write(f"PROOF OF CONCEPT LOOP - CYCLE {cycle_num}\n")
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
        
        return filepath, output[:500]
    
    def commit_to_github(self, filepath):
        """Commit Explorer output to GitHub"""
        
        print("\n📤 Committing to GitHub...")
        
        try:
            subprocess.run(['git', 'add', str(filepath)], check=True)
            subprocess.run([
                'git', 'commit', '-m',
                f'Loop cycle: {filepath.name}'
            ], check=True)
            subprocess.run(['git', 'push'], check=True)
            
            print("✅ Pushed to GitHub")
            print(f"\nBackground script will detect this in ~30 seconds...")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Git error: {e}")
            return False

def run_single_cycle(cycle_num=1):
    """Run one complete cycle"""
    
    loop = ProofOfConceptLoop()
    
    # Run Explorer
    filepath, preview = loop.run_explorer(cycle_num)
    
    print("\n📄 Output Preview:")
    print("-"*70)
    print(preview)
    print("...")
    print("-"*70)
    
    # Commit to GitHub
    success = loop.commit_to_github(filepath)
    
    if success:
        print("\n" + "="*70)
        print("✅ CYCLE COMPLETE")
        print("="*70)
        print("\nBackground synthesis script will:")
        print("  1. Detect new file on GitHub (~30 sec)")
        print("  2. Auto-synthesize")
        print("  3. Set alert flag")
        print("\nThen message Claude anything to trigger auto-check!")
    else:
        print("\n❌ GitHub commit failed - check git status")

if __name__ == "__main__":
    cycle_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    run_single_cycle(cycle_num)
