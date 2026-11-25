# WSProbe

**A Python-based WebSocket security testing tool for controlled localhost environments.**

WSProbe is an educational security-testing utility that helps developers and cybersecurity learners observe how a WebSocket service handles Origin validation, authentication, malformed JSON payloads, unexpected JSON data types, and oversized frames.

> **Safety scope:** WSProbe intentionally restricts scan targets to loopback addresses (`localhost`, `127.0.0.1`, and `::1`). Use it only against services you own or are explicitly authorized to test. It is designed for local labs and learning, not for scanning public systems.

## Key capabilities

- Validates that scan targets use an allowed localhost address.
- Tests baseline WebSocket behavior.
- Checks handling of trusted, foreign, and missing `Origin` headers.
- Checks behavior when an authentication token is missing.
- Sends valid JSON, malformed JSON, unexpected JSON arrays/numbers, and oversized frames.
- Classifies observed responses and exports a machine-readable JSON report.
- Includes a local WebSocket lab server, Windows helper scripts, and unit tests.

## Project layout

```text
WSProbe/
├── docs/
│   ├── INSTALLATION_WINDOWS_URDU.md
│   └── WSProbe_Presentation.pdf
├── reports/
│   └── sample-report.json
├── tests/
│   ├── test_classifier.py
│   └── test_scanner.py
├── wsprobe/
│   ├── __init__.py
│   ├── classifier.py
│   ├── lab_server.py
│   └── scanner.py
├── .gitignore
├── CONTRIBUTING.md
├── SECURITY.md
├── requirements.txt
├── run_lab_server.bat
└── run_wsprobe.bat
```

## Requirements

- Python 3.10 or newer
- pip
- Dependency pinned in `requirements.txt`: `websockets==15.0.1`

## Installation

```bash
git clone https://github.com/wini12350/wsprobe.git
cd wsprobe
python -m venv .venv
```

Activate the virtual environment:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the local lab

Start the intentionally local lab server in one terminal:

```bash
python -m wsprobe.lab_server
```

The lab server listens on `127.0.0.1:8765` by default. In a second terminal, activate the same virtual environment and run:

```bash
python -m wsprobe.scanner ws://127.0.0.1:8765 --token lab-token --report reports/my-report.json
```

The included `lab-token` is a demonstration value for the local lab only. Do not reuse it in a real application.

Windows users can also use `run_lab_server.bat` and `run_wsprobe.bat`; see [the Urdu Windows installation guide](docs/INSTALLATION_WINDOWS_URDU.md).

## Run tests

```bash
python -m unittest discover -s tests -v
```

The project test suite contains seven unit tests. The development validation run also exercised the scanner against the local lab server, covering nine probe scenarios. Results are environment-specific; rerun the tests in your own environment before relying on them.

## Understanding results

The report records what the tested local lab did in response to each probe. A `PASS` means the observed behavior matched the lab's expected behavior for that specific test. It does **not** mean the target is completely secure, and it is not a substitute for a full security assessment.

For example, Origin validation is only one control. An accepted or rejected Origin by itself does not prove whether an application is vulnerable to Cross-Site WebSocket Hijacking (CSWSH). Authentication, session handling, authorization, deployment configuration, and application-specific behavior also matter.

## Documentation

- [Windows installation guide (Urdu)](docs/INSTALLATION_WINDOWS_URDU.md)
- [Security policy](SECURITY.md)
- [Contribution guidelines](CONTRIBUTING.md)
- [Project presentation](docs/WSProbe_Presentation.pdf)

## Responsible use

Run WSProbe only against your own localhost lab or another system for which you have explicit permission. The loopback-only target restriction is an intentional safety feature. Do not modify or bypass it to test systems without authorization.

## License

No open-source license is currently included. All rights remain with the project author unless a license is added. Please contact the author before redistributing or reusing this project.
