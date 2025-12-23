**FREE
ctl-opt dftactgrp(*no) actgrp('WS360');

dcl-f LEAVE usage(*update) keyed;

dcl-pi *n;
  empId packed(6);
  fromDate date;
  toDate date;
end-pi;

if toDate < fromDate;
   dsply 'Invalid date range';
   return;
endif;

write LEAVEREC;
commit;

dsply 'Leave Applied Successfully';

