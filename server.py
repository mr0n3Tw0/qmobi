from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib
import json


class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if parse.urlparse(self.path).path == '/usdtorub':
            params = dict(parse.parse_qsl(parse.urlsplit(self.path).query))

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            data = get_json_from_cbr()
            result = {'Valute':data['CharCode'],
                      'Value':int(params['usd']),
                      'Result': int(params['usd']) * data['Value'] }
            self.wfile.write(json.dumps({'data': result})).encode()

        else:
            self.send_response(404)


def get_json_from_cbr():
    try:
        url = request.urlopen('https://www.cbr-xml-daily.ru/daily_json.js').read()
    except urllib.error.URLError:
        print("\nService is unavailable")
    else:
        file = (url.decode('utf-8'))
        data = json.loads(file)
        return data['Valute']['USD']


def run(server_class=HTTPServer, handler_class=GetHandler):
    server = server_class(('', 8080), handler_class)
    try:
        print('Starting server, listening on: http://127.0.0.1:8080/, use <Ctrl-C> to stop')
        server.serve_forever()
    except KeyboardInterrupt:
        print ('\nServer stopped')
        server.server_close()

if __name__ == '__main__':
    run()
