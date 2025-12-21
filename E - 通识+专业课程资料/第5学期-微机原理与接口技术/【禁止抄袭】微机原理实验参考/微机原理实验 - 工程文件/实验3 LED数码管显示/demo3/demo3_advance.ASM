;====================================================================
; 实验名称：LED数码管显示与按钮输入 (修正版)
; 硬件映射：
;   数据总线：P2.0 - P2.7  -> 接 74HC573 输入 (D0-D7)
;   段选控制：P3.0         -> 接 段码锁存器 LE (上方的573)
;   位选控制：P3.1         -> 接 位码锁存器 LE (下方的573)
;   按键输入：P3.2         -> 接 按钮公共端 (INT0)
;====================================================================

;--- 定义变量与引脚 ---
SEG_LE      BIT P3.0        ; 段锁存使能 (根据原理图修改)
BIT_LE      BIT P3.1        ; 位锁存使能 (根据原理图修改)
KEY_IN      BIT P3.2        ; 按键输入

DISP_BUF    EQU 30H         ; 显示缓冲区起始地址 (30H-37H)

;--- 程序入口 ---
ORG 0000H
    LJMP MAIN

;--- 主程序 ---
ORG 0030H
MAIN:
    MOV SP, #60H            ; 初始化堆栈
    CALL INIT_BUFFER        ; 初始化显示内容 "HELLO-- "

MAIN_LOOP:
    CALL DISPLAY_SCAN       ; 循环调用扫描
    SJMP MAIN_LOOP

;--------------------------------------------------------------------
; 子程序：初始化显示缓冲区
; 内容：H E L L O - - (空格)
;--------------------------------------------------------------------
INIT_BUFFER:
    MOV 30H, #10            ; H
    MOV 31H, #11            ; E
    MOV 32H, #12            ; L
    MOV 33H, #12            ; L
    MOV 34H, #00            ; O (用0代替)
    MOV 35H, #13            ; -
    MOV 36H, #13            ; -
    MOV 37H, #14            ; 空格
    RET

;--------------------------------------------------------------------
; 子程序：显示扫描与按键检测
;--------------------------------------------------------------------
DISPLAY_SCAN:
    MOV R0, #DISP_BUF       ; R0指向缓冲区
    MOV R1, #0FEH           ; 位扫描初值 (1111 1110)
    MOV R2, #0              ; 键号计数器 (0-7)

SCAN_LOOP:
    ; 1. 送位选码 (选择哪一位显示，同时拉低对应的按键列线)
    MOV P2, R1              ; 【修改】数据送 P2 口
    SETB BIT_LE             ; 打开位锁存
    CLR  BIT_LE             ; 锁存位码

    ; 2. 按键检测 (检测 P3.2 是否被当前列的低电平拉低)
    JB KEY_IN, NO_KEY       ; 若 P3.2 为高，说明无键按下，跳过
    
    ; --- 按键处理 ---
    CALL DELAY_SMALL        ; 消抖
    JB KEY_IN, NO_KEY       ; 再次确认
    
    CALL SHIFT_DISPLAY      ; 移位并存入新键号(R2)
    CALL WAIT_KEY_UP        ; 等待按键释放
    ; ---------------

NO_KEY:
    ; 3. 送段选码 (显示字符)
    MOV A, @R0              ; 取显示内容索引
    MOV DPTR, #SEG_TABLE    ; 查表
    MOVC A, @A+DPTR
    MOV P2, A               ; 【修改】数据送 P2 口
    SETB SEG_LE             ; 打开段锁存
    CLR  SEG_LE             ; 锁存段码

    ; 4. 延时显示
    CALL DELAY_SCAN

    ; 5. 消隐 (防止拖影)
    MOV P2, #00H            ; 【修改】关断所有段
    SETB SEG_LE
    CLR  SEG_LE

    ; 6. 准备下一位
    INC R0                  ; 指向下一个显存单元
    MOV A, R1
    RL A                    ; 位码左移
    MOV R1, A
    INC R2                  ; 键号加1
    
    CJNE R2, #8, SCAN_LOOP  ; 扫完8位则结束
    RET

;--------------------------------------------------------------------
; 子程序：移位处理
; 功能：缓冲区左移，新键值 R2 存入最右侧 (37H)
;--------------------------------------------------------------------
SHIFT_DISPLAY:
    MOV 30H, 31H
    MOV 31H, 32H
    MOV 32H, 33H
    MOV 33H, 34H
    MOV 34H, 35H
    MOV 35H, 36H
    MOV 36H, 37H
    MOV 37H, R2             ; 新按键值存入最后一位
    RET

;--------------------------------------------------------------------
; 子程序：等待按键释放
; 等待过程中必须持续刷新显示，否则数码管会闪烁或熄灭
;--------------------------------------------------------------------
WAIT_KEY_UP:
    PUSH 00H
    PUSH 01H
    PUSH 02H

WAIT_LOOP:
    JB KEY_IN, WAIT_EXIT    ; 按键释放(变为高电平)则退出
    
    ; 简单的显示刷新循环 (不检测按键)
    MOV R0, #DISP_BUF
    MOV R1, #0FEH
    MOV R2, #8
REFRESH_LOOP:
    ; 送位
    MOV P2, R1              ; 【修改】P2
    SETB BIT_LE
    CLR  BIT_LE
    ; 送段
    MOV A, @R0
    MOV DPTR, #SEG_TABLE
    MOVC A, @A+DPTR
    MOV P2, A               ; 【修改】P2
    SETB SEG_LE
    CLR  SEG_LE
    ; 延时
    CALL DELAY_SCAN
    ; 消隐
    MOV P2, #00H            ; 【修改】P2
    SETB SEG_LE
    CLR  SEG_LE
    ; 下一位
    INC R0
    MOV A, R1
    RL A
    MOV R1, A
    DJNZ R2, REFRESH_LOOP
    
    SJMP WAIT_LOOP

WAIT_EXIT:
    POP 02H
    POP 01H
    POP 00H
    RET

;--------------------------------------------------------------------
; 延时子程序
;--------------------------------------------------------------------
DELAY_SCAN:                 ; 扫描延时 (~1ms)
    MOV R3, #200
    DJNZ R3, $
    RET

DELAY_SMALL:                ; 消抖延时 (~10ms)
    MOV R3, #20
D1: MOV R4, #248
    DJNZ R4, $
    DJNZ R3, D1
    RET

;--------------------------------------------------------------------
; 段码表 (共阴极)
;--------------------------------------------------------------------
SEG_TABLE:
    DB 3FH  ; 0
    DB 06H  ; 1
    DB 5BH  ; 2
    DB 4FH  ; 3
    DB 66H  ; 4
    DB 6DH  ; 5
    DB 7DH  ; 6
    DB 07H  ; 7
    DB 7FH  ; 8
    DB 6FH  ; 9
    DB 76H  ; 10 (H)
    DB 79H  ; 11 (E)
    DB 38H  ; 12 (L)
    DB 40H  ; 13 (-)
    DB 00H  ; 14 (空格)

END