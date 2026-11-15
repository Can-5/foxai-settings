@echo off
REM Foxai-Settings.exe — Windows için yerel derleme betiği.
REM Repo kökünden çalıştırın: packaging\windows\Build-Windows.bat
setlocal

python -m venv .venv-win
call .venv-win\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt pyinstaller
pyinstaller --noconfirm packaging\windows\foxai-settings.spec

echo.
echo Derleme bitti: dist\Foxai-Settings.exe
echo Not: Bu dosya imzasızdir; SmartScreen uyarısını "Yine de çalıştır" ile geçmeniz gerekebilir.
endlocal
