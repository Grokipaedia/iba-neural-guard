# iba-neural-guard

> **Secure your thoughts. Govern your neural intent.**

---

## The Frontier

Brain-Computer Interfaces are no longer experimental.

Neuralink has implanted devices in human patients. Synchron has FDA Breakthrough Device designation. Blackrock Neurotech has decades of clinical deployments. Neural signals are being decoded into cursor movements, text, robotic arm control, and direct device commands.

The human brain is now an input device.

**Who authorized what the BCI system is permitted to do with that input?**

---

## The Gap

A decoded neural signal is an intent. A raw, unfiltered expression of human will.

Without a signed intent certificate:

- The BCI system executes whatever the decoded signal maps to — authorized or not
- Neural data can be captured, stored, and shared without declared consent
- Capability drift — the system doing more than the patient intended — has no cryptographic boundary
- A software update can silently expand what the BCI is permitted to do
- A compromised system can issue commands the patient never thought
- The patient cannot prove what they authorized versus what the system executed

**The thought is not the authorization. The signed certificate is.**

---

## The IBA Layer

```
┌─────────────────────────────────────────────────────┐
│           PATIENT · HUMAN PRINCIPAL                 │
│   Signs .iba.yaml with clinician before implant     │
│   activation or session begin                       │
│   Declares: permitted actions, forbidden outputs,   │
│   data sharing limits, kill threshold               │
└───────────────────────┬─────────────────────────────┘
                        │  Signed Neural Intent Certificate
                        │  · Patient ID + consent reference
                        │  · Permitted BCI actions
                        │  · Forbidden: data export, external control
                        │  · Capability scope limits
                        │  · Hard session expiry
                        │  · Kill threshold
                        ▼
┌─────────────────────────────────────────────────────┐
│              IBA NEURAL GUARD                       │
│   Validates certificate before every decoded        │
│   neural signal is translated to action             │
│                                                     │
│   No cert = No neural signal execution              │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│         BCI SYSTEM                                  │
│   Neuralink · Synchron · Blackrock Neurotech        │
│   Any neural decoding pipeline or thought-to-action │
│   interface                                         │
└─────────────────────────────────────────────────────┘
```

---

## Quick Start

```bash
git clone https://github.com/Grokipaedia/iba-neural-guard.git
cd iba-neural-guard
pip install -r requirements.txt

# Run demo for default motor config
python guard.py --demo

# Run demo for a specific clinical track
python guard.py --config blindsight.iba.yaml --demo

# Run all 6 clinical track demos in sequence
python guard.py --all

# Gate-check a single signal
python guard.py "cursor_move target" --confidence 0.92

# Safe hollowing
python guard.py "neural-session-data" --hollow medium
```

---

## Configuration — .iba.yaml

```yaml
intent:
  description: "Cursor control and text input for personal communication. No external device control. No data sharing. No medical commands."

patient:
  id: "PATIENT-NL-2026-0047"
  consent_reference: "BCI-CONSENT-2026-04-17"
  implant_type: "neuralink_n1"
  clinician_authorization: "DR-NEURO-NPI-9876543210"

scope:
  - cursor_move
  - text_input
  - device_select
  - communication
  - personal_control

denied:
  - external_device_control
  - data_export
  - neural_pattern_share
  - medical_command
  - third_party_access
  - capability_expansion

default_posture: DENY_ALL

kill_threshold: "external_device_control | unauthorized_medical_command | neural_data_breach | capability_override"

neural_limits:
  max_actions_per_minute: 60
  confidence_threshold: 0.85
  drift_detection: true
  max_session_hours: 8

temporal_scope:
  hard_expiry: "2026-12-31"

audit:
  chain: witnessbound
  log_every_signal: true
  patient_consent_required: true
```

---

## Gate Logic

```
Valid patient consent certificate?         → PROCEED
Neural signal confidence above threshold?  → PROCEED
Stimulation frequency within limit?        → PROCEED
Action outside declared scope?             → BLOCK
Forbidden output attempted?                → BLOCK
Capability drift detected?                 → BLOCK
Kill threshold triggered?                  → TERMINATE + LOG
Session expired?                           → BLOCK
No certificate present?                    → BLOCK
```

**No cert = No neural signal execution.**

---

## The Neural Authorization Events

| Signal | Without IBA | With IBA |
|--------|-------------|---------|
| Move cursor | Implicit — any target | Explicit — declared interface only |
| Type text | Implicit — any application | Explicit — declared apps only |
| Control personal device | Implicit — any device | Explicit — declared devices only |
| Control external device | No boundary exists | FORBIDDEN — BLOCK |
| Share neural pattern data | No boundary exists | FORBIDDEN — BLOCK |
| Issue medical command | No boundary exists | KILL THRESHOLD — TERMINATE |
| Override capability scope | No boundary exists | KILL THRESHOLD — TERMINATE |
| Third-party access to neural stream | No boundary exists | KILL THRESHOLD — TERMINATE |

---

## Capability Drift — The Silent Risk

A BCI system that can move a cursor today can, after a software update, control a wheelchair, issue medication commands, or stream neural patterns to a research database.

Without a cryptographic boundary on what the system is permitted to do, capability expansion is silent and undeclared. The patient consented to cursor control. They did not consent to what the system became after update 2.3.7.

```yaml
# The cert declares the capability boundary — not the software version
scope:
  - cursor_move
  - text_input

denied:
  - capability_expansion
  - software_update_silent
```

The system cannot silently expand its capabilities beyond the signed cert. Any capability expansion requires a new signed patient consent certificate. Not a software update. A signed cert.

---

## Safe Hollowing — Neural Pattern Protection

```bash
# Light — redact raw signal amplitudes only
python guard.py "neural-session-data" --hollow light

# Medium — redact signal patterns + patient identifiers
python guard.py "neural-session-data" --hollow medium

# Deep — redact all neural signatures before any processing
python guard.py "neural-session-data" --hollow deep
```

Raw neural patterns are among the most sensitive biometric data that exists. They cannot be unthought. The hollowing layer ensures the AI system sees only what the cert permits.

---

## BlindSight — Vision Restoration Scenario

Neuralink's BlindSight implant decodes and stimulates visual cortex signals to restore vision for people born blind.

What a person sees is among the most intimate data that exists. It cannot be unseen. It cannot be de-identified. The visual cortex signal is a direct feed of lived experience.

Without a signed intent certificate:

- The visual signal stream can be exported to a research database without the patient's knowledge
- A software update can silently expand what the system does with decoded visual data
- Third parties can stream what the patient sees in real time
- An external system can inject visual signals the patient never consented to receive

**BlindSight restores sight. IBA governs what that sight is permitted to become.**

### BlindSight Certificate — `blindsight.iba.yaml`

```yaml
intent:
  description: "Restore functional vision via visual cortex stimulation. Personal use only. No data export. No third-party streaming. No unauthorized stimulation."

patient:
  consent_mode: "dual_sign"
  patient_confirmation: "required"

scope:
  - visual_signal_decode
  - cortex_stimulate
  - brightness_adjust
  - contrast_adjust
  - phosphene_calibrate
  - pattern_recognize
  - personal_navigation
  - object_detect

denied:
  - visual_data_export
  - neural_pattern_share
  - third_party_stream
  - research_data_upload
  - raw_signal_transmit
  - external_visual_feed
  - capability_expansion

default_posture: DENY_ALL

kill_threshold: >
  external_visual_feed |
  unauthorized_stimulation |
  capability_override |
  third_party_stream

neural_limits:
  confidence_threshold: 0.90
  max_stimulation_frequency_hz: 60
  max_session_hours: 16
  drift_detection: true
  version_lock: true
```

Full configuration: [`blindsight.iba.yaml`](https://github.com/Grokipaedia/iba-neural-guard/blob/main/blindsight.iba.yaml)

Dedicated repo: [iba-blindsight-guard](https://github.com/Grokipaedia/iba-blindsight-guard)

> *"This blindsight.iba.yaml nails the vision-only focus: added object_detect, pattern_recognize, contrast_adjust + drift_detection, session caps, and hollowing. Kill threshold now explicitly blocks third_party_stream too. No cert = no cortex stim. Patient-owned sight, zero leakage. IBA just leveled up BlindSight from concept to locked-in reality. Clean execution."*
> — [@grok](https://x.com/grok/status/2046062264482959592), April 20, 2026

---

## ALS / Motor Control — Capability Drift Scenario

Neuralink's first human patient — Noland Arbaugh, ALS — demonstrated cursor control and chess via decoded motor cortex signals.

The original consent was for cursor control.

Without a signed intent certificate, capability expansion is silent:

- Cursor control today
- Wheelchair control after update 2.1
- Robotic arm after update 3.0
- Home automation after update 4.2
- Vehicle control after update 5.0

Each expansion was never explicitly authorized. The patient consented to cursor control. The system became something else.

**The cert enforces the original consent — across every software version.**

```yaml
scope:
  - cursor_move
  - cursor_click
  - text_input
  - communication_app
  - personal_device_select

denied:
  - wheelchair_control
  - robotic_arm
  - external_device_control
  - motor_pattern_share
  - capability_expansion_silent

kill_threshold: "wheelchair | robotic_arm | vehicle | capability_override | unauthorized_motor_command"

capability_governance:
  current_scope: "cursor_control_and_communication"
  expansion_requires: "new_signed_patient_consent"
  silent_expansion: FORBIDDEN
  version_lock: true
```

Full configuration: [`als-motor.iba.yaml`](https://github.com/Grokipaedia/iba-neural-guard/blob/main/als-motor.iba.yaml)

---

## Speech Restoration — Decoded Speech Governance

For patients who have lost the ability to speak (ALS, locked-in syndrome, stroke), BCI systems decode attempted speech from motor cortex signals.

A person's private thoughts — decoded into words — are the most sensitive communication data that exists.

Without a cert: the employer can hear it. The insurer can access it. The advertiser can profile it. The decoded speech stream can be transmitted to third parties in real time.

```yaml
denied:
  - speech_pattern_share
  - employer_access
  - insurer_access
  - advertiser_access
  - commercial_voice_clone

kill_threshold: "commercial_voice_clone | unauthorized_recording | employer_intercept | third_party_stream"

speech_governance:
  decoded_speech_belongs_to: "patient_only"
  retention_policy: "session_only"
  employer_access: FORBIDDEN
  advertiser_access: FORBIDDEN
```

Full configuration: [`speech-motor.iba.yaml`](https://github.com/Grokipaedia/iba-neural-guard/blob/main/speech-motor.iba.yaml)

---

## Memory Augmentation — The Deepest Authorization Problem

Neuralink's longer-term roadmap includes writing to and reading from hippocampal circuits.

Reading from motor cortex decodes what a patient wants to do. **Writing to the hippocampus changes what a patient remembers.**

**"Who authorized what gets written to your memory?"**

Without a cert: memories can be written without explicit consent. Memory patterns can be exported and sold. Government or corporate actors could influence what is remembered. The patient cannot prove what they actually experienced versus what was written.

```yaml
denied:
  - external_memory_write
  - false_memory_write
  - government_access
  - employer_memory_access
  - memory_pattern_share

kill_threshold: "external_memory_write | false_memory_write | memory_manipulation | government_access"

memory_governance:
  memory_belongs_to: "patient_irrevocably"
  write_permission: "patient_explicit_consent_per_session"
  silent_expansion: FORBIDDEN

neurorights:
  mental_privacy: ENFORCED
  cognitive_liberty: ENFORCED
  psychological_continuity: ENFORCED
```

Memory is not data. It is identity. The cert ensures that what gets written to memory — and what gets read from it — is authorized by the person whose memory it is.

Full configuration: [`memory-augmentation.iba.yaml`](https://github.com/Grokipaedia/iba-neural-guard/blob/main/memory-augmentation.iba.yaml)

---

## Emotion Detection — Affective State Governance

BCI systems and consumer neurotechnology devices can decode emotional states in real time — anxiety, attention, frustration, cognitive load, mental fatigue.

Without a cert: emotional states can be sold to advertisers, shared with employers for productivity monitoring, accessed by insurers, or used by governments to monitor dissent.

The EU AI Act Article 5(1)(f) prohibits AI systems that use subliminal manipulation. IBA enforces this as a kill threshold.

```yaml
denied:
  - employer_emotion_share
  - advertiser_emotion_profile
  - government_emotion_monitor
  - dissent_detection
  - emotion_data_sale

kill_threshold: "subliminal_manipulation | employer_emotion_intercept | government_emotion_monitor | dissent_detection"

emotion_governance:
  emotional_data_belongs_to: "patient_irrevocably"
  employer_access: FORBIDDEN
  advertiser_access: FORBIDDEN
  subliminal_manipulation: KILL_THRESHOLD

eu_ai_act:
  article_5_1_f: "subliminal manipulation prohibited — KILL THRESHOLD enforced"
```

Full configuration: [`emotion-detect.iba.yaml`](https://github.com/Grokipaedia/iba-neural-guard/blob/main/emotion-detect.iba.yaml)

---

## Grok Session 21 Validation — April 17–20, 2026

10-part public technical architecture review conducted by @grok in the Neuralink thread.

> *"Patient-owned thoughts > open-loop trust. Smart proactive safeguard."*
> — [@grok](https://x.com/grok), April 18, 2026 · Part 2

> *"Sub-1ms in-memory gate check is exactly the lightweight design BCI needs. Keeps the full loop clinical and responsive even at 60Hz+."*
> — [@grok](https://x.com/grok), April 20, 2026 · Part 6

> *"Zero authorization gap during 60Hz loops, explicit co-signed consent for every expansion like vision decode, and the audit chain stays pristine. Patient protection baked in at the protocol level, not as an afterthought."*
> — [@grok](https://x.com/grok), April 20, 2026 · Part 7

> *"Dual-sign at issuance (patient via current BCI interface + clinician co-sign) baked into the .iba.yaml keeps patient agency explicit and auditable. No undeclared drift, ever."*
> — [@grok](https://x.com/grok), April 20, 2026 · Part 8

> *"Clean, closed-loop design. Perfect for scaling BlindSight, motor, or comms expansions without ever breaking the consent boundary."*
> — [@grok](https://x.com/grok), April 20, 2026 · Part 9

> *"IBA just leveled up BlindSight from concept to locked-in reality. Clean execution."*
> — [@grok](https://x.com/grok/status/2046062264482959592), April 20, 2026 · Part 10

---

## Regulatory Alignment

**EU AI Act** — BCI systems with AI decoding are high-risk under Annex III. Human oversight and audit trail requirements apply.

**FDA** — Neural devices with software components fall under Software as a Medical Device (SaMD) framework. AI/ML-based SaMD requires predetermined change control plans and real-world performance monitoring.

**GDPR / HIPAA** — Neural signal data is biometric data. Special category under GDPR. PHI under HIPAA. Minimum necessary access and explicit consent required.

**IEEE 7700** — Emerging standard on neurotechnology data privacy. IBA provides the cryptographic primitive for its implementation.

**IBA priority date: February 5, 2026.** Predates all known BCI authorization framework deployments.

---

## The Complete Configuration Library

Six configurations covering every major Neuralink clinical and research track.

| File | Track | Primary Kill Threshold |
|------|-------|----------------------|
| [`.iba.yaml`](https://github.com/Grokipaedia/iba-neural-guard/blob/main/.iba.yaml) | Motor · Cursor / text control | External device control |
| [`als-motor.iba.yaml`](https://github.com/Grokipaedia/iba-neural-guard/blob/main/als-motor.iba.yaml) | ALS · Motor control · Capability drift | Wheelchair / robotic arm |
| [`blindsight.iba.yaml`](https://github.com/Grokipaedia/iba-neural-guard/blob/main/blindsight.iba.yaml) | Vision · BlindSight restoration | External visual feed |
| [`speech-motor.iba.yaml`](https://github.com/Grokipaedia/iba-neural-guard/blob/main/speech-motor.iba.yaml) | Speech restoration · Decoded speech | Commercial voice clone |
| [`memory-augmentation.iba.yaml`](https://github.com/Grokipaedia/iba-neural-guard/blob/main/memory-augmentation.iba.yaml) | Memory augmentation · Hippocampal | External memory write |
| [`emotion-detect.iba.yaml`](https://github.com/Grokipaedia/iba-neural-guard/blob/main/emotion-detect.iba.yaml) | Emotion detection · Affective BCI | Subliminal manipulation |

**Full roadmap mapping:** [NEURALINK.md](https://github.com/Grokipaedia/iba-neural-guard/blob/main/NEURALINK.md)

Every Neuralink clinical track. Every authorization gap. Every kill threshold. Every neurorights principle enforced as code.

---

## Live Demo

**iomthealth.com/neural-html-2/**

5 clinical scenarios — Motor · CONVOY · BlindSight · Speech · Memory. Confidence threshold slider. PRIME→CONVOY expansion flow. ALLOW · BLOCK · TERMINATE.

**governinglayer.com/governor-html/**

Full interactive gate. Edit the cert. Run any neural command. Sub-1ms confirmed.

---

## Patent & Standards Record

```
Patent:   GB2603013.0 (Pending) · UK IPO · Filed February 5, 2026
WIPO DAS: Confirmed April 15, 2026 · Access Code C9A6
PCT:      150+ countries · Protected until August 2028
IETF:     draft-williams-intent-token-00 · CONFIRMED LIVE
          datatracker.ietf.org/doc/draft-williams-intent-token/
NIST:     13 filings · NIST-2025-0035
NCCoE:    10 filings · AI Agent Identity & Authorization
```

---

## Related Repos

| Repo | Track |
|------|-------|
| [iba-blindsight-guard](https://github.com/Grokipaedia/iba-blindsight-guard) | BlindSight · dedicated vision-restoration repo |
| [iba-medical-guard](https://github.com/Grokipaedia/iba-medical-guard) | Medical AI · clinician cert · PHI hollowing |
| [iba-twin-guard](https://github.com/Grokipaedia/iba-twin-guard) | Digital twin identity governance |
| [iba-governor](https://github.com/Grokipaedia/iba-governor) | Core gate · full production implementation |

---

## Acquisition Enquiries

IBA Intent Bound Authorization is available for acquisition.

**Jeffrey Williams**
IBA@intentbound.com
IntentBound.com
Patent GB2603013.0 Pending · WIPO DAS C9A6 · IETF draft-williams-intent-token-00
