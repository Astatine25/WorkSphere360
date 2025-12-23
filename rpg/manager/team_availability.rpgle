**free
Dcl-F EMPBYTEAM Usage(*Input);
Dcl-F LEAVES Usage(*Input);

Dcl-S Total Packed(3);
Dcl-S OnLeave Packed(3);

Read EMPBYTEAM;
Dow Not %Eof(EMPBYTEAM);
   Total += 1;
   Chain EMPID LEAVES;
   If %Found() and STATUS = 'A';
      OnLeave += 1;
   EndIf;
   Read EMPBYTEAM;
EndDo;

Dsply ('Availability % = ' + 
       %Char((Total-OnLeave)*100/Total));
