@echo off
echo ========================================
echo   OpenStoryline MCP Server 启动脚本
echo ========================================
echo.

cd /d "%~dp0openstoryline"

echo [1/2] 激活虚拟环境...
call .venv\Scripts\activate.bat

echo [2/2] 启动 MCP Server (端口 8001)...
echo.
set PYTHONPATH=src
python -m open_storyline.mcp.server

pause
