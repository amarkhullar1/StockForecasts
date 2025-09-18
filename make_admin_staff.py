#!/usr/bin/env python
"""
Script to make admin user a staff member.
Run this script to give admin user staff privileges.
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_forecast_app.settings')
django.setup()

from django.contrib.auth.models import User

def make_admin_staff():
    try:
        admin_user = User.objects.get(username='admin')
        admin_user.is_staff = True
        admin_user.save()
        print("Admin user is now a staff member!")
        print("Username: admin")
        print("Password: cursorproject")
    except User.DoesNotExist:
        print("Admin user not found. Please create a superuser first.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    make_admin_staff() 