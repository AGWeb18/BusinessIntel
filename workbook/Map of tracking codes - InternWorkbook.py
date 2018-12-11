#   NP
#   Any of the "Initial Tx Billing" counts as NP 
#   WSIB Init + MIG Init also count
{"6100 NC":"NP", "6100 Reeval - NP credit":"NP", "Bronte Reeval NP credit":"NP", "GLAD CMCC NP":"NP", "GLAD NP":"NP",
"IB Bronte":"NP","IB INIT":"NP", "IB Outreach":"NP", "IB Sherb":"NP", "IB STJ":"NP", "Sher Reeval - NP credit":"NP",
"SRV initial":"NP", "SRV Reeval - NP credit":"NP", "STJ Reeval - NP credit":"NP",
"WSIB initial":"NP", "MIG initial":"NP"}

#   SUBS
#   Anything under "Sub Tx Billing"
#   SB POC Sub + WSIB SUB + MIG SUB
#   IB Cont/ SB No Show NO CREDIT
{"GLAD sub":"SUB","IB Bronte reeval":"SUB", "IB NC":"SUB","IB REEVAL":"SUB",
"IB Sherb reeval":"SUB","IB SRV reeval":"SUB","IB STJ NC":"SUB","IB STJ Re Eval":"SUB",
"SB Bronte":"SUB","SB Extended":"SUB","SB HR sub":"SUB", "SB no show":"SUB",
"SB one hour":"SUB", "SB OT":"SUB", "SB OT return":"SUB","SB Outreach MACC":"SUB",
"SB Sherb":"SUB","SB STJ":"SUB","SB SUB":"SUB", "SB TXIN":"SUB", "SRV sub":"SUB",
"SB POC Sub":"SUB", "WSIB sub":"SUB","MIG sub":"SUB"}

#   SMT
#   2 values, only count 1 per visit for ACCREDITATION. Count Each as well
#   SMT - ADJ CER, LUM, PEL, THOR | MOBS CER, LUM, PEL, THR
#   EXT SMT - All other adjustments
{"ADJ CER":"SMT", "ADJ LUM":"SMT","ADJ PEL":"SMT", "ADJ THOR":"SMT",
"MOBS CER":"SMT", "MOBS LUM":"SMT","MOBS PEL":"SMT","MOBS THR":"SMT",
"MOBS ANK":"EXT-SMT","MOBS ELB":"EXT-SMT","MOBS FT":"EXT-SMT","MOBS HIP":"EXT-SMT",
"MOBS HND":"EXT-SMT","MOBS KNE":"EXT-SMT","MOBS RIB":"EXT-SMT","MOBS SHD":"EXT-SMT",
"MOBS TMJ":"EXT-SMT", "ADJ ANK":"EXT-SMT", "ADJ ELB":"EXT-SMT","ADJ FT":"EXT-SMT",
"ADJ":"EXT-SMT", "ADJ KNEE":"EXT-SMT", "ADJ RIB":"EXT-SMT", "ADJ SHD":"EXT-SMT", 
"ADJ TMJ":"EXT-SMT","ADJ WRT":"EXT-SMT","AJD HIP":"EXT-SMT"}
