**FREE
ctl-opt dftactgrp(*no);

dcl-f LEAVE usage(*update) keyed;

dcl-pi *n;
  leaveId packed(7);
end-pi;

chain leaveId LEAVE;
if %found(LEAVE);
   STATUS = 'A';
   update LEAVEREC;
endif;

commit;
