**free
Dcl-F LEAVES Usage(*Input);

Dcl-Pi *N Ind;
   pEmpId Packed(5);
   pStart Date;
   pEnd   Date;
End-Pi;

Read LEAVES;
Dow Not %Eof(LEAVES);
   If EMPID <> pEmpId and
      (pStart <= ENDDATE and pEnd >= STARTDATE);
      Return *On;
   EndIf;
   Read LEAVES;
EndDo;

Return *Off;
