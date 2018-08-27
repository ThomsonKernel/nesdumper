def make(binary)
    name=input("Please input file name: ")
    try:
        with open(name+'.nes','xb') as f:
            f.write(binary)
    except FileExistsError as e:
        print(e)
        make(binary)
