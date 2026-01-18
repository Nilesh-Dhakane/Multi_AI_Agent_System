import subprocess
import threading
import time
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from dotenv import load_dotenv

load_dotenv()
logger = get_logger("main.py")


def run_backend():
    try:
        logger.info("Starting backend service...")
        subprocess.run(["uvicorn","app.backend.api:app","--host","127.0.0.1","--port","9999"],check=True)
    except Exception as e:
        logger.exception("Problem with backend service")
        raise CustomException("Failed to start backend",e)
    
def run_frontend():
    try:
        logger.info("Starting frontend service...")
        subprocess.run(["streamlit",
                        "run",
                        "app/frontend/ui.py",
                        "--server.port",
                        "8501",
                        "--server.address", "0.0.0.0",
                        "--server.headless", "true"],check=True)
    except Exception as e:
        logger.exception("Problem with frontend service")
        raise CustomException("Failed to start frontend",e)    
    

if __name__=="__main__":
    try:
        threading.Thread(target=run_backend).start()
        time.sleep(3)
        run_frontend()
    except Exception as e:
        logger.exception("Error in starting asynchronous run processes")
        raise CustomException("Error in main file.",e)


