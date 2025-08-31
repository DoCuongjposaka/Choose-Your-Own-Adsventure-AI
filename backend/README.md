##B1 
cd backend
##B2
python -m pip install fastapi uvicorn sqlalchemy pydantic-settings python-dotenv langchain langchain-google-genai google-generativeai google-ai-generativelanguage psycopg2-binary
##B3
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload