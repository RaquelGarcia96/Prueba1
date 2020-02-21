import sys
import json
import pyodbc
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    request = req.get_json()

    if not request:
        return func.HttpResponse("Please pass a Json in the request body", status_code=400)
    else:
        try:
            # el codigo aquí
            result = request["variable"]
            prueba = sim()
            # if (result==-1):
            #     print("well done")
            toma = Toma(result)
            response = toma
            return func.HttpResponse(body=response.toJSON(), status_code=200)
        except:
            errorMsg = sys.exc_info()[1].__str__()
            print("Unexpected error:", errorMsg)
            return func.HttpResponse(errorMsg, status_code=400)

class Toma:
    def __init__(self, variable):
        self.variable = variable
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
## -- -- -- -- -- -- -- -- -- --


def get_dbconnection(configfilepath="config_ham.txt"):
    driver = get_dbdata("Driver", configfilepath)
    server = get_dbdata("dbservername", configfilepath) + ".database.windows.net"
    dbname = get_dbdata("dbname", configfilepath)
    dbuser = get_dbdata("dbuser", configfilepath)
    dbpassword = get_dbdata("dbpassword", configfilepath)
    cnxn = pyodbc.connect(Driver=driver, Server=server, Database=dbname, Uid=dbuser, Pwd=dbpassword)
    return cnxn


def get_sql_driver():
    return '{ODBC Driver 17 for SQL Server}'


def get_dbdata(varname, configfilepath="config"):
    if varname == "Driver":
        return get_sql_driver()
    conf = open("./configs/" + configfilepath, 'r')

    configdb_data = {}
    for line in conf.readlines():
        if '=' in line:
            line = line.split('=')
            configdb_data[line[0]] = str(line[1].split('\n')[0])
    conf.close()
    if varname not in configdb_data.keys(): return 
    return configdb_data[varname]


def write_db(cnxn, tabla, col, value, cond):
    cursor = cnxn.cursor()
    comand= 'UPDATE '+tabla+' SET '+col+'='+value+' WHERE '+cond+';'
    print("Executing: ", comand)
    cursor.execute(comand)
    cnxn.commit()
    return "Update OK"

def sim():
    cnx = get_dbconnection()
    write_db(cnx, 'jamones', 'peso', '11', 'id_jamon=1')
    cnx.close()
    return -1
