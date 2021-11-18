import argparse
import re

def verify_id(arg):
    if len(arg) != 36:
        return 'ID is 36 characters long !!!'

    return arg

def verify_username(arg):
    value = re.findall('\W+', arg)
    value1 = re.findall('^[A-Za-z]{1,}\d+$', arg)

    if len(value) > 0 or len(value1) == 0 or len(arg) < 5 or len(arg) > 30:
        raise argparse.ArgumentTypeError('Username between 5 - 30 characters including letters and numbers (Must start with a letter) !!!')

    return arg

def verify_password(arg):
    value = re.findall('[A-Z]{1,}[a-z]{1,}\d+', arg)
    if len(value) == 0 or len(arg) < 6:
        raise argparse.ArgumentTypeError('Password must be at least 6 characters including 1 uppercase letter, 1 lowercase letter and number !!!')

    return arg

def verify_fullname(arg):
    value = re.findall('\d+|\W+', arg.replace(' ', ''))
    if len(arg) == 0 or len(value) > 0:
        raise argparse.ArgumentTypeError('Fullname only includes letters !!!')

    return arg

def verify_phone(arg):
    if type(arg) != int or len(str(arg)) != 10:
        raise argparse.ArgumentTypeError('Phone must be numeric and have 10 characters!!!')

    return arg

def verify_group_name(arg):
    if len(arg) < 3 or len(arg) > 50:
        raise argparse.ArgumentTypeError('Username between 3 - 50 characters including letters and numbers (Must start with a letter) !!!')

    return arg

def verify_message(arg):
    if len(arg) == 0:
        raise argparse.ArgumentTypeError('Message cantnot be blank !!!')

    return arg

