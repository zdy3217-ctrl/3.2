#!/usr/bin/env python3
"""Extract remaining damaged positions with full context for manual mapping."""
import sys
from pathlib import Path

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

def extract_remaining():
    """Extract all remaining damaged positions with context."""
    results = []
    for fname in FILES:
        fpath = BASE / fname
        if not fpath.exists():
            continue
        data = fpath.read_bytes()
        i = 0
        while i < len(data) - 2:
            b0, b1, b2 = data[i], data[i+1], data[i+2]
            if 0xE0 <= b0 <= 0xEF and 0x80 <= b1 <= 0xBF and b2 == 0x3F:
                # Get context: 30 bytes before and after
                ctx_start = max(0, i - 30)
                ctx_end = min(len(data), i + 33)
                ctx_before = data[ctx_start:i]
                ctx_after = data[i+3:ctx_end]
                
                # Decode context
                try:
                    before_text = ctx_before.decode('utf-8', errors='replace')
                except:
                    before_text = repr(ctx_before)
                try:
                    after_text = ctx_after.decode('utf-8', errors='replace')
                except:
                    after_text = repr(ctx_after)
                
                results.append({
                    'file': fname,
                    'pos': i,
                    'b0': b0,
                    'b1': b1,
                    'byte_after': data[i+3] if i+3 < len(data) else None,
                    'before_text': before_text[-50:] if len(before_text) > 50 else before_text,
                    'after_text': after_text[:50],
                })
            i += 1
    return results

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    
    results = extract_remaining()
    print(f"Remaining damaged positions: {len(results)}")
    print()
    
    # Group by (b0, b1, byte_after)
    from collections import defaultdict
    grouped = defaultdict(list)
    for r in results:
        key = (r['b0'], r['b1'], r['byte_after'])
        grouped[key].append(r)
    
    print(f"Unique (b0,b1,byte_after) triples: {len(grouped)}")
    print()
    
    # Show each triple with context examples
    for (b0, b1, ba), items in sorted(grouped.items()):
        prefix = f"{b0:02X}{b1:02X}"
        ba_str = f"0x{ba:02X}({chr(ba) if 32<=ba<127 else '?'})" if ba else "EOF"
        print(f"=== {prefix} + {ba_str} ({len(items)} occurrences) ===")
        
        for item in items[:2]:  # Show first 2 examples
            print(f"  File: {item['file']}:{item['pos']}")
            print(f"  Context: ...{item['before_text']}[?]{item['after_text']}...")
            print()
