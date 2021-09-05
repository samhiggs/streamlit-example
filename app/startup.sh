PORT = $1
uvicorn api.main:app --reload --host 0.0.0.0 --port 8001 &
streamlit run --browser.serverAddress 0.0.0.0 --server.enableCORS False --server.port $PORT main.py