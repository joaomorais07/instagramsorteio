import mysql.connector
from mysql.connector import Error

def mysqlconector():
    '''Takes no args, and returns a connection to MYDB via MYSQL.'''
    try:
        conexao = mysql.connector.connect(user='8ijaiyutxz7hhgicc7iy', password='pscale_pw_M43YdDeRLGUijbfSKWhPrGhUHySVmRhgN0Jx46FWwxZ', host='aws.connect.psdb.cloud', database='instagram_sorteio', port=3306)
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
