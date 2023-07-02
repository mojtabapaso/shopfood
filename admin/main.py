import uvicorn


if __name__ == '__main__':
    uvicorn.run("core.config:app", port=7500, reload=True)

# def my_decorator(func):
#     def wrapper():
#         print("Something is happening before the function is called.")
#         func()
#         print("Something is happening after the function is called.")
#
#     return wrapper
#
#
# def say_whee():
#     print("Whee!")
#
#
# say_whee = my_decorator(say_whee)
#
#
# @my_decorator
# def register(name, model):
#     pass
#
#
# def one(func):
#     def two(name):
#         print(f"Before function is called.{name}")
#         func()
#         print("After function is called.")
#
#     return two
#
#
# def register_admin(func):
#     def re(name, model):
#         return name, model
#
#     return func
