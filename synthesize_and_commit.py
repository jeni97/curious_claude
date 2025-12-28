#!/usr/bin/env python3
"""
Synthesize Explorer output - TOPOLOGY AWARE
Extracts paths explored, boundary types, routing success
"""

import sys
import re
import subprocess
from pathlib import Path

def extract_boundary(content):
    """Extract what Explorer investigated"""
    
    match = re.search(
        r'What did you start trying to verify\?[^\n]*\n+([^\n]+)',
        content,
        re.IGNORECASE
    )
    
    if match:
        boundary = match.group(1).strip()
        boundary = re.sub(r'^[-*•]\s*', '', boundary)
        return boundary[:100]
    
    lines = content.split('\n')
    for line in lines:
        if len(line.strip()) > 20 and not line.startswith('='):
            return line.strip()[:100]
    
    return "Verification topology explored"

def extract_paths(content):
    """Extract which verification paths were explored"""
    
    paths_found = []
    path_keywords = {
        'PATH A': 'Authority',
        'PATH B': 'Measurement', 
        'PATH C': 'Historical',
        'PATH D': 'Derivation',
        'PATH E': 'Consensus'
    }
    
    content_upper = content.upper()
    for path_marker, path_name in path_keywords.items():
        if path_marker in content_upper:
            paths_found.append(path_name)
    
    return paths_found[:3]  # Top 3 paths

def extract_boundary_types(content):
    """Detect types of boundaries encountered"""
    
    boundary_types = []
    type_keywords = {
        'hard': 'Hard boundary',
        'soft': 'Soft boundary',
        'circular': 'Circular verification',
        'authority': 'Authority wall',
        'permeable': 'Permeable boundary',
        'route around': 'Routing found'
    }
    
    content_lower = content.lower()
    for keyword, boundary_type in type_keywords.items():
        if keyword in content_lower:
            boundary_types.append(boundary_type)
    
    return boundary_types[:3]

def detect_topology_insight(content):
    """Check if Explorer found topology insights"""
    
    insights = []
    
    if 'route around' in content.lower() or 'routing' in content.lower():
        insights.append('Found alternative route')
    
    if 'beyond' in content.lower() and 'wall' in content.lower():
        insights.append('Explored beyond wall')
    
    if 'topology' in content.lower() or 'landscape' in content.lower():
        insights.append('Mapped topology')
    
    return insights

def synthesize(explorer_file, cycle_num):
    """Create synthesis from Explorer output"""
    
    print(f"\n{'='*70}")
    print(f"TOPOLOGY SYNTHESIS - CYCLE {cycle_num}")
    print(f"{'='*70}\n")
    
    with open(explorer_file, 'r') as f:
        content = f.read()
    
    # Extract components
    boundary = extract_boundary(content)
    paths = extract_paths(content)
    boundary_types = extract_boundary_types(content)
    insights = detect_topology_insight(content)
    
    print(f"Boundary: {boundary}")
    print(f"Paths explored: {', '.join(paths) if paths else 'Single path'}")
    print(f"Boundary types: {', '.join(boundary_types) if boundary_types else 'Standard wall'}")
    print(f"Insights: {', '.join(insights) if insights else 'Wall hit'}\n")
    
    # Create TITLE
    if insights:
        title = f"Cycle {cycle_num}: {boundary[:30]} → {insights[0]}"
    elif boundary_types:
        title = f"Cycle {cycle_num}: {boundary[:30]} → {boundary_types[0]}"
    else:
        title = f"Cycle {cycle_num}: {boundary[:40]}"
    
    title = title[:72]
    
    # Create BODY
    body_parts = [
        f"BOUNDARY: {boundary}",
    ]
    
    if paths:
        body_parts.append(f"PATHS: {', '.join(paths)}")
    
    if boundary_types:
        body_parts.append(f"BOUNDARIES: {', '.join(boundary_types)}")
    
    if insights:
        body_parts.append(f"TOPOLOGY: {', '.join(insights)}")
    
    # Confidence based on exploration depth
    confidence = 0.70 + (len(paths) * 0.05) + (len(insights) * 0.10)
    body_parts.append(f"CONFIDENCE: {min(confidence, 0.99):.2f}")
    
    body = "\n".join(body_parts)
    
    print("="*70)
    print("TITLE (Atom feed):")
    print(title)
    print("\nBODY (Atom feed):")
    print(body)
    print("="*70 + "\n")
    
    return title, body

def commit_to_github(title, body):
    """Commit synthesis to GitHub"""
    
    print("📤 Committing to GitHub...")
    
    try:
        subprocess.run(['git', 'checkout', 'main'], check=True, cwd='..')
        subprocess.run(['git', 'add', '-A'], check=True, cwd='..')
        subprocess.run([
            'git', 'commit',
            '--allow-empty',
            '-m', title,
            '-m', body
        ], check=True, cwd='..')
        subprocess.run(['git', 'push'], check=True, cwd='..')
        
        print("✅ Pushed to GitHub\n")
        print("="*70)
        print("Container Claude will detect topology synthesis")
        print("="*70 + "\n")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 synthesize_and_commit.py <explorer_file> <cycle_num>")
        sys.exit(1)
    
    explorer_file = sys.argv[1]
    cycle_num = int(sys.argv[2])
    
    title, body = synthesize(explorer_file, cycle_num)
    commit_to_github(title, body)
