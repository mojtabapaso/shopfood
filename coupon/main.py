import uvicorn

if __name__ == '__main__':
    uvicorn.run('core.config:app', port=3500, reload=True)
