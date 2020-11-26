# python version to test network latency

# firewall setting on server, to allow udp on specified port
firewall-cmd --zone=public --permanent --add-port=8123/udp
firewall-cmd --reload
