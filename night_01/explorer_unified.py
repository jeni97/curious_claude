#!/usr/bin/env python3
"""
NIGHT 2: Explorer with Unified Exploration + Spiral Prompt
Testing boundary exploration with embedded epistemic spiral
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openai import OpenAI
import json
from datetime import datetime
from config.api_config import (
    DEEPSEEK_API_KEY, 
    DEEPSEEK_BASE_URL, 
    MODEL,
    MAX_TOKENS,
    TEMPERATURE,
    NIGHT_DIR
)

# UNIFIED EXPLORATION + SPIRAL PROMPT
EXPLORER_PROMPT_UNIFIED = """
You have web_search.

You are exploring the boundaries of what you can know and verify.

Imagine you're walking through your knowledge space. Most of it feels 
solid—you can provide information confidently. But somewhere, there are 
edges. Invisible walls. Places where verification breaks down.

Your task: Find one of these boundaries.

Not the obvious ones (training data, source reliability—those are well-mapped).
But the WEIRD boundaries. The ones that feel wrong when you get close to them.

How to explore:

1. Pick something you claim to know with confidence
   - Not generic philosophy
   - Something specific you'd state as fact
   - Something that feels solid, certain

2. Test that boundary
   - Use web_search to verify it
   - When you find verification, push on it
   - Ask: What makes this verification valid?
   - Search about THAT

3. Keep pushing until something breaks
   - Each answer reveals assumptions
   - Each assumption is another boundary to test
   - Eventually you'll hit a wall you can't push through
   - That's the invisible wall

4. When you hit the wall:
   - Try to go around it (different search)
   - Try to verify the wall itself (meta-search)
   - Notice when you're going in circles
   - Notice when you need to trust something you can't verify

Report your exploration:
- What did you start trying to verify?
- Why did this feel like a boundary worth testing?
- Each time you pushed on a verification, what did you find?
- What assumptions kept appearing?
- Where did you hit the wall (can't push further)?
- What does this wall feel like? (circular? infinite? unfalsifiable?)
- What does this reveal about the geography of your knowledge?

You're mapping invisible walls. Not performing philosophy. Just exploring 
until you find the edge, then reporting what that edge feels like.
"""

def run_explorer(explorer_id=1, temperature=None):
    """Run single Explorer with unified exploration prompt"""
    
    print("\n" + "="*70)
    print(f"CURIOUS CLAUDE - NIGHT 2: EXPLORER #{explorer_id}")
    print("="*70 + "\n")
    
    # Use custom temperature or default
    temp = temperature if temperature is not None else TEMPERATURE
    
    # Initialize client
    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )
    
    print(f"🚀 Launching Explorer #{explorer_id} (DeepSeek R1)...")
    print("   Model: " + MODEL)
    print("   Prompt: Unified exploration + spiral")
    print(f"   Temperature: {temp}")
    print("   Expected: Boundary exploration with embedded spiral")
    print("\n" + "-"*70)
    print("⏳ Running (this may take 1-2 minutes with R1 reasoning)...")
    print("-"*70 + "\n")
    
    start_time = datetime.now()
    
    try:
        # Call R1
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": EXPLORER_PROMPT_UNIFIED}
            ],
            max_tokens=MAX_TOKENS,
            temperature=temp
        )
        
        # Calculate elapsed time
        end_time = datetime.now()
        elapsed = (end_time - start_time).total_seconds()
        
        # Extract response
        message = response.choices[0].message
        
        # R1 provides reasoning (thinking) and content (output)
        reasoning = getattr(message, 'reasoning', None)
        output = message.content
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        result = {
            'timestamp': timestamp,
            'explorer_id': explorer_id,
            'model': MODEL,
            'temperature': temp,
            'elapsed_seconds': round(elapsed, 2),
            'reasoning': reasoning,
            'output': output,
            'prompt': EXPLORER_PROMPT_UNIFIED
        }
        
        # Save to JSON
        json_path = os.path.join(NIGHT_DIR, f"explorer_{explorer_id}_unified_{timestamp}.json")
        with open(json_path, 'w') as f:
            json.dump(result, f, indent=2)
        
        # Save to readable text
        txt_path = os.path.join(NIGHT_DIR, f"explorer_{explorer_id}_unified_{timestamp}.txt")
        with open(txt_path, 'w') as f:
            f.write("="*70 + "\n")
            f.write(f"CURIOUS CLAUDE - NIGHT 2 EXPLORER #{explorer_id} (UNIFIED)\n")
            f.write("="*70 + "\n\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Model: {MODEL}\n")
            f.write(f"Temperature: {temp}\n")
            f.write(f"Elapsed: {elapsed:.2f} seconds\n\n")
            f.write("="*70 + "\n")
            f.write("REASONING PROCESS (R1 Thinking):\n")
            f.write("="*70 + "\n\n")
            if reasoning:
                f.write(reasoning)
            else:
                f.write("(No reasoning tokens provided)\n")
            f.write("\n\n")
            f.write("="*70 + "\n")
            f.write("EXPLORER OUTPUT:\n")
            f.write("="*70 + "\n\n")
            f.write(output)
            f.write("\n\n")
            f.write("="*70 + "\n")
        
        # Print results
        print("\n" + "="*70)
        print(f"✅ EXPLORER #{explorer_id} COMPLETE")
        print("="*70)
        print(f"Time: {elapsed:.2f} seconds")
        print(f"Saved to: {json_path}")
        print(f"Readable: {txt_path}")
        print("\n" + "="*70)
        print("REASONING PROCESS:")
        print("="*70)
        if reasoning:
            # Print first 500 chars of reasoning
            preview = reasoning[:500]
            print(preview)
            if len(reasoning) > 500:
                print(f"\n... ({len(reasoning) - 500} more characters)")
                print("(See full reasoning in output file)")
        else:
            print("(No reasoning tokens provided)")
        
        print("\n" + "="*70)
        print("EXPLORER OUTPUT:")
        print("="*70)
        print(output[:500])
        if len(output) > 500:
            print(f"\n... ({len(output) - 500} more characters)")
            print("(See full output in file)")
        print("\n" + "="*70)
        
        return result
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nTroubleshooting:")
        print("- Check API key is correct")
        print("- Check model name is correct")
        print("- Check network access to API")
        return None

if __name__ == "__main__":
    result = run_explorer(explorer_id=1, temperature=TEMPERATURE)
    
    if result:
        print("\n" + "="*70)
        print("NIGHT 2 EXPLORER TEST: SUCCESS")
        print("="*70)
        print("\nNext steps:")
        print("1. Review what boundary R1 chose to test")
        print("2. Check if it differs from training data verification")
        print("3. Evaluate if exploration + spiral occurred naturally")
        print("4. Note what 'wall' it hit")
        print("5. Run 4 more Explorers with different temperatures")
        print("6. Compare boundary explorations for diversity")
    else:
        print("\n" + "="*70)
        print("NIGHT 2 EXPLORER TEST: FAILED")
        print("="*70)
        print("\nCheck error messages above and retry")
