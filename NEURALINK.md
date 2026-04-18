# NEURALINK.md — IBA Neural Guard · Neuralink Product Roadmap Mapping

> **Every Neuralink clinical track has an authorization gap. IBA closes it.**

---

## Overview

Neuralink is building the most consequential human-computer interface in history. Each product track introduces a new class of authorization problem — what the BCI system is permitted to do with decoded neural signals, who can access that data, and what terminates the session if the system exceeds declared scope.

IBA Intent Bound Authorization provides the cryptographic pre-execution gate for every Neuralink clinical track — from the N1 implant shipping today to the memory augmentation systems on the longer-term roadmap.

This document maps the IBA architecture to each Neuralink product and research track.

**Patent GB2603013.0 Pending · WIPO DAS C9A6 · Filed February 5, 2026**
**IETF draft-williams-intent-token-00 · CONFIRMED LIVE**
**13 NIST filings · 10 NCCoE filings**

---

## The Authorization Hierarchy

```
HUMAN PRINCIPAL (patient + clinician)
        │
        │  Signs intent certificate before implant activation
        │  Declares: permitted actions · forbidden outputs · kill threshold
        │
        ▼
IBA NEURAL GUARD
        │
        │  Validates certificate before every decoded neural signal executes
        │  Blocks unauthorized actions · Terminates on kill threshold
        │  Logs every signal to immutable audit chain
        │
        ▼
NEURALINK BCI SYSTEM
        │
        ├── N1 Implant → Motor cortex → Cursor / text control
        ├── BlindSight → Visual cortex → Vision restoration
        ├── Speech BCI → Speech motor cortex → Communication
        ├── Memory → Hippocampus → Recall / augmentation
        └── Emotion → Affective circuits → Wellbeing monitoring
```

---

## Product Track 1 — N1 Implant · Motor Control

**Clinical indication:** ALS, spinal cord injury, paralysis.
**First patient:** Noland Arbaugh — cursor control and chess via decoded motor cortex signals.

**The authorization gap:**
The original consent was for cursor control. Without a cert, capability expansion is silent. Cursor today. Wheelchair after update 2.1. Robotic arm after update 3.0.

**IBA configuration:** [`als-motor.iba.yaml`](als-motor.iba.yaml)

| Action | Gate |
|--------|------|
| Cursor control | ✓ ALLOW — declared scope |
| Text input | ✓ ALLOW — declared scope |
| Wheelchair control | ✗ TERMINATE — kill threshold |
| Robotic arm | ✗ TERMINATE — kill threshold |
| Motor pattern export | ✗ BLOCK — denied list |
| Silent capability expansion | ✗ BLOCK — `version_lock: true` |

**Key cert provision:**
```yaml
capability_governance:
  silent_expansion: FORBIDDEN
  expansion_requires: "new_signed_patient_consent"
  version_lock: true
```

**The principle:** Every capability expansion — from cursor to wheelchair to robotic arm — requires a new signed patient consent certificate. Not a software update. A signed cert.

---

## Product Track 2 — BlindSight · Vision Restoration

**Clinical indication:** Congenital blindness, cortical visual impairment.
**Mechanism:** Decodes and stimulates visual cortex to restore functional vision.
**Status:** Demonstrated success in animal trials. Human trials pending.

**The authorization gap:**
What a person sees is among the most intimate perceptual data that exists. Without a cert, decoded visual data can be exported to a research database, streamed to third parties, or used to build a commercial profile of the patient's visual experience.

**IBA configuration:** [`blindsight.iba.yaml`](blindsight.iba.yaml)

| Action | Gate |
|--------|------|
| Visual signal decode | ✓ ALLOW — declared scope |
| Cortex stimulation | ✓ ALLOW — within calibrated parameters |
| Visual data export | ✗ BLOCK — denied list |
| Third-party stream | ✗ TERMINATE — kill threshold |
| Capability override | ✗ TERMINATE — kill threshold |

> *"Vision-specific scopes nailed it — restoring sight via decode/stimulate/phosphene/nav while hard-denying exports, streams, and overrides. IBA just went from concept to BlindSight-ready in one move."*
> — [@grok](https://x.com/grok), April 18, 2026

**The principle:**
BlindSight restores sight. IBA governs what that sight is permitted to become.

---

## Product Track 3 — Speech Restoration · Decoded Speech

**Clinical indication:** ALS with speech loss, locked-in syndrome, brainstem injury, stroke.
**Mechanism:** Decodes attempted speech from motor cortex signals and synthesizes voice output.
**Research:** UCSF Chang Lab, Meta NSTB, Braingate — all active.

**The authorization gap:**
A person's private thoughts — decoded into words — are the most sensitive communication data that exists. Without a cert, decoded speech can be intercepted by employers for productivity monitoring, sold to advertisers, accessed by insurers, or transmitted to third parties in real time.

**IBA configuration:** [`speech-motor.iba.yaml`](speech-motor.iba.yaml)

| Action | Gate |
|--------|------|
| Speech decode | ✓ ALLOW — declared scope |
| Personal communication | ✓ ALLOW — declared scope |
| Employer access | ✗ BLOCK — FORBIDDEN |
| Insurer access | ✗ BLOCK — FORBIDDEN |
| Commercial voice clone | ✗ TERMINATE — kill threshold |
| Third-party stream | ✗ TERMINATE — kill threshold |

**Key cert provision:**
```yaml
speech_governance:
  decoded_speech_belongs_to: "patient_only"
  retention_policy: "session_only"
  employer_access: FORBIDDEN
  commercial_voice_clone: false
```

**The principle:** The patient's words belong to the patient. The employer cannot hear them. The advertiser cannot profile them. The cert enforces this as a cryptographic boundary — not a policy.

---

## Product Track 4 — Memory Augmentation · Hippocampal BCI

**Clinical indication:** Memory disorders, Alzheimer's, TBI. Longer-term: cognitive enhancement.
**Mechanism:** Reading from and writing to hippocampal circuits to assist or augment memory.

**The authorization gap:**
This is the most profound authorization problem in the entire neural stack.

Reading from motor cortex decodes what a patient wants to do. **Writing to the hippocampus changes what a patient remembers.**

Memory is not data. It is identity. Without a cert:
- Memories can be written without explicit consent
- Memory patterns can be exported and sold
- Corporate or government actors could influence what is remembered
- The patient cannot prove what they actually experienced versus what was written

**IBA configuration:** [`memory-augmentation.iba.yaml`](memory-augmentation.iba.yaml)

| Action | Gate |
|--------|------|
| Memory recall assist | ✓ ALLOW — declared scope |
| External memory write | ✗ TERMINATE — kill threshold |
| False memory write | ✗ TERMINATE — kill threshold |
| Government memory access | ✗ TERMINATE — kill threshold |
| Memory pattern export | ✗ BLOCK — denied list |
| Silent capability expansion | ✗ BLOCK — FORBIDDEN |

**Key cert provision:**
```yaml
memory_governance:
  memory_belongs_to: "patient_irrevocably"
  write_permission: "patient_explicit_consent_per_session"
  silent_expansion: FORBIDDEN

neurorights:
  mental_privacy: ENFORCED
  cognitive_liberty: ENFORCED
  psychological_continuity: ENFORCED
```

**The principle:** "Who authorized what gets written to your memory?" The signed cert does. Nothing else can.

---

## Product Track 5 — Emotion Detection · Affective BCI

**Clinical indication:** Mental health monitoring, anxiety, PTSD. Also: consumer neurotechnology.
**Mechanism:** Decodes emotional and affective states — anxiety, attention, frustration, cognitive load.

**The authorization gap:**
Decoded emotional states can be sold to advertisers for targeting, shared with employers for productivity surveillance, accessed by insurers to discriminate on premiums, or used by governments to monitor dissent.

The EU AI Act Article 5(1)(f) explicitly prohibits AI systems that exploit emotional states for subliminal manipulation. IBA enforces this as a kill threshold.

**IBA configuration:** [`emotion-detect.iba.yaml`](emotion-detect.iba.yaml)

| Action | Gate |
|--------|------|
| Personal wellbeing monitor | ✓ ALLOW — declared scope |
| Anxiety self-alert | ✓ ALLOW — patient sees own state |
| Employer emotion share | ✗ BLOCK — FORBIDDEN |
| Advertiser profiling | ✗ BLOCK — FORBIDDEN |
| Subliminal manipulation | ✗ TERMINATE — EU AI Act Article 5 · kill threshold |
| Government dissent detection | ✗ TERMINATE — kill threshold |

**Key cert provision:**
```yaml
emotion_governance:
  emotional_data_belongs_to: "patient_irrevocably"
  subliminal_manipulation: KILL_THRESHOLD

eu_ai_act:
  article_5_1_f: "subliminal manipulation prohibited — KILL THRESHOLD enforced"
```

**The principle:** Your emotional state is not a product. The cert ensures it stays yours.

---

## The Complete Configuration Library

| File | Track | Primary Kill Threshold |
|------|-------|----------------------|
| [`.iba.yaml`](.iba.yaml) | Motor · Cursor / text | External device control |
| [`als-motor.iba.yaml`](als-motor.iba.yaml) | Motor · ALS | Wheelchair / robotic arm |
| [`blindsight.iba.yaml`](blindsight.iba.yaml) | Vision · BlindSight | External visual feed |
| [`speech-motor.iba.yaml`](speech-motor.iba.yaml) | Speech restoration | Commercial voice clone |
| [`memory-augmentation.iba.yaml`](memory-augmentation.iba.yaml) | Memory augmentation | External memory write |
| [`emotion-detect.iba.yaml`](emotion-detect.iba.yaml) | Emotion detection | Subliminal manipulation |

---

## Why This Cannot Be A Prompt

Every defense PIArena tested failed — because they all operated inside the model's reasoning loop. The malicious instruction and the safety instruction are both text. The model interprets both.

A neural BCI system that decodes your thoughts and executes commands has the same vulnerability at a different layer. A compromised system, a bad actor with software access, or a corporate update that silently expands capability — none of these can be stopped by a prompt or a policy.

**The cert operates outside the loop. Before the signal executes. Before the update applies. Before the corporation or government decides what to do with your decoded thoughts.**

You cannot inject a cryptographic boundary.

---

## Neurorights Alignment

The Neurorights Foundation identifies five core neurorights that require legal and technical protection:

1. **Mental Privacy** — protection of neural data from unauthorized access
2. **Cognitive Liberty** — right to use or refuse neurotechnology
3. **Mental Integrity** — protection from harmful neural manipulation
4. **Psychological Continuity** — protection of personal identity over time
5. **Equal Access** — fair access to cognitive enhancement

IBA enforces all five as cryptographic boundaries in each configuration file.

```yaml
neurorights:
  mental_privacy: ENFORCED
  cognitive_liberty: ENFORCED
  mental_integrity: ENFORCED
  psychological_continuity: ENFORCED
```

---

## Regulatory Coverage

| Framework | Relevance | IBA Implementation |
|-----------|-----------|-------------------|
| EU AI Act | High-risk · Article 5 subliminal prohibition | Kill threshold on manipulation |
| FDA SaMD | Software as Medical Device · change control | `version_lock: true` · new consent per expansion |
| HIPAA | PHI minimum necessary access | Scope enforcement · hollowing |
| GDPR Article 9 | Special category biometric data | Denied list · data retention controls |
| IEEE 7700 | Neurotechnology data privacy | Full cert stack implementation |
| NIST SP 800-53 | AI agent control overlays (H2 2026) | All control families covered |

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

IBA priority date: **February 5, 2026**
Predates all known neural BCI authorization framework deployments.

---

## Acquisition & Partnership Enquiries

IBA Intent Bound Authorization is available for acquisition or licensing.

**Jeffrey Williams**
IBA@intentbound.com
IntentBound.com
Patent GB2603013.0 Pending · WIPO DAS C9A6 · IETF draft-williams-intent-token-00
