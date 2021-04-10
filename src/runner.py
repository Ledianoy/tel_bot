from dotenv import load_dotenv
import uvicorn


load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "tel_bot.asgi:app",
        host="localhost",
        log_level="debug",
        port=8000,
        reload=True,
        reload_dirs=["src"],
    )