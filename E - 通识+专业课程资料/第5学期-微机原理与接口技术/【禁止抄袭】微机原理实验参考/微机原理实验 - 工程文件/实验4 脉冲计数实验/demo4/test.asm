; 定义变量存储单元 (4个字节对应8位十进制数)
; 每个字节存储 0-99 的数值
CNT_LL  EQU 30H    ; 最低2位 (个位, 十位)
CNT_LH  EQU 31H    ; 次低2位 (百位, 千位)
CNT_HL  EQU 32H    ; 次高2位 (万位, 十万位)
CNT_HH  EQU 33H    ; 最高2位 (百万位, 千万位)

; 复位入口
ORG 0000H
    LJMP MAIN       ; 上电跳转到主程序

; 中断向量表
ORG 0003H           ; 外部中断0入口 (启动/暂停)
    LJMP ISR_INT0

ORG 0013H           ; 外部中断1入口 (清零)
    LJMP ISR_INT1

ORG 001BH           ; 定时器1中断入口 (脉冲计数)
    LJMP ISR_T1

;-------------------------主程序-------------------------
ORG 0030H
MAIN:
    ; 1. 堆栈初始化
    MOV SP, #60H

    ; 2. 变量初始化 (清零显示)
    MOV CNT_LL, #0
    MOV CNT_LH, #0
    MOV CNT_HL, #0
    MOV CNT_HH, #0

    ; 3. 定时器T1配置 (设计提示2)
    ; TMOD: Gate=0, C/T=1(计数), M1=1, M0=0 (方式2: 8位自动重装)
    ; 高4位控制T1, 低4位控制T0. 二进制: 0110 0000
    MOV TMOD, #60H  
    
    ; 设置初值为0xFF, 只要来1个脉冲就溢出中断
    MOV TH1, #0FFH
    MOV TL1, #0FFH

    ; 4. 中断配置
    SETB EA         ; 开总中断
    SETB ET1        ; 开定时器1中断
    SETB EX0        ; 开外部中断0
    SETB EX1        ; 开外部中断1
    
    ; 设置触发方式为下降沿 (ITx = 1)
    SETB IT0
    SETB IT1

    ; 设置外部中断优先级为高 (设计提示1)
    SETB PX0
    SETB PX1

    ; 5. 初始状态: 停止计数
    CLR TR1         ; TR1=0 停止, TR1=1 开始

; 主循环: 负责数码管动态扫描显示
LOOP:
    LCALL DISPLAY_ALL
    SJMP LOOP

; 中断服务程序

; 外部中断0 (启动/暂停)
ISR_INT0:
    CPL TR1         ; 取反TR1位: 运行->暂停, 暂停->运行
    RETI

; 外部中断1 (清零)
ISR_INT1:
    CLR TR1         ; 停止计数
    ; 清除所有计数值
    MOV CNT_LL, #0
    MOV CNT_LH, #0
    MOV CNT_HL, #0
    MOV CNT_HH, #0
    ; 恢复T1初值 (保险起见)
    MOV TL1, #0FFH 
    RETI

;--------------------------------------------------------------------
; 定时器1中断 (脉冲计数核心逻辑)
; 逻辑参考流程图: 多字节十进制加1
;--------------------------------------------------------------------
ISR_T1:
    PUSH PSW        ; 保护现场
    PUSH ACC

    ; --- 最低2位加1 ---
    MOV A, CNT_LL
    ADD A, #1       ; 加1
    DA A            ; BCD调整(虽然存储的是HEX值0-99, 但逻辑上我们需要判100)
                    ; 注意: 这里直接用HEX判断更简单, 因为DA A是针对BCD运算的
                    ; 按照题目流程图逻辑：
    MOV A, CNT_LL
    INC A           ; 寄存器值加1
    MOV CNT_LL, A   ; 存回
    
    CJNE A, #100, T1_EXIT ; 如果不等于100 (即0-99), 退出
    
    ; --- 进位处理 1 ---
    MOV CNT_LL, #0  ; 清零最低2位
    
    MOV A, CNT_LH   ; 取次低2位
    INC A
    MOV CNT_LH, A
    CJNE A, #100, T1_EXIT ; 判断是否满100
    
    ; --- 进位处理 2 ---
    MOV CNT_LH, #0  ; 清零
    
    MOV A, CNT_HL   ; 取次高2位
    INC A
    MOV CNT_HL, A
    CJNE A, #100, T1_EXIT
    
    ; --- 进位处理 3 ---
    MOV CNT_HL, #0  ; 清零
    
    MOV A, CNT_HH   ; 取最高2位
    INC A
    MOV CNT_HH, A
    CJNE A, #100, T1_EXIT
    
    ; --- 溢出归零 (虽然很少发生) ---
    MOV CNT_HH, #0

T1_EXIT:
    POP ACC         ; 恢复现场
    POP PSW
    RETI

DISPLAY_ALL:
    ; 显示第8位 (最高位千万位) - 对应 CNT_HH 的十位
    MOV A, CNT_HH
    MOV B, #10
    DIV AB          ; A = 十位, B = 个位
    MOV DPTR, #TAB
    MOVC A, @A+DPTR ; 查表得段码
    MOV P0, #00H    ; 消隐
    MOV P2, #0FEH   ; 选中第1位 (1111 1110)
    MOV P0, A       ; 输出段码
    LCALL DELAY     ; 延时

    ; 显示第7位 (百万位) - 对应 CNT_HH 的个位
    MOV A, B        ; 取刚才DIV剩下的余数(个位)
    MOVC A, @A+DPTR
    MOV P0, #00H
    MOV P2, #0FDH   ; 选中第2位 (1111 1101)
    MOV P0, A
    LCALL DELAY

    ; 显示第6位 (十万位) - 对应 CNT_HL 的十位
    MOV A, CNT_HL
    MOV B, #10
    DIV AB
    MOVC A, @A+DPTR
    MOV P0, #00H
    MOV P2, #0FBH   ; 选中第3位
    MOV P0, A
    LCALL DELAY

    ; 显示第5位 (万位) - 对应 CNT_HL 的个位
    MOV A, B
    MOVC A, @A+DPTR
    MOV P0, #00H
    MOV P2, #0F7H   ; 选中第4位
    MOV P0, A
    LCALL DELAY

    ; 显示第4位 (千位) - 对应 CNT_LH 的十位
    MOV A, CNT_LH
    MOV B, #10
    DIV AB
    MOVC A, @A+DPTR
    MOV P0, #00H
    MOV P2, #0EFH   ; 选中第5位
    MOV P0, A
    LCALL DELAY

    ; 显示第3位 (百位) - 对应 CNT_LH 的个位
    MOV A, B
    MOVC A, @A+DPTR
    MOV P0, #00H
    MOV P2, #0DFH   ; 选中第6位
    MOV P0, A
    LCALL DELAY

    ; 显示第2位 (十位) - 对应 CNT_LL 的十位
    MOV A, CNT_LL
    MOV B, #10
    DIV AB
    MOVC A, @A+DPTR
    MOV P0, #00H
    MOV P2, #0BFH   ; 选中第7位
    MOV P0, A
    LCALL DELAY

    ; 显示第1位 (个位) - 对应 CNT_LL 的个位
    MOV A, B
    MOVC A, @A+DPTR
    MOV P0, #00H
    MOV P2, #7FH    ; 选中第8位
    MOV P0, A
    LCALL DELAY
    
    MOV P0, #00H    ; 关闭显示
    RET

; 短延时子程序 (控制显示亮度与扫描频率)
DELAY:
    MOV R7, #100    ; 延时计数，可根据仿真速度调整
D1: DJNZ R7, D1
    RET

; 共阴极数码管段码表 (0-9)，对应: P0.0-P0.6 (A-G), P0.7 (DP)
TAB:
    DB 3FH, 06H, 5BH, 4FH, 66H, 6DH, 7DH, 07H, 7FH, 6FH; 对应0~9

    END