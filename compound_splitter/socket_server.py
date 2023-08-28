import socketserver
from typing import cast, Dict
from compound_splitter.splitter import get_method, Module

started_methods = cast(Dict[str, Module], {})


class TCPHandler(socketserver.BaseRequestHandler):
    "Request handler class"

    def handle(self):
        '''
        Handle a request to split a compound

        Data of the request must be of form "lemma,method"

        Returns the output of the splitter as a comma-separated
        string of the parts
        '''

        self.data = self.request.recv(1024).strip()

        # parse data
        datastring = self.data.decode('UTF-8')  # convert from binary
        print('{} wrote: "{}"'.format(self.client_address[0], datastring))
        parsed = datastring.split(",")
        if len(parsed) == 2:
            compound, method_name = parsed
        else:
            raise ValueError('Input must be of form "lemma,method".')

        # split
        print("Splitting {} with method {}".format(compound, method_name))
        if method_name in started_methods:
            method = started_methods[method_name]
        else:
            method = get_method(method_name)
            method.start()
            started_methods[method_name] = method
        results = method.split(compound)

        # convert result to succinct format
        top_result = results['candidates'][0]
        parts = top_result['parts']
        print("Top result:", " + ".join(parts))
        output = ','.join(parts).encode('UTF-8')

        # send back parts
        self.request.sendall(output)


def cleanup():
    '''
    Executed on shutdown.

    Run the `stop` function of each method
    '''

    for method in started_methods.values():
        method.stop()


def main():
    '''
    Start a socket server at localhost:7005
    '''

    HOST, PORT = "localhost", 7005
    print("Listening at {}:{}".format(HOST, PORT))
    try:
        with socketserver.TCPServer((HOST, PORT), TCPHandler) as server:
            server.serve_forever()
    finally:
        cleanup()


if __name__ == "__main__":
    main()
