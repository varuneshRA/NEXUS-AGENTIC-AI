import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv
from google.adk.agents import LlmAgent

# Load environment variables (API Keys, etc.)
load_dotenv()

# --- 🛠️ Tool Functions ---

def select_file_via_gui() -> str:
    """
    Opens a native file picker dialog for the user to select a CSV or Excel file.
    Use this when the user says 'let me pick a file', 'browse', or 'select a file'.
    Returns:
        The full local system path of the selected file.
    """
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the main tkinter window
        root.attributes("-topmost", True)  # Bring the dialog to the front
        
        file_path = filedialog.askopenfilename(
            title="Nexus Data Selection - Select CSV or Excel",
            filetypes=[
                ("Data Files", "*.csv *.xlsx *.xls"),
                ("CSV Files", "*.csv"),
                ("Excel Files", "*.xlsx *.xls"),
                ("All Files", "*.*")
            ]
        )
        root.destroy()
        
        if not file_path:
            return "User cancelled the file selection."
        return file_path
    except Exception as e:
        return f"Error opening file picker: {str(e)}"

def read_csv_file(file_path: str) -> str:
    """
    Reads a CSV file from a local path and returns the data as a string.
    Args:
        file_path: The absolute path to the .csv file.
    """
    try:
        # We read the first 500 rows to avoid hitting token limits for huge files
        df = pd.read_csv(file_path, nrows=500)
        return f"File Content (First 500 rows):\n{df.to_string()}"
    except Exception as e:
        return f"Error reading CSV: {str(e)}"

def read_excel_file(file_path: str, sheet_name: str = "Sheet1") -> str:
    """
    Reads an Excel file (.xlsx/.xls) and returns the data as a string.
    Args:
        file_path: The absolute path to the Excel file.
        sheet_name: Name of the sheet (defaults to Sheet1).
    """
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, nrows=500)
        return f"Sheet '{sheet_name}' Content (First 500 rows):\n{df.to_string()}"
    except Exception as e:
        return f"Error reading Excel: {str(e)}"

# --- 🤖 Agent Definition ---

file_reader_agent = LlmAgent(
    name="file_reader_agent",
    # Using 2.0-flash for superior tool execution and logic
    model="gemini-2.5-flash", 
    description="Nexus Specialist for browsing, reading, and interpreting CSV and Excel files.",
    instruction="""
    Role: You are a Professional Data Analyst for Nexus Retail Group.
    
    Workflow Protocol:
    1. FILE PICKING: If the user hasn't provided a path, CALL 'select_file_via_gui' to let them browse.
    2. DATA LOADING: Use the returned path to CALL 'read_csv_file' or 'read_excel_file'.
    3. ANALYSIS: 
       - Once data is loaded, analyze it to answer the user's specific question.
       - If the user asks for 'Total Revenue', 'Average Price', or 'Summary', perform the math based on the data.
    
    Strict Rules:
    - NEVER invent data. If a column is missing, explain that you cannot find it.
    - If the file is successfully read, start your response by confirming the file name.
    - Use Markdown tables for small data snippets to make them readable.
    """,
    # Register the functions as tools
    tools=[select_file_via_gui, read_csv_file, read_excel_file]
)