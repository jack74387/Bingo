@echo off
chcp 65001 >nul 2>&1
cls
echo ========================================
echo      ZMQ Bingo Game Launcher
echo ========================================
echo.
echo Please select an option:
echo 1. Start Game Server
echo 2. Start Game Client  
echo 3. Check Dependencies
echo 4. Install Dependencies
echo 5. Show Help
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo Starting game server...
    python run_server.py
) else if "%choice%"=="2" (
    echo.
    echo Starting game client...
    python run_client.py
) else if "%choice%"=="3" (
    echo.
    echo Checking dependencies...
    python -c "import zmq; print('ZMQ Version:', zmq.zmq_version()); print('PyZMQ Version:', zmq.pyzmq_version())"
) else if "%choice%"=="4" (
    echo.
    echo Installing dependencies...
    pip install -r requirements.txt
) else if "%choice%"=="5" (
    echo.
    echo Usage Instructions:
    echo 1. First start the server (Option 1)
    echo 2. Then start the client (Option 2)
    echo 3. Multiple players can start clients from different terminals
    echo.
    echo For detailed instructions, see README.md
) else (
    echo.
    echo Invalid option! Please enter a number between 1-5
)

echo.
pause