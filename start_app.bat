@echo off
echo Starting Stock Forecast Application...
echo.
echo The application will be available at:
echo - Main app: http://127.0.0.1:8000/
echo - Admin interface: http://127.0.0.1:8000/admin/
echo - Forecast History: http://127.0.0.1:8000/forecast/history/
echo.
echo Admin credentials:
echo - Username: admin
echo - Password: tea123
echo.
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver 0.0.0.0:8000 