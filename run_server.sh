#!/bin/bash

set -e

echo "🛠️ Setting up Chat-to-SQL (FastMCP + PostgreSQL + Gemini)..."

# 1. Remove old venv
if [ -d ".venv" ]; then
    echo "🧹 Removing existing virtual environment..."
    rm -rf .venv
fi

# 2. Create new Python venv
echo "📦 Creating Python 3.11 virtual environment..."
python3.11 -m venv .venv
source .venv/bin/activate

# 3. Install Python packages
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Setup .env
if [ ! -f ".env" ]; then
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
fi

export $(grep -v '^#' .env | xargs)

# 5. Install PostgreSQL if not present
if ! command -v psql &> /dev/null; then
    echo "📦 Installing PostgreSQL..."
    brew install postgresql
    brew services start postgresql
else
    echo "✅ PostgreSQL already installed."
fi

# 6. Create database if not exists
echo "📊 Creating database if it doesn't exist..."
psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d postgres -c "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || \
psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d postgres -c "CREATE DATABASE $DB_NAME"

# 7. Run init.sql to create table and insert data
echo "📄 Running SQL from init.sql..."
psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -f db/init.sql

# 8. Register DB with FastMCP
echo "⚙️ Registering DB in FastMCP..."
python -m mcp_server.tools add postgres \
  --name chattosql \
  --host "$DB_HOST" \
  --port "$DB_PORT" \
  --user "$DB_USER" \
  --password "$DB_PASS" \
  --database "$DB_NAME"

echo "✅ All done! You can now run:"
echo "   source .venv/bin/activate && python main.py"
