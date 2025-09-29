;本程序完成温度采集并在最左边的2只数码管显示温度值

LEDSCAN  	EQU 30H  ; LED数码管扫描码单元	
LED_D0  	EQU 50H  ; 8个LED数码管数据缓存器
LED_D1  	EQU 51H
LED_D2  	EQU 52H
LED_D3  	EQU 53H
LED_D4  	EQU 54H
LED_D5  	EQU 55H
LED_D6  	EQU 56H
LED_D7  	EQU 57H
TDATA_H16	EQU 40H	 ; 温度十六进制值
T_NUM		EQU 41H	 ; 定时循环次数
ADC_STAR	BIT P2.2 ;  AD启动位
ADC_RD		BIT P2.1 ;  AD值读取控制位
ADC_EOC		BIT P3.4 ;  AD转换完毕查询位
LEDSEG_LE	BIT P2.6 ; LED数码管段数据锁存位
BITSAN_LE	BIT P2.7 ; LED数码管或按钮位扫描数据锁存位



			ORG		0000H                    
			AJMP   	MAIN
			
			ORG    	000BH				;定时器0  用于LED状态变化 AD采样
			AJMP   	TIME0

           	ORG    	0100H
MAIN:      	MOV    	SP,#60H
           	MOV    	TMOD,#01H		   	;定时器0工作方式1
           	MOV    	TL0,#0DCH           ;装载计数初值
           	MOV    	TH0,#0BH            ;每次循环125ms

           	SETB   	TR0                 ;开启定时器0
           	SETB   	ET0                 ;允许定时0中断
           	SETB   	EA

        
           	MOV    	TDATA_H16,#25		;当前测得的温度值,此初赋值32度，实际没有意义,因为程序运行后立马更新         
           	MOV    	T_NUM,#08H          ;125ms基本定时循环次数
	   		CLR    	ADC_RD			 	; AD数据读取无效
	   		CLR    	ADC_STAR			; AD启动无效

HERE:      	ACALL 	SHOW
           	ACALL 	DISP         
           	JMP 	HERE



SHOW:      
           	MOV    	A,TDATA_H16			;TDATA_H16里放着实际温度
           	MOV    	B,#0AH				;拆数字
           	DIV    	AB
           	MOV    	LED_D0,A			;十位送54H
           	MOV    	LED_D1,B			;个位送55H
	   		MOV    	LED_D2, #10H		;右边6个LED不显示
           	MOV    	LED_D3, #10H
	   		MOV    	LED_D4, #10H				
           	MOV    	LED_D5, #10H
	   		MOV    	LED_D6, #10H				
	   		MOV    	LED_D7, #10H				        
           	RET


DISP:   	PUSH	DPH
        	PUSH 	DPL
        	PUSH 	PSW
        	PUSH 	ACC
        	MOV 	R0, #LED_D0			;显示缓冲单元首地址
       	 	MOV 	LEDSCAN, #0FEH  	;位控码
LD0:      
        	MOV 	P0,#0FFH	    	;清位控口	 
        	SETB 	BITSAN_LE			; LED数码管或按钮位扫描数据锁存位
        	NOP
        	CLR 	BITSAN_LE
        	MOV 	DPTR, #TABLE    	;查段码    
        	MOV 	A, @R0
        	MOVC 	A, @A+DPTR	 	       	     
	 		MOV 	P0,A            	;送段码
        	SETB 	LEDSEG_LE			; LED数码管段数据锁存位
        	NOP
        	CLR 	LEDSEG_LE
        	MOV 	A, LEDSCAN
        	MOV 	P0,A            	;送位控码
	  		SETB 	BITSAN_LE			; LED数码管或按钮位扫描数据锁存位
        	NOP
        	CLR 	BITSAN_LE
        	ACALL  	DELAY
        	INC 	R0
        	MOV 	A, LEDSCAN
        	JNB  	ACC.7,LD1		 
        	RL  	A
        	MOV 	LEDSCAN, A
        	AJMP 	LD0
LD1:    	MOV 	P0,#00	        	;清段控口,修改
        	SETB 	LEDSEG_LE			; LED数码管段数据锁存位
        	NOP
        	CLR 	LEDSEG_LE   
       		MOV 	P0,#0FFH	    	;清位控口
	  		SETB 	BITSAN_LE			; LED数码管或按钮位扫描数据锁存位
        	NOP
        	CLR 	BITSAN_LE   
        	POP 	ACC
        	POP 	PSW
        	POP 	DPL
        	POP 	DPH
        	RET

TABLE:    	DB 3FH,06H,5BH,4FH,66H     ; 0    1    2   3   4
          	DB 6DH,7DH,07H,7FH,6FH     ; 5    6    7   8   9
          	DB 77H,7CH,39H,5EH,79H     ; A    B    C   D   E
          	DB 71H,00H,76H,38H,40H     ; F    灭	 H   L	 -

DELAY:    	MOV 	R1,#02H            ;延时约1ms
DEL0:     	MOV 	R2, #00H
DEL1:     	DJNZ 	R2, DEL1
          	DJNZ 	R1, DEL0
	      	RET



TIME0:
          	PUSH 	DPH
          	PUSH 	DPL
          	PUSH 	ACC
          	PUSH 	PSW
          	MOV 	TL0,#0DCH
          	MOV 	TH0,#0BH
          	MOV 	A,T_NUM
          	DEC 	A
          	MOV 	T_NUM,A
          	JNZ 	RET0
          	MOV 	T_NUM,#08H
          	MOV 	P1,#00H             ;启动IN0通道
          	SETB 	ADC_STAR
	  		NOP
          	CLR 	ADC_STAR
WW:
          	JNB 	ADC_EOC,WW      	; 查询转化结果,这里也可以使用软件延时100ms，以避免死循环。
          	SETB 	ADC_RD
          	NOP
          	MOV 	P1,#0FFH            ; 读数据前先写入高电平
	  		MOV 	A,P1
	  		CLR 	ADC_RD
          	SUBB 	A,#22H             	; 减偏移24
          	MOV 	DPTR,#TEM_TAB
          	MOVC 	A,@A+DPTR
          	MOV 	TDATA_H16,A

RET0:     	POP 	PSW
          	POP 	ACC
          	POP 	DPL
          	POP 	DPH
          	RETI

TEM_TAB:   	DB     63H,61H,5FH,5DH,5CH,5AH,59H,58H,56H,55H,54H,52H,51H,50H,4FH,4EH
           	DB     4DH,4CH,4BH,4AH,49H,48H,47H,46H,45H,44H,43H,42H,41H,41H,40H,3FH
           	DB     3EH,3EH,3DH,3CH,3BH,3AH,3AH,39H,38H,38H,37H,37H,36H,35H,34H,34H
           	DB     33H,33H,32H,32H,31H,30H,30H,2FH,2EH,2EH,2DH,2DH,2CH,2CH,2BH,2BH
           	DB     2AH,2AH,29H,29H,28H,28H,27H,27H,26H,26H,25H,25H,24H,24H,23H,23H
           	DB     22H,22H,21H,21H,20H,20H,1FH,1FH,1EH,1EH,1EH,1DH,1DH,1CH,1CH,1BH
           	DB     1BH,1BH,1AH,1AH,19H,19H,18H,18H,18H,17H,17H,16H,16H,15H,15H,15H
           	DB     15H,15H,13H,13H,12H,12H,12H,11H,11H,10H,10H,0FH,0FH,0FH,0EH,0EH
           	DB     0DH,0DH,0CH,0CH,0CH,0BH,0BH,0AH,0AH,0AH,09H,09H,08H,08H,08H,07H
           	DB     07H,06H,06H,05H,05H,04H,04H,04H,03H,03H,02H,02H,01H,01H,00H,00H


END



