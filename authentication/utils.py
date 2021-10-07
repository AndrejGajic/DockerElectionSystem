from email.utils import parseaddr
from models import User, Role
import re

def checkEmptyRegistration(data):
    if data["jmbg"] == "":
        return "Field jmbg is missing."
    elif data["forename"] == "":
        return "Field forename is missing."
    elif data["surname"] == "":
        return "Field surname is missing."
    elif data["email"] == "":
        return "Field email is missing."
    elif data["password"] == "":
        return "Field password is missing."
    else:
        return "OK"

def checkEmptyLogin(data):
    if data["email"] == "":
        return "Field email is missing."
    elif data["password"] == "":
        return "Field password is missing."
    else:
        return "OK"

def checkJMBG(jmbg):
    msg = "Invalid jmbg."
    if len(jmbg) != 13:
        return msg
    checker = jmbg[0:2]
    if int(checker) < 1 or int(checker) > 31:
        return msg
    checker = jmbg[2:4]
    if int(checker) < 1 or int(checker) > 12:
        return msg
    checker = jmbg[4:7]
    if int(checker) < 0 or int(checker) > 999:
        return msg
    checker = jmbg[7:9]
    if int(checker) < 70 or int(checker) > 99:
        return msg
    checker = jmbg[9:12]
    if int(checker) < 0 or int(checker) > 999:
        return msg
    checker = 11 - ((7 * (int(jmbg[0]) + int(jmbg[6])) + 6 * (int(jmbg[1]) + int(jmbg[7])) + 5 * (int(jmbg[2]) + int(jmbg[8])) +
                     4 * (int(jmbg[3]) + int(jmbg[9])) + 3 * (int(jmbg[4]) + int(jmbg[10])) + 2 * (int(jmbg[5]) + int(jmbg[11]))) % 11)
    if checker == 10 or checker == 11:
        checker = 0
    if checker != int(jmbg[12]):
        return msg
    return "OK"

def checkEmail(email):
    checker = parseaddr(email)
    if len(checker) == 0 or len(checker[1]) == 0 or not '@' in checker[1] or not ".com" in checker[1]:
        return "Invalid email."
    return "OK"

def checkEmailNotInDatabase(email):
    for user in User.query.all():
        if email == user.email:
            return "Email already exists."
    return "OK"

def checkEmailInDatabase(email):
    for user in User.query.all():
        if email == user.email:
            return "OK"
    return "Invalid credentials."

def checkPassword(password):
    msg = "Invalid password."
    if len(password) < 8 or len(password) > 256 or not re.search("[a-z]", password) or not re.search("[A-Z]", password) or not re.search("[0-9]", password):
            return msg
    else:
        return "OK"

def findRole(role):
    return Role.query.filter(Role.name == "zvanicnik").first().id