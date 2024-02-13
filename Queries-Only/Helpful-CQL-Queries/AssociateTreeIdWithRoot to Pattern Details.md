```
#event_simpleName=AssociateTreeIdWithRoot
| PatternId =~ match(file="falcon/investigate/detect_patterns.csv", column=PatternId, strict=false)
| select([@timestamp, aid, ComputerName, PatternId,name,scenario,scenarioFriendly,description,severity,show_in_ui,killchain_stage,tactic,technique,objective,pattern_updated])
```