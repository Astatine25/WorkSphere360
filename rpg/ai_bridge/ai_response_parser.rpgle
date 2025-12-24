**FREE
dcl-s approvalProb packed(3:2);

approvalProb = 0.85;

if approvalProb > 0.75;
   dsply 'AI Recommendation: APPROVE';
else;
   dsply 'AI Recommendation: REVIEW';
endif;
