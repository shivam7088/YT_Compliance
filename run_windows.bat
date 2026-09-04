@echo off
echo Starting YouTube Compliance Checker...
if not exist .venv (
    python -m venv .venv
)
call .venv\Scripts\activate
pip install -r requirements.txt
python main.py
pause
