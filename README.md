# ryu-practice
## hw2

```
mininet> s1 ovs-ofctl -O OpenFlow13 dump-flows "s1"
OFPST_FLOW reply (OF1.3) (xid=0x2):
 cookie=0x0, duration=45.382s, table=0, n_packets=2, n_bytes=140, priority=1,in_port=1 actions=output:2
 cookie=0x0, duration=45.381s, table=0, n_packets=1, n_bytes=70, priority=1,in_port=2 actions=output:1
```
