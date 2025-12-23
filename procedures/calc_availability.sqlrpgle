**FREE
exec sql
  select count(*) into :avail
  from EMPLOYEE
  where STATUS = 'A';

dsply ('Available: ' + %char(avail));
