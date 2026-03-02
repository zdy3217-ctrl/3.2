#!/usr/bin/env python3
import sys
sys.stdout.reconfigure(encoding='utf-8')

data = open(r'E:\MyClawBot\workspace\narrator-ai\src\components\AiDirectorPanel.tsx', 'rb').read()

# Find the GENRES line and show bytes around damaged chars
idx = data.find(b'GENRES')
if idx >= 0:
    start = data.find(b'[', idx)
    end = data.find(b']', start) + 1
    segment = data[start:end]
    
    print('GENRES array bytes:')
    i = 0
    while i < len(segment):
        b = segment[i]
        if 0xE0 <= b <= 0xEF and i+2 < len(segment):
            b0, b1, b2 = segment[i], segment[i+1], segment[i+2]
            if b2 == 0x3F:
                next_byte = segment[i+3] if i+3 < len(segment) else None
                next_ch = chr(next_byte) if next_byte and 32<=next_byte<127 else '?'
                print(f'  DAMAGED at {i}: {b0:02X} {b1:02X} {b2:02X} (next={next_byte:02X}={next_ch})')
                ctx_start = max(0, i-10)
                ctx_end = min(len(segment), i+13)
                ctx = segment[ctx_start:ctx_end]
                print(f'    Context bytes: {ctx.hex(" ")}')
                try:
                    ctx_text = ctx.decode('utf-8', errors='replace')
                    print(f'    Context text: {ctx_text}')
                except:
                    pass
            i += 3
        else:
            i += 1

# Also check STYLES line
print()
idx = data.find(b'STYLES')
if idx >= 0:
    start = data.find(b'[', idx)
    end = data.find(b']', start) + 1
    segment = data[start:end]
    
    print('STYLES array bytes:')
    i = 0
    while i < len(segment):
        b = segment[i]
        if 0xE0 <= b <= 0xEF and i+2 < len(segment):
            b0, b1, b2 = segment[i], segment[i+1], segment[i+2]
            if b2 == 0x3F:
                next_byte = segment[i+3] if i+3 < len(segment) else None
                next_ch = chr(next_byte) if next_byte and 32<=next_byte<127 else '?'
                print(f'  DAMAGED at {i}: {b0:02X} {b1:02X} {b2:02X} (next={next_byte:02X}={next_ch})')
            i += 3
        else:
            i += 1
