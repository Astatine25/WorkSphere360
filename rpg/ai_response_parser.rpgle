**free
Dcl-S Risk Char(10);
Dcl-S Prob Packed(5:2);

/* Parse JSON response */
Risk = 'LOW';
Prob = 0.85;

Dsply ('AI Risk: ' + Risk);
Dsply ('Approval Probability: ' + %Char(Prob));
