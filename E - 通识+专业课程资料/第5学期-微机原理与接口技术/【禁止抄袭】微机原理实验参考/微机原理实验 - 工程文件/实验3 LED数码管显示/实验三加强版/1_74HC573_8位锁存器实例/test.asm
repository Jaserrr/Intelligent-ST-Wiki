           CLR P3.0
LOOP:      JB P3.3, LOOP
           SETB P3.0
           NOP
           CLR P3.0
           LJMP LOOP
           END
