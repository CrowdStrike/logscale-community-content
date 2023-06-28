| case {
    // First look for the filterlog and apply the CSV parser.
    /\sfilterlog\[/ 
      | parseCsv(field=@rawstring, delimiter=",", columns=[header, subrule, placeholder1, tracker, iface, reason, action, direction, ip_ver, tos, ttl, id, offset, placeholder2, flags, proto_id, proto, length, src_ip, dst_ip, src_port, dst_port, data_length]) ;
    // Next parse the DHCP logs and create the fields with capture groups. 
    /\sdhcpd\[.*?\]\:\s(?<dhcp_type>.*?)\s(for|on)\s(?<src_ip>.*?)\s(to|from)\s(?<src_mac>.*?)\s\((?<dhcp_hostname>.*?)\)\svia\s(?<dhcp_int>.*?)\s/ ;
    *
  }
| case {
    // Apply when the src_ip is a non-RFC1918 IP address. 
    !cidr(src_ip, subnet=["224.0.0.0/4", "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "127.0.0.0/8", "169.254.0.0/16", "0.0.0.0/32"])
      | ipLocation(src_ip)
      | ioc:lookup(["src_ip"], type="ip_address") ;
    * ;
  }
| case {
    // Apply when the dst_ip is a non-RFC1918 IP address. 
    !cidr(dst_ip, subnet=["224.0.0.0/4", "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "127.0.0.0/8", "169.254.0.0/16", "0.0.0.0/32"])
      | ipLocation(dst_ip)
      | ioc:lookup(["dst_ip"], type="ip_address") ;
    * ;
  }