#include <LiquidCrystal.h>

LiquidCrystal lcd(8, 9, 4, 5, 6, 7);           // select the pins used on the LCD panel

unsigned int tokenseed[] = {0x02,0x5E,0xF8,0x7E,0x78,0x19,0xE3,0xA3,0xB4,0x8E,0x92,0xCD,0x92,0xE7,0xAB,0x35};
unsigned int token = 0x0FDE45E3;

unsigned int ck = 0;
unsigned int pre_p = 0;
unsigned int p = 0;
unsigned int pre_c = 0;
unsigned int c = 0;
unsigned b = 0;

void func1(){
    // 1-1 clock
    ck ^= 1;
    // 1-2 clock up counter
    // U12B
    pre_p = p;
    if(ck == 1){
        p += 1;
        if((p & 4) != 0){
            p = 0;
        }
        // U12A
        pre_c = c;
        if((pre_p & 2) < (p & 2)){
            c += 1;
            if((c & 16) != 0){
                c = 0;
            }
        }
    }
    else{
        pre_c = c;
    }
    // 1-3 select layer
    b = token >> ((c & 7) * 4);
    b &= 15;
}

unsigned int a = 0;
unsigned int b2 = 0;
unsigned int pre_p2 = 0;
unsigned int p2 = 0;
unsigned int p3 = 0;
unsigned int pre_d = 9;
unsigned int d = 9;

void func2(){
    // 2-1
    b2 = c ^ b;
    a = tokenseed[b2];
    // 2-2
    pre_p2 = p2;
    p2 = (p & 1) & ((c & 1) ^ 1);
    p3 = (p & 1) & (c & 1);
    p2 |= p3 << 1;
    p3 ^= 1;
    pre_d = d;
    if(p3 == 0){
        d = (c & 0b110) >> 1;
    }
    else{
        d = 9;
    }
}

unsigned int a2 = 0;
unsigned int b3 = 0;
unsigned int a3 = 0;

void func3(){
    // 3-1
    if((pre_p2 & 1) < (p2 & 1)){
        a2 = a ^ 0xf0;
    }
    if((pre_p2 & 2) < (p2 & 2)){
        b3 = a ^ 0xf0;
    }
    // 3-2
    a3 = a2 ^ b3;
}

unsigned int b4 = 0xffffffff;
void func4(){
    if(d <= 3 && pre_d != d){
        b4 &= 0xffffffff ^ (0xff << (d * 8));
        b4 |= (a3 ^ 0xff) << (d * 8);
    }
}

unsigned int a5 = 0;
void func5(){
    a5 = (token ^ 0xffffffff) ^ b4;
    a5 = ((a5 << 1) & 0xffffffff) | ((a5 & 0x80000000) >> 31);
}

int func6(){
    if((pre_c & 0b1000) < (c & 0b1000)){
        token = a5;
        return 1;
    }
    return 0;
}

void setup(){
   lcd.begin(16, 2);               // start the library
}

unsigned int j = 0;
void loop(){
    func1();
    func2();
    func3();
    func4();
    func5();
    int ret = func6();
    if(ret){
        //lcd.setCursor(10,0);
        //lcd.print(millis()/1000);
        lcd.setCursor(0,0);
        lcd.print(j,DEC);
        lcd.setCursor(0,1);
        lcd.print(token,HEX);
        //print "%05d" % j, "%08X" % token
        j+=1;
        delay(1000);
    }
}
