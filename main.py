from starlette.responses import JSONResponse
from utils.mongo import get_mongo_connection
from fastapi import FastAPI, Request
from datetime import datetime
from utils.scrap_token import scrap_token
from utils.auth import auth
from utils.request_wrapper import make_request
import uvicorn

app = FastAPI()

def validate_request(request: Request):
    if "Authorization" not in request.headers:
        return {"status": 400, "error": "Encabezado no encontrado"}
    else:
        return auth(request.headers["Authorization"])


def get_adeudos_token():
    db_conn = get_mongo_connection()
    tk_list = list(db_conn["telcel_adeudos"]["service"].find({}, {"_id": 0}))

    if len(tk_list) == 0:
        return None
    else:
        return tk_list[0]


def save_token():
    db_conn = get_mongo_connection()
    tk = scrap_token()
    today = datetime.now().strftime("%Y-%m-%d")
    db_conn["telcel_adeudos"]["service"].delete_many({})
    db_conn["telcel_adeudos"]["service"].insert_one({
        "token": tk,
        "date": today
    })

    return tk


@app.get("/api")
def test_api():
    return JSONResponse(status_code=200, content={"message": "Ok"})

@app.get("/api/adeudos")
def obtener_adeudo_cliente(celular: str, request: Request):
    req_status = validate_request(request)
    if req_status["status"] != 200:
        return JSONResponse(status_code=req_status["status"], content={"error": req_status["error"]})

    actual_token = get_adeudos_token()

    if actual_token is None:
        print("Obtaining and saving...")
        actual_token = save_token()

    print("Actual token: {}".format(actual_token))

    actual_token = actual_token["token"]

    status, resp = make_request(celular, actual_token)

    if status == 200:
        print("Response obtained: {}".format(resp))
        return JSONResponse(status_code=200, content=resp)
    elif status == 401:
        # Recargar la Token y solicitar de nuevo
        print("La token ha expirado, recargando...")
        save_token()
        obtener_adeudo_cliente(celular, request)
    elif not isinstance(resp, dict):
        print("Ha ocurrido un error al realizar la consulta")
        return JSONResponse(status_code=status, content={ "error": resp })
    else:
        return JSONResponse(status_code=status, content=resp)

#5610181957

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
