from serial import Serial
baud=115200
tty="/dev/cu.wchusbserial1410"

t=Serial(tty,baud)

def off():
    t.write(b'0')
def on():
    t.write(b'1')
def read():
    t.write(b'2')
    print(t.read());
