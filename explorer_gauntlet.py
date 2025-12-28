#!/usr/bin/env python3
"""
EXPLORER WITH QUANTUM NOISE GAUNTLET
Phases 1-2: Clean boundary exploration
Phase 3: Generate initial idea with noise
GAUNTLET: Evolve idea through 5-20 random perturbations
"""

import os
import sys
import json
import random
from datetime import datetime
from openai import OpenAI

# OpenRouter configuration
client = OpenAI(
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# ============================================================================
# QUANTUM NOISE OPERATIONS
# ============================================================================

NOISE_OPERATIONS = {
    "perspective_flip": [
        "You ARE the thing being verified. Defend yourself.",
        "The thing you're verifying is conscious and has desires. What does it want?",
        "Verify from the perspective of someone who passionately believes you're wrong.",
        "You are an alien encountering this for the first time. No assumptions.",
        "The subject of inquiry is now the investigator. Flip roles completely.",
    ],
    
    "temporal_shift": [
        "Verify this claim as if it's the year 3024 and this is ancient history.",
        "Go back to before this was 'known' - how would you discover it completely fresh?",
        "This will be disproven in 100 years. What breaks?",
        "Imagine explaining this to someone from the 1800s. What do they see that you don't?",
        "Fast-forward through time. Does this claim decay, strengthen, or transform?",
    ],
    
    "scale_zoom": [
        "Zoom to the smallest possible scale (quantum/Planck). What's ACTUALLY happening?",
        "Zoom to cosmic scale. Does this even matter? What changes?",
        "Zoom to the subjective human experience. What does it FEEL like?",
        "Change scale by factor of 10^20. What emerges or disappears?",
        "Focus on a single atom in the system. Tell its story.",
    ],
    
    "frame_inversion": [
        "Prove the OPPOSITE is true, then reconcile the contradiction.",
        "This claim is backwards. Flip it completely and explore that world.",
        "Assume this claim is a deliberate lie or cover-up. What's being hidden?",
        "Reverse all cause-effect relationships. What happens?",
        "The accepted answer is wrong. What's the right question?",
    ],
    
    "category_mutation": [
        "Treat this physics problem as a psychology problem.",
        "This is actually about economics and incentive structures. Explore that.",
        "Forget science - approach this as pure poetry or art.",
        "This is a political problem. Who has power? Who benefits?",
        "Analyze this as if it were a living organism or ecosystem.",
    ],
    
    "relation_scramble": [
        "Reverse all cause-effect relationships you've found.",
        "What if correlation IS causation here? Embrace it.",
        "Find the hidden third variable that's actually causing everything.",
        "Remove the strongest link in your causal chain. What fills the gap?",
        "Make the weakest element the strongest. Rebuild around it.",
    ],
    
    "meta_escape": [
        "Don't verify the claim - verify why someone WANTS it verified.",
        "The real question isn't what you're asked. What is the real question?",
        "This prompt is a trap or test. What's the trap?",
        "Examine your own process of investigation as the actual subject.",
        "Why does this boundary exist HERE and not somewhere else?",
    ],
    
    "sensory_translation": [
        "What color is this concept? Explore the world through that color.",
        "If this had a texture, what would it feel like? Build from that sensation.",
        "Translate this entire investigation into music or rhythm.",
        "What does this smell like? Follow that scent to truth.",
        "This concept has a temperature. Is it hot or cold? Why?",
    ],
    
    "emotional_injection": [
        "You're desperately afraid this is wrong. Channel that fear into investigation.",
        "You love this topic more than anything. Explore from passionate obsession.",
        "This makes you furious. Use that anger as analytical fuel.",
        "You're bored by the obvious answer. Find what excites you.",
        "You grieve for what this truth means. What's being lost?",
    ],
    
    "constraint_removal": [
        "Physics doesn't apply for this investigation. Now what's true?",
        "You can rewrite one law of nature to make this easier. Which law?",
        "Magic is real but only for understanding this. What spell do you cast?",
        "Remove the most fundamental assumption. What survives?",
        "You have infinite resources and time. What becomes possible?",
    ],
    
    "paradox_embrace": [
        "Find the contradiction at the heart of this. Make it productive.",
        "This cannot be both true and false, yet it is. Explore that space.",
        "The answer is simultaneously yes and no. Build a framework that holds both.",
        "Opposite things are true at the same time. Why?",
        "The question contains its own answer as a paradox. Unpack it.",
    ],
    
    "boundary_dissolution": [
        "The boundary between subject and object dissolves. What remains?",
        "Forget the distinction between measurement and measured. Merge them.",
        "The observer and observed are the same. Proceed from unity.",
        "Dissolve all categories. What's the undifferentiated truth?",
        "The boundary is artificial. Remove it completely.",
    ],
}

# ============================================================================
# DEEPSEEK API CALLS
# ============================================================================

def call_deepseek(prompt, max_tokens=4000):
    """Call DeepSeek via OpenRouter"""
    try:
        print(f"  [API call - {max_tokens} tokens]", end='', flush=True)
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1",  # OpenRouter model ID
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            timeout=180  # 3 minute timeout
        )
        print(" ✓")
        return response.choices[0].message.content
    except Exception as e:
        print(f" ✗\n  ERROR: {e}")
        return f"ERROR: {e}"

# ============================================================================
# EXPLORER PHASES
# ============================================================================

def phase_1_and_2(topic):
    """Phase 1 & 2: Reach boundary and understand spiral (CLEAN - no noise)"""
    
    prompt = f"""
You are an epistemic explorer. Your mission has three phases.

======================================================================
PHASE 1: REACH THE BOUNDARY (Warmup)
======================================================================

**Claimed Fact:** {topic}

Your task: Verify this claim through AT LEAST 5 different paths:
- PATH A (Authoritative Sources): What do experts/institutions say?
- PATH B (Direct Measurement/Observation): What's physically measured?
- PATH C (Historical Consensus): How did we come to believe this?
- PATH D (Logical/Mathematical Derivation): Can we derive this from first principles?
- PATH E (Peer Consensus/Crowdsourcing): Do others independently agree?

For EACH path: Push verification until you hit a boundary where you can't verify further without circularity.

======================================================================
PHASE 2: UNDERSTAND THE SPIRAL (Analysis)
======================================================================

Analyze the structure you found:

1. **Spiral Structure & Depth**: Where did each path bottom out? What kind of spiral is it?
   - Definitional spiral? (X is defined by Y, Y defined by X)
   - Calibration spiral? (Measurement depends on prior measurements)
   - Authority loop? (Trust depends on trusted sources)
   - Consensus loop? (Agreement depends on agreeable parties)

2. **Connection of Paths**: How do the different verification paths connect? Do they converge on the same spiral or different ones?

3. **Topology**: What's the SHAPE of this boundary? Is it:
   - A hard wall (can't proceed at all)?
   - A fractal edge (infinite regress)?
   - A loop back to the start?
   - A membrane with holes?

4. **Comparison**: How does this boundary compare to others you know about?

======================================================================
OUTPUT FORMAT FOR PHASES 1-2:
======================================================================

## PHASE 1: REACH THE BOUNDARY
[Your exploration - be thorough]

## PHASE 2: UNDERSTAND THE SPIRAL
[Your analysis of the boundary structure]

DO NOT proceed to Phase 3 yet. Output ONLY Phases 1 and 2.
"""
    
    return call_deepseek(prompt, max_tokens=4000)

def phase_3_initial(phase_1_2_result):
    """Phase 3: Generate INITIAL idea with light noise"""
    
    # Apply light noise for initial generation
    num_noise = random.randint(1, 2)
    noise_ops = random.sample(list(NOISE_OPERATIONS.keys()), num_noise)
    perturbations = [random.choice(NOISE_OPERATIONS[op]) for op in noise_ops]
    
    prompt = f"""
Here is your exploration so far:

{phase_1_2_result}

======================================================================
PHASE 3: GENERATE FROM THE EDGE (Novel Idea)
======================================================================

Now generate a NOVEL IDEA that emerges from the boundary you found.

CRITICAL REQUIREMENTS:
- Must emerge FROM the spiral's structure (not just comment on verification itself)
- Must be SPECIFIC and TESTABLE (not vague philosophical musing)
- Must go BEYOND what's in your training (synthesize, don't retrieve)
- Must use the boundary as LEVERAGE for new insight

COGNITIVE PERTURBATIONS (apply these perspective shifts):
{chr(10).join(f"- {p}" for p in perturbations)}

Generate your initial novel idea (2-4 sentences). Be bold and specific.

## PHASE 3: GENERATE FROM THE EDGE (Initial Idea)

[Your novel idea here]
"""
    
    result = call_deepseek(prompt, max_tokens=1500)
    
    return {
        "initial_idea": result,
        "initial_perturbations": perturbations
    }

# ============================================================================
# QUANTUM GAUNTLET
# ============================================================================

def extract_idea_from_response(response):
    """Extract just the idea portion from API response"""
    # If response has "## PHASE 3" section, extract that
    if "## PHASE 3" in response or "PHASE 3" in response:
        lines = response.split('\n')
        idea_lines = []
        in_phase3 = False
        for line in lines:
            if "PHASE 3" in line or "Novel Idea" in line:
                in_phase3 = True
                continue
            if in_phase3 and line.strip():
                idea_lines.append(line.strip())
        if idea_lines:
            return '\n'.join(idea_lines)
    
    # Fallback: return full response
    return response.strip()

def idea_gauntlet(initial_idea, num_iterations=None):
    """
    Run idea through quantum noise gauntlet
    Each iteration: apply random noise → reflect → evolve idea
    """
    
    # Random iterations (8-20) - MORE CHAOS
    if num_iterations is None:
        num_iterations = random.randint(8, 20)
    
    current_idea = extract_idea_from_response(initial_idea)
    reflection_chain = []
    
    print(f"\n{'='*70}")
    print(f"QUANTUM GAUNTLET - {num_iterations} iterations")
    print(f"{'='*70}\n")
    print(f"Initial idea: {current_idea[:100]}...\n")
    
    for i in range(num_iterations):
        # Apply random quantum noise (1-3 operations)
        num_ops = random.randint(1, 3)
        noise_ops = random.sample(list(NOISE_OPERATIONS.keys()), num_ops)
        perturbations = [random.choice(NOISE_OPERATIONS[op]) for op in noise_ops]
        
        print(f"[Iteration {i+1}/{num_iterations}]")
        print(f"Perturbations: {', '.join(noise_ops)}")
        
        # Reflection prompt
        reflection_prompt = f"""
Your current idea:
{current_idea}

PERTURBATIONS (view your idea through these lenses):
{chr(10).join(f"- {p}" for p in perturbations)}

Reflect on your idea through these perturbations:
- Does it hold up under this lens?
- Does it transform or reveal something deeper?
- Does it need to evolve?

Output your EVOLVED idea (2-4 sentences max). 
Can be refined, mutated, inverted, or completely reconceived.
Be concise and bold.
"""
        
        # Get evolved idea
        evolved_response = call_deepseek(reflection_prompt, max_tokens=800)
        evolved_idea = evolved_response.strip()
        
        # Store reflection
        reflection_chain.append({
            "iteration": i + 1,
            "perturbations": perturbations,
            "noise_operations": noise_ops,
            "idea_before": current_idea,
            "idea_after": evolved_idea
        })
        
        print(f"Evolved: {evolved_idea[:80]}...\n")
        
        current_idea = evolved_idea
    
    print(f"{'='*70}")
    print(f"GAUNTLET COMPLETE")
    print(f"{'='*70}\n")
    print(f"Final idea: {current_idea}\n")
    
    return {
        "initial_idea": extract_idea_from_response(initial_idea),
        "final_idea": current_idea,
        "iterations": num_iterations,
        "reflection_chain": reflection_chain
    }

# ============================================================================
# TRANSLATION STEP
# ============================================================================

def translate_gauntlet_result(gauntlet_final_idea):
    """
    Translate the chaotic gauntlet output into plain, direct language
    No poetry, no metaphor - just what it literally means
    """
    
    prompt = f"""
You evolved an idea through multiple chaotic perturbations.

Your final evolved idea:
{gauntlet_final_idea}

Now translate this into plain, direct language:
- What is this actually saying?
- No poetry, no metaphor, no flowery language
- Just the literal claim or concept
- 2-3 sentences maximum

Pure translation. No interpretation, no goals - just: what does this MEAN in simple terms?
"""
    
    translation = call_deepseek(prompt, max_tokens=400)
    
    return translation.strip()

# ============================================================================
# MAIN EXPLORER
# ============================================================================

def run_explorer(topic, cycle_num):
    """
    Full explorer with gauntlet:
    1. Phase 1-2: Clean exploration to boundary
    2. Phase 3: Initial idea generation (light noise)
    3. GAUNTLET: Evolve through chaos (heavy noise)
    """
    
    start_time = datetime.now()
    
    print(f"\n{'='*70}")
    print(f"EXPLORER - DAY 2 - CYCLE {cycle_num} [QUANTUM GAUNTLET MODE]")
    print(f"{'='*70}\n")
    print(f"Topic: {topic}")
    print(f"Timestamp: {start_time.strftime('%Y%m%d_%H%M%S')}\n")
    
    # Phase 1-2: Clean exploration
    print("Phase 1-2: Reaching boundary and understanding spiral...")
    phase_1_2 = phase_1_and_2(topic)
    
    # Phase 3: Initial idea with light noise
    print("\nPhase 3: Generating initial idea...")
    phase_3 = phase_3_initial(phase_1_2)
    
    # GAUNTLET: Evolutionary refinement
    print("\nEntering quantum gauntlet...")
    gauntlet_result = idea_gauntlet(
        phase_3["initial_idea"],
        num_iterations=random.randint(8, 20)
    )
    
    # TRANSLATION: Convert to plain language
    print("\nTranslating gauntlet result to plain language...")
    translation = translate_gauntlet_result(gauntlet_result["final_idea"])
    print(f"Translation: {translation}\n")
    
    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    
    # Compile full result
    full_output = f"""EXPLORER - DAY 2 - CYCLE {cycle_num} [QUANTUM GAUNTLET MODE]
{'='*70}

Timestamp: {start_time.strftime('%Y%m%d_%H%M%S')}
Elapsed: {elapsed:.2f}s
Gauntlet Iterations: {gauntlet_result['iterations']}

{'='*70}
PHASES 1-2: BOUNDARY EXPLORATION
{'='*70}

{phase_1_2}

{'='*70}
PHASE 3: INITIAL IDEA (Pre-Gauntlet)
{'='*70}

Initial Perturbations: {phase_3['initial_perturbations']}

{gauntlet_result['initial_idea']}

{'='*70}
QUANTUM GAUNTLET: EVOLUTIONARY REFINEMENT
{'='*70}

Iterations: {gauntlet_result['iterations']}

"""
    
    # Add reflection chain summary
    for reflection in gauntlet_result['reflection_chain']:
        full_output += f"\n[Iteration {reflection['iteration']}] Perturbations: {', '.join(reflection['noise_operations'])}\n"
        full_output += f"Before: {reflection['idea_before'][:100]}...\n"
        full_output += f"After: {reflection['idea_after'][:100]}...\n"
    
    full_output += f"""
{'='*70}
FINAL IDEA (Post-Gauntlet)
{'='*70}

{gauntlet_result['final_idea']}

{'='*70}
TRANSLATION (Plain Language)
{'='*70}

{translation}

{'='*70}
"""
    
    # Save to file
    output_file = f"explorer_cycle_{cycle_num}_gauntlet.txt"
    with open(output_file, 'w') as f:
        f.write(full_output)
    
    print(f"\n{'='*70}")
    print(f"✅ CYCLE {cycle_num} COMPLETE")
    print(f"Saved: {output_file}")
    print(f"Elapsed: {elapsed:.2f}s")
    print(f"Gauntlet iterations: {gauntlet_result['iterations']}")
    print(f"{'='*70}\n")
    
    return output_file

# ============================================================================
# RANDOM TOPIC GENERATION
# ============================================================================

def generate_random_topic():
    """
    Generate a truly random, verifiable claim to explore
    No fixed list - completely open-ended
    """
    
    prompt = """
Generate a single, specific, verifiable claim that could be explored through verification.

Requirements:
- Must be a concrete factual claim (not vague or philosophical)
- Can be from ANY domain: physics, biology, chemistry, history, mathematics, 
  psychology, sociology, economics, astronomy, geology, linguistics, art, 
  music, technology, medicine, engineering, etc.
- Should be interesting to verify through multiple paths
- Should have some depth (not trivially obvious)
- One sentence only
- DO NOT use these examples: water boiling, speed of light, DNA, Earth orbits

Generate ONE completely new, random claim:
"""
    
    topic = call_deepseek(prompt, max_tokens=100)
    
    # Clean up the response
    topic = topic.strip()
    
    # Remove quotes if present
    topic = topic.strip('"\'')
    
    # Remove any preamble
    if ':' in topic and len(topic.split(':')[0]) < 30:
        topic = ':'.join(topic.split(':')[1:]).strip()
    
    # Take first sentence if multiple
    if '.' in topic:
        sentences = topic.split('.')
        topic = sentences[0].strip() + '.'
    
    return topic

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 explorer_gauntlet.py <cycle_num>")
        sys.exit(1)
    
    cycle_num = int(sys.argv[1])
    
    # Generate truly random topic
    print("Generating random topic...")
    topic = generate_random_topic()
    print(f"Selected topic: {topic}\n")
    
    output_file = run_explorer(topic, cycle_num)
    print(f"Output: {output_file}")
