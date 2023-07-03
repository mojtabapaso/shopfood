import uvicorn

# from project.core.config import app
if __name__ == '__main__':
    uvicorn.run("project.core.config:app", port=8000, reload=True)
