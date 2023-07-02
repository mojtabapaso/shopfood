from fastapi import FastAPI
from api import router

app = FastAPI()
app.include_router(router.router, tags=["admin_api"])
app.include_router(router.router2, tags=["admin_api_2"])

# @app.middleware('http')
# async def add_process_time_header(request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers['X-Process-Time'] = str(process_time)
#     return response
# import websocket_client
import os
# @app.on_event('startup')
# def startup_event():
#     os.system('python3 websocket_client.py')

    # with open('server_time_log.log', 'a') as log:
    #     log.write(f'Application started at: {datetime.datetime.now()} \n')

#
# @app.on_event('shutdown')
# def shutdown_event():
#     with open('server_time_log.log', 'a') as log:
#         log.write(f'Application shut down at: {datetime.datetime.now()} \n')
