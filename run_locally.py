import os

from dash_rq_demo import app

if __name__ == "__main__":
    app.run_server(debug=True, host=os.getenv("APP_HOST", "127.0.0.1"))
