START:      MOV P1, #0F0H     ;关掉所有LED管
KEYSCAN:    MOV P3, #0F0H     ;列选全部输出0,此时若有开关按下,则行信号必然有0
            SETB C
            ANL C, P2.0
            ANL C, P2.1
            ANL C, P2.2
            ANL C, P2.3
            JC KEYSCAN

COL0:       MOV P3, #0FEH     ;第0列选通
ELE00:      JB P2.0, ELE10
            MOV A, #0E1H
            LJMP KEY_Delay
ELE10:      JB P2.1, ELE20
            MOV A, #0D1H
            LJMP KEY_Delay
ELE20:      JB P2.2, ELE30
            MOV A, #0B1H
            LJMP KEY_Delay
ELE30:      JB P2.3, COL1
            MOV A, #71H
            LJMP KEY_Delay

COL1:       MOV P3, #0FDH     ;第1列选通
ELE01:      JB P2.0, ELE11
            MOV A, #0E2H
            LJMP KEY_Delay
ELE11:      JB P2.1, ELE21
            MOV A, #0D2H
            LJMP KEY_Delay
ELE21:      JB P2.2, ELE31
            MOV A, #0B2H
            LJMP KEY_Delay
ELE31:      JB P2.3, COL2
            MOV A, #072H
            LJMP KEY_Delay

COL2:       MOV P3, #0FBH     ;第2列选通
ELE02:      JB P2.0, ELE12
            MOV A, #0E4H
            LJMP KEY_Delay
ELE12:      JB P2.1, ELE22
            MOV A, #0D4H
            LJMP KEY_Delay
ELE22:      JB P2.2, ELE32
            MOV A, #0B4H
            LJMP KEY_Delay
ELE32:      JB P2.3, COL3
            MOV A, #74H
            LJMP KEY_Delay

COL3:       MOV P3, #0F7H     ;第3列选通
ELE03:      JB P2.0, ELE13
            MOV A, #0E8H
            LJMP KEY_Delay
ELE13:      JB P2.1, ELE23
            MOV A, #0D8H
            LJMP KEY_Delay
ELE23:      JB P2.2, ELE33
            MOV A, #0B8H
            LJMP KEY_Delay
ELE33:      JB P2.3, NOBTN
            MOV A, #78H
            LJMP KEY_Delay
NOBTN:      LJMP KEYSCAN

KEY_Delay:  MOV P1, A
            MOV P3, #0F0H     ;列选全部输出0,此时若有开关按下,则行信号必然有0
            SETB C
            ANL C, P2.0
            ANL C, P2.1
            ANL C, P2.2
            ANL C, P2.3
            JNC KEY_Delay
            MOV P1, #0F0H
            LJMP KEYSCAN

            END
