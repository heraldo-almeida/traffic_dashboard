@echo off
title Recife Traffic Dashboard Server
echo Starting the Recife Traffic Dashboard...
echo Please wait a few seconds for the browser to open.
echo Do not close this window while you are using the dashboard!
echo.

C:\Users\heraldoneto\AppData\Local\Programs\Python\Python311\python.exe -m streamlit run C:\Users\heraldoneto\Documents\01_projects\traffic_dashboard\app.py

pause