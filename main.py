from selenium import webdriver
from selenium.webdriver.chrome.service import Service


service = Service(executable_path="chromedriver")
driver = webdriver.Chrome(service=service)

from api import app

# This file can be run with: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )