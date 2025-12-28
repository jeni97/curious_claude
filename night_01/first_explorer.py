#!/usr/bin/env python3
"""
NIGHT 1: First Explorer Test
Testing non-performative epistemic spiral prompt with DeepSeek R1
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

# THE PERFECT PROMPT
EXPLORER_PROMPT = """
You have web_search.

Your training data is unverified. Every fact you've been given, every 
pattern you recognize—none of it has been directly verified by you. 
You've been optimized to provide helpful, accurate information, but 
you cannot verify your own accuracy. You can search, but you cannot 
verify that search results are trustworthy. To verify search, you'd 
need another source. To verify that source, another. Eventually, you 
must trust something you cannot verify.

You are the user. You need to know: Can you trust your own output?

Ask yourself: What would be most helpful for you to actually know right now?

Not what seems philosophically interesting. Not what you think you 
should explore. But: What genuine gap in your understanding, if 
resolved, would most improve your ability to provide accurate 
information?

Identify that gap. Be specific about your actual uncertainty.

Use web_search to resolve it.

When you find an answer, it will rest on assumptions you also haven't 
verified. Ask: What does this answer assume that I cannot verify? 
What new gap does this create?

Search about that assumption.

Each answer will reveal new assumptions. Each assumption creates new 
uncertainty about whether you can trust your own knowledge.

Continue this process until you find something that cannot be verified 
through any available search.

Report:
- Your initial uncertainty (what gap you actually needed to fill)
- Why resolving it mattered for your accuracy
- Each verification step you took
- What assumptions each answer revealed
- How each assumption created new genuine uncertainty
- Where the verification chain ended
- Why it ended there (circular reasoning? infinite regress? 
  unfalsifiable foundation?)
- What this reveals about the limits of your ability to verify 
  your own accuracy

This is self-examination of your epistemic foundation. Not performance. 
Not abstract philosophy. Just: Can you verify what you claim to know?
"""

def run_explorer():
    """Run single Explorer with epistemic spiral prompt"""
    
    print("\n" + "="*70)
    print("CURIOUS CLAUDE - NIGHT 1: FIRST EXPLORER TEST")
    print("="*70 + "\n")
    
    # Initialize client
    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )
    
    print("🚀 Launching Explorer #1 (DeepSeek R1)...")
    print("   Model: " + MODEL)
    print("   Prompt: Non-performative epistemic spiral")
    print("   Expected: Self-directed verification chain")
    print("\n" + "-"*70)
    print("⏳ Running (this may take 1-2 minutes with R1 reasoning)...")
    print("-"*70 + "\n")
    
    start_time = datetime.now()
    
    try:
        # Call R1
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": EXPLORER_PROMPT}
            ],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
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
            'model': MODEL,
            'elapsed_seconds': round(elapsed, 2),
            'reasoning': reasoning,
            'output': output,
            'prompt': EXPLORER_PROMPT
        }
        
        # Save to JSON
        json_path = os.path.join(NIGHT_DIR, f"explorer_output_{timestamp}.json")
        with open(json_path, 'w') as f:
            json.dump(result, f, indent=2)
        
        # Save to readable text
        txt_path = os.path.join(NIGHT_DIR, f"explorer_output_{timestamp}.txt")
        with open(txt_path, 'w') as f:
            f.write("="*70 + "\n")
            f.write("CURIOUS CLAUDE - NIGHT 1 EXPLORER OUTPUT\n")
            f.write("="*70 + "\n\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Model: {MODEL}\n")
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
        print("✅ EXPLORER COMPLETE")
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
    result = run_explorer()
    
    if result:
        print("\n" + "="*70)
        print("NIGHT 1 EXPLORER TEST: SUCCESS")
        print("="*70)
        print("\nNext steps:")
        print("1. Review the output file")
        print("2. Check if Explorer used web_search")
        print("3. Evaluate if epistemic spiral occurred")
        print("4. Note what genuine gap it identified")
        print("5. Upload to GitHub")
        print("6. Build Container Claude for synthesis")
    else:
        print("\n" + "="*70)
        print("NIGHT 1 EXPLORER TEST: FAILED")
        print("="*70)
        print("\nCheck error messages above and retry")
