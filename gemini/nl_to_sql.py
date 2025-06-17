import os
import google.generativeai as genai
from dotenv import load_dotenv
import re

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Using 'gemini-2.0-flash' which is generally available and supports the free tier.
model = genai.GenerativeModel("gemini-2.0-flash")

PROMPT_TEMPLATE = """
You are a PostgreSQL expert. Convert the following natural language question into a valid SQL query.
Only use the 'employees' table with columns: id, name, salary, phone_no, address, department.

Question: "{question}"

SQL:
"""

def nl_to_sql(question: str) -> str:
    prompt = PROMPT_TEMPLATE.format(question=question)
    try:
        response = model.generate_content(prompt)
        if response and response.text:
            # Get the generated text
            sql_text = response.text.strip().split("SQL:")[-1].strip("` \n")

            # Remove leading 'sql' (case-insensitive), if present
            sql_text = re.sub(r"^\s*sql[:\-]?\s*", "", sql_text, flags=re.IGNORECASE)

            return sql_text.strip()
        else:
            print("Warning: Model returned an empty or invalid response.")
            return "Error: Could not generate SQL query."
    except Exception as e:
        print(f"An error occurred during content generation: {e}")
        return f"Error: Failed to generate SQL query due to API error: {e}"

# Example Usage (optional, for testing)
if __name__ == "__main__":
    # Make sure your GEMINI_API_KEY is set in your .env file
    # Example: GEMINI_API_KEY="YOUR_API_KEY_HERE"

    print("Testing nl_to_sql function with gemini-2.0-flash...")

    question1 = "Get all employees earning more than 50000"
    sql1 = nl_to_sql(question1)
    print(f"\nQuestion: {question1}\nSQL: {sql1}")

    question2 = "Find the name and department of employee with id 123"
    sql2 = nl_to_sql(question2)
    print(f"\nQuestion: {question2}\nSQL: {sql2}")

    question3 = "Show me all employees in the 'Sales' department"
    sql3 = nl_to_sql(question3)
    print(f"\nQuestion: {question3}\nSQL: {sql3}")

    question4 = "List employees by salary in descending order"
    sql4 = nl_to_sql(question4)
    print(f"\nQuestion: {question4}\nSQL: {sql4}")