ORG 0000H 
LJMP MAIN 
ORG 0003H 
LJMP INT0_Handler  ; 外部中断0跳转至对应服务函数
ORG 000BH 
LJMP T0_Handler    ; 定时器0中断跳转至对应服务函数
ORG 001BH 
LJMP T1_Handler    ; 定时器1中断跳转至对应服务函数

ORG 0040H 
MAIN:          
    MOV SP, #5FH         ; 栈指针设为5FH，分配足够堆栈空间
    ; 定时器0配置：模式2（8位自动重装），定时200个机器周期
    MOV TH0, #-200       
    MOV TL0, TH0 
    ; 定时器1配置：模式1（16位），初值0FE0CH
    MOV TH1, #0FEH       
    MOV TL1, #0CH 
    MOV TMOD, #52H       ; T1=模式1+计数器模式；T0=模式2+定时器模式
    MOV TCON, #09H       ; INT0边沿触发，预启动T0
    MOV IP, #05H         ; INT0、T0设为高优先级中断
    MOV IE, #8FH         ; 开启总中断、INT0、T0、T1中断
    MOV 30H, #0A0H       ; 初始化待显示数据存储单元
    MOV 31H, #00H        ; 初始化INT0中断计数单元
    SETB TR0              ; 启动定时器0
    SETB TR1              ; 启动定时器1
    
    ; 初始化显示位选引脚，P0口置高避免乱码
    CLR P2.0             
    CLR P2.1
    CLR P2.2
    MOV P0, #0FFH        
    
    LJMP $                ; 主程序循环等待中断

; 外部中断0服务函数：读取P0口数据并存储到30H
INT0_Handler:              
    INC 31H               ; 累计INT0中断触发次数
    SETB P2.7       ; 显示使能
    CLR P3.7        ; 数据读取选通
    NOP             
    MOV P0, #0FFH
    MOV A, P0       ; 读取P0口外部数据
    MOV 30H, A      ; 更新待显示数据
    SETB P3.7       
    RETI

; 定时器0中断服务函数：在P1.0输出窄脉冲
T0_Handler:    
    SETB P1.0
    NOP
    CLR P1.0
    RETI

; 定时器1中断服务函数：分段显示30H中的数据（高位+低位）
T1_Handler:    
    CLR TR1               ; 关闭T1避免重装初值出错
    MOV TH1, #0FEH        ; 重装T1初值
    MOV TL1, #0CH
    SETB TR1              ; 重启T1
    SETB P2.7       ; 显示使能
    CLR P3.6        ; 显示锁存
    MOV R1, #10     ; 短延时稳定显示
    DJNZ R1, $      
    SETB P3.6       

    ; 显示高位段码：从BCD_H查表输出到P0口
    MOV A, 30H      
    MOV DPTR, #BCD_H
    MOVC A, @A+DPTR
    MOV P0, A       
    SETB P2.0       ; 选通高位显示位
    CLR P2.7        
    CLR P3.6        
    NOP
    NOP             
    SETB P2.7       
    SETB P3.6       
    CLR P2.0        

    ; 显示低位段码：从BCD_L查表输出到P0口
    MOV A, 30H      
    MOV DPTR, #BCD_L
    MOVC A, @A+DPTR
    MOV P0, A       
    CLR P2.7        
    CLR P3.6        
    NOP
    NOP             
    SETB P2.7       
    SETB P3.6       

    RETI 

; 高位显示段码表
BCD_H:         
    DB 1FH, 1FH, 1FH, 1FH, 1FH, 1FH, 11H, 11H, 11H, 11H, 11H, 11H, 11H, 10H, 10H, 10H 
    DB 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H 
    DB 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H 
    DB 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H 
    DB 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H 
    DB 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H 
    DB 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H 
    DB 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H 
    DB 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H 
    DB 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H 
    DB 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H 
    DB 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H 
    DB 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 10H, 00H, 00H, 00H, 00H, 00H 
    DB 00H, 00H, 00H, 00H, 00H, 00H, 00H, 00H, 00H, 00H, 00H, 00H, 00H, 00H, 00H, 00H 
    DB 00H, 00H, 00H, 00H, 00H, 00H, 00H, 00H, 00H, 00H, 00H, 00H, 00H, 00H, 00H, 00H 
    DB 00H, 00H, 00H, 00H, 00H, 00H, 1FH, 1FH, 1FH, 1FH, 1FH, 1FH, 1FH, 1FH, 1FH, 1FH 

; 低位显示段码表
BCD_L:         
    DB 0FFH, 0FFH, 0FFH, 0FFH, 0FFH, 0FFH,  25H,  20H,  15H,  11H,  07H,  04H,  01H,  98H,  96H,  93H 
    DB  91H,  89H,  87H,  86H,  84H,  83H,  81H,  80H,  78H,  77H,  76H,  75H,  74H,  73H,  71H,  71H 
    DB  70H,  69H,  68H,  67H,  66H,  65H,  65H,  64H,  63H,  62H,  62H,  61H,  60H,  59H,  59H,  58H 
    DB  58H,  57H,  56H,  56H,  55H,  55H,  54H,  53H,  53H,  52H,  52H,  51H,  51H,  50H,  50H,  49H 
    DB  49H,  48H,  48H,  47H,  47H,  47H,  46H,  46H,  45H,  45H,  44H,  44H,  43H,  43H,  43H,  42H 
    DB  42H,  41H,  41H,  41H,  40H,  40H,  39H,  39H,  39H,  38H,  38H,  38H,  37H,  37H,  36H,  36H 
    DB  36H,  35H,  35H,  35H,  34H,  34H,  34H,  33H,  33H,  33H,  32H,  32H,  32H,  31H,  31H,  31H 
    DB  30H,  30H,  30H,  29H,  29H,  29H,  28H,  28H,  28H,  27H,  27H,  27H,  26H,  26H,  26H,  25H 
    DB  25H,  25H,  24H,  24H,  24H,  23H,  23H,  23H,  23H,  22H,  22H,  22H,  21H,  21H,  21H,  20H 
    DB  20H,  20H,  19H,  19H,  19H,  18H,  18H,  18H,  17H,  17H,  17H,  17H,  16H,  16H,  16H,  15H 
    DB  15H,  15H,  14H,  14H,  14H,  13H,  13H,  13H,  12H,  12H,  12H,  11H,  11H,  11H,  10H,  10H 
    DB  10H,  09H,  09H,  09H,  08H,  08H,  07H,  07H,  07H,  06H,  06H,  06H,  05H,  05H,  04H,  04H 
    DB  04H,  03H,  03H,  03H,  02H,  02H,  01H,  01H,  00H,  00H,  00H,  01H,  01H,  02H,  02H,  03H 
    DB  03H,  04H,  04H,  05H,  05H,  06H,  06H,  07H,  07H,  08H,  09H,  09H,  10H,  10H,  11H,  12H 
    DB  12H,  13H,  14H,  15H,  15H,  16H,  17H,  18H,  19H,  20H,  21H,  22H,  23H,  24H,  26H,  27H 
    DB  29H,  30H,  32H,  34H,  37H,  40H, 0FFH, 0FFH, 0FFH, 0FFH, 0FFH, 0FFH, 0FFH, 0FFH, 0FFH, 0FFH 

END