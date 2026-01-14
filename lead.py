import os
import json
from datetime import datetime

LEADS = "leads.json"

# Mock lead capture function
def mock_lead_capture(name, email, platform):
    info = {
        "name": name,
        "email": email,
        "platform": platform,
        "timestamp": datetime.now().isoformat()
    }

    if os.path.exists(LEADS):
        with open(LEADS, "r") as f:
            try:
                leads = json.load(f)
            except json.JSONDecodeError:
                leads = []
    else:
        leads = []

    leads.append(info)

    with open(LEADS, "w") as f:
        json.dump(leads, f, indent=2)

    print(f"Lead captured: {name}, {email}, {platform}")
    return "Lead captured successfully"