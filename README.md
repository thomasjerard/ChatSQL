# 💬 ChatSQL — Natural Language to SQL using Gemini & FastMCP

ChatSQL is a command-line tool that lets you query a PostgreSQL database using natural language.
It uses **Google Gemini** to convert your questions into SQL, and **FastMCP** to execute them against your database.

---

## 🚀 Tech Stack

* Python 3.11+
* PostgreSQL (via `psycopg2`)
* FastMCP (Modular Composable Protocol)
* Google Gemini (for Natural Language to SQL conversion)
* Rich (for pretty command-line interface output)
* python-dotenv (for environment variable configuration)

---

## 🧠 Use Case

You ask a question in plain English, and ChatSQL generates and executes the SQL, then displays the results.

> **Input:**
> "Get all employees earning more than 50000"

> **Generated SQL:**
> `SELECT * FROM employees WHERE salary > 50000;`

> **Output:**  

+----+---------+--------+------------+-----------+------------+
| id | name | salary | phone_no | address | department |
+----+---------+--------+------------+-----------+------------+
| 1 | Alice | 75000 | 9876543210 | New York | HR |
| 2 | Bob | 65000 | 1234567890 | Chicago | Finance |
+----+---------+--------+------------+-----------+------------+


---

## ⚙️ Setup Instructions

### ✅ 1. Clone the Repository & Configure Environment

```bash
> git clone https://github.com/yourname/chatSQL.git
> cd chatSQL

### ✅ 2. Prerequisites

* Bash shell is required (default on macOS/Linux).
* Python 3.11+ must be installed and accessible via your terminal.

### ✅ 3. Create a .env file in the root folder with the following content:

env
Copy
Edit
DB_NAME=chattosql
DB_USER=postgres
DB_PASS=yourpassword
DB_HOST=localhost
DB_PORT=5432
GEMINI_API_KEY=your-gemini-api-key

### ✅ 3. Run the Application
You’ll need two separate terminals:

🖥️ Terminal 1 — Start the Server
./run_server.sh

💬Terminal 2 — Start the Client
./run_client.sh
Once the client starts, you'll see a prompt like:

💬 ChatSQL (Gemini + FastMCP)
🗨️ Ask (NL):

🔧 What Happens Internally

Each script (run_server.sh / run_client.sh) performs the following:

Deletes any existing virtual environment and creates a fresh one.

Loads environment variables from the .env file.

Installs required Python dependencies from requirements.txt.

Sets up PostgreSQL:

Creates the database (chattosql)

Adds the user (postgres)

Creates a sample employees table

Starts the FastMCP server or the ChatSQL CLI client, depending on the script.






