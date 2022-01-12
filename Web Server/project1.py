"""
Creator: Michaela Ann Hay
Student ID: 1001649623
Resources used: https://www.codementor.io/@joaojonesventura/building-a-basic-http-server-from-scratch-in-python-1cedkg0842
The above helped me with creating the socket- all else I had to figure out on my own.
Class: CSE 4344-001
Date Completed: 10/14/2021
Profsesor: Liu, Yongh

University of Texas at Arlington
"""

import socket

"""
This function will take in the HTTP generated request message from the client
and will parse through it to find:
    1. What file type is the client HTTP request asking for
    2. Is it an object file that exists in the directory
"""
def handle_request(request):

    # Tokenize the request into an array based on the '\n' character
    headers = request.split('\n')
    # Save the name of the requested file from the client on the first header
    filename = headers[0].split()[1]
    # Look for if the client is requesting a generic root- replace with index.html
    if filename == '/':
        filename = '/index.html'
    # Remove the '/' from the filename. Causes error when parsed by open() function
    filename = filename[1:]


    try:
        # Hard-code the webpage that will causet he user to be redirected for 301
        if filename.endswith("test.html"):
        # Save content as the 301 error message per HTTP protocol
            content = "HTTP/1.0 301 Moved Permanently\r\n\r\n"
        # If normal .html then search for the file in the current dir
        # If the .html file cannot be found, FileNotFoundError will be triggered
        elif filename.endswith(".html"):
            fin = open(filename)
            # This saves the raw string data from the file into content- note that
            # it needs to be encoded for this reason
            content = fin.read()
            fin.close()

        # Search for filenames that end with .png or .jpg - for these files
        # the image_file function will be called to the data inside them
        elif filename.endswith(".png"):
            content = image_file(filename)
            fin.close()

        elif filename.endswith(".jpg"):
            content = image_file(filename)
        # If no file found that falls under the previous categories,
        # issue a 404 so the program doesn't crash and so the user is
        # informed the object doesn't exist
        else:
            content = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'

    # If file error happens because file not found, put 404 in content response
    except FileNotFoundError:
        content = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'

    return content

# Read the file passed through this function as a binary one. This is a must for
# image objects since they should not be read as literal string values.
def image_file(filename):
    with open(filename, 'rb') as image:
        return image.read()

# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
# This makes it to where the webserver is receptive to a client trying to
# initiate a TCP handshake.
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

while True:
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    request = client_connection.recv(1024).decode()
    print(request)

    # Return an HTTP response
    response = handle_request(request)
    # If the response is a normal .html page that is available, send 200 status
    try:
         # Used code in this link as a reference for finding key words in the response string:
         # https://stackoverflow.com/questions/50430865/send-image-over-http-python
        if str(response).find("html") > 0:
            client_connection.send('HTTP/1.1 200 OK\n\n'.encode())
            # Encode the webpage so it's not a raw string of data but bytes
            client_connection.send(response.encode())
        # If the response is a 404 error, print response out to user
        elif str(response).find("404") > 0:
            client_connection.send('HTTP/1.0 404 NOT FOUND\r\n\r\nFile Not Found'.encode())
        elif str(response).find("301") > 0:
            # 301 Message warning user that the website has moved
            client_connection.send('HTTP/1.0 301 Moved Permanently\r\n\r\n'.encode())
            # Open the index.html file and read
            fin = open('index.html')
            response = fin.read()
            fin.close()
            # Redirect user to the index.html file when they put in test.html
            client_connection.send(response.encode())

        else:
            # Program will think the HTTP protcol wants a jpg img
            client_connection.send('HTTP/1.0 200 OK\r\n'.encode())
            # Set content type to jpeg per protocol
            client_connection.send('Content-Type: image/jpeg\r\n'.encode())
            client_connection.send('Accept-Ranges: bytes\r\n\r\n'.encode())
            # Don't have to encode an image- will cause error.
            client_connection.send(response)
    except KeyboardInterrupt:
        client_connection.close()

    # Close connection
    client_connection.close()

# Close socket
server_socket.close()