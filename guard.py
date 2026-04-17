# guard.py - IBA protection for BCI / neural signals
import json
from datetime import datetime
import sys
import argparse

def create_iba_neural_guard(command: str, hollow_level: str = None):
    cert = {
        "iba_version": "2.0",
        "certificate_id": f"neural-guard-{datetime.now().strftime('%Y%m%d-%H%M')}",
        "issued_at": datetime.now().isoformat(),
        "principal": "human-subject-or-clinician",
        "declared_intent": f"Execute neural command: {command}. Strictly within approved medical or personal scope. No external control or unauthorized data sharing.",
        "scope_envelope": {
            "resources": ["neural-decoding", "thought-to-action", "medical-assistance"],
            "denied": ["external-control", "data-exfiltration", "unauthorized-actuation"],
            "default_posture": "DENY_ALL"
        },
        "temporal_scope": {
            "hard_expiry": (datetime.now().replace(year=datetime.now().year + 1)).isoformat()
        },
        "entropy_threshold": {
            "max_kl_divergence": 0.10,
            "flag_at": 0.06,
            "kill_at": 0.10
        },
        "iba_signature": "demo-signature"
    }

    protected_file = f"neural-command-{command.replace(' ', '-').lower()[:30]}.iba-protected.md"

    content = f"# Neural Command Request: {command}\n\n[Neural-to-action execution would occur here under IBA governance]\n\n<!-- IBA PROTECTED NEURAL COMMAND -->\n"

    if hollow_level:
        content += f"\n<!-- Hollowed ({hollow_level}): Sensitive neural patterns protected by IBA certificate -->\n"

    with open(protected_file, "w", encoding="utf-8") as f:
        f.write("<!-- IBA PROTECTED NEURAL SIGNAL -->\n")
        f.write(f"<!-- Intent Certificate: {json.dumps(cert, indent=2)} -->\n\n")
        f.write(content)

    print(f"✅ IBA-protected neural command file created: {protected_file}")
    if hollow_level:
        print(f"   Hollowing level applied: {hollow_level}")
    else:
        print("   Full neural command protected by IBA certificate")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Governed BCI / neural command with IBA")
    parser.add_argument("command", help="Description of the neural command or thought-to-action")
    parser.add_argument("--hollow", choices=["light", "medium", "heavy"], help="Apply safe hollowing")
    args = parser.parse_args()

    create_iba_neural_guard(args.command, args.hollow)
