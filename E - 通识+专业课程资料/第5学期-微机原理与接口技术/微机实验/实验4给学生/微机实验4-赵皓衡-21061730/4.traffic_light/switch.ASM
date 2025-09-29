ORG  0000H
LJMP MAIN
ORG  0003H
LJMP INTA
ORG  0100H

MAIN: MOV SP, #60H
      SETB IT0
      SETB EA
      SETB EX0
      CLR P2.6
      CLR A  
      CALL STATUS0

CIRCLE: LCALL STATUS1
        JNZ MAIN
        LCALL STATUS2
        JNZ MAIN
        LCALL STATUS3
        JNZ MAIN
        LCALL STATUS4
        JNZ MAIN
        LJMP CIRCLE

STATUS0: SETB P2.6
         LCALL CLRLIGHT        
         SETB P0.0
         SETB P0.3
         CLR P2.6
         LCALL DELAY2S
         RET

STATUS1: SETB P2.6
         LCALL CLRLIGHT  
         SETB P0.0
         SETB P0.5
         CLR P2.6
         LCALL DELAY3S
         RET

STATUS2: SETB P2.6
         LCALL CLRLIGHT  
         SETB P0.0
         SETB P0.4
         CLR P2.6
         LCALL DELAY2S
         RET

STATUS3: SETB P2.6
         LCALL CLRLIGHT  
         SETB P0.2
         SETB P0.3
         CLR P2.6
         LCALL DELAY3S
         RET

STATUS4: SETB P2.6
         LCALL CLRLIGHT  
         SETB P0.1
         SETB P0.3
         CLR P2.6
         LCALL DELAY2S
         RET

CLRLIGHT: CLR P0.0
          CLR P0.1
          CLR P0.2
          CLR P0.3
          CLR P0.4
          CLR P0.5
          RET

INTA: CLR A
      SETB P2.6
      LCALL CLRLIGHT  
      SETB P0.0
      SETB P0.3
      CLR P2.6
      INC A
      RETI

DELAY3S:
    MOV R7,#0BDH
DL1:
    MOV R6,#0E6H
DL0:
    MOV R5,#21H
    DJNZ R5,$
    DJNZ R6,DL0
    DJNZ R7,DL1
    RET

DELAY2S:   
    MOV R7,#7FH
DL3:
    MOV R6,#0EBH
DL2:
    MOV R5,#20H
    DJNZ R5,$
    DJNZ R6,DL2
    DJNZ R7,DL3
    NOP
    RET

END

