"""All Jev question wording lives here. The description (state) is the only thing that varies.

One Choice per CVSS v3.1 base metric. Option names are descriptive (the skill warns that
positional/letter names can bias answers); OPTION_TO_LETTER maps them back to vector letters.
Criteria paraphrase the FIRST CVSS v3.1 specification definitions.
"""
from typesafe_sdk import Choice

STATE_KEY = "vulnerability_description"


def state(description: str) -> dict:
    return {STATE_KEY: description.strip()}


D = f"`{STATE_KEY}`"

METRICS = {
    "AV": Choice(
        instructions=f"In {D}, from where must an attacker act to exploit the vulnerability?",
        criteria={
            "network": "Exploitable remotely across the internet or other routed networks.",
            "adjacent_network": "Requires being on the same physical or logical local network segment, such as the same Wi-Fi, Bluetooth range, or LAN.",
            "local": "Requires local access to the system: a local login or shell, or tricking a local user into opening a file.",
            "physical": "Requires physically touching or manipulating the device.",
        },
    ),
    "AC": Choice(
        instructions=f"In {D}, does a successful attack depend on conditions outside the attacker's control?",
        criteria={
            "low": "No special conditions; the attacker can succeed repeatedly at will.",
            "high": "Success depends on conditions the attacker cannot control, such as winning a race condition, gathering target-specific secrets, or being positioned in the network path (man-in-the-middle).",
        },
    ),
    "PR": Choice(
        instructions=f"In {D}, what privileges must the attacker already have before the attack?",
        criteria={
            "none": "No account or authentication needed.",
            "low": "A basic user account or privileges limited to the attacker's own resources.",
            "high": "Administrative or significant control over the vulnerable component.",
        },
    ),
    "UI": Choice(
        instructions=f"In {D}, must a person other than the attacker take some action for the attack to succeed?",
        criteria={
            "none": "The attack succeeds without any action from another user.",
            "required": "Another user must take an action, such as clicking a link, opening a file, or visiting a page.",
        },
    ),
    "S": Choice(
        instructions=f"In {D}, can the attack affect resources beyond the vulnerable component's own security authority?",
        criteria={
            "unchanged": "Impact stays within the vulnerable component, governed by the same security authority.",
            "changed": "Impact reaches components under a different security authority, such as escaping a sandbox or VM, or a web app flaw that runs script in other users' browsers.",
        },
    ),
    "C": Choice(
        instructions=f"In {D}, how much confidential information can the attacker read?",
        criteria={
            "high": "Total loss of confidentiality, or disclosure of highly sensitive data such as passwords or keys.",
            "low": "Some restricted information is disclosed, but the attacker does not control what or how much, and it is not serious.",
            "none": "No information is disclosed.",
        },
    ),
    "I": Choice(
        instructions=f"In {D}, how much can the attacker modify data or system behavior?",
        criteria={
            "high": "Total loss of integrity: the attacker can modify any or all protected data, or modifications have serious consequences.",
            "low": "Some data can be modified, but with limited control or no serious consequences.",
            "none": "No data can be modified.",
        },
    ),
    "A": Choice(
        instructions=f"In {D}, how much can the attacker reduce availability of the affected component?",
        criteria={
            "high": "Total loss of availability, or a serious sustained or persistent denial of service.",
            "low": "Reduced performance or interruptions, but not a complete or serious denial of service.",
            "none": "No impact on availability.",
        },
    ),
}

OPTION_TO_LETTER = {
    "AV": {"network": "N", "adjacent_network": "A", "local": "L", "physical": "P"},
    "AC": {"low": "L", "high": "H"},
    "PR": {"none": "N", "low": "L", "high": "H"},
    "UI": {"none": "N", "required": "R"},
    "S": {"unchanged": "U", "changed": "C"},
    "C": {"high": "H", "low": "L", "none": "N"},
    "I": {"high": "H", "low": "L", "none": "N"},
    "A": {"high": "H", "low": "L", "none": "N"},
}
