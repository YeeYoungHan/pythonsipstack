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

import sys
from .SipClientSetup import SipClientSetup
from .SipClient import SipClient

if( len(sys.argv) == 1 ):
  print( "[Usage] python -m sip.SipClient.SipClientMain {setup file path}")
  exit()

strSetupFileName = sys.argv[1]
clsSetupFile = SipClientSetup()

if( clsSetupFile.Read( strSetupFileName ) == False ):
  print( "lsSetupFile.Read(" + strSetupFileName + ") error" )
  exit()

clsClient = SipClient()
if( clsClient.Start( clsSetupFile ) == False ):
  print( "clsClient.Start() error" )
  exit()

while True:
  strLine = sys.stdin.readline()
  strLine = strLine[:-1]
  
  if( len(strLine) == 0 ):
    continue

  if( strLine[0] == 'c' ):
    strNumber = strLine[2:]
    clsClient.StartCall( strNumber )
  elif( strLine[0] == 'a' ):
    clsClient.AcceptCall( )
  elif( strLine[0] == 'e' ):
    clsClient.StopCall( )
  elif( strLine[0] == 'q' ):
    break
