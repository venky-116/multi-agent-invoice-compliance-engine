import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

def main():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "YOUR_GROQ_API_KEY":
        print("Error: Please set your GROQ_API_KEY in the .env file.")
        return
    
    print("Testing connection to Groq API...")
    try:
        llm = ChatGroq(model="llama-3.3-70b-versatile")
        response = llm.invoke("Hello! Are you online and ready to audit?")
        print("Success! Groq Response:")
        print(response.content)
    except Exception as e:
        print(f"Error connecting to Groq API: {e}")

if __name__ == "__main__":
    main()
