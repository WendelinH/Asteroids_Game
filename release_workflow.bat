@echo off
setlocal enabledelayedexpansion

:: Define ANSI Escape Codes for Colors
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do set "ESC=%%b"

set "CLR_RESET=%ESC%[0m"
set "CLR_HEADER=%ESC%[95m"   :: Magenta
set "CLR_STEP=%ESC%[96m"     :: Cyan
set "CLR_SUCCESS=%ESC%[92m"  :: Green
set "CLR_WARN=%ESC%[93m"     :: Yellow
set "CLR_ERROR=%ESC%[91m"    :: Red

echo %CLR_HEADER%===================================================%CLR_RESET%
echo %CLR_HEADER%             AUTO-BUILD \& RELEASE WORKFLOW          %CLR_RESET%
echo %CLR_HEADER%===================================================%CLR_RESET%
echo.

:: 1. Versionsnummer abfragen
set /p VERSION="Bitte neue Versionsnummer eingeben (z.B. 1.1.0): "

if "%VERSION%"=="" (
    echo %CLR_ERROR%[FEHLER]%CLR_RESET% Keine Version eingegeben. Abbruch.
    pause
    exit /b
)

echo.
echo %CLR_STEP%[1/5] Erstelle '_version.py' mit Version %VERSION% %CLR_RESET%
echo VERSION = "%VERSION%" > _version.py

:: 2. PyInstaller ausführen
echo %CLR_STEP%[2/5] Starte PyInstaller...%CLR_RESET%
py run_pyinstaller.py
if %ERRORLEVEL% NEQ 0 (
    echo %CLR_ERROR%[FEHLER]%CLR_RESET% PyInstaller-Build fehlgeschlagen!
    pause
    exit /b
)

:: 3. Inno Setup ausführen
echo %CLR_STEP%[3/5] Starte Inno Setup Compiler (ISCC) %CLR_RESET%
:: /D übergibt die Variable "AppVersion" direkt an das Inno-Skript
"%HOMEPATH%\AppData\Local\Programs\Inno Setup 7\ISCC.exe" /DMyAppVersion=%VERSION% inno_setup.iss
if %ERRORLEVEL% NEQ 0 (
    echo %CLR_ERROR%[FEHLER]%CLR_RESET% Inno Setup Compilation fehlgeschlagen!
    pause
    exit /b
)

:: 4. Git Versionierung
echo %CLR_STEP%[4/5] Starte Git-Commit fuer Version %VERSION% %CLR_RESET%
git add _version.py
git commit -m "Bump version to %VERSION%"
if %ERRORLEVEL% NEQ 0 (
    echo %CLR_WARN%[WARNUNG]%CLR_RESET% Git Commit fehlgeschlagen (vielleicht keine Aenderungen?)
)

:: 5. Git Tag erstellen
echo %CLR_STEP%[5/5] Erstelle Git-Tag v%VERSION%%CLR_RESET%
git tag -a v%VERSION% -m "Release version %VERSION%"
git push --tags
if %ERRORLEVEL% NEQ 0 (
    echo %CLR_ERROR%[FEHLER]%CLR_RESET% Git-Tag konnte nicht erstellt werden!
    pause
    exit /b
)

echo.
echo %CLR_SUCCESS%===================================================%CLR_RESET%
echo %CLR_SUCCESS% ERFOLG! Version %VERSION% wurde erfolgreich gebaut,%CLR_RESET%
echo %CLR_SUCCESS% verpackt und in Git getaggt.%CLR_RESET%
echo %CLR_SUCCESS%===================================================%CLR_RESET%
echo.
pause