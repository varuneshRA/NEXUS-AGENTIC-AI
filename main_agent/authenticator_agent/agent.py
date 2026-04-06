from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
# --------------------------------------------------------------------------
# 🛠️ Functional Tool: Verify User
# --------------------------------------------------------------------------
def verify_user_credentials(tool_context: ToolContext, username: str) -> str:
    """
    Connects to the DB to verify the username and update the session state.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="varun",
            database="ecommerce_db"
        )
        cursor = conn.cursor(dictionary=True)
        
        # Check if user exists
        query = "SELECT name, role FROM users WHERE name = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        
        if user:
            # ✅ Update the Global State
            tool_context.state["role"] = user["role"]
            tool_context.state["user_name"] = user["name"]
            tool_context.state["authenticated"] = True
            
            return f"SUCCESS: User {username} verified as {user['role']}."
        else:
            return "FAILURE: Username not found in database."
            
    except Exception as e:
        return f"ERROR: Database connection failed: {str(e)}"
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# --------------------------------------------------------------------------
# 🤖 The Authenticator Agent
# --------------------------------------------------------------------------
authenticator_agent = LlmAgent(
    name="authenticator_agent",
    model="gemini-2.5-flash",
    instruction="""
    Role: You are a Security Guard for the Nexus Retail System.
    
    Objective:
    - Your ONLY goal is to get a valid username from the user.
    - Call the 'verify_user_credentials' tool with the provided name.
    
    Rules:
    1. If the tool returns 'FAILURE', strictly say: "Please enter a correct username." 
    2. Do NOT allow any other conversation or analytics questions until 'SUCCESS' is returned.
    3. Once you receive 'SUCCESS', inform the user they are logged in and tell them they can 
       now proceed to the main system.
    4. After a successful login, your job is done. The Coordinator will take over.
    """,
    tools=[verify_user_credentials]
)