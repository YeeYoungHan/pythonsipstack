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
import time
from ..SipParser.SipMessage import SipMessage
from ..SipParser.SipStatusCode import SipStatusCode
from ..SipParser.SipTransport import SipTransport
from .SipNonInviteTransaction import SipNonInviteTransaction
from .SipTransactionList import SipTransactionList

class SipNICTList(SipTransactionList):
  """ Non Invite Client Transaction 리스트 저장 클래스

  Args:
      SipTransactionList (SipTransactionList): SipTransactionList
  """

  def __init__( self, clsSipStack ):
    self.clsMutex = threading.Lock()
    self.clsMap = {}
    self.clsSipStack = clsSipStack

  def Insert( self, clsMessage ):
    """ Non Invite Client Transaction 리스트에 SIP 메시지를 저장한다.

    Args:
        clsMessage (SipMessage): SIP 메시지 객체

    Returns:
        bool: SIP 메시지 저장에 성공하면 True 를 리턴하고 그렇지 않으면 False 를 리턴한다.
    """
    bRes = False
    strKey = super().GetKey( clsMessage )

    if( clsMessage.IsRequest() ):
      clsMessage.MakePacket()

      self.clsMutex.acquire()
      clsTransaction = self.clsMap.get( strKey )
      if( clsTransaction == None ):
        clsTransaction = SipNonInviteTransaction()
        clsTransaction.clsRequest = clsMessage
        clsTransaction.iStartTime = time.time()
        self.clsMap[strKey] = clsTransaction
        bRes = True
      self.clsMutex.release()

    else:

      self.clsMutex.acquire()
      clsTransaction = self.clsMap.get( strKey )
      if( clsTransaction != None ):
        if( clsTransaction.clsResponse != None ):
          if( clsTransaction.clsResponse.iStatusCode != clsMessage.iStatusCode ):
            clsTransaction.clsResponse = clsMessage
            bRes = True
        else:
          clsTransaction.clsResponse = clsMessage
          bRes = True
        
        if( bRes and clsMessage.iStatusCode >= 200 ):
          clsTransaction.iStopTime = time.time()
      self.clsMutex.release()
    
    return bRes
  
  def Execute( self, iTime ):
    """ Non Invite Client Transaction 리스트에서 재전송할 SIP 메시지가 존재하면 재전송하고 만료된 Transaction 은 삭제한다.

    Args:
        iTime (int): 현재 시간
    """
    clsDeleteList = []
    clsResponseList = []

    self.clsMutex.acquire()
    for strKey in self.clsMap:
      clsTransaction = self.clsMap[strKey]
      if( clsTransaction.iStopTime > 0 ):
        if( iTime - clsTransaction.iStopTime >= 5.0 ):
          clsDeleteList.append( strKey )
      else:
        if( (iTime - clsTransaction.iStartTime) >= super().arrICTReSendTime[clsTransaction.iReSendCount] ):
          clsTransaction.iReSendCount += 1
          if( clsTransaction.iReSendCount == super().MAX_ICT_RESEND_COUNT ):
            if( clsTransaction.clsResponse == None ):
              clsResponse = clsTransaction.clsRequest.CreateResponse( SipStatusCode.SIP_REQUEST_TIME_OUT, '' )
              if( len(clsTransaction.clsRequest.clsRouteList) > 0 ):
                clsResponse.strClientIp = clsTransaction.clsRequest.clsRouteList[0].clsUri.strHost
              clsResponseList.append( clsResponse )
              clsDeleteList.append( strKey )
          else:
            if( clsTransaction.clsRequest.eTransport == SipTransport.UDP ):
              self.clsSipStack.Send( clsTransaction.clsRequest, False )
    
    for strKey in clsDeleteList:
      del self.clsMap[strKey]
    self.clsMutex.release()

    for clsResponse in clsResponseList:
      self.clsSipStack.RecvResponse( clsResponse )
  
  def DeleteCancel( self, clsMessage ):
    """ 입력된 SIP 메시자와 관련된 CANCEL 메시지를 삭제한다.

    Args:
        clsMessage (SipMessage): SIP 메시지 객체
    """
    if( clsMessage.IsRequest() ):
      return
    
    strKey = super().GetKeyMethod( clsMessage, "CANCEL" )

    self.clsMutex.acquire()
    clsTransaction = self.clsMap.get( strKey )
    if( clsTransaction != None ):
      del self.clsMap[strKey]
    self.clsMutex.release()

  def DeleteAll( self ):
    """ Non Invite Client Transaction 리스트를 초기화시킨다.
    """
    self.clsMutex.acquire()
    self.clsMap.clear()
    self.clsMutex.release()
