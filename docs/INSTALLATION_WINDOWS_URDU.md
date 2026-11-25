# Windows par WSProbe install aur run karne ka guide

## 1. Python install karein
1. https://www.python.org/downloads/release/python-31210/ kholein.
2. Windows installer download karein.
3. Installer ke first screen par **Add python.exe to PATH** tick karein.
4. Install Now press karein.
5. Naya PowerShell/VS Code terminal khol kar `py --version` chalayein. Python 3.12.x aana chahiye.

## 2. VS Code install karein
1. https://code.visualstudio.com/Download se Windows installer download karein.
2. Install karein.
3. VS Code khol kar Extensions icon par click karein.
4. Microsoft ki **Python** extension install karein.

## 3. ZIP extract karein
1. `WSProbe_Project.zip` par right-click karein.
2. **Extract All...** select karein.
3. Extract ki hui `WSProbe_Project` folder ko VS Code mein File > Open Folder se kholein.

## 4. Virtual environment aur dependency
VS Code mein Terminal > New Terminal kholein aur project folder mein ye commands ek ek karke chalayein:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 5. Lab server start karein
Pehle terminal mein:

```powershell
.venv\Scripts\python.exe -m wsprobe.lab_server
```

Terminal ko khula rehne dein. Server `127.0.0.1:8765` par chalega.

## 6. WSProbe run karein
VS Code mein doosra terminal kholein. Project folder mein ye command chalayein:

```powershell
.venv\Scripts\python.exe -m wsprobe.scanner --url ws://127.0.0.1:8765 --token lab-token --output reports/wsprobe-report.json
```

## 7. Report dekhein
VS Code Explorer mein `reports/wsprobe-report.json` kholein. Har probe ke saath classification, verdict aur evidence hoga.

## 8. Unit tests
```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Expected: 7 tests pass.

## 9. Server band karein
Server wale terminal par `Ctrl+C` press karein.

## Troubleshooting
- `py` command nahi milti: Python dobara install karein aur **Add python.exe to PATH** tick karein; VS Code restart karein.
- Connection refused: pehle lab server start karein.
- Port in use: purana server band karein.
- Module not found: ensure karein ke aap commands project folder se aur `.venv\Scripts\python.exe` ke saath chala rahe hain.

**Safety:** Tool sirf localhost/loopback URL allow karta hai. Sirf apne ya written permission wale lab systems par test karein.
