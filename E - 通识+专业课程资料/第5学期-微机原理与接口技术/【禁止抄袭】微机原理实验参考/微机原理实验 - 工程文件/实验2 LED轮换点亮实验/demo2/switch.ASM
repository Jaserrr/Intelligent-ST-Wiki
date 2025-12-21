ORG 0000H
LJMP MAIN  ; 跳转到主程序

ORG 0100H
MAIN:
MOV R0, #08H  ; 循环8次（覆盖P1.0~P1.7共8个LED）
MOV A, #0FEH  ; 初始值：二进制11111110 → P1.0=0（亮），P1.1~P1.7=1（灭）

LOOP:
MOV P1, A     ; 将电平状态输出到P1口（控制LED）
LCALL DELAY   ; 延时保持当前亮灯状态
RL A          ; 左移指令：低电平（亮灯）从P1.0→P1.1→...→P1.7移动
DJNZ R0, LOOP ; 循环次数减1，未到8次则继续
SJMP MAIN     ; 循环完成后重新开始，往复执行

; 延时函数（数值越小，速度越快）
DELAY:
MOV R7, #1FH  ; 外层循环次数（控制总延时）
DELAY0:
MOV R6, #3FH  ; 中层循环次数
DELAY1:
MOV R5, #3FH  ; 内层循环次数
DJNZ R5, $    ; 内层空循环（消耗时间）
DJNZ R6, DELAY1
DJNZ R7, DELAY0
RET

END