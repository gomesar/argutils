

def do_captcha(text):
    sum = 0
    for i in range( len(text)-1 ):
        if text[i] == text[i+1]:
            sum += int(text[i])

    if text[-1] == text[0]:
        sum += int(text[0])

    return sum


if __name__ == "__main__":
    tests = ["1122", "1111", "1234", "91212129"]

    with open("captcha", "r") as c:
        cap = c.readline()
        resp = do_captcha( cap[:-1] )

    print(resp)
