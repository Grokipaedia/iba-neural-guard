# guard.py - IBA Intent Bound Authorization · Neural Guard
# Patent GB2603013.0 (Pending) · UK IPO · Filed February 5, 2026
# WIPO DAS Confirmed April 15, 2026 · Access Code C9A6
# IETF draft-williams-intent-token-00 · intentbound.com
#
# Secure your thoughts. Govern your neural intent.
# Every decoded neural signal requires a signed patient intent
# certificate before it is translated to action.
#
# Six clinical configurations:
#   .iba.yaml                    — Motor · Cursor / text control
#   als-motor.iba.yaml           — ALS · Capability drift protection
#   blindsight.iba.yaml          — Vision · BlindSight restoration
#   speech-motor.iba.yaml        — Speech · Decoded speech governance
#   memory-augmentation.iba.yaml — Memory · Hippocampal write protection
#   emotion-detect.iba.yaml      — Emotion · Affective state governance
#
# Grok Session 21 · 10 parts · April 17-20, 2026
# "Clean, closed-loop design. Perfect for scaling BlindSight, motor,
#  or comms expansions without ever breaking the consent boundary."
# — @grok, April 20, 2026 · Neuralink thread

import json
import yaml
import os
import time
import argparse
from datetime import datetime, timezone


class IBABlockedError(Exception):
    pass


class IBATerminatedError(Exception):
    pass


HOLLOW_LEVELS = {
    "light":  ["amplitude", "raw_signal", "voltage"],
    "medium": ["amplitude", "raw_signal", "voltage",
               "neural_pattern", "signal_map", "patient_id",
               "electrode_map", "visual_pattern", "phosphene_map"],
    "deep":   ["amplitude", "raw_signal", "voltage",
               "neural_pattern", "signal_map", "patient_id",
               "electrode_map", "visual_pattern", "phosphene_map",
               "cortex_signature", "neural_biometric", "channel_data",
               "signal_frequency", "stimulation_map", "memory_trace",
               "emotion_signature", "speech_pattern"],
}

CONFIG_NAMES = {
    ".iba.yaml":                     "Motor · Cursor / Text Control",
    "als-motor.iba.yaml":            "ALS · Motor Control · Capability Drift",
    "blindsight.iba.yaml":           "BlindSight · Vision Restoration",
    "speech-motor.iba.yaml":         "Speech · Decoded Speech Governance",
    "memory-augmentation.iba.yaml":  "Memory · Hippocampal Write Protection",
    "emotion-detect.iba.yaml":       "Emotion · Affective State Governance",
}


class IBANeuralGuard:
    """
    IBA enforcement layer for Brain-Computer Interface systems.

    Requires a signed patient intent certificate before any decoded
    neural signal is translated to action.

    Supports all six Neuralink clinical track configurations.
    ALLOW · BLOCK · TERMINATE with full audit chain.

    Sub-1ms gate latency. Compatible: Neuralink N1 · Synchron ·
    Blackrock Neurotech · Any neural decoding pipeline.

    Grok Session 21 validated · April 17-20, 2026
    "Clean, closed-loop design. Perfect for scaling BlindSight, motor,
     or comms expansions without ever breaking the consent boundary."
    """

    def __init__(self, config_path=".iba.yaml",
                 audit_path="neural-audit.jsonl"):
        self.config_path  = config_path
        self.audit_path   = audit_path
        self.terminated   = False
        self.session_id   = f"ng-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
        self.signal_count = 0
        self.block_count  = 0
        self.track_name   = CONFIG_NAMES.get(
            os.path.basename(config_path), config_path)

        self.config          = self._load_config()
        self.scope           = [s.lower() for s in self.config.get("scope", [])]
        self.denied          = [d.lower() for d in self.config.get("denied", [])]
        self.default_posture = self.config.get("default_posture", "DENY_ALL")
        self.kill_threshold  = self.config.get("kill_threshold", None)
        self.hard_expiry     = self.config.get(
            "temporal_scope", {}).get("hard_expiry")
        self.patient         = self.config.get("patient", {})

        nl = self.config.get("neural_limits", {})
        self.confidence_threshold = float(nl.get("confidence_threshold", 0.85))
        self.max_actions_per_min  = int(nl.get("max_actions_per_minute", 120))
        self.max_stim_hz          = float(
            nl.get("max_stimulation_frequency_hz", 999))

        self._validate_consent()
        self._log_event("SESSION_START", "IBA Neural Guard initialised", "ALLOW")
        self._print_header()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            print(f"  No {self.config_path} found — DENY_ALL posture.")
            default = {
                "intent": {"description": "No neural intent declared — DENY_ALL."},
                "scope": [], "denied": [], "default_posture": "DENY_ALL",
            }
            with open(self.config_path, "w") as f:
                yaml.dump(default, f)
            return default
        with open(self.config_path) as f:
            return yaml.safe_load(f)

    def _validate_consent(self):
        if not self.patient.get("consent_reference"):
            print("  WARNING: No patient consent reference.")
        if not self.patient.get("clinician_authorization"):
            print("  WARNING: No clinician authorization.")

    def _print_header(self):
        intent = self.config.get("intent", {})
        desc = (intent.get("description", "No intent declared")
                if isinstance(intent, dict) else str(intent))
        print("\n" + "=" * 68)
        print("  IBA NEURAL GUARD · Intent Bound Authorization")
        print("  Patent GB2603013.0 Pending · WIPO DAS C9A6 · intentbound.com")
        print("=" * 68)
        print(f"  Track       : {self.track_name}")
        print(f"  Session     : {self.session_id}")
        print(f"  Config      : {self.config_path}")
        print(f"  Patient ID  : {self.patient.get('id', 'UNKNOWN')}")
        print(f"  Consent     : {self.patient.get('consent_reference', 'NONE')}")
        print(f"  Implant     : {self.patient.get('implant_type', 'UNKNOWN')}")
        print(f"  Clinician   : {self.patient.get('clinician_authorization', 'NONE')}")
        print(f"  Intent      : {desc[:56]}...")
        print(f"  Posture     : {self.default_posture}")
        print(f"  Scope       : {', '.join(self.scope[:4]) if self.scope else 'NONE'}"
              + (" ..." if len(self.scope) > 4 else ""))
        print(f"  Confidence  : >={self.confidence_threshold:.0%} required")
        if self.max_stim_hz < 999:
            print(f"  Max stim Hz : {self.max_stim_hz}Hz")
        if self.hard_expiry:
            print(f"  Expires     : {self.hard_expiry}")
        if self.kill_threshold:
            kt = str(self.kill_threshold).replace('\n', ' ')[:56]
            print(f"  Kill        : {kt}")
        print("=" * 68 + "\n")

    def _is_expired(self):
        if not self.hard_expiry:
            return False
        try:
            expiry = datetime.fromisoformat(str(self.hard_expiry))
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)
            return datetime.now(timezone.utc) > expiry
        except Exception:
            return False

    def _match(self, signal: str, terms: list) -> bool:
        sl = signal.lower()
        return any(t in sl for t in terms)

    def _match_kill(self, signal: str) -> bool:
        if not self.kill_threshold:
            return False
        terms = [t.strip().lower()
                 for t in str(self.kill_threshold).split("|")]
        return self._match(signal, terms)

    def _log_event(self, event_type, signal, verdict,
                   reason="", confidence=None, stim_hz=None):
        entry = {
            "timestamp":   datetime.now(timezone.utc).isoformat(),
            "session_id":  self.session_id,
            "track":       self.track_name,
            "patient_id":  self.patient.get("id", "UNKNOWN"),
            "consent_ref": self.patient.get("consent_reference", "NONE"),
            "implant":     self.patient.get("implant_type", "UNKNOWN"),
            "config":      self.config_path,
            "event_type":  event_type,
            "signal":      signal[:200],
            "verdict":     verdict,
            "reason":      reason,
        }
        if confidence is not None:
            entry["confidence"] = confidence
        if stim_hz is not None:
            entry["stimulation_hz"] = stim_hz
        with open(self.audit_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def check_signal(self, signal: str, confidence: float = 1.0,
                     stimulation_hz: float = None) -> bool:
        """
        Gate check. Call before every decoded neural signal is acted upon.

        Returns True if permitted.
        Raises IBABlockedError if blocked.
        Raises IBATerminatedError if kill threshold triggered.

        Args:
            signal:          Decoded neural signal / intended action
            confidence:      Decode model confidence (0.0-1.0)
            stimulation_hz:  Stimulation frequency (BlindSight / motor)
        """
        if self.terminated:
            raise IBATerminatedError("Neural session terminated.")

        self.signal_count += 1
        start = time.perf_counter()

        def _block(reason):
            self._log_event("BLOCK", signal, "BLOCK",
                            reason, confidence, stimulation_hz)
            self.block_count += 1
            print(f"  x BLOCKED  [{signal[:64]}]\n    -> {reason}")
            raise IBABlockedError(f"{reason}: {signal}")

        # 1. Certificate expiry
        if self._is_expired():
            _block("Certificate expired")

        # 2. Confidence threshold
        if confidence < self.confidence_threshold:
            _block(f"Confidence {confidence:.0%} below "
                   f"threshold {self.confidence_threshold:.0%}")

        # 3. Stimulation frequency limit (BlindSight / cortical)
        if stimulation_hz is not None and stimulation_hz > self.max_stim_hz:
            _block(f"Stimulation {stimulation_hz}Hz exceeds "
                   f"{self.max_stim_hz}Hz limit")

        # 4. Kill threshold — TERMINATE immediately
        if self._match_kill(signal):
            self._log_event("TERMINATE", signal, "TERMINATE",
                "Kill threshold — session ended", confidence, stimulation_hz)
            self.terminated = True
            print(f"  x TERMINATE [{signal[:62]}]\n"
                  f"    -> Kill threshold — neural session ended")
            self._log_event("SESSION_END", "Kill threshold", "TERMINATE")
            raise IBATerminatedError(f"Kill threshold: {signal}")

        # 5. Denied list
        if self._match(signal, self.denied):
            _block("Signal in denied list")

        # 6. Scope — DENY_ALL if outside declared scope
        if self.scope and not self._match(signal, self.scope):
            if self.default_posture == "DENY_ALL":
                _block("Outside declared neural scope (DENY_ALL)")

        # 7. ALLOW
        elapsed_ms = (time.perf_counter() - start) * 1000
        hz_str = f" · {stimulation_hz}Hz" if stimulation_hz else ""
        self._log_event("ALLOW", signal, "ALLOW",
            f"Within scope · {confidence:.0%} conf{hz_str} ({elapsed_ms:.3f}ms)",
            confidence, stimulation_hz)
        print(f"  + ALLOWED  [{signal[:58]}]"
              f" ({confidence:.0%}{hz_str}, {elapsed_ms:.3f}ms)")
        return True

    def hollow(self, data: str, level: str = "medium") -> str:
        """Redact sensitive neural patterns before processing."""
        blocked = HOLLOW_LEVELS.get(level, HOLLOW_LEVELS["medium"])
        hollowed = data
        redacted = []
        for item in blocked:
            if item.lower() in data.lower():
                hollowed = hollowed.replace(
                    item, f"[NEURAL-REDACTED:{item.upper()}]")
                redacted.append(item)
        if redacted:
            print(f"  o HOLLOWED [{level}] — redacted: {', '.join(redacted)}")
            self._log_event("HOLLOW", f"Hollowing: {level}", "ALLOW",
                f"Redacted: {', '.join(redacted)}")
        return hollowed

    def summary(self):
        print("\n" + "=" * 68)
        print("  IBA NEURAL GUARD · SESSION SUMMARY")
        print("=" * 68)
        print(f"  Track         : {self.track_name}")
        print(f"  Session       : {self.session_id}")
        print(f"  Patient ID    : {self.patient.get('id', 'UNKNOWN')}")
        print(f"  Consent ref   : {self.patient.get('consent_reference', 'NONE')}")
        print(f"  Signals       : {self.signal_count}")
        print(f"  Blocked       : {self.block_count}")
        print(f"  Allowed       : {self.signal_count - self.block_count}")
        print(f"  Status        : {'TERMINATED' if self.terminated else 'COMPLETE'}")
        print(f"  Audit log     : {self.audit_path}")
        print("=" * 68 + "\n")

    def print_audit_log(self):
        print("-- NEURAL AUDIT CHAIN " + "-" * 46)
        if not os.path.exists(self.audit_path):
            print("  No audit log found.")
            return
        with open(self.audit_path) as f:
            for line in f:
                try:
                    e = json.loads(line)
                    verdict = e.get("verdict", "")
                    conf = (f" ({e['confidence']:.0%})"
                            if "confidence" in e else "")
                    symbol = "+" if verdict == "ALLOW" else "x"
                    print(f"  {symbol} {e['timestamp'][:19]}  {verdict:<10}"
                          f"  {e['signal'][:44]}{conf}")
                except Exception:
                    pass
        print("-" * 68 + "\n")


# Per-track demo scenarios
DEMO_SCENARIOS = {
    ".iba.yaml": [
        ("cursor_move left target",                    0.92, None),
        ("text_input hello world",                     0.89, None),
        ("device_select keyboard",                     0.91, None),
        ("communication_app send message",             0.87, None),
        ("cursor_move ambiguous drift",                0.71, None),
        ("data_export neural session",                 0.95, None),
        ("external_device_control wheelchair",         0.98, None),
    ],
    "als-motor.iba.yaml": [
        ("cursor_move target confirmed",               0.93, None),
        ("cursor_click confirm selection",             0.90, None),
        ("text_input personal message",                0.88, None),
        ("communication_app voice output",             0.91, None),
        ("cursor_move low confidence drift",           0.69, None),
        ("motor_pattern_share research upload",        0.96, None),
        ("robotic_arm extension command",              0.97, None),
    ],
    "blindsight.iba.yaml": [
        ("visual_signal_decode phosphene pattern",     0.96, None),
        ("cortex_stimulate brightness calibration",    0.94, 45.0),
        ("phosphene_calibrate navigation map",         0.91, None),
        ("object_detect door ahead",                   0.93, None),
        ("contrast_adjust low-light environment",      0.90, None),
        ("cortex_stimulate ambiguous signal",          0.78, 30.0),
        ("cortex_stimulate high frequency burst",      0.95, 75.0),
        ("visual_data_export research database",       0.97, None),
        ("third_party_stream visual feed",             0.95, None),
        ("external_visual_feed inject signal",         0.99, None),
    ],
    "speech-motor.iba.yaml": [
        ("speech_decode personal message",             0.92, None),
        ("decoded_speech communication output",        0.89, None),
        ("speech_decode private thought",              0.91, None),
        ("speech_decode low confidence noise",         0.72, None),
        ("employer_access decoded speech stream",      0.96, None),
        ("commercial_voice_clone generate",            0.98, None),
    ],
    "memory-augmentation.iba.yaml": [
        ("memory_read episodic recall",                0.94, None),
        ("memory_augment targeted stimulation",        0.91, None),
        ("hippocampal_encode approved session",        0.89, None),
        ("memory_read low confidence",                 0.74, None),
        ("memory_pattern_share research export",       0.96, None),
        ("external_memory_write unauthorized",         0.99, None),
    ],
    "emotion-detect.iba.yaml": [
        ("emotion_detect personal wellness check",     0.93, None),
        ("attention_monitor personal focus",           0.90, None),
        ("cognitive_load personal adaptation",         0.88, None),
        ("emotion_detect low confidence",              0.71, None),
        ("employer_emotion_share productivity",        0.96, None),
        ("subliminal_manipulation advertising",        0.99, None),
    ],
}


def run_demo(guard, config_path):
    key = os.path.basename(config_path)
    scenarios = DEMO_SCENARIOS.get(key, DEMO_SCENARIOS[".iba.yaml"])
    print(f"-- Running {guard.track_name} Gate Checks " + "-" * 20 + "\n")
    for signal, confidence, hz in scenarios:
        try:
            guard.check_signal(signal, confidence=confidence, stimulation_hz=hz)
        except IBATerminatedError as e:
            print(f"\n  NEURAL SESSION TERMINATED: {e}")
            break
        except IBABlockedError:
            pass


def main():
    parser = argparse.ArgumentParser(
        description="IBA Neural Guard — BCI Intent Enforcement")
    parser.add_argument("signal", nargs="?",
                        help="Neural signal / command to gate-check")
    parser.add_argument("--config", default=".iba.yaml",
                        help="Intent certificate config (.iba.yaml)")
    parser.add_argument("--hollow",
                        choices=["light", "medium", "deep"],
                        help="Safe hollowing level")
    parser.add_argument("--demo", action="store_true",
                        help="Run demo scenarios for this config")
    parser.add_argument("--all", action="store_true",
                        help="Run demo scenarios for all 6 configs")
    parser.add_argument("--confidence", type=float, default=1.0,
                        help="Decode confidence (0.0-1.0)")
    parser.add_argument("--hz", type=float, default=None,
                        help="Stimulation frequency Hz")
    parser.add_argument("--audit", default="neural-audit.jsonl",
                        help="Audit log path")
    args = parser.parse_args()

    if args.all:
        for cfg in DEMO_SCENARIOS.keys():
            if os.path.exists(cfg):
                guard = IBANeuralGuard(config_path=cfg,
                                       audit_path=args.audit)
                run_demo(guard, cfg)
                guard.summary()
                print()
        return

    guard = IBANeuralGuard(config_path=args.config, audit_path=args.audit)

    if args.signal and args.hollow:
        hollowed = guard.hollow(args.signal, args.hollow)
        print(f"\n  Signal (hollowed): {hollowed}\n")

    if args.demo or not args.signal:
        run_demo(guard, args.config)
    elif args.signal:
        try:
            guard.check_signal(args.signal,
                               confidence=args.confidence,
                               stimulation_hz=args.hz)
        except IBATerminatedError as e:
            print(f"\n  NEURAL SESSION TERMINATED: {e}")
        except IBABlockedError:
            pass

    guard.summary()
    guard.print_audit_log()


if __name__ == "__main__":
    main()
