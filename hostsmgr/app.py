from http import HTTPStatus
from os import name

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
from pydantic import BaseModel

from db import Machine, User


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"]
)


class UpdateMachineSchema(BaseModel):
    connection: str
    occupied_by: str


class CreateMachineSchema(BaseModel):
    name: str
    connection: str
    occupied_by: str


class CreateUserSchema(BaseModel):
    id: str
    name: str
    email: str
    role: str

class UpdateUserSchema(BaseModel):
    name: str
    email: str
    role: str

@app.get("/machines", status_code=HTTPStatus.OK)
def read_machines(response: Response):
    try:
        _machines = Machine.query({})
        machines = {}
        for machine in _machines:
            mname = getattr(machine, Machine.KEY)
            machines[mname] = machine.json()

        return machines
    except Exception as e:
        response.status_code = HTTPStatus.NOT_FOUND
        return str(e)

@app.put("/machine", status_code=HTTPStatus.ACCEPTED)
def update_machines(name: str, machine: UpdateMachineSchema, response: Response):
    ms = Machine.query({"name": name})
    if len(ms) == 0:
        response.status_code = HTTPStatus.NOT_FOUND
        return "{} not found!".format(name)
    elif len(ms) !=1:
        response.status_code = HTTPStatus.CONFLICT
        return "Find multiple documents, please check database."

    m = ms[0]
    m.update_attr("connection", machine.connection)
    m.update_attr("occupied_by", machine.occupied_by)

    try:
        m.update()
        return "Machine {} updated!".format(name)
    except Exception as e:
        response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        return str(e)


@app.post("/machine", status_code=HTTPStatus.CREATED)
def create_machine(machine: CreateMachineSchema, response: Response):
    ms = Machine.query({"name": machine.name})
    if len(ms) == 0:
        try:
            Machine.create({"name": machine.name, 
                            "connection": machine.connection,
                            "occupied_by": machine.occupied_by})
            return "Machine {} created!".format(machine.name)
        except Exception as e:
            response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            return str(e)

    response.status_code = HTTPStatus.CONFLICT
    return "Machine {} existed, please check!".format(machine.name)


@app.delete("/machine/{name}", status_code=HTTPStatus.OK)
def delete_machine(name: str, response: Response):
    ms = Machine.query({"name": name})
    if len(ms) == 1:
        try:        
            ms[0].delete()
            return "Machine {} deleted!".format(name)
        except Exception as e:
            response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            return "Machine {} delete Failed!".format(name)

    elif len(ms) == 0:
        response.status_code = HTTPStatus.NOT_FOUND
        return "Machine {} not found!".format(name)

    response.status_code = HTTPStatus.CONFLICT
    return "Found multiple machines!"


@app.get("/users", status_code=HTTPStatus.OK)
def read_users(response: Response):
    try:
        _users = User.query({})
        users = {}
        for user in _users:
            uname = getattr(user, User.KEY)
            users[uname] = user.json()

        return users
    except Exception as e:
        response.status_code = HTTPStatus.NOT_FOUND
        return str(e)


@app.get("/user/{idsid}", status_code=HTTPStatus.OK)
def read_user(idsid: str, response: Response):
    users = User.query({"id": idsid})
    try:
        if not users:
            response.status_code = HTTPStatus.NOT_FOUND
            return "User {} not found".format(idsid)
        return users[0].json()
    except Exception as e:
        response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        return str(e)

@app.post("/user", status_code=HTTPStatus.CREATED)
def create_user(user: CreateUserSchema, response: Response):
    _user = User.query({"id": user.id})
    if len(_user) == 0:
        try:
            User.create({"id": user.id,
                         "name": user.name, 
                         "email": user.email,
                         "role": user.role})
            return "User {} created!".format(user.id)
        except Exception as e:
            response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            return str(e)

    response.status_code = HTTPStatus.CONFLICT
    return "User {} existed, please check!".format(user.id)


@app.put("/user", status_code=HTTPStatus.ACCEPTED)
def update_users(id: str, user: UpdateUserSchema, response: Response):
    _users = User.query({"id": id})
    if len(_users) == 0:
        response.status_code = HTTPStatus.NOT_FOUND
        return "{} not found!".format(id)
    elif len(_users) !=1:
        response.status_code = HTTPStatus.CONFLICT
        return "Find multiple documents, please check database."

    u = _users[0]
    u.update_attr("name", user.name)
    u.update_attr("email", user.email)
    u.update_attr("role", user.role)

    try:
        u.update()
        return "User {} updated!".format(id)
    except Exception as e:
        response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        return str(e)


@app.delete("/user/{id}", status_code=HTTPStatus.OK)
def delete_user(id: str, response: Response):
    _user = User.query({"id": id})
    if len(_user) == 1:
        try:        
            _user[0].delete()
            return "User {} deleted!".format(id)
        except Exception as e:
            response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            return "User {} delete Failed!".format(id)

    elif len(_user) == 0:
        response.status_code = HTTPStatus.NOT_FOUND
        return "User {} not found!".format(id)

    response.status_code = HTTPStatus.CONFLICT
    return "Found multiple User!"
