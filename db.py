import mysql.connector
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")

try:
    mydb = mysql.connector.connect(
        host = config["DB"]["host"],
        user = config["DB"]["user"],
        password = config["DB"]["password"],
        database = config["DB"]["database"]
    )

    print(mydb)
except ValueError:
    print("ValueError")
