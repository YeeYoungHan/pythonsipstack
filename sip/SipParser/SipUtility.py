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
  global gstrSystemId

  gstrSystemId = strId

def SipMakeTag( ):
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


def SipIpv6Print( strHost ):
  iLen = len(strHost)

  if( iLen > 2 and strHost[0] != '[' and strHost.find(':') != -1 ):
    return "[" + strHost + "]"
  
  return strHost

