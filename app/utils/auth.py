from flask import session, redirect
from functools import wraps # functoons module contains several helper functions that can be used to change other functions

def login_required(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs): # these args ensure that no matter how many args there are, the function captures them all
        # if logged in, call original function with original arguments
        if session.get('loggedIn') == True:
            return func(*args, **kwargs)

        return redirect('/login')

    return wrapped_function

    # @login_required
    # def callback():
    #   print('hello')
    # callback() # prints 'wrapper', then 'hello'

    # A decorator is intended to return a new function—hence, we have the wrapped_function(). However, by returning a new function, we change the internal name of the original function. 
    # To clarify, printing callback.__name__ prints wrapped_function instead of callback. That might not seem serious, but it can make debugging harder. 
    # Thankfully, the @wraps(func) decorator preserves the original name when creating the wrapped function.

    # We want to preserve not only the name but any arguments that the original function received. For example, 
    # callback('data') should translate to func('data') when called inside the decorator. 
    # The *args and **kwargs keywords ensure that no matter how many arguments are given (if any), the wrapped_function() captures them all.