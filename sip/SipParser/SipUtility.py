''' 
Copyright (C) 2020 Yee Young Han <websearch@naver.com> (http://blog.naver.com/websearch)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''

import threading
import random
import time

gclsMutex = threading.Lock()
giTag = 0
giBranch = 0
giCallId = 0
gstrSystemId = ''

def SipSetSystemId( strId ):
  """ 시스템 아이디 전역 변수에 입력된 문자열을 저장한다.

  Args:
      strId (string): 시스템 아이디
  """
  global gstrSystemId

  gstrSystemId = strId

def SipMakeTag( ):
  """ tag 문자열을 리턴한다.

  Returns:
      string: tag 문자열을 리턴한다.
  """
  global gclsMutex, giTag

  gclsMutex.acquire()
  if( giTag <= 0 or giTag > 2000000000 ):
    giTag = random.randint( 1, 1000000000 )
  else:
    giTag += 1
  iTag = giTag
  gclsMutex.release()

  return str( iTag )

def SipMakeBranch( ):
  """ branch 문자열을 리턴한다.

  Returns:
      string: branch 문자열을 리턴한다.
  """
  global gclsMutex, giBranch, gstrSystemId

  gclsMutex.acquire()
  if( giBranch <= 0 or giBranch > 2000000000 ):
    giBranch = random.randint( 1, 1000000000 )
  else:
    giBranch += 1
  iBranch = giBranch
  gclsMutex.release()

  strBranch = "z9hG4bKWPSS"
  
  if( len(gstrSystemId) > 0 ):
    strBranch += gstrSystemId

  strBranch += str(iBranch) + str(time.time()).replace(".", "")

  return strBranch

def SipMakeCallIdName( ):
  """ SIP Call-ID 이름에 저장할 문자열을 리턴한다.

  Returns:
      string: SIP Call-ID 이름에 저장할 문자열을 리턴한다.
  """
  global gclsMutex, giCallId, gstrSystemId

  gclsMutex.acquire()
  if( giCallId <= 0 or giCallId > 2000000000 ):
    giCallId = random.randint( 1, 1000000000 )
  else:
    giCallId += 1
  iCallId = giCallId
  gclsMutex.release()

  strCallId = "WPSS"
  
  if( len(gstrSystemId) > 0 ):
    strCallId += gstrSystemId

  strCallId += str(iCallId) + str(time.time()).replace(".", "")

  return strCallId

def SipIpv6Parse( strHost ):
  """ IPv6 구분자([])를 제거한 IP 주소를 리턴한다.

  Args:
      strHost (string): IP 주소

  Returns:
      string: IPv6 구분자를 제거한 IP 주소를 리턴한다.
  """
  iLen = len(strHost)
  if( iLen > 0 and strHost[0] == '[' and strHost[iLen-1] == ']' ):
    return strHost[1:iLen]
  
  return strHost

def SipIpv6Print( strHost ):
  """ IPv6 구분자([])를 포함한 IP 주소 문자열을 리턴한다.

  Args:
      strHost (string): IP 주소

  Returns:
      string: IPv6 구분자([])를 포함한 IP 주소 문자열을 리턴한다.
  """
  iLen = len(strHost)

  if( iLen > 2 and strHost[0] != '[' and strHost.find(':') != -1 ):
    return "[" + strHost + "]"
  
  return strHost

