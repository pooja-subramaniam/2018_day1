import pickle
import random
import string

def get_credentials():
    username = input('Please type your user name: ')
    password = input('Please type your password: ')
    return username, password

def authenticate(username, password, pwdb):
    status = False
    if username in pwdb:
        hash, salt = pwdb[username]
        if hash == hashing(password, salt):
            status = True
    else:
        ans = input('User not known. Add it to db? [y/n]')
        if ans == 'y':
            add_user(username, password, pwdb)
            status = True
    return status

def add_user(username, password, pwdb):
    if username not in pwdb:
        salt = salt_f(5)
        hash = hashing(password, salt)
        pwdb[username] = (hash,salt)
        write_pwdb(pwdb)
    else:
        print('User already known!')

def read_pwdb():
    pwdb_path = get_path()
    try:
        with open(pwdb_path, 'rb') as pwdb_file:
            pwdb = pickle.load(pwdb_file)
    except FileNotFoundError:
        pwdb = {}
    return pwdb

def write_pwdb(pwdb):
    pwdb_path = get_path()
    with open(pwdb_path, 'wb') as pwdb_file:
        pickle.dump(pwdb, pwdb_file)

def hashing(password, salt):
    val = 0
    for i,c in enumerate(password+salt):
        val+=ord(c)*i
    return val

def salt_f(m):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=m))

def get_path():
    return 'pwdb.pkl'

pwdb = read_pwdb()
username, password = get_credentials()
if authenticate(username, password, pwdb):
    print(pwdb)
else:
    print('No match!')
