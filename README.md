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
### Request
* controller 對每個 switch 初始設置一條 flow entry: 當收到的封包型態為 LLDP 時發給 controller
* controller 讓 switch 每個使用中的 port 送出 LLDP 封包
* 設計一個資料結構存取 LLDP 得到的 topo
* 需要 packet in handler 取得 switch 收到 LLDP 封包中的資訊
### Result
```
$ sudo python hw3_net.py -n 6
```
```
loading app hw3_ryuapp.py
loading app ryu.controller.ofp_handler
instantiating app ryu.controller.ofp_handler of OFPHandler
instantiating app hw3_ryuapp.py of hw3_RyuApp
{2: {1: ['1', '2']}}
{2: {1: ['1', '2'], 2: ['3', '1']}}
{2: {1: ['1', '2'], 2: ['3', '1']}, 6: {2: ['5', '2']}}
{2: {1: ['1', '2'], 2: ['3', '1']}, 4: {1: ['3', '2']}, 6: {2: ['5', '2']}}
{2: {1: ['1', '2'], 2: ['3', '1']}, 4: {1: ['3', '2'], 2: ['5', '1']}, 6: {2: ['5', '2']}}
```
## hw4
[link](https://wiki.kshuang.xyz/doku.php/ccis_lab:sdn:hw4)
### Request
* 使用 RESTful API 請求取得 hw3 lldp_struct
### Result
```
araielwu@araielwu-VirtualBox:~/ryu-folder$ ryu-manager hw4_ryuapp.py 
loading app hw4_ryuapp.py
loading app ryu.controller.ofp_handler
creating context wsgi
instantiating app hw4_ryuapp.py of hw4_RyuApp
instantiating app ryu.controller.ofp_handler of OFPHandler
(6945) wsgi starting up on http://0.0.0.0:8080
{1: {2: ['2', '1']}}
{1: {2: ['2', '1']}, 2: {2: ['3', '1']}}
{1: {2: ['2', '1']}, 2: {2: ['3', '1']}, 3: {2: ['4', '1']}}
{1: {2: ['2', '1']}, 2: {2: ['3', '1']}, 3: {2: ['4', '1']}, 4: {2: ['5', '1']}}
{1: {2: ['2', '1']}, 2: {2: ['3', '1']}, 3: {2: ['4', '1']}, 4: {2: ['5', '1']}, 5: {2: ['6', '2']}}
(6945) accepted ('127.0.0.1', 38916)
127.0.0.1 - - [09/Feb/2019 15:56:22] "GET /lldp/1 HTTP/1.1" 200 155 0.001103
(6945) accepted ('127.0.0.1', 38918)
127.0.0.1 - - [09/Feb/2019 15:56:24] "GET /lldp/2 HTTP/1.1" 200 155 0.021078
(6945) accepted ('127.0.0.1', 38920)
127.0.0.1 - - [09/Feb/2019 15:56:28] "GET /lldp/3 HTTP/1.1" 200 155 0.000471
(6945) accepted ('127.0.0.1', 38922)
127.0.0.1 - - [09/Feb/2019 15:56:30] "GET /lldp/4 HTTP/1.1" 200 155 0.002926
(6945) accepted ('127.0.0.1', 38924)
127.0.0.1 - - [09/Feb/2019 15:56:32] "GET /lldp/5 HTTP/1.1" 200 155 0.000404
(6945) accepted ('127.0.0.1', 38926)
127.0.0.1 - - [09/Feb/2019 15:56:35] "GET /lldp/6 HTTP/1.1" 404 133 0.000439

```

```
araielwu@araielwu-VirtualBox:~$ curl http://0.0.0.0:8080/lldp/1
{
    "2": [
        "2", 
        "1"
    ]
}
araielwu@araielwu-VirtualBox:~$ curl http://0.0.0.0:8080/lldp/2
{
    "2": [
        "3", 
        "1"
    ]
}
araielwu@araielwu-VirtualBox:~$ curl http://0.0.0.0:8080/lldp/3
{
    "2": [
        "4", 
        "1"
    ]
}
araielwu@araielwu-VirtualBox:~$ curl http://0.0.0.0:8080/lldp/4
{
    "2": [
        "5", 
        "1"
    ]
}
araielwu@araielwu-VirtualBox:~$ curl http://0.0.0.0:8080/lldp/5
{
    "2": [
        "6", 
        "2"
    ]
}
araielwu@araielwu-VirtualBox:~$ curl http://0.0.0.0:8080/lldp/6
Not found

```
