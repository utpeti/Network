import socket

def connect(server, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, port))
    response = s.recv(1024).decode()
    print(response)
    return s

def send_command(socket, command, expected_response_code):
    socket.send((command + '\r\n').encode())
    response = socket.recv(1024).decode()
    if not response.startswith(str(expected_response_code)):
        raise Exception(response)
    return response

def send_email(server, port, sender, recipient, subject, body):
    try:
        s = connect(server, port)
        if s:
            send_command(s, "EHLO example.com", 250)
            send_command(s, "MAIL FROM: <{}>".format(sender), 250)
            send_command(s, "RCPT TO: <{}>".format(recipient), 250)
            send_command(s, "DATA", 354)
            message = "From: {}\r\nTo: {}\r\nSubject: {}\r\n\r\n{}\r\n.\r\n".format(sender, recipient, subject, body)
            send_command(s, message, 250)
            send_command(s, "QUIT", 221)
            s.close()
    except Exception as e:
        print("Error sending the email:", e)

def main():
    try:
        recipient = input("Enter recipient email address: ")
        sender = input("Enter sender email address: ")
        subject = input("Enter email subject: ")
        print("Enter email body:")
        body_lines = []
        while True:
            line = input()
            if line == '.':
                break
            body_lines.append(line)
        body = '\r\n'.join(body_lines)

        server = "localhost" 
        port = 25

        send_email(server, port, sender, recipient, subject, body)
    except KeyboardInterrupt:
        print("\nProcess interrupted.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
