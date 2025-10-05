from google import genai
from google.genai import types
import os

# --- 1. Client Initialization (This part is now correct) ---
client = genai.Client()

# --- 2. Correctly Define the Google Search Tool ---
# The validation error requires that the tool be a specific Pydantic object (types.Tool).

# 2a. Create the GoogleSearch object
google_search_config = types.GoogleSearch()

# 2b. Wrap it in a Tool object
# Note the argument name is 'google_search', matching the type defined above.
google_search_tool = types.Tool(google_search=google_search_config)

# --- 3. Create the configuration for the chat session ---
config = types.GenerateContentConfig(
    # Pass the Tool object in the 'tools' list
    tools=[google_search_tool] 
)

# --- 4. Create the chat session with the 'config' ---
chat = client.chats.create(
    model="gemini-2.5-flash", 
    history=[],              
    config=config            # Correctly pass config
)

# --- 5. Start the Chat Loop ---
print("--- Gemini Chatbot Initialized (with Google Search) ---")
print("Start chatting. Ask a current events question.")

while True:
    prompt = input("You: ")
    if prompt.lower() in ['quit', 'exit']:
        break

    try:
        response = chat.send_message(prompt)
        
        # Check if the tool was used and print the response
        if response.candidates and response.candidates[0].grounding_metadata:
             print(f"Gemini (Grounded): {response.text}")
             # Print the search queries used for extra detail
             queries = response.candidates[0].grounding_metadata.web_search_queries
             print(f"  [Used Google Search with queries: {queries}]")
        else:
             print(f"Gemini: {response.text}")
             
    except Exception as e:
        print(f"An error occurred: {e}")