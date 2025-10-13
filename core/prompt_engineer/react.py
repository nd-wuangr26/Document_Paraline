import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Initialize OpenAI client with the API key
client = OpenAI(
    api_key=OPENAI_API_KEY,
)

# Define the legal document to analyze
legal_document = """
This Agreement is made effective as of May 1st, 2024, by and between Alpha Holdings Ltd. ("Party A") and BrightCloud Inc. ("Party B").

1. Termination: Either party may terminate this Agreement with 30 days' notice. However, Party B can terminate the Agreement immediately in the case of a "major violation" by Party A, but the term "major violation" is not explicitly defined.

2. Payment Terms: Party A will make quarterly payments to Party B. In the event of delayed payments exceeding 15 days, Party B reserves the right to charge 10% interest. The clause does not specify whether the interest compounds monthly or annually.

3. Intellectual Property: Any innovations created jointly by the parties will be owned by both. However, Party A retains the right to commercialize any joint innovation without needing further approval from Party B, except when it involves proprietary code developed solely by Party B.

4. Dispute Resolution: Any disputes will be resolved via mediation. However, the Agreement later refers to arbitration as a potential resolution method but does not specify which applies in what circumstances.
"""

# Define a simple prompt to analyze the legal document (no detailed reasoning)
basic_prompt = f"""
Analyze the following legal document for key clauses, potential issues, and suggest improvements. Provide a high-level summary without detailed reasoning:

{legal_document}
"""

# Create the chat completion request using the updated OpenAI client
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a legal expert tasked with analyzing legal documents.",
        },
        {
            "role": "user",
            "content": basic_prompt,
        },
    ],
    model="gpt-3.5-turbo",  # You can use "gpt-3.5-turbo" or other models
)

for choice in chat_completion.choices:
    print(choice.message.content)