@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo             AUTO-BUILD & RELEASE WORKFLOW          
echo ===================================================
echo.

:: 1. Versionsnummer abfragen
set /p VERSION="Bitte neue Versionsnummer eingeben (z.B. 1.1.0): "

if "%VERSION%"=="" (
    echo [FEHLER] Keine Version eingegeben. Abbruch.
    pause
    exit /b
)

echo.
echo [1/5] Erstelle '_version.py' mit Version %VERSION%...
echo VERSION = "%VERSION%" > _version.py

:: 2. PyInstaller ausführen
echo [2/5] Starte PyInstaller...
py run_pyinstaller.py
if %ERRORLEVEL% NEQ 0 (
    echo [FEHLER] PyInstaller-Build fehlgeschlagen!
    pause
    exit /b
)

:: 3. Inno Setup ausführen
echo [3/5] Starte Inno Setup Compiler (ISCC)...
:: /D übergibt die Variable "AppVersion" direkt an das Inno-Skript
"%HOMEPATH%\AppData\Local\Programs\Inno Setup 7\ISCC.exe" /DMyAppVersion=%VERSION% inno_setup.iss
if %ERRORLEVEL% NEQ 0 (
    echo [FEHLER] Inno Setup Compilation fehlgeschlagen!
    pause
    exit /b
)

:: 4. Git Versionierung
echo [4/5] Starte Git-Commit fuer Version %VERSION%...
git add _version.py
git commit -m "Bump version to %VERSION%"
if %ERRORLEVEL% NEQ 0 (
    echo [WARNUNG] Git Commit fehlgeschlagen (vielleicht keine Aenderungen?). Fahre fort...
)

:: 5. Git Tag erstellen
echo [5/5] Erstelle Git-Tag v%VERSION%...
git tag -a v%VERSION% -m "Release version %VERSION%"
if %ERRORLEVEL% NEQ 0 (
    echo [FEHLER] Git-Tag konnte nicht erstellt werden!
    pause
    exit /b
)

echo.
echo ===================================================
echo  ERFOLG! Version %VERSION% wurde erfolgreich gebaut,
echo  verpackt und in Git getaggt.
echo ===================================================
echo.
pause