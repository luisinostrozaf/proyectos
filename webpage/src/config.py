import cx_Oracle


BD_USER = "TRAVIS" 
BD_PASWORD = "1234"
BD_SERVICIO = "localhost:1521/xe"
try:
    connection = cx_Oracle.connect(
        BD_USER, 
        BD_PASWORD, 
        BD_SERVICIO
    )
except Exception as err:
    print(err)