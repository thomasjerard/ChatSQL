#!/bin/bash

set -e

echo "🔧 Setting up ChatSQL Client Environment..."

# 1. 🧼 Clean old virtual env
if [ -d ".venv" ]; then
    echo "🧹 Removing existing virtual environment..."
    rm -rf .venv
fi

# 2. 🐍 Create new virtual environment
echo "📦 Creating Python 3.11 virtual environment..."
python3.11 -m venv .venv

echo "⚙️ Activating virtual environment..."
source .venv/bin/activate

# 3. 📦 Install dependencies
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. 🔐 Load .env if present
if [ -f ".env" ]; then
    echo "📂 .env found. Loading environment variables..."
    export $(grep -v '^#' .env | xargs)
else
    echo "⚙️ Creating default .env..."
    cat <<EOF > .env
DB_NAME=chattosql
DB_USER=postgres
DB_PASS=yourpassword
DB_HOST=localhost
DB_PORT=5432
GEMINI_API_KEY=your_gemini_api_key_here
EOF
    echo "📌 Please update '.env' with actual database credentials and Gemini API key."
    export $(grep -v '^#' .env | xargs)
fi

# 5. 🚀 Run the CLI
echo "🚀 Running ChatSQL Client..."
python cli.py
