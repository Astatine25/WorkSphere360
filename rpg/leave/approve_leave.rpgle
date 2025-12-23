**free
Dcl-F LEAVES Usage(*Update);

Chain LEAVEID LEAVES;
If %Found();
   STATUS = 'A';
   Update LEAVEREC;
EndIf;
