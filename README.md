# ryu-practice
## hw2
[link](https://wiki.kshuang.xyz/doku.php/ccis_lab:sdn:hw2)
### Request
* 寫一個 Ryu App :
  controller 對每個 switch 初始設置兩條 flow entry
  從 port A 進來的封包就送往 port B
  從 port B 進來的封包就送往 port A
  A, B port 必須動態偵測，不能直接 hardcode 在程式內
  不寫 packet_in handler，這兩條 flow entry 必須為初始化設定，而非等到 packet_in 的監聽事件發生才設置
* Tips : 
  Controller 必須去詢問 switch 有哪些 port 是 active 的，此時應該會得到三個 port，其中一個是 special port(接到 controller)，埠號會大於 ofpp_max 這個常數，剩下兩個即是連接 hosts 的 port
### Result
```
mininet> s1 ovs-ofctl -O OpenFlow13 dump-flows "s1"
OFPST_FLOW reply (OF1.3) (xid=0x2):
 cookie=0x0, duration=45.382s, table=0, n_packets=2, n_bytes=140, priority=1,in_port=1 actions=output:2
 cookie=0x0, duration=45.381s, table=0, n_packets=1, n_bytes=70, priority=1,in_port=2 actions=output:1
```
## hw3
[link](https://wiki.kshuang.xyz/doku.php/ccis_lab:sdn:hw3)
