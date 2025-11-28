<div align="center">

<img src="https://readme-typing-svg.herokuapp.com/?font=Roboto+Mono&size=30&duration=4000&color=38BDF8&center=true&vCenter=true&width=600&height=70&lines=🛡️+Blue+Team+Operator;🔍+Security+Researcher;🐍+Python+Tool+Dev;⚡+Flow+Architect" alt="Animated Header" />

> **"To open the door, you have to make the door itself."**

<br />

<table>
  <tr>
    <td width="50%">
      <img height="165em" src="https://github-readme-stats.vercel.app/api?username=abisinraj&show_icons=true&theme=radical&hide_border=true&include_all_commits=true&count_private=true&cache_seconds=0" />
    </td>
    <td width="50%">
      <img height="165em" src="https://github-readme-stats.vercel.app/api/top-langs/?username=abisinraj&layout=compact&theme=radical&hide_border=true&langs_count=6" />
    </td>
  </tr>
</table>

<img height="160em" src="https://github-readme-streak-stats.herokuapp.com/?user=abisinraj&theme=radical&hide_border=true&background=0D1117" />

<br />
<br />

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">

<br />

### 🚀 **Featured Project: FLOW | Custom SIEM & Threat Hunting**

**Engineering detection logic from the ground up to master the art of defense.**

</div>

---

### 🧠 **Project Philosophy**

<p align="center">
  <i>FLOW is not just a tool; it's my research platform. By building a SIEM's core components manually, I deconstruct modern attacks to engineer more effective defenses.</i>
</p>

### 🔍 **Detection Capabilities**

<div align="center">

| **🚨 Active Threat Detection** | **🔍 Forensic & Static Analysis** |
|:-------------------------------|:----------------------------------|
| • MITM & Tunneling | • File Integrity (SHA-256) |
| • Reverse Shell Patterns | • Fuzzy Hashing |
| • Brute Force Heuristics | • Signature Database Matching |

</div>

### 🛠️ **Technical Implementation**

```python
#!/usr/bin/env python3
"""
FLOW Core Engine
Polymorphic Malware Detection using ssdeep fuzzy hashing
"""

import ssdeep
import hashlib
from core.alert_engine import AlertEngine


class PolymorphicDetector:
    def __init__(self, malware_db):
        """
        malware_db structure:
        {
            "<ssdeep_hash>": {
                "family": "MalwareFamilyName",
                "severity": "high",
                "source": "local-db"
            },
            ...
        }
        """
        self.malware_db = malware_db
        self.alert = AlertEngine()

    def sha256(self, path):
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()

    def fuzzy_hash(self, path):
        return ssdeep.hash_from_file(path)

    def detect(self, file_path):
        file_sha = self.sha256(file_path)
        file_fuzzy = self.fuzzy_hash(file_path)

        for known_hash, meta in self.malware_db.items():
            similarity = ssdeep.compare(file_fuzzy, known_hash)

            if similarity > 75:
                self.alert.send(
                    title="Polymorphic Malware Detected",
                    message=(
                        f"File: {file_path}\n"
                        f"SHA256: {file_sha}\n"
                        f"Matched family: {meta.get('family')}\n"
                        f"Similarity score: {similarity}"
                    ),
                    severity=meta.get("severity", "medium")
                )
                return {
                    "file": file_path,
                    "sha256": file_sha,
                    "fuzzy": file_fuzzy,
                    "match_family": meta.get("family"),
                    "similarity": similarity,
                    "result": "detected"
                }

        return {
            "file": file_path,
            "sha256": file_sha,
            "fuzzy": file_fuzzy,
            "result": "clean"
        }
```

---

### 🧰 **Operational Arsenal**

<div align="center">

<img src="https://skillicons.dev/icons?i=python,bash,linux,git,mysql" /><br />
**Core Stack**

<img src="https://img.shields.io/badge/Security-Blue_Team-111111?style=for-the-badge&logo=hackthebox&logoColor=green" />
<img src="https://img.shields.io/badge/Network-Wireshark-1679A7?style=for-the-badge&logo=wireshark&logoColor=white" />
<img src="https://img.shields.io/badge/Defense-SIEM_Dev-FF6B6B?style=for-the-badge&logo=elasticstack&logoColor=white" />

</div>

**Core Competencies:**

* 🛡️ Defensive Engineering
* 🔬 Malware Analysis
* 🌐 Network Forensics

---

### 📫 **Connect & Collaborate**

<div align="center">

<a href="https://www.linkedin.com/in/abisin-raj/">
<img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" />
</a>

<a href="mailto:abisinraj04@gmail.com">
<img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" />
</a>

<br />
<br />

<img src="https://komarev.com/ghpvc/?username=abisinraj&label=Profile%20Views&color=0e75b6&style=flat" alt="Profile Views" />

</div>
