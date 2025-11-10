

import os
from openai import OpenAI
import sys

try:
    client = OpenAI()
except Exception as e:
    # This error occurs if the API key is not set.
    print("Error: OpenAI client could not initialize.")
    print("Please ensure your OPENAI_API_KEY environment variable is set.")
    print(f"Details: {e}")
    sys.exit(1)

TASK_DESCRIPTIONS = [
    """
    I need to completely reorganize all the documents, spreadsheets, and PDFs 
    stored in the shared folder on the company server. This involves creating 
    a new, standardized folder structure based on project codes, renaming files 
    to match the standard 'YYYYMMDD-ProjectCode-Description' format, and 
    archiving any documents older than two years into a separate 'Archive' drive.
    """,
    """
    The main task is to update the inventory system for the quarterly report. 
    This includes cross-referencing all physical counts taken by the warehouse 
    team with the digital records in the ERP system, investigating any discrepancy 
    greater than 5%, and preparing a summary report detailing stock levels, 
    write-offs, and necessary reorders for the next fiscal period.
    """,
]


def summarize_task(description):
    """
    Sends a paragraph description to the AI and requests a short phrase summary.
    """
    print(f"\n--- Processing Task: {description[:50].strip()}... ---")
    
    system_prompt = "You are a task summarization assistant. Your only job is to condense the user's detailed task description into a short, concise, 3-5 word phrase."
    
    try:
        
        response = client.chat.completions.create(
        
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": description}
            ],
            
            max_tokens=20 
        )
        
      
        summary = response.choices[0].message.content.strip()
        return summary
        
    except Exception as e:
        print(f"An error occurred during API call: {e}")
        return "ERROR: Could not summarize task."

def main():
    """
    Adds a loop to summarize multiple tasks and prints the results.
    This function is called by `uv run tasks4`.
    """
    print("Starting Task Summarization using OpenAI Chat Completions API.")
    
    for i, description in enumerate(TASK_DESCRIPTIONS):
        summary = summarize_task(description)
        
        print(f"Summary {i+1}: **{summary}**")

if __name__ == "__main__":
    main()