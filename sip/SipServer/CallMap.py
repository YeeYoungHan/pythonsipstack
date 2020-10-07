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

class CallInfo():

  def __init__( self ):
    # 상대 SIP 클라이언트와 연결된 통화 SIP Call-ID
    self.strPeerCallId = ''
    # 최초 INVITE 를 수신하였는가?
    self.bRecv = False

class CallMap():

  def __init__( self, clsUserAgent ):
    self.clsMutex = threading.Lock()
    self.clsMap = {}
    self.clsUserAgent = clsUserAgent
  
  def Insert( self, strRecvCallId, strSendCallId ):
    self.clsMutex.acquire()
    # INVITE 메시지를 수신한 Dialog 를 저장한다.
    if( self.clsMap.get( strRecvCallId ) == None ):
      clsCallInfo = CallInfo()

      clsCallInfo.strPeerCallId = strSendCallId
      clsCallInfo.bRecv = True

      self.clsMap[strRecvCallId] = clsCallInfo
    # INVITE 메시지를 전송한 Dialog 를 저장한다.
    if( self.clsMap.get( strSendCallId ) == None ):
      clsCallInfo = CallInfo()

      clsCallInfo.strPeerCallId = strRecvCallId
      clsCallInfo.bRecv = False

      self.clsMap[strSendCallId] = clsCallInfo
    self.clsMutex.release()
  
  def InsertCallInfo( self, strCallId, clsCallInfo ):
    bRes = False

    self.clsMutex.acquire()
    if( self.clsMap.get( strCallId ) == None ):
      self.clsMap[strCallId] = clsCallInfo
      bRes = True
    self.clsMutex.release()

    return bRes
  
  def Update( self, strCallId, strPeerCallId ):
    self.clsMutex.acquire()
    clsCallInfo = self.clsMap.get( strCallId )
    if( clsCallInfo != None ):
      clsCallInfo.strPeerCallId = strPeerCallId
    self.clsMutex.release()
  
  def SelectCallId( self, strCallId ):
    strPeerCallId = ''

    self.clsMutex.acquire()
    clsCallInfo = self.clsMap.get( strCallId )
    if( clsCallInfo != None ):
      strPeerCallId = clsCallInfo.strPeerCallId
    self.clsMutex.release()

    return strPeerCallId
  
  def SelectCallInfo( self, strCallId ):
    self.clsMutex.acquire()
    clsCallInfo = self.clsMap.get( strCallId )
    self.clsMutex.release()

    return clsCallInfo
  
  def Select( self, strCallId ):
    bRes = False

    self.clsMutex.acquire()
    if( self.clsMap.get( strCallId ) != None ):
      bRes = True
    self.clsMutex.release()

    return bRes
  
  def SelectToRing( self, strTo ):
    strReturnCallId = ''

    self.clsMutex.acquire()
    for strCallId in self.clsMap:
      clsCallInfo = self.clsMap[strCallId]
      if( clsCallInfo.bRecv ):
        continue
      if( self.clsUserAgent.IsRingCall( strCallId, strTo ) == False ):
        continue
      strReturnCallId = strCallId
      break
    self.clsMutex.release()

    return strReturnCallId
  
  def Delete( self, strCallId ):
    self.clsMutex.acquire()
    clsCallInfo = self.clsMap.get( strCallId )
    if( clsCallInfo != None ):
      del self.clsMap[strCallId]
    
      if( self.clsMap.get( clsCallInfo.strPeerCallId ) != None ):
        del self.clsMap[clsCallInfo.strPeerCallId]
    self.clsMutex.release()
  
  def DeleteOne( self, strCallId ):
    self.clsMutex.acquire()
    clsCallInfo = self.clsMap.get( strCallId )
    if( clsCallInfo != None ):
      del self.clsMap[strCallId]
    self.clsMutex.release()
  
  def StopCallAll( self ):
    self.clsMutex.acquire()
    for strCallId in self.clsMap:
      self.clsUserAgent.StopCall( strCallId, 0 )
    self.clsMutex.release()
  
  