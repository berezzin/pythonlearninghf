from flask import session

def check_logged_in(func):
    def wrapper:
        if  'logged in' in session:
            return 'You are logged in'
        return func
