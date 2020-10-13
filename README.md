# Python SIP stack 프로젝트
Python 언어로 SIP stack 을 개발하는 프로젝트입니다.

### 개요
본 프로젝트의 목표는 다음과 같습니다.

* C++ SIP stack 프로젝트를 Python 언어로 포팅한다.
  * https://github.com/YeeYoungHan/cppsipstack
* Python 언어로 SIP stack 개발
* Python SIP stack 기반 IP-PBX 개발

### 개발자 정보
본 프로젝트를 진행하는 개발자 정보는 다음과 같습니다.

* 이메일: websearch@naver.com
* 블로그: http://blog.naver.com/websearch

### 라이선스

* 본 프로젝트의 라이선스는 GPLv3 입니다.
* 본 프로젝트에 대한 상용 라이선스 발급을 원하시면 websearch@naver.com 로 연락해 주세요.

### API 문서
C++ SIP stack API 문서는 아래의 홈페이지에서 확인하실 수 있습니다.

* https://yeeyounghan.github.io/doc/PythonSipStack/html/index.html

### 폴더 설명
본 프로젝트에 포함된 폴더에 대한 설명은 다음과 같습니다.

* sip
  * EchoSipServer : 통화 수신시 해당 통화를 발신자에게 다시 연결하는 프로그램
    * 통화 수신 처리 기능이 포함된 전화 발신 서비스를 테스트하는 용도로 사용될 수 있다.
  * SdpParser : SDP 메시지 파서/생성 라이브러리
  * SipParser : SIP 메시지 파서/생성 라이브러리
  * SipPlatform : 본 프로젝트에서 공통으로 사용하는 라이브러리
  * SipServer : SIP 서버 프로그램
    * Python SIP stack 기반 IP-PBX 프로그램
  * SipStack : SIP stack 라이브러리
  * SipUserAgent : SIP stack 기반 User Agent 라이브러리

* test
  * TestSipParser : SIP/SDP 메시지 파서/생성 라이브러리 테스트 프로그램
  * TestSipPlatform : 공통 라이브러리 테스트 프로그램
  * TestSipUserAgent : SipUserAgent 테스트 프로그램

### SipServer 실행 방법

* sip/SipServer/SipServer.xml 설정 파일을 자신의 환경에 적합하게 수정한다.
  * Sip -> LocalIp 를 수정한다.
  * Log -> Folder 를 수정한다.
* 현재 폴더에서 아래와 같이 실행한다.
```
python -m sip.SipServer.SipServerMain sip\SipServer\SipServer.xml
```

* Python SipServer 는 KSipServer 와 거의 비슷한 설정 파일을 사용하므로 설정 파일 관련 설명은 KSipServer 설정 파일을 설명한 아래의 포스트를 참고하세요.
  * https://blog.naver.com/websearch/70147577937 : KSipServer 설정 파일 설명
  * https://blog.naver.com/websearch/70148992602 : KSipServer 사용자 XML 파일 설명
  * https://blog.naver.com/websearch/70149037102 : KSipServer 외부 IP-PBX XML 파일 설명

### EchoSipServer 실행 방법

* sip/EchoSipServer/EchoSipServer.xml 설정 파일을 자신의 환경에 적합하게 수정한다.
  * Sip -> LocalIp 를 수정한다.
  * Log -> Folder 를 수정한다.
* 현재 폴더에서 아래와 같이 실행한다.
```
python -m sip.EchoSipServer.EchoSipServer sip\EchoSipServer\EchoSipServer.xml
```
