        MOV DPTR, #TABLE
START:  MOV A, P3
        ANL A, #1FH
        MOV R0, A
        CLR C
        SUBB A, #20
        JNC START
        MOV A, R0
        MOVC A, @A+DPTR
        MOV P2, A
        LJMP START

TABLE:  DB 3FH,06H,5BH,4FH,66H     ; 0    1    2   3   4
        DB 6DH,7DH,07H,7FH,6FH     ; 5    6    7   8   9
        DB 77H,7CH,39H,5EH,79H     ; A    B    C   D   E
        DB 71H,00H,76H,38H,40H     ; F   灭    H   L   -
                                   ;01H,上   02H,右上   04H,右下   08H,下   10H,左下   20H,左上   40H,中   80H,小数点       bit[7:0] = {小数点，中，左上，左下，下，右下，右上，上} = {DP,G,F,E,D,C,B,A}
        END
