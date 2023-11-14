import mysql.connector
from mysql.connector import Error

def mysqlconector():
    '''Takes no args, and returns a connection to MYDB via MYSQL.'''
    try:
        conexao = mysql.connector.connect(user='ct54qfrgminot5og0met', password='pscale_pw_CcdN1ueBYks33JJuHb9CLTQFouh3B7wfewEIG7O72Qy', host='aws.connect.psdb.cloud', database='instagram_sorteio', port=3306)
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
