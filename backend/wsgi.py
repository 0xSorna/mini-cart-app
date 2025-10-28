#!/usr/bin/env python3

import os
from main import app

# This is the WSGI entry point for Gunicorn
application = app

if __name__ == "__main__":
    # For local development
    application.run()
