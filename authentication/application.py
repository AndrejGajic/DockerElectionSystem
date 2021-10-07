from flask import Flask, request, Response, jsonify
from configuration import AuthConfiguration
from models import authDb, User, Role
from utils import checkEmptyRegistration, checkEmptyLogin, checkJMBG, checkEmail, checkPassword,\
    checkEmailInDatabase, checkEmailNotInDatabase, findRole
from sqlalchemy import and_, or_
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, get_jwt, get_jwt_identity, \
    jwt_required
from roleCheck import roleCheck

# ---------------------------- PORT 5000 -------------------------------------- #

authApp = Flask(__name__)
authApp.config.from_object(AuthConfiguration)
jwt = JWTManager(authApp)




@authApp.route("/register", methods=["POST"])
def registration():
    data = {
        "jmbg": request.json.get("jmbg", ""),
        "forename": request.json.get("forename", ""),
        "surname": request.json.get("surname", ""),
        "email": request.json.get("email", ""),
        "password": request.json.get("password", "")
    }
    msg = checkEmptyRegistration(data)
    if msg != "OK":
        return jsonify(message = msg), 400
    msg = checkJMBG(data["jmbg"])
    if msg != "OK":
        return jsonify(message = msg), 400
    # check if email already exists
    msg = checkEmail(data["email"])
    if msg != "OK":
        return jsonify(message = msg), 400
    msg = checkPassword(data["password"])
    if msg != "OK":
        return jsonify(message=msg), 400
    msg = checkEmailNotInDatabase(data["email"])
    if msg != "OK":
        return jsonify(message = msg), 400
    user = User(jmbg=data["jmbg"], forename=data["forename"], surname=data["surname"],
                email=data["email"], password=data["password"], roleId=findRole("zvanicnik"))
    authDb.session.add(user)
    authDb.session.commit()


    return Response(status=200)


@authApp.route("/login", methods=["POST"])
def login():
    data = {
        "email": request.json.get("email", ""),
        "password": request.json.get("password", "")
    }
    msg = checkEmptyLogin(data)
    if msg != "OK":
        return jsonify(message = msg), 400
    msg = checkEmail(data["email"])
    if msg != "OK":
        return jsonify(message = msg), 400
    msg = checkEmailInDatabase(data["email"])
    if msg != "OK":
        return jsonify(message = msg), 400
    user = User.query.filter(and_(User.email == data["email"], User.password == data["password"])).first()
    if not user:
        return jsonify(message = "Invalid credentials."), 400

    additionalClaims = {
        "jmbg": user.jmbg,
        "forename": user.forename,
        "surname": user.surname,
        "role": user.role.name
    }
    accessToken = create_access_token(identity=user.email, additional_claims=additionalClaims)
    refreshToken = create_refresh_token(identity=user.email, additional_claims=additionalClaims)

    return jsonify(accessToken=accessToken, refreshToken=refreshToken), 200



@authApp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refreshToken():
    identity = get_jwt_identity()
    refreshClaims = get_jwt()
    additionalClaims = {
        "jmbg": refreshClaims["jmbg"],
        "forename": refreshClaims["forename"],
        "surname": refreshClaims["surname"],
        "role": refreshClaims["role"]
    }
    accessToken = create_access_token(identity=identity, additional_claims=additionalClaims)
    return jsonify(accessToken=accessToken), 200



@authApp.route("/delete", methods=["POST"])
@roleCheck(role="administrator")
def deleteUser():
    identity = get_jwt_identity()
    additionalClaims = get_jwt()
    email = request.json.get("email", "")
    if not email or email == "":
        return jsonify(message="Field email is missing."), 400
    msg = checkEmail(email)
    if msg != "OK":
        return jsonify(message=msg), 400
    msg = checkEmailInDatabase(email)
    if msg != "OK":
        return jsonify(message="Unknown user."), 400
    user = User.query.filter(User.email == email).first()
    print(user.email)
    authDb.session.delete(user)
    authDb.session.commit()
    return jsonify(""), 200

@authApp.route("/check", methods=["POST"])
@jwt_required()
def checkToken():
    return Response("Token is valid.", status=200)

@authApp.route("/", methods=["GET", "POST"])
def index():
    return AuthConfiguration.homeText


if(__name__ == "__main__"):
    authDb.init_app(authApp)
    authApp.run(debug=True, host="0.0.0.0", port=5000)