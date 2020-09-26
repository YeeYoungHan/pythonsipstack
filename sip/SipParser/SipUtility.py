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

gclsMutex = threading.Lock()
giTag = 0

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

def SipIpv6Print( strHost ):
  iLen = len(strHost)

  if( iLen > 2 and strHost[0] != '[' and strHost.find(':') != -1 ):
    return "[" + strHost + "]"
  
  return strHost

