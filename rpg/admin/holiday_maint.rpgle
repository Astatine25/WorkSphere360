**free
Dcl-F HOLIDAYS Usage(*Update);

Dcl-S HolDate Date;
Dcl-S Desc Char(30);

Accept HolDate;
Accept Desc;

HOLDATE = HolDate;
DESCRIPTION = Desc;
Write HOLREC;
