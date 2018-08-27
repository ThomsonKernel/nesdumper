from serial import Serial
######Serial Interface######
baud=115200
tty="/dev/cu.wchusbserial1410"
buf=64
chunk=buf>>1
dev=None
def write(h):
    dev.write(h)
def read(size=1):
    return dev.read(size)
def fetch(addr):
    write(addr)
    return read(chunk)
def reset():
    dev.reset_input_buffer()
    dev.setDTR(False)
    dev.setDTR(True)
    read()
def sel_prg():
    reset()
    write(b'\x0e')
    read()
def sel_chr():
    reset()
    write(b'\x0f')
    read()
def is_vert():
    reset()
    write(b'\x10')
    ciram_a10=read()
    return ciram_a10==b'\x01'
def dump(size,addr=b'\x00\x00'):
    data=b''
    for p in range(1,size+1):
        print_percent(p,size)
        if(not p%chunk):
            data+=fetch(addr)
            addr=b''
        addr+=p.to_bytes(2,'big')
    return data
def print_percent(p,size):
    if(p==(size>>2)):
        print('25%...')
    if(p==(size>>1)):
        print('50%...')
    if(p==(size>>1|size>>2)):
        print('75%...')
    if(p==size):
        print('100%!!')
######################
def make(binary):
    name=input("Please input file name: ")
    try:
        with open(name+'.nes','xb') as f:
            f.write(binary)
        print('Done\U0001F37A %s.nes has been created!!' % name)
    except FileExistsError as e:
        print(e)
        make(binary)
########header########
prg_chunk=2**14#16KiB
chr_chunk=2**13#8KiB
######################
def nrom():
    print('Dumping PRG_ROM...')
    sel_prg()
    prg_rom=dump(prg_chunk*2)#32KiB
    ###########################
    if prg_rom[prg_chunk:]==prg_rom[:prg_chunk]:
        X=b'\x01'
        prg_rom=prg_rom[prg_chunk]
    else:
        X=b'\x02'
    print('PRG_ROM size is '+X.hex())
    ###########################
    print('Dumping CHR_ROM...')
    sel_chr()
    chr_rom=dump(chr_chunk)
    ###########################
    Y,m= (b'\x01','Vertical') if is_vert() else (b'\x00','Horizontal')
    print('%s mirroring was detected.' % m) 
    ###########################
    header=b'NES\x1a'+X+b'\x01'+Y+b'\x08'+(0).to_bytes(8,'big')
    make(header+prg_rom+chr_rom)
####################################
i=input("This is nrom dumber!! Let's get started!!....y/n?:")
if(i=='y'):
    dev=Serial(tty,baud)
    nrom()
