from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import socket

class NumberServer(BaseHTTPRequestHandler):

    NEXT_NUMBER_FILE_NAME = "next_number.txt"

    def _set_headers(self, response_code):
        self.send_response(response_code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        try:
            # open number file and read number
            f = open(self.NEXT_NUMBER_FILE_NAME, "r")
            number = int(f.read())
            f.close()

            # send the number to the client
            self._set_headers(200)
            self.wfile.write(str(number))
            
            # write incremented number back to file
            f = open(self.NEXT_NUMBER_FILE_NAME, "w")
            number = str(number + 1)
            f.write(number)
            f.close()
        except IOError, ValueError:
            self._set_headers(500)

    def do_HEAD(self):
        self._set_headers(200)

class HTTPServerV6(HTTPServer):
  address_family = socket.AF_INET6

def run(server_class=HTTPServerV6, handler_class=NumberServer, port=80):
    server_address = ('::', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting number server...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
