#!/bin/bash
echo "Starting NOVA OMNIS Securely..."

if [ ! -f .env ]; then
  echo "Missing .env file! Create one with OPENAI_API_KEY=your-key-here"
  exit 1
fi

export $(grep -v '^#' .env | xargs)
pip install --quiet openai requests

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.10"

if [[ "$PYTHON_VERSION" < "$REQUIRED_VERSION" ]]; then
  echo "Python 3.10+ required. Detected: $PYTHON_VERSION"
  exit 1
fi

echo "Launching Nova Omnis..."
python3 nova_omnis_grey_ethics.py
