#!/bin/bash

set -e

echo "🛠️ Setting up FastMCP Server..."

# 1. 🧼 Clean old venv if it exists
if [ -d ".venv" ]; then
    echo "🧹 Removing existing virtual environment..."
    rm -rf .venv
fi

# 2. 🐍 Create virtual environment
echo "📦 Creating Python 3.11 virtual environment..."
python3.11 -m venv .venv

echo "⚙️ Activating virtual environment..."
source .venv/bin/activate

# 3. 📦 Install Python dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. 🔐 Load environment variables from .env
if [ -f ".env" ]; then
    echo "📂 Loading .env variables..."
    export $(grep -v '^#' .env | xargs)
else
    echo "⚠️ No .env found. Creating default .env..."
    cat <<EOF > .env
DB_NAME=chattosql
DB_USER=postgres
DB_PASS=yourpassword
DB_HOST=localhost
DB_PORT=5432
GEMINI_API_KEY=your_gemini_api_key_here
EOF
    echo "📌 Please update '.env' with actual credentials and API key."
    export $(grep -v '^#' .env | xargs)
fi

# 5. 🚀 Run FastMCP Server
echo "🚀 Starting FastMCP Server..."
python mcp_server/tools.py
