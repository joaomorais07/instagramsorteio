import mysql.connector
from mysql.connector import Error

def mysqlconector():
    '''Takes no args, and returns a connection to MYDB via MYSQL.'''
    try:
        conexao = mysql.connector.connect(user='b7a0b507d55ac1', password='6b694eed', host='us-cdbr-east-06.cleardb.net', database='heroku_ac60b498dc6c78c')
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DV_ERROR:
            print("Database does not exist")
        else:
            print(err)
    # the else will happen if there was no error!
    else:
        return conexao
    
    return conexao
