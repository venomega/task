import socket, ssl, json, os

# missing load config

class Webdav():
    @classmethod
    def parse(self, configpath):
        self = self()
        d = json.load(open(configpath))
        if d['username'] == "" or d["password"] == "":
            self.auth = False
        else:
            self.auth = True
            self.base64encoded = ssl.base64.b64encode(":".join([d['username'], d["password"]]).encode())
        self.hostname = d["hostname"]
        self.port = d["port"]
        self.ssl = d["ssl"]
        return self
    
    def __exec(self):
        s = socket.socket()

        try:
            if ssl.wrap_socket:
                s = ssl.wrap_socket(s)
        except:
            ctx = ssl.create_default_context()  # python latest versions
            s = ctx.wrap_socket(s, server_hostname=self.hostname)
        try:
            s.connect((self.hostname, self.port))
        except:
            raise("Error Connecting")
            print("THIS IS NOT SUPPOSED TO BE REACHED")
        if self.sendall: # uploading file
            s.sendall(self.request + self.content)
        else: # reading file
            s.send(self.request)
        self.response = b""
        while True:
            data = s.recv(3333)
            if not data:
                s.close()
                break
            self.response += data
        msg = b" ".join(self.response.split(b"\r\n")[0].split(b" ")[2:]).decode() 
        print (msg + "\n")
        if not self.sendall:
            if "Not Found" in msg:
                return '[]'
            n = self.response.index(b"\r\n\r\n")
            #open("/dev/stdout", "wb").write(self.response[n+4:])
            return self.response[n+4:].decode()
        

    def get(self, filepath, outputfilepath="dump"):
        self.outputfilepath = outputfilepath
        if "/" != filepath[0]:
            filepath = "/" + filepath
        if self.auth:
            self.request = b"GET %b HTTP/1.1\r\nAuthorization: Basic %b\r\nConnection: Close\r\nHost: %b:%i\r\n\r\n" % (filepath.encode(), self.base64encoded, self.hostname.encode(), self.port)
        else:
            self.request = b"GET %b HTTP/1.1\r\nConnection: Close\r\nHost: %b:%i\r\n\r\n" % (filepath, self.hostname.encode(), self.port)
        self.sendall = False
        return self.__exec()

    def put(self, filepath, outputfiledir="/"): 
        if  "/" != outputfiledir[0]: 
            outputfiledir = "/" + outputfiledir
        if  "/" != outputfiledir[-1]:
            outputfiledir = outputfiledir + "/"
        self.outputfiledir = outputfiledir
        print(self.outputfiledir)
        self.content = open(filepath, "rb").read()
        if self.auth:
            self.request = b"PUT %b HTTP/1.1\r\nAuthorization: Basic %b\r\nContent-Length: %i\r\nConnection: Close\r\nHost: %b:%i\r\n\r\n" % ((self.outputfiledir + os.path.basename(filepath)).encode(), self.base64encoded, len(self.content), self.hostname.encode(), self.port)
        else:
            self.request = b"PUT %b HTTP/1.1\r\nConnection: Close\r\nContent-Length: %i\r\nHost: %b:%i\r\n\r\n" % ((self.outputfiledir + os.path.basename(filepath)).encode(), len(self.content), self.hostname.encode(), self.port)
        self.sendall = True
        self.__exec()

