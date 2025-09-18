#!/usr/bin/env python
"""
Script to set admin password for the superuser account.
Run this script to set a password for the admin user.
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_forecast_app.settings')
django.setup()

from django.contrib.auth.models import User

def set_admin_password():
    try:
        admin_user = User.objects.get(username='admin')
        password = input("Enter new password for admin user: ")
        admin_user.set_password(password)
        admin_user.save()
        print("Admin password updated successfully!")
    except User.DoesNotExist:
        print("Admin user not found. Please create a superuser first.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    set_admin_password() 