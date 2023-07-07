def requestDict(filepath):
    # Reads the .txt file and returns a dictionary of key-value pairs.
    headers = {}
    with open(filepath) as f:
        lines = f.readlines()
        for line in lines:
            if ':' in line:
                header, value = line.split(':')
                headers[header] = value
        return headers

def flag(filepath):
    print(f"Checking for conflicting headers in request located at: {filepath}")
    headers = requestDict(filepath)

    if 'Content-Length' in headers.keys() and 'Transfer-Encoding' in headers.keys():
        print(f"Conflicting headers found")
    else:
        print(f"Conflicting headers absent")

