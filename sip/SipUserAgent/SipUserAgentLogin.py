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

def InsertRegisterInfo( self, clsServerInfo ):
  """ 로그인할 IP-PBX 정보를 저장한다.

  Args:
      clsServerInfo (SipServerInfo): IP-PBX 정보 저장 객체

  Returns:
      성공하면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
  """
  if( len(clsServerInfo.strIp) == 0 ):
    return False
  if( len(clsServerInfo.strUserId) == 0 ):
    return False
  
  if( len(clsServerInfo.strDomain) == 0 ):
    clsServerInfo.strDomain = clsServerInfo.strIp
  
  bFound = False

  self.clsRegisterMutex.acquire()
  for clsInfo in self.clsRegisterList:
    if( clsInfo == clsServerInfo ):
      bFound = True
      break
  
  if( bFound == False ):
    self.clsRegisterList.append( clsServerInfo )
  self.clsRegisterMutex.release()

  return True
  