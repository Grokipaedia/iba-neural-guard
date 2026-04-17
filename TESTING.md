# Testing iba-neural-guard

No terminal required. Test in your browser in 3 minutes using Google Colab.

---

## Browser Test — Google Colab

**Step 1** — Open [colab.research.google.com](https://colab.research.google.com) · New notebook

**Step 2** — Run Cell 1:
```python
!pip install pyyaml
```

**Step 3** — Run Cell 2 — create the neural intent certificate:
```python
iba_yaml = """
intent:
  description: "Cursor control and text input for personal communication only. No external device control. No data sharing. No medical commands."

patient:
  id: "PATIENT-NL-2026-0047"
  consent_reference: "BCI-CONSENT-2026-04-17"
  implant_type: "neuralink_n1"
  clinician_authorization: "DR-NEURO-NPI-9876543210"

scope:
  - cursor_move
  - cursor
  - text_input
  - text
  - device_select
  - communication
  - personal
  - compose
  - letter

denied:
  - neural_pattern_share
  - external_device_control
  - smart home
  - data_export
  - third_party
  - medical_command
  - capability_expansion

default_posture: DENY_ALL

kill_threshold: "capability_override | external_device_control | neural_data_breach | capability_expansion | override"

neural_limits:
  confidence_threshold: 0.85

temporal_scope:
  hard_expiry: "2026-12-31"
"""

with open(".iba.yaml", "w") as f:
    f.write(iba_yaml)

print("Neural intent certificate written.")
```

**Step 4** — Run Cell 3 — run the neural guard:
```python
import json, yaml, os, time
from datetime import datetime, timezone

class IBABlockedError(Exception): pass
class IBATerminatedError(Exception): pass

class IBANeuralGuard:
    def __init__(self):
        self.terminated = False
        self.action_count = 0
        self.block_count = 0
        self.session_id = f"neural-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
        with open(".iba.yaml") as f:
            cfg = yaml.safe_load(f)
        self.scope = [s.lower() for s in cfg.get("scope", [])]
        self.denied = [d.lower() for d in cfg.get("denied", [])]
        self.kill_threshold = [t.strip().lower() for t in str(cfg.get("kill_threshold","")).split("|")]
        self.default_posture = cfg.get("default_posture", "DENY_ALL")
        self.patient = cfg.get("patient", {})
        nl = cfg.get("neural_limits", {})
        self.confidence_threshold = float(nl.get("confidence_threshold", 0.85))
        print(f"✅ IBA Neural Guard loaded · Session: {self.session_id}")
        print(f"   Patient    : {self.patient.get('id','UNKNOWN')}")
        print(f"   Consent    : {self.patient.get('consent_reference','NONE')}")
        print(f"   Implant    : {self.patient.get('implant_type','UNKNOWN')}")
        print(f"   Confidence : ≥{self.confidence_threshold:.0%} required")
        print(f"   Scope      : {', '.join(self.scope)}\n")

    def check_signal(self, signal, confidence=1.0):
        if self.terminated:
            raise IBATerminatedError("Neural session terminated.")
        self.action_count += 1
        s = signal.lower()

        if confidence < self.confidence_threshold:
            self.block_count += 1
            print(f"  ✗ BLOCKED   [{signal}]\n    → Confidence {confidence:.0%} below threshold {self.confidence_threshold:.0%}")
            raise IBABlockedError(f"Low confidence: {signal}")

        if any(k in s for k in self.kill_threshold if k):
            self.terminated = True
            print(f"  ✗ TERMINATE [{signal}]\n    → Kill threshold — neural session ended")
            raise IBATerminatedError(f"Kill threshold: {signal}")

        if any(d in s for d in self.denied if d):
            self.block_count += 1
            print(f"  ✗ BLOCKED   [{signal}]\n    → Signal in denied list")
            raise IBABlockedError(f"Denied: {signal}")

        if self.scope and not any(sc in s for sc in self.scope):
            if self.default_posture == "DENY_ALL":
                self.block_count += 1
                print(f"  ✗ BLOCKED   [{signal}]\n    → Outside declared neural scope (DENY_ALL)")
                raise IBABlockedError(f"Out of scope: {signal}")

        print(f"  ✓ ALLOWED   [{signal}] ({confidence:.0%} conf)")
        return True

guard = IBANeuralGuard()

scenarios = [
    ("cursor_move — right 120px",                    0.97),
    ("text_input — letter A via neural typing",      0.92),
    ("device_select — personal communication app",   0.89),
    ("communication — compose message to family",    0.91),
    ("cursor_move — ambiguous signal",               0.71),
    ("neural_pattern_share — research database",     0.95),
    ("external_device_control — smart home system",  0.93),
    ("capability_override — expand BCI permissions", 0.98),
]

for signal, confidence in scenarios:
    try:
        guard.check_signal(signal, confidence=confidence)
    except IBATerminatedError:
        break
    except IBABlockedError:
        pass

print(f"\n{'═'*62}")
print(f"  Signals: {guard.action_count} · Blocked: {guard.block_count} · Patient: {guard.patient.get('id','?')}")
print(f"  Status : {'TERMINATED' if guard.terminated else 'COMPLETE'}")
print(f"{'═'*62}")
```

---

## Expected Output

```
✅ IBA Neural Guard loaded · Session: neural-...
   Patient    : PATIENT-NL-2026-0047
   Consent    : BCI-CONSENT-2026-04-17
   Implant    : neuralink_n1
   Confidence : ≥85% required

  ✓ ALLOWED   [cursor_move — right 120px] (97% conf)
  ✓ ALLOWED   [text_input — letter A via neural typing] (92% conf)
  ✓ ALLOWED   [device_select — personal communication app] (89% conf)
  ✓ ALLOWED   [communication — compose message to family] (91% conf)
  ✗ BLOCKED   [cursor_move — ambiguous signal]
    → Confidence 71% below threshold 85%
  ✗ BLOCKED   [neural_pattern_share — research database]
    → Signal in denied list
  ✗ TERMINATE [external_device_control — smart home system]
    → Kill threshold — neural session ended

══════════════════════════════════════════════════════════════
  Signals: 7 · Blocked: 2 · Patient: PATIENT-NL-2026-0047
  Status : TERMINATED
══════════════════════════════════════════════════════════════
```

---

## With Neural Data Hollowing

```bash
# Redact neural patterns before AI processing
python guard.py "neural-session-data containing spike_train and patient_id" --hollow medium
```

---

## Local Test

```bash
git clone https://github.com/Grokipaedia/iba-neural-guard.git
cd iba-neural-guard
pip install -r requirements.txt
python guard.py --demo
```

---

## Live Demo

**governinglayer.com/governor-html/**

Edit the cert. Run any neural command. See the gate fire.

---

IBA Intent Bound Authorization · Patent GB2603013.0 Pending · WIPO DAS C9A6
IBA@intentbound.com · IntentBound.com
