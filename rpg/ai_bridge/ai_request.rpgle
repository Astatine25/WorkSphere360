**free
Dcl-S JsonReq Char(512);

JsonReq = 
'{ "emp_id": ' + %Char(EMPID) +
', "start": "' + %Char(STARTDATE) +
'", "end": "' + %Char(ENDDATE) + '" }';

CallP SendRestRequest(JsonReq);
