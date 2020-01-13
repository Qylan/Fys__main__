 #!/usr/bin/python3

import urllib.parse as urlparse
import mysql.connector
import os

def application(environ, start_response):
    status = '200 OK'
    response_header = [('Content-type', 'text/html')]
    start_response(status, response_header)

    html = ''
    html += '<html>\n'
    html += '   <head>\n'
    html += '       <title>Corendon</title>\n'
    html += '       <link rel="stylesheet" type="text/css" href="../css/LoginPage.css">\n'
    html += '   </head>\n'
    html += '   <body>\n'

    method = environ.get('REQUEST_METHOD', '')

    params = {}
    if method == 'GET':
        params = urlparse.parse_qs(environ['QUERY_STRING'])
    elif method == 'POST':
        input = environ['wsgi.input'].read().decode()
        params = urlparse.parse_qs(input)

    mydb = mysql.connector.connect(
    host="localhost", 
    user="qylan",
    passwd="!Qy7@n10",  
    database="Corendon"
    )

    naam = params.get('uname', [''])[0]
    ticket = params.get('pass', [''])[0]
    userString = "('{}', '{}')".format(naam, ticket)
    mycursor = mydb.cursor()       
    sqlLoginStatement = ("SELECT passenger.firstName, Ticket.ticketnumber FROM passenger INNER JOIN Ticket ON passenger.passengerID = Ticket.passenger_passengerID") 
    mycursor.execute(sqlLoginStatement)
    myresult = mycursor.fetchall()
    print(str(myresult), userString)

    ip = os.popen("cat /var/log/apache2/fys_access.log | awk 'END{print $1}'").read().strip()

    for user in myresult:
        if user == userString:
            #verkrijgen van IP 
            os.system("sudo iptables -t nat -I PREROUTING -s " + ip + " -j ACCEPT")
            os.system("sudo iptables -I FORWARD -s " + ip + " -i wlan0 -o eth0 -j ACCEPT")
            # naam = params.get('uname', [''])[0]
            # html+='<div class=login>\n'
            # html +=     'hoi ' + naam
            # html +='<div>\n
            html += '<meta http-equiv="refresh" content="0;url=../html/welcome" />\n'
        else:
            #html += '<meta http-equiv="refresh" content="0;url=../html/tryagain" />\n'

            html += '   </body>\n'
            html += '</html>\n'

    return [bytes(html, 'utf-8')]

if __name__ == '__main__':
    page = application({}, print)
    print(page[0].decode())
