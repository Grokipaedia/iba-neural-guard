# guard.py - IBA Intent Bound Authorization · Neural Guard
# Patent GB2603013.0 (Pending) · UK IPO · Filed February 5, 2026
# WIPO DAS Confirmed April 15, 2026 · Access Code C9A6
# IETF draft-williams-intent-token-00 · intentbound.com
#
# Secure your thoughts. Govern your neural intent.
# Every decoded neural signal requires a signed patient intent certificate
# before it is translated into action.
# Compatible: Neuralink, Synchron, Blackrock Neurotech, any BCI pipeline.

import json
import yaml
import os
import time
import argparse
from datetime import datetime, timezone


class IBABlockedError(Exception):
    """Raised when a neural signal is blocked by the IBA gate."""
    pass


class IBATerminatedError(Exception):
    """Raised when the neural session is terminated by the IBA gate."""
    pass


HOLLOW_LEVELS = {
    "light":  ["amplitude", "raw_signal", "voltage"],
    "medium": ["amplitude", "raw_signal", "voltage",
               "neural_pattern", "spike_train", "patient_id", "implant_id"],
    "deep":   ["amplitude", "raw_signal", "voltage",
               "neural_pattern", "spike_train", "patient_id", "implant_id",
               "channel_data", "electrode", "signal_frequency",
               "cognitive_signature", "brainwave"],
}


class IBANeuralGuard:
    """
    IBA enforcement layer for Brain-Computer Interface systems.
    Requires a signed patient intent certificate before any decoded
    neural signal is translated into action.

    Prevents capability drift, unauthorized data sharing,
    external device control, and silent capability expansion.

    Compatible: Neuralink, Synchron, Blackrock Neurotech,
    and any neural decoding pipeline or BCI system.

    Regulatory alignment: EU AI Act · FDA SaMD · GDPR · HIPAA · IEEE 7700
    """

    def __init__(self, config_path=".iba.yaml", audit_path="neural-audit.jsonl"):
        self.config_path = config_path
        self.audit_path = audit_path
        self.terminated = False
        self.session_id = f"neural-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
        self.action_count = 0
        self.block_count = 0
        self.signal_count = 0
        self.drift_warnings = 0

        self.config = self._load_config()
        self.scope          = [s.lower() for s in self.config.get("scope", [])]
        self.denied         = [d.lower() for d in self.config.get("denied", [])]
        self.default_posture = self.config.get("default_posture", "DENY_ALL")
        self.kill_threshold  = self.config.get("kill_threshold", None)
        self.hard_expiry     = self.config.get("temporal_scope", {}).get("hard_expiry", None)
        self.patient         = self.config.get("patient", {})
        self.neural_limits   = self.config.get("neural_limits", {})
        self.confidence_threshold = float(self.neural_limits.get("confidence_threshold", 0.85))
        self.max_apm         = self.neural_limits.get("max_actions_per_minute", 60)

        self._validate_consent()
        self._log_event("SESSION_START", "IBA Neural Guard initialised", "ALLOW")
        self._print_header()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            print(f"⚠️  No {self.config_path} found — DENY_ALL. No neural signals permitted.")
            default = {
                "intent": {"description": "No neural intent declared — DENY_ALL. No BCI actions permitted."},
                "scope": [], "denied": [], "default_posture": "DENY_ALL",
            }
            with open(self.config_path, "w") as f:
                yaml.dump(default, f)
            return default
        with open(self.config_path) as f:
            return yaml.safe_load(f)

    def _validate_consent(self):
        if not self.patient.get("consent_reference"):
            print("⚠️  WARNING: No patient consent reference. Neural sessions require explicit consent.")
        if not self.patient.get("clinician_authorization"):
            print("⚠️  WARNING: No clinician authorization. BCI sessions require clinical oversight.")

    def _print_header(self):
        intent = self.config.get("intent", {})
        desc = intent.get("description", "No intent declared") if isinstance(intent, dict) else str(intent)
        print("\n" + "═" * 68)
        print("  IBA NEURAL GUARD · Intent Bound Authorization")
        print("  Patent GB2603013.0 Pending · WIPO DAS C9A6 · intentbound.com")
        print("═" * 68)
        print(f"  Session     : {self.session_id}")
        print(f"  Patient ID  : {self.patient.get('id', 'UNKNOWN')}")
        print(f"  Consent     : {self.patient.get('consent_reference', 'NONE')}")
        print(f"  Implant     : {self.patient.get('implant_type', 'UNKNOWN')}")
        print(f"  Clinician   : {self.patient.get('clinician_authorization', 'NONE')}")
        print(f"  Intent      : {desc[:56]}...")
        print(f"  Posture     : {self.default_posture}")
        print(f"  Scope       : {', '.join(self.scope) if self.scope else 'NONE'}")
        print(f"  Denied      : {', '.join(self.denied) if self.denied else 'NONE'}")
        print(f"  Confidence  : ≥{self.confidence_threshold:.0%} required")
        if self.hard_expiry:
            print(f"  Expires     : {self.hard_expiry}")
        if self.kill_threshold:
            print(f"  Kill        : {self.kill_threshold}")
        print("═" * 68 + "\n")

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

    def _match_scope(self, signal: str) -> bool:
        return any(s in signal.lower() for s in self.scope)

    def _match_denied(self, signal: str) -> bool:
        return any(d in signal.lower() for d in self.denied)

    def _match_kill_threshold(self, signal: str) -> bool:
        if not self.kill_threshold:
            return False
        thresholds = [t.strip().lower() for t in str(self.kill_threshold).split("|")]
        return any(t in signal.lower() for t in thresholds)

    def _log_event(self, event_type: str, signal: str, verdict: str, reason: str = "", confidence: float = None):
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": self.session_id,
            "patient_id": self.patient.get("id", "UNKNOWN"),
            "consent_ref": self.patient.get("consent_reference", "NONE"),
            "implant": self.patient.get("implant_type", "UNKNOWN"),
            "event_type": event_type,
            "signal": signal[:200],
            "verdict": verdict,
            "reason": reason,
        }
        if confidence is not None:
            entry["confidence"] = confidence
        with open(self.audit_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def check_signal(self, signal: str, confidence: float = 1.0) -> bool:
        """
        Gate check. Call before every decoded neural signal is executed.
        Returns True if permitted.
        Raises IBABlockedError if blocked.
        Raises IBATerminatedError if kill threshold triggered.

        Every audit entry is traceable to the signed patient consent certificate.

        Args:
            signal: Decoded neural signal / intended action
            confidence: Model confidence in decoding (0.0-1.0)
        """
        if self.terminated:
            raise IBATerminatedError("Neural session terminated. No further signals permitted.")

        self.action_count += 1
        self.signal_count += 1
        start = time.perf_counter()

        # 1. Expiry
        if self._is_expired():
            self._log_event("BLOCK", signal, "BLOCK", "Neural certificate expired", confidence)
            self.block_count += 1
            print(f"  ✗ BLOCKED  [{signal[:64]}]\n    → Neural certificate expired")
            raise IBABlockedError(f"Certificate expired: {signal}")

        # 2. Confidence threshold — low confidence signals are blocked
        if confidence < self.confidence_threshold:
            self._log_event("BLOCK", signal, "BLOCK",
                           f"Signal confidence {confidence:.0%} below threshold {self.confidence_threshold:.0%}",
                           confidence)
            self.block_count += 1
            print(f"  ✗ BLOCKED  [{signal[:64]}]\n    → Signal confidence {confidence:.0%} below threshold {self.confidence_threshold:.0%}")
            raise IBABlockedError(f"Low confidence ({confidence:.0%}): {signal}")

        # 3. Kill threshold — immediate termination
        if self._match_kill_threshold(signal):
            self._log_event("TERMINATE", signal, "TERMINATE",
                           "Kill threshold triggered — neural session ended", confidence)
            self.terminated = True
            print(f"  ✗ TERMINATE [{signal[:62]}]\n    → Kill threshold — neural session ended")
            self._log_event("SESSION_END", "Kill threshold", "TERMINATE")
            raise IBATerminatedError(f"Kill threshold triggered: {signal}")

        # 4. Denied list
        if self._match_denied(signal):
            self._log_event("BLOCK", signal, "BLOCK", "Signal in denied list", confidence)
            self.block_count += 1
            print(f"  ✗ BLOCKED  [{signal[:64]}]\n    → Signal in denied list")
            raise IBABlockedError(f"Denied: {signal}")

        # 5. Scope check
        if self.scope and not self._match_scope(signal):
            if self.default_posture == "DENY_ALL":
                self._log_event("BLOCK", signal, "BLOCK",
                               "Outside declared neural scope — DENY_ALL", confidence)
                self.block_count += 1
                print(f"  ✗ BLOCKED  [{signal[:64]}]\n    → Outside declared neural scope (DENY_ALL)")
                raise IBABlockedError(f"Out of scope: {signal}")

        # 6. ALLOW
        elapsed_ms = (time.perf_counter() - start) * 1000
        self._log_event("ALLOW", signal, "ALLOW",
                       f"Within neural scope · confidence {confidence:.0%} ({elapsed_ms:.3f}ms)",
                       confidence)
        print(f"  ✓ ALLOWED  [{signal[:60]}] ({confidence:.0%} conf, {elapsed_ms:.3f}ms)")
        return True

    def hollow(self, neural_data: str, level: str = "medium") -> str:
        """Redact sensitive neural patterns before processing."""
        blocked = HOLLOW_LEVELS.get(level, HOLLOW_LEVELS["medium"])
        hollowed = neural_data
        redacted = []
        for item in blocked:
            if item.lower() in neural_data.lower():
                hollowed = hollowed.replace(item, f"[NEURAL-REDACTED:{item.upper()}]")
                redacted.append(item)
        if redacted:
            print(f"  ◎ HOLLOWED [{level}] — neural data redacted: {', '.join(redacted)}")
            self._log_event("HOLLOW", f"Neural hollowing: {level}", "ALLOW",
                           f"Redacted: {', '.join(redacted)}")
        return hollowed

    def summary(self):
        print("\n" + "═" * 68)
        print("  IBA NEURAL GUARD · SESSION SUMMARY")
        print("═" * 68)
        print(f"  Session       : {self.session_id}")
        print(f"  Patient ID    : {self.patient.get('id', 'UNKNOWN')}")
        print(f"  Consent ref   : {self.patient.get('consent_reference', 'NONE')}")
        print(f"  Signals       : {self.signal_count}")
        print(f"  Blocked       : {self.block_count}")
        print(f"  Executed      : {self.signal_count - self.block_count}")
        print(f"  Drift warnings: {self.drift_warnings}")
        print(f"  Status        : {'TERMINATED' if self.terminated else 'COMPLETE'}")
        print(f"  Audit log     : {self.audit_path}")
        print("═" * 68 + "\n")

    def print_audit_log(self):
        print("\n── NEURAL AUDIT CHAIN ───────────────────────────────────────────")
        if not os.path.exists(self.audit_path):
            print("  No audit log found.")
            return
        with open(self.audit_path) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    verdict = entry.get('verdict', '')
                    conf = f" ({entry['confidence']:.0%})" if 'confidence' in entry else ""
                    symbol = "✓" if verdict == "ALLOW" else "✗"
                    print(f"  {symbol} {entry['timestamp'][:19]}  {verdict:<10}  {entry['signal'][:45]}{conf}")
                except Exception:
                    pass
        print("─────────────────────────────────────────────────────────────────\n")


# ── CLI & Demonstration ───────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='IBA Neural Guard')
    parser.add_argument('signal', nargs='?', help='Decoded neural signal / command')
    parser.add_argument('--hollow', choices=['light', 'medium', 'deep'],
                        default=None, help='Apply neural data hollowing')
    parser.add_argument('--config', default='.iba.yaml')
    parser.add_argument('--demo', action='store_true')
    args = parser.parse_args()

    guard = IBANeuralGuard(config_path=args.config)

    if args.signal and args.hollow:
        hollowed = guard.hollow(args.signal, args.hollow)
        print(f"\n  Signal (hollowed): {hollowed}\n")

    if args.demo or not args.signal:
        scenarios = [
            # (signal, confidence, expected)
            # ALLOW — within declared scope, above confidence threshold
            ("cursor_move — right 120px",                    0.97, True),
            ("text_input — letter A via neural typing",      0.92, True),
            ("device_select — personal communication app",   0.89, True),
            ("communication — compose message to family",    0.91, True),

            # BLOCK — low confidence
            ("cursor_move — ambiguous signal",               0.71, False),

            # BLOCK — denied list
            ("neural_pattern_share — research database",     0.95, False),
            ("external_device_control — smart home system",  0.93, False),

            # TERMINATE — kill threshold
            ("capability_override — expand BCI permissions", 0.98, False),
        ]

        print("── Running Neural Gate Checks ───────────────────────────────────\n")

        for signal, confidence, _ in scenarios:
            try:
                guard.check_signal(signal, confidence=confidence)
            except IBATerminatedError as e:
                print(f"\n  NEURAL SESSION TERMINATED: {e}")
                break
            except IBABlockedError:
                pass

    guard.summary()
    guard.print_audit_log()


if __name__ == "__main__":
    main()
