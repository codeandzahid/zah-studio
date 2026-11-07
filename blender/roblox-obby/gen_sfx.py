"""Generate the Roblox obby game-sound track: 60s, 44100 Hz mono WAV.
- soft wind bed (brown noise, very low)
- jump boing every second (hop peaks at t = 0.5, 1.5, ... 59.5)
- coin ding every 3 seconds (coins at t = 2, 5, 8, ...)
- little finish fanfare in the last second
"""
import math, random, struct, wave

SR = 44100
DUR = 60.0
N = int(SR * DUR)
out = [0.0] * N

def add(t0, samples):
    i0 = int(t0 * SR)
    for i, s in enumerate(samples):
        j = i0 + i
        if 0 <= j < N:
            out[j] += s

# --- wind bed: brown noise, smoothed, very low ---
random.seed(3)
last = 0.0
for i in range(N):
    last = (last + (random.random() * 2 - 1) * 0.02) * 0.998
    out[i] += last * 0.5

# --- jump boing: chirp 280 -> 750 Hz, 0.16 s, decaying ---
def boing(amp=0.30):
    n = int(0.16 * SR)
    s = []
    for i in range(n):
        t = i / SR
        f = 280 + (750 - 280) * (t / 0.16)
        phase = 2 * math.pi * (280 * t + (750 - 280) * t * t / (2 * 0.16))
        s.append(amp * math.sin(phase) * math.exp(-t * 14))
    return s

for k in range(60):
    add(0.5 + k, boing())

# --- coin ding: 1318 Hz then 1760 Hz ---
def ding(amp=0.35):
    s = []
    for i in range(int(0.06 * SR)):
        t = i / SR
        s.append(amp * math.sin(2 * math.pi * 1318 * t))
    for i in range(int(0.09 * SR)):
        t = i / SR
        s.append(amp * math.sin(2 * math.pi * 1760 * t) * math.exp(-t * 8))
    return s

for k in range(20):
    add(2 + 3 * k, ding())

# --- finish fanfare: C5 E5 G5 C6, last second ---
notes = [523.25, 659.25, 783.99, 1046.50]
for j, f in enumerate(notes):
    n = int(0.22 * SR)
    s = []
    for i in range(n):
        t = i / SR
        s.append(0.32 * (math.sin(2 * math.pi * f * t)
                         + 0.3 * math.sin(2 * math.pi * f * 2 * t))
                 * math.exp(-t * 6))
    add(59.0 + j * 0.22, s)

# normalize + write
peak = max(abs(v) for v in out) or 1.0
scale = 0.9 / peak
with wave.open('/tmp/roblox-sfx.wav', 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    frames = b''.join(struct.pack('<h', int(max(-1.0, min(1.0, v * scale)) * 32767))
                      for v in out)
    w.writeframes(frames)
print('WROTE /tmp/roblox-sfx.wav', DUR, 's')
