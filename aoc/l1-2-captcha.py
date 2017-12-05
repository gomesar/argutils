

def do_captcha(text):
    mySize = len(text)
    sum = 0
    for i in range(len(text)):
        if text[i] == text[(i + int(mySize/2))%(mySize)]:
            sum += int(text[i])

    return sum


if __name__ == "__main__":
    tests = ["1122", "1111", "1234", "91212129"]

    with open("captcha", "r") as c:
        cap = c.readline()
        resp = do_captcha( cap[:-1] )

    print(resp)
