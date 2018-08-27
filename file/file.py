name=input("Please input file name: ")
header=b'NES'
f=open(name+'.nes','xb')
f.write(header)
f.close()

