#!/usr/bin/env python2

# token
tokenseed = "025EF87E7819E3A3B48E92CD92E7AB35" # product_id
tokenseed = [int(tokenseed[i*2:i*2+2],16) for i in range(16)]
token = 0x0FDE45E3

############################################################
# 1
ck = 0
pre_p = 0
p = 0
pre_c = 0
c = 0
b = 0
def func1():
    ##############################
    # 1-1 clock
    global ck
    ck ^= 1
    ##############################
    # 1-2 clock up counter
    global pre_p, p, pre_c, c
    # U12B
    pre_p = p
    if ck == 1:
        p += 1
        if p & 0b100 != 0:
            p = 0
        # U12A
        pre_c = c
        if (pre_p & 2) < (p & 2):
            c += 1
            if c & 0b10000 != 0:
                c = 0
    else:
        pre_c = c
    ##############################
    # 1-3 select layer
    global token, b
    b = token >> ((c & 0b111) * 4)  # take 4 bits
    b &= 0b1111

############################################################
# 2
a = 0
b2 = 0
pre_p2 = 0  # init
p2 = 0
p3 = 0
pre_d = 9   # init
d = 9
def func2():
    ##############################
    # 2-1
    global c, b, b2, a, p3
    b2 = c ^ b
    a = tokenseed[b2]
    ##############################
    # 2-2
    global p, pre_p2, p2, pre_d, d
    pre_p2 = p2
    p2 = (p & 1) & ((c & 1) ^ 1)
    p3 = (p & 1) & (c & 1)
    p2 |= p3 << 1
    p3 ^= 1
    pre_d = d
    if p3 == 0:
        d = (c & 0b110) >> 1
    else:
        d = 9

############################################################
# 3
a2 = 0
b3 = 0
a3 = 0
def func3():
    ##############################
    # 3-1
    global pre_p2, p2, a, a2, b3, a3
    if (pre_p2 & 1) < (p2 & 1):
        a2 = a ^ 0xf0
    if (pre_p2 & 2) < (p2 & 2):
        b3 = a ^ 0xf0
    ##############################
    # 3-2
    a3 = a2 ^ b3

############################################################
# 4
b4 = 0xffffffff
def func4():
    global pre_d, d, a3, b4
    if d <= 3 and pre_d != d:
        b4 &= 0xffffffff ^ (0xff << (d * 8))    # set 0 for update byte
        b4 |= (a3 ^ 0xff) << (d * 8)    # set not(a3)

############################################################
# 5
a5 = 0
def func5():
    global token, b4, a5
    a5 = (token ^ 0xffffffff) ^ b4
    a5 = ((a5 << 1) & 0xffffffff) | ((a5 & 0x80000000) >> 31)

############################################################
# 6
def func6():
    global pre_c, c, a5, token
    if (pre_c & 0b1000) < (c & 0b1000):
        token = a5
        return True
    return False

############################################################
# main
j = 0
while True:
    func1()
    func2()
    func3()
    func4()
    func5()
    ret = func6()
    if ret:
        print "%05d" % j, "%08X" % token
        j+=1
        if j > 323:
            break


"""
# timing chart
   0         1         2         3         4         5         6         7         8         9         0         1         2
Å@ 01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567
ck X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X
p  XX  XX  XX  XX  XX  XX  XX  XX  XX  XX  XX  XX  XX  XX  XX  XX  XX  XX  XX  XX  XX  XX  XX  XX  XX  XX  XX  XX  XX  XX  XX  XX 
     XXXX    XXXX    XXXX    XXXX    XXXX    XXXX    XXXX    XXXX    XXXX    XXXX    XXXX    XXXX    XXXX    XXXX    XXXX    XXXX 
c0   XXXXXXXX        XXXXXXXX        XXXXXXXX        XXXXXXXX        XXXXXXXX        XXXXXXXX        XXXXXXXX        XXXXXXXX     
 1           XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX                XXXXXXXXXXXXXXXX     
 2                           XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                                XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX     
 3                                                           XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX     
p2 XX          XX  XX          XX  XX          XX  XX          XX  XX          XX  XX          XX  XX          XX  XX          XX 
       XX  XX          XX  XX          XX  XX          XX  XX          XX  XX          XX  XX          XX  XX          XX  XX     
p3XXXXX  XX  XXXXXXXXXX  XX  XXXXXXXXXX  XX  XXXXXXXXXX  XX  XXXXXXXXXX  XX  XXXXXXXXXX  XX  XXXXXXXXXX  XX  XXXXXXXXXX  XX  XXXXX
d      00  00          11  11          22  22          33  33          00  00          11  11          22  22          33  33     
a    U       U       U       U       U       U       U       U       U       U       U       U       U       U       U       U    
a2 U           U   U           U   U           U   U           U   U           U   U           U   U           U   U           U  
b3     U   U           U   U           U   U           U   U           U   U           U   U           U   U           U   U      
a3 U   U   U   U   U   U   U   U   U   U   U   U   U   U   U   U   U   U   U   U   U   U   U   U   U   U   U   U   U   U   U   U  
b4     0   0           1   1           2   2           3   3           0   0           1   1           2   2           3   3      
tk                                                           U                                                                    


#print "%05d"%i,ck,p,"%02d"%c,"%02d"%b,"%02d"%b2,p2,p3,d,"%02X"%a,"%02X"%a2,"%02X"%b3,"%02X"%a3,"%08X"%b4,"%08X"%a5,"%08X"%token
#print "%05d"%i,ck,p,"%02d"%c,"%02d"%b,"%02d"%b2,p2,p3,d,"%02X"%a,"%02X"%a2,"%02X"%b3,"%02X"%a3,"%08X"%b4,"%08X"%a5,"%08X"%token
#print "%05dck p  c  b b2p2p3 d a  a2 b3 a3 b4       a5       token" % i
"""