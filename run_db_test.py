#!/usr/bin/env python3
"""
Script to run the database connection test with environment variables loaded automatically
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Now execute the test script
exec(open('test_db_connection.py').read())