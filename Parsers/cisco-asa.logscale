/(<(?<priority>\d+)>)?(?<@timestamp>\S+\s+\S+\s+\S+\s+\S+)\s+(?<host>\S+)?\s+(?<app>[^\s\[:]+)?(\[(?<pid>[^\]]+)\]:)?(?<msg>.*)/ 
| /%(?<cisco_facility>[A-Z0-9_]+)-(?<cisco_severity>[0-7]+)-(?<cisco_mnemonic>[A-Z0-9_]+): (?<cisco_message>.+)/

// enrich events with severity name
| match("cisco-asa_severity_lookup.csv",field="cisco_severity")

// enrich events with class names
| cisco_className:="-unknown-" | cisco_classDefinition:="-unknown-"
| regex("(?<cisco_messageClass>.{3})", field=cisco_mnemonic)
| match("cisco-asa_message_class.csv",column=cisco_messageClass,field=cisco_messageClass,strict=false)
| drop(cisco_messageClass)

// generic from/to IPv4 address extraction
// + based on mnemonic, do targeted extraction
| case {
    regex("from (?<cisco_interfaceSrc>\S+):(?<src_addr>\d+\.\d+\.\d+\.\d+)\/(?<cisco_srcPort>\d+) to (?<cisco_interfaceDest>\S+):(?<dest_addr>\d+\.\d+\.\d+\.\d+)\/(?<cisco_destPort>\d+)",field=cisco_message) ;
    regex("71000[23]", field=cisco_mnemonic) | regex("(?<cisco_protocol>\S+) access (?<cisco_action>\S+).+from (?<src_addr>\S+)\/(?<cisco_srcPort>\d+) to (?<cisco_interface>\S+):(?<dest_addr>\S+)\/(?<cisco_destPort>\d+)", field=cisco_message) ;
    regex("1060(06|15)", field=cisco_mnemonic) | regex("(?<cisco_action>\S+).+from (?<src_addr>\d+\.\d+\.\d+\.\d+)\/(?<cisco_srcPort>\d{1,5}) to (?<dest_addr>\d+\.\d+\.\d+\.\d+)\/(?<cisco_destPort>\d{1,5}).+on interface (?<cisco_interface>\S+)", field=cisco_message) ;
    regex("30201[3-6]", field=cisco_mnemonic) | regex("(?<cisco_action>\S+).+for (?<cisco_interfaceSrc>\S+):(?<src_addr>\d+\.\d+\.\d+\.\d+)\/(?<cisco_srcPort>\d{1,5}).+to (?<cisco_interfaceDest>\S+):(?<dest_addr>\d+\.\d+\.\d+\.\d+)\/(?<cisco_destPort>\d{1,5})", field=cisco_message) ;
    * ;
  }

| parseTimestamp("MMM [ ]d yyyy HH:mm:ss", field=@timestamp, timezone="UTC")
| kvParse()