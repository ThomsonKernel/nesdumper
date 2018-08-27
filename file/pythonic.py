name=input("Please input file name: ")
header=b'NES'
with open(name+'.nes','xb') as f:
    f.write(header)

