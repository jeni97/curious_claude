#!/usr/bin/env python3
"""
Complete Cycle: Explorer + Synthesis + Commit
"""

import sys
import subprocess
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python3 run_cycle.py <cycle_num>")
    sys.exit(1)

cycle_num = sys.argv[1]

print(f"\n{'='*70}")
print(f"RUNNING CYCLE {cycle_num}")
print(f"{'='*70}\n")

# Step 1: Run Explorer
print("Step 1: Running Explorer...")
subprocess.run(['python3', 'run_explorer.py', cycle_num], check=True)

# Step 2: Find Explorer output
local_outputs = Path("local_outputs")
files = sorted(local_outputs.glob(f"explorer_{cycle_num}_*.txt"))

if not files:
    print(f"❌ No Explorer output found")
    sys.exit(1)

explorer_file = files[-1]

# Step 3: Synthesize and commit
print(f"\nStep 2: Synthesizing...")
subprocess.run(['python3', 'synthesize_and_commit.py', str(explorer_file), cycle_num], check=True)

print(f"\n{'='*70}")
print(f"✅ CYCLE {cycle_num} COMPLETE")
print(f"{'='*70}")
print("\nWait ~60 seconds for Container Claude to detect.")
print("Then message Chat Claude: 'check cycle " + cycle_num + "'")
