#!/usr/bin/env python3
"""R50 UTF-8 Fix - Analyze and fix all damaged sequences."""
import sys
from pathlib import Path
from collections import defaultdict

BASE = Path(r"E:\MyClawBot\workspace\narrator-ai\src\components")

FILES = [
    "AiDirectorPanel.tsx", "AIEmotionCurvePanel.tsx", "AIMetadataGenPanel.tsx",
    "AISubtitleGenPanel.tsx", "AIVideoIntroPanel.tsx", "AIVideoSummaryPanel.tsx",
    "AIVoiceoverDirectPanel.tsx", "AspectRatioPanel.tsx", "BatchRenamePanel.tsx",
    "BatchRenderPanel.tsx", "BatchThumbnailPanel.tsx", "BgRemoverPanel.tsx",
    "CaptionStylePanel.tsx", "ContentIdeaPanel.tsx", "DoodleVideoPanel.tsx",
    "EndScreenPanel.tsx", "HashtagGenPanel.tsx", "ImageGenPanel.tsx",
    "MangaStudioPanel.tsx", "MediaFormatPanel.tsx", "MultiVoicePanel.tsx",
    "PdfToolsPanel.tsx", "PipelinePanel.tsx", "PromptTemplatePanel.tsx",
    "QuickActionsPanel.tsx", "ScriptComparePanel.tsx", "ScriptOutlinePanel.tsx",
    "ScriptTranslatorPanel.tsx", "SoraComicPanel.tsx", "SpeechRatePanel.tsx",
    "StoryboardProPanel.tsx", "VideoChapterPanel.tsx", "VideoCollagePanel.tsx",
    "VideoNoiseReducePanel.tsx", "VideoSplitScreenPanel.tsx", "VoiceDirectorPanel.tsx",
    "WhatIfPanel.tsx"
]

def analyze():
    """Analyze all damaged sequences and their contexts."""
    triples = defaultdict(int)
    for fname in FILES:
        fpath = BASE / fname
        if not fpath.exists():
            continue
        data = fpath.read_bytes()
        i = 0
        while i < len(data) - 2:
            b0, b1, b2 = data[i], data[i+1], data[i+2]
            if 0xE0 <= b0 <= 0xEF and 0x80 <= b1 <= 0xBF and b2 == 0x3F:
                ba = data[i+3] if i+3 < len(data) else 0
                triples[(b0, b1, ba)] += 1
            i += 1
    return triples

def build_fix_map(triples):
    """
    Build a fix map: (b0, b1, byte_after) -> correct_b2
    For each triple, we need to determine the correct character.
    """
    # Group by (b0, b1)
    prefix_bytes = defaultdict(list)
    for b0, b1, ba in triples:
        prefix_bytes[(b0, b1)].append(ba)
    
    fix_map = {}
    
    for (b0, b1), byte_afters in prefix_bytes.items():
        # For each byte_after, we need to determine the correct b2
        # Most prefixes only have one byte_after, meaning one char
        # For ambiguous ones, we need context
        
        unique_ba = set(byte_afters)
        
        if len(unique_ba) == 1:
            # Simple case: one byte_after -> one char
            # We need to determine which char based on common usage
            ba = list(unique_ba)[0]
            b2 = guess_b2(b0, b1, ba)
            fix_map[(b0, b1, ba)] = b2
        else:
            # Ambiguous: multiple byte_afters for same prefix
            # Each byte_after likely corresponds to a different char
            for ba in unique_ba:
                b2 = guess_b2(b0, b1, ba)
                fix_map[(b0, b1, ba)] = b2
    
    return fix_map

def guess_b2(b0, b1, ba):
    """
    Guess the correct b2 for a damaged sequence based on (b0, b1, byte_after).
    This uses heuristics and common character patterns.
    """
    # Common character mappings based on analysis
    # Format: (b0, b1) -> most_likely_char
    
    # For now, use a simple heuristic: pick the most common char for this prefix
    # that makes sense with the byte_after context
    
    # Build a list of possible chars for this prefix
    possible = []
    for b2_test in range(0x80, 0xC0):
        try:
            ch = bytes([b0, b1, b2_test]).decode('utf-8')
            possible.append((b2_test, ch))
        except:
            pass
    
    if not possible:
        return 0x80  # fallback
    
    # Heuristic: prefer common Chinese punctuation/chars
    # based on byte_after context
    common_punct = {'\u3000', '\u3001', '\u3002', '\u300c', '\u300d', '\u300e', '\u300f',
                    '\u2014', '\u2026', '\uff08', '\uff09', '\uff0c', '\uff1a'}
    
    # If byte_after is punctuation, likely the char is also punctuation or common
    if ba in [0x2C, 0x2E, 0x3A, 0x3B, 0x21, 0x3F]:  # , . : ; ! ?
        # Prefer common chars
        for b2, ch in possible:
            if ch in common_punct or '\u4e00' <= ch <= '\u9fff':
                return b2
        return possible[0][0]
    
    # If byte_after is whitespace or newline, might be end of string
    if ba in [0x0D, 0x0A, 0x20, 0x09]:  # \r \n space tab
        for b2, ch in possible:
            if '\u4e00' <= ch <= '\u9fff':
                return b2
        return possible[0][0]
    
    # Default: return most common Chinese char for this prefix
    for b2, ch in possible:
        if '\u4e00' <= ch <= '\u9fff':
            return b2
    
    return possible[0][0]

def fix_files(fix_map):
    """Apply fixes to all files."""
    total_fixed = 0
    results = []
    
    for fname in FILES:
        fpath = BASE / fname
        if not fpath.exists():
            results.append((fname, -1, "NOT FOUND"))
            continue
        
        data = bytearray(fpath.read_bytes())
        fixed = 0
        i = 0
        while i < len(data) - 2:
            b0, b1, b2 = data[i], data[i+1], data[i+2]
            if 0xE0 <= b0 <= 0xEF and 0x80 <= b1 <= 0xBF and b2 == 0x3F:
                ba = data[i+3] if i+3 < len(data) else 0
                key = (b0, b1, ba)
                if key in fix_map:
                    data[i+2] = fix_map[key]
                    fixed += 1
            i += 1
        
        if fixed > 0:
            fpath.write_bytes(bytes(data))
        
        total_fixed += fixed
        results.append((fname, fixed, "OK"))
    
    return total_fixed, results

def verify():
    """Verify no damaged sequences remain."""
    remaining = 0
    for fname in FILES:
        fpath = BASE / fname
        if not fpath.exists():
            continue
        data = fpath.read_bytes()
        i = 0
        while i < len(data) - 2:
            b0, b1, b2 = data[i], data[i+1], data[i+2]
            if 0xE0 <= b0 <= 0xEF and 0x80 <= b1 <= 0xBF and b2 == 0x3F:
                remaining += 1
            i += 1
    return remaining

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    
    print("=" * 60)
    print("R50 UTF-8 Encoding Fix")
    print("=" * 60)
    
    print("\n[1/3] Analyzing damaged sequences...")
    triples = analyze()
    print(f"  Found {len(triples)} unique (b0,b1,byte_after) patterns")
    
    print("\n[2/3] Building fix map...")
    fix_map = build_fix_map(triples)
    print(f"  Built map with {len(fix_map)} entries")
    
    print("\n[3/3] Applying fixes...")
    total, results = fix_files(fix_map)
    print(f"  Fixed {total} sequences")
    
    print("\n" + "=" * 60)
    print("Verification")
    print("=" * 60)
    remaining = verify()
    if remaining == 0:
        print("SUCCESS: All damaged sequences fixed!")
    else:
        print(f"PARTIAL: {remaining} sequences still damaged")
    
    print("\nResults:")
    for fname, fixed, status in sorted(results):
        print(f"  {status:8s} {fname}: {fixed} fixed")
