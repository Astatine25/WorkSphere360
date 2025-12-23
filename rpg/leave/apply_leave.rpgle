**free
Dcl-F LEAVES Usage(*Update:*Output);
Dcl-F LEAVEBAL Usage(*Update);

Dcl-Pi *N;
   pEmpId  Packed(5);
   pStart  Date;
   pEnd    Date;
End-Pi;

Chain pEmpId LEAVEBAL;
If %Found();
   If USEDLEAVE + (%Diff(pEnd:pStart)+1) <= TOTALLEAVE;
      Write LEAVEREC;
   Else;
      Dsply 'Insufficient Leave Balance';
   EndIf;
EndIf;
