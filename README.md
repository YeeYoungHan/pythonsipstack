# Python SIP stack ������Ʈ
Python ���� SIP stack �� �����ϴ� ������Ʈ�Դϴ�.

### ����
�� ������Ʈ�� ��ǥ�� ������ �����ϴ�.

* C++ SIP stack ������Ʈ�� Python ���� �����Ѵ�.
  * https://github.com/YeeYoungHan/cppsipstack
* Python ���� SIP stack ����
* Python SIP stack ��� IP-PBX ����

### ������ ����
�� ������Ʈ�� �����ϴ� ������ ������ ������ �����ϴ�.

* �̸���: websearch@naver.com
* ��α�: http://blog.naver.com/websearch

### ���̼���

* �� ������Ʈ�� ���̼����� GPLv3 �Դϴ�.
* �� ������Ʈ�� ���� ��� ���̼��� �߱��� ���Ͻø� websearch@naver.com �� ������ �ּ���.

### ���� ����
�� ������Ʈ�� ���Ե� ������ ���� ������ ������ �����ϴ�.

* sip
  * EchoSipServer : ��ȭ ���Ž� �ش� ��ȭ�� �߽��ڿ��� �ٽ� �����ϴ� ���α׷�
  * SdpParser : SDP �޽��� �ļ�/���� ���̺귯��
  * SipParser : SIP �޽��� �ļ�/���� ���̺귯��
  * SipPlatform : �� ������Ʈ���� �������� ����ϴ� ���̺귯��
  * SipServer : SIP ���� ���α׷�
  * SipStack : SIP stack ���̺귯��
  * SipUserAgent : SIP stack ��� User Agent ���̺귯��

* test
  * TestSipParser : SIP/SDP �޽��� �ļ�/���� ���̺귯�� �׽�Ʈ ���α׷�
  * TestSipPlatform : ���� ���̺귯�� �׽�Ʈ ���α׷�
  * TestSipUserAgent : SipUserAgent �׽�Ʈ ���α׷�

### EchoSipServer ���� ���

* sip/EchoSipServer/EchoSipServer.xml ���� ������ �ڽ��� ȯ�濡 �����ϰ� �����Ѵ�.
  * Sip -> LocalIp �� �����Ѵ�.
  * Log -> Folder �� �����Ѵ�.
* ���� �������� �Ʒ��� ���� �����Ѵ�.
```
python -m sip.EchoSipServer.EchoSipServer sip\EchoSipServer\EchoSipServer.xml
```
