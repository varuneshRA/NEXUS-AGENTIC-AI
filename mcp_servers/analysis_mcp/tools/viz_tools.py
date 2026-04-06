import os
import pandas as pd
import matplotlib
# Use 'Agg' backend to ensure the server runs headlessly without GUI issues
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk

# 1. Set Directory to Project Root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../../generated_plots"))

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def display_chart_popup(filepath):
    """
    Opens a native Tkinter window to show the generated chart.
    """
    try:
        root = tk.Tk()
        root.title("Nexus Visualizer - Latest Analytics")
        
        # Load the image from the saved path
        img = Image.open(filepath)
        
        # Resize for display if the chart is too large for the screen
        img.thumbnail((1000, 700)) 
        
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(root, image=photo)
        label.pack(padx=20, pady=20)
        
        # Keep a reference to prevent garbage collection
        label.image = photo 
        
        root.attributes("-topmost", True)  # Bring to front
        root.mainloop()
    except Exception as e:
        print(f"⚠️ GUI Popup failed: {e}")

def generate_visual(data, chart_type, x, y=None, title=None, hue=None):
    """
    Improved plotting tool with root directory output and Tkinter display.
    """
    if not data:
        return {"status": "error", "message": "No data provided for visualization."}

    # 2. Prepare and Clean Data
    df = pd.DataFrame(data)
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')
    
    # 3. Styling and Figure Setup
    sns.set_theme(style="whitegrid", palette="viridis")
    fig, ax = plt.subplots(figsize=(11, 6))
    
    try:
        # 4. Chart Execution
        if chart_type == 'bar':
            sns.barplot(data=df, x=x, y=y, hue=hue, ax=ax, errorbar=None)
        elif chart_type == 'line':
            sns.lineplot(data=df, x=x, y=y, hue=hue, marker='o', ax=ax)
        elif chart_type == 'pie':
            if y:
                pie_data = df.groupby(x)[y].sum()
                pie_data.plot.pie(autopct='%1.1f%%', ax=ax, startangle=140)
                ax.set_ylabel('') 
        elif chart_type == 'scatter':
            sns.scatterplot(data=df, x=x, y=y, hue=hue, s=100, alpha=0.8, ax=ax)
        elif chart_type == 'heatmap':
            pivot = df.pivot(index=x, columns=hue, values=y)
            sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlGnBu", ax=ax)

        # 5. Formatting
        plt.title(title or f"{chart_type.upper()} Analysis", fontsize=15, pad=20, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # 6. Save to Root Directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"nexus_{chart_type}_{timestamp}.png"
        filepath = os.path.normpath(os.path.join(OUTPUT_DIR, filename))
        
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close(fig) # Memory safety

        # 7. ✅ NEW: Display the image in a Tkinter Popup
        display_chart_popup(filepath)

        return {
            "status": "success",
            "chart_details": {
                "type": chart_type,
                "file_name": filename,
                "file_path": filepath,
                "saved_at": OUTPUT_DIR
            }
        }
    except Exception as e:
        if 'fig' in locals(): plt.close(fig)
        return {"status": "error", "message": f"Plotting failed: {str(e)}"}