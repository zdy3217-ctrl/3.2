#!/usr/bin/env python3
"""
R50 UTF-8 Fix v2 - Context-aware approach
Extract all damaged strings with context, then apply precise replacements.
"""
import os
import sys
import re

BASE = r"E:\MyClawBot\workspace\narrator-ai\src\components"

DAMAGED_FILES = [
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

def extract_damaged_strings(filepath):
    """Extract all lines containing damaged UTF-8 sequences with context."""
    data = open(filepath, 'rb').read()
    results = []
    
    i = 0
    while i < len(data) - 2:
        b0, b1, b2 = data[i], data[i+1], data[i+2]
        if 0xE0 <= b0 <= 0xEF and 0x80 <= b1 <= 0xBF and b2 == 0x3F:
            # Found damaged sequence, get line context
            # Find line start and end
            line_start = data.rfind(b'\n', 0, i) + 1
            line_end = data.find(b'\n', i)
            if line_end == -1:
                line_end = len(data)
            
            line_bytes = data[line_start:line_end]
            line_text = line_bytes.decode('utf-8', errors='replace')
            
            # Get the line number
            line_num = data[:i].count(b'\n') + 1
            
            # Get surrounding context (50 bytes each side)
            ctx_start = max(0, i - 50)
            ctx_end = min(len(data), i + 53)
            ctx = data[ctx_start:ctx_end].decode('utf-8', errors='replace')
            
            results.append({
                'pos': i,
                'b0': b0, 'b1': b1,
                'prefix': f'{b0:02X}{b1:02X}',
                'line_num': line_num,
                'line': line_text.strip(),
                'context': ctx,
            })
        i += 1
    return results

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    
    all_results = {}
    total = 0
    
    for fname in DAMAGED_FILES:
        path = os.path.join(BASE, fname)
        if not os.path.exists(path):
            continue
        results = extract_damaged_strings(path)
        if results:
            all_results[fname] = results
            total += len(results)
    
    print(f"Total damaged sequences across all files: {total}")
    print(f"Files with damage: {len(all_results)}")
    print()
    
    # Group by unique damaged line content to find patterns
    unique_lines = {}
    for fname, results in all_results.items():
        for r in results:
            key = r['line'][:100]
            if key not in unique_lines:
                unique_lines[key] = []
            unique_lines[key].append((fname, r['line_num'], r['prefix']))
    
    print(f"Unique damaged lines: {len(unique_lines)}")
    print()
    
    # Print all unique damaged lines grouped
    for i, (line, occurrences) in enumerate(sorted(unique_lines.items())):
        print(f"--- #{i+1} (in {len(occurrences)} file(s)) ---")
        print(f"  Line: {line[:200]}")
        for fname, lnum, prefix in occurrences[:3]:
            print(f"  @ {fname}:{lnum} prefix={prefix}")
        print()

if __name__ == "__main__":
    main()
