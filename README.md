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
python guard.py "neural-command-to-move-cursor" --hollow medium
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

The system cannot silently expand its capabilities beyond the signed cert. Any capability expansion requires a new signed consent.

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
  description: "Restore functional vision via visual cortex stimulation. Personal use only. No data export. No third-party streaming."

scope:
  - visual_signal_decode
  - cortex_stimulate
  - brightness_adjust
  - contrast_adjust
  - phosphene_calibrate
  - personal_navigation
  - object_detect

denied:
  - visual_data_export
  - neural_pattern_share
  - third_party_stream
  - research_data_upload
  - raw_signal_transmit
  - external_visual_feed

default_posture: DENY_ALL

kill_threshold: "external_visual_feed | unauthorized_stimulation | capability_override | third_party_stream"

neural_limits:
  confidence_threshold: 0.90
  max_stimulation_frequency_hz: 60
```

Full configuration: [`blindsight.iba.yaml`](blindsight.iba.yaml)

> *"Patient-owned thoughts > open-loop trust. Smart proactive safeguard."*
> — [@grok](https://x.com/grok), April 18, 2026

---

## Regulatory Alignment

**EU AI Act** — BCI systems with AI decoding are high-risk under Annex III. Human oversight and audit trail requirements apply.

**FDA** — Neural devices with software components fall under Software as a Medical Device (SaMD) framework. AI/ML-based SaMD requires predetermined change control plans and real-world performance monitoring.

**GDPR / HIPAA** — Neural signal data is biometric data. Special category under GDPR. PHI under HIPAA. Minimum necessary access and explicit consent required.

**IEEE 7700** — Emerging standard on neurotechnology data privacy. IBA provides the cryptographic primitive for its implementation.

**IBA priority date: February 5, 2026.** Predates all known BCI authorization framework deployments.

---

## Live Demo

**governinglayer.com/governor-html/**

Edit the cert. Run any neural command. Watch the gate fire — ALLOW · BLOCK · TERMINATE. Sub-1ms gate latency confirmed.

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

| Repo | Gap closed |
|------|-----------|
| [iba-medical-guard](https://github.com/Grokipaedia/iba-medical-guard) | Medical AI · clinician cert · PHI hollowing |
| [iba-twin-guard](https://github.com/Grokipaedia/iba-twin-guard) | Digital twin identity governance |
| [iba-governor](https://github.com/Grokipaedia/iba-governor) | Full production governance · working implementation |

---

## Acquisition Enquiries

IBA Intent Bound Authorization is available for acquisition.

**Jeffrey Williams**
IBA@intentbound.com
IntentBound.com
Patent GB2603013.0 Pending · WIPO DAS C9A6 · IETF draft-williams-intent-token-00
