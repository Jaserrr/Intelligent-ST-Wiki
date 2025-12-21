;设8个数码管的从左到右显示缓冲区为片内RAM的50H～57H单元
        ORG  0000H
        LJMP MAIN
        ORG  0100H
MAIN:  MOV A,#0                ;显示缓冲区50H～57H单元初始化为0～7
        MOV  R2,#8
        MOV  R0,#50H
LOOP:  MOV  @R0,A
        INC R0
        INC A
        DJNZ  R2,LOOP
LOOP1: LCALL DISPLAY           ;调用显示子程序
        SJMP  LOOP1
        SJMP  $
;显示子程序
DISPLAY:MOV  R0,#57H           ;动态显示初始化,使R0指向缓冲区首地址
        MOV  R3,#7FH           ;首位位选字送R3
        MOV  A,R3
LD0:    MOV  P2,A              ;从P2口送出位选字
        MOV  A,@R0             ;读要显示数
        ADD  A,#0EH            ;调整距离字段码表首的偏移量
        MOVC A,@A+PC           ;查表取得字段码
        MOV  P0,A              ;字段码从P0口输出
        ACALL  DL1             ;调用1ms延时子程序
        DEC  R0                ;指向缓冲区下一单元
        MOV  A,R3              ;位选码送累加器A
        JNB  ACC.0,LD1         ;判断8位是否显示完毕,显示完返回
        RR  A                  ;未显示完,把位选字变为下一位选字
        MOV  R3,A              ;修改后的位选字送R3
        AJMP  LD0              ;循环实现按位序依次显示
LD1:    RET
TAB:    DB  76H,79H,38H,38H,3FH,40H,7FH,7FH;字段码表
DL1:    MOV  R7,#02H           ;延时子程序
DL:     MOV  R6,#0FFH
DL0:    DJNZ  R6,DL0
        DJNZ  R7,DL
        RET
        END