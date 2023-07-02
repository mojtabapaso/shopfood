import getpass
import sys
import requests

# / Need to test
def create():
    phone_number = input("phone_number : ")

    password = getpass.getpass('password : ')

    json = {"phone_number": phone_number, "password": password}
    response = requests.post("http://127.0.0.1:7500/admin/create/super/user/", json=json)
    prt = response.json()
    print(prt)
    if prt is False:
        print('not found')
    if prt:
        print("founded")
    # print(f"phone_number : {phone_number}")


def change():
    response = requests.post('http://127.0.0.1:1500/show/all/')
    print(response.json())


def help():
    print("This is help ")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "createsuperuser":
        create()
    if len(sys.argv) > 1 and sys.argv[1] == 'change':
        change()
    if len(sys.argv) > 1 and sys.argv[1] == 'help':
        help()
    else:
        print("Usage: python myprogram.py start")
        sys.exit(1)
