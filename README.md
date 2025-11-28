<!-- Full Page Multi-Layer Glass Layout | White & Gold | True Left Alignment -->

<div style="
    width:100%;
    padding:60px 0;
    background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(0,0,0,0.3));
    backdrop-filter: blur(16px);
">

<!-- Main Intro Glass -->
<div style="
    max-width:900px;
    padding:40px;
    background: rgba(255,255,255,0.08);
    border-radius:18px;
    border:1px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(18px);
    margin:auto;
    text-align:left;
">

<h1 style="color:white; font-weight:500; letter-spacing:0.3px;">
Student Researcher · Independent Security Learner
</h1>

<p style="font-size:15px; color:#d6bb6a; max-width:760px; line-height:1.7;">
I study cybersecurity through self learning, structured practice, and experiments on my own systems.  
I focus on understanding how attacks behave, writing minimal tools, and verifying concepts with real logs and traffic.  
My approach is simple. Learn the fundamentals, test everything, improve through repetition.
</p>

</div>



<!-- Stats Glass Card -->
<div style="
    max-width:900px;
    padding:32px;
    margin-top:32px;
    background: rgba(255,255,255,0.06);
    border-radius:18px;
    border:1px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(14px);
    margin:auto;
    text-align:left;
">

<h2 style="color:#ffffff; font-weight:500;">
Statistics
</h2>

<table style="width:100%; text-align:left;">
  <tr>
    <td width="50%" style="text-align:left;">
      <img height="170em" src="https://github-readme-stats.vercel.app/api?username=abisinraj&show_icons=true&hide_border=true&theme=transparent&title_color=d6bb6a&text_color=ffffff&icon_color=d6bb6a" />
    </td>
    <td width="50%" style="text-align:left;">
      <img height="170em" src="https://github-readme-stats.vercel.app/api/top-langs/?username=abisinraj&layout=compact&hide_border=true&theme=transparent&title_color=d6bb6a&text_color=ffffff" />
    </td>
  </tr>
</table>

<div style="margin-top:20px; text-align:left;">
  <img height="155em" src="https://github-readme-streak-stats.herokuapp.com/?user=abisinraj&theme=transparent&hide_border=true&ring=d6bb6a&fire=d6bb6a&currStreakLabel=d6bb6a&sideNums=ffffff&sideLabels=aaaaaa" />
</div>

</div>



<!-- FLOW Overview Glass -->
<div style="
    max-width:900px;
    padding:32px;
    margin-top:32px;
    background: rgba(255,255,255,0.08);
    border-radius:18px;
    border:1px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(16px);
    margin:auto;
    text-align:left;
">

<h2 style="color:#ffffff; font-weight:500;">
FLOW · Custom SIEM and Threat Analysis Framework
</h2>

<p style="color:#d6bb6a; line-height:1.7; max-width:780px;">
FLOW is a personal research environment for learning detection engineering.  
Every part is written manually to understand monitoring, correlation, and response at a low level.  
The framework provides a structured space for analyzing attacker behavior and improving defensive logic.
</p>

</div>



<!-- Capabilities Glass -->
<div style="
    max-width:900px;
    padding:32px;
    margin-top:32px;
    background: rgba(255,255,255,0.06);
    border-radius:18px;
    border:1px solid rgba(255,255,255,0.12);
    backdrop-filter: blur(12px);
    margin:auto;
    text-align:left;
">

<h2 style="color:#ffffff; font-weight:500;">
Detection Capabilities
</h2>

<div style="margin-top:12px; text-align:left;">

| Network Detection | Forensic Analysis |
|------------------|------------------|
| MITM identification | SHA 256 integrity checks |
| Tunneling analysis | Fuzzy hashing (ssdeep) |
| Reverse shell behavior | Signature comparison |
| Brute force heuristics | File behavior examination |

</div>

</div>



<!-- Implementation Glass -->
<div style="
    max-width:900px;
    padding:32px;
    margin-top:32px;
    background: rgba(255,255,255,0.05);
    border-radius:18px;
    border:1px solid rgba(255,255,255,0.12);
    backdrop-filter: blur(12px);
    margin:auto;
    text-align:left;
">

<h2 style="color:#ffffff; font-weight:500;">
Technical Implementation Example
</h2>

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

</div>



<!-- Skills Glass -->
<div style="
    max-width:900px;
    padding:32px;
    margin-top:32px;
    background: rgba(255,255,255,0.04);
    border-radius:18px;
    border:1px solid rgba(255,255,255,0.12);
    backdrop-filter: blur(10px);
    margin:auto;
    text-align:left;
">

<h2 style="color:#ffffff; font-weight:500;">
Technical Stack
</h2>

<div style="margin-top:10px;">
<img src="https://skillicons.dev/icons?i=python,bash,linux,git,mysql&theme=light" />
</div>

<p style="color:#d6bb6a; font-size:14px; margin-top:10px; max-width:780px;">
Focused on network defense, log analysis, malware behavior, and Python tooling for investigation and monitoring.
</p>

</div>



<!-- Contact Glass -->
<div style="
    max-width:900px;
    padding:32px;
    margin-top:32px;
    margin-bottom:60px;
    background: rgba(255,255,255,0.05);
    border-radius:18px;
    border:1px solid rgba(255,255,255,0.12);
    backdrop-filter: blur(12px);
    margin:auto;
    text-align:left;
">

<h2 style="color:#ffffff; font-weight:500;">
Contact
</h2>

<div style="margin-top:10px;">

<a href="https://www.linkedin.com/in/abisin-raj/">
<img src="https://img.shields.io/badge/LinkedIn-d6bb6a?style=flat&logo=linkedin&logoColor=000000" />
</a>

<a href="mailto:abisinraj04@gmail.com" style="margin-left:10px;">
<img src="https://img.shields.io/badge/Email-d6bb6a?style=flat&logo=gmail&logoColor=000000" />
</a>

</div>

<div style="margin-top:16px;">
<img src="https://komarev.com/ghpvc/?username=abisinraj&label=Profile+Views&color=d6bb6a&style=flat" />
</div>

</div>

</div>
