import http.server
import time
import subprocess

#-------------user modification-----------------

path = '/home/pi/hub-ctrl.c/hub-ctrl'
ip=''
port=8000

#-------------------------------------------

off_cmd = ['sudo',path,'-h','0','-P','2','-p','0']
on_cmd = ['sudo',path,'-h','0','-P','2','-p','1']

class test_Handler(http.server.BaseHTTPRequestHandler):
    def set_header(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def off(self):
        result = subprocess.Popen(on_cmd).wait()
        self.check_result(result)
        result = subprocess.Popen(off_cmd).wait()
        self.check_result(result)
        time.sleep(1)
        result = subprocess.Popen(off_cmd).wait()
        self.check_result(result)
        print("USB power off")

    def on(self):
        result = subprocess.Popen(on_cmd).wait()
        self.check_result(result)
        print("USB power on")

    def restart(self):
        self.off()
        self.on()

    def check_result(self, result):
        if result != 0:
            raise Exception('hub-ctrl error')

    def do_GET(self):
        try:
            if self.path=="/off":
                self.off()
                self.set_header()
                self.wfile.write(b"USB Off Success\n")

            elif self.path=="/on":
                self.on()
                self.set_header()
                self.wfile.write(b"USB On Success\n")

            elif self.path=="/restart":
                self.restart()
                self.set_header()
                self.wfile.write(b"USB Restart Success\n")

            else:
                self.set_header()
                self.wfile.write(b"USB Restart Failure\n")

        except:
            self.set_header()
            self.wfile.write(b"USB Restart Failure\n")

def run(server_class=http.server.HTTPServer, handler_class=http.server.BaseHTTPRequestHandler):
    server_address = (ip, port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run(handler_class = test_Handler)
