# host: 77.83.100.110
# db_name: slrlvbsp_wp598
# db_user: slrlvbsp_devbasic
# pass : DEVbasic121413!!

# логин: slrlvbsp_wp598 и пароль 03121980
import mysql.connector

try:
    mydb = mysql.connector.connect(
    host = "77.83.100.110",
    user = "slrlvbsp_devbasic",
    password = "DEVbasic121413!!",
    database = "slrlvbsp_wp598"
)

    print(mydb)
except ValueError:
    print("ValueError")
