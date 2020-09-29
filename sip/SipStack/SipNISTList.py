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

class SipNISTList(SipTransactionList):

  def __init__( self, clsSipStack ):
    self.clsMutex = threading.Lock()
    self.clsMap = {}
    self.clsSipStack = clsSipStack
    self.iTimerJ = 32.0

  def Insert( self, clsMessage ):
    bRes = False
    strKey = super().GetKey( clsMessage )

    if( clsMessage.IsRequest() ):
      self.clsMutex.acquire()
      clsTransaction = self.clsMap.get( strKey )
      if( clsTransaction == None ):
        clsTransaction = SipNonInviteTransaction()
        clsTransaction.clsRequest = clsMessage
        clsTransaction.iStartTime = time.time()
        self.clsMap[strKey] = clsTransaction
        bRes = True
      else:
        if( clsTransaction.clsResponse != None ):
          self.clsSipStack.Send( clsTransaction.clsResponse, False )
      self.clsMutex.release()

    else:
      clsMessage.MakePacket()

      self.clsMutex.acquire()
      clsTransaction = self.clsMap.get( strKey )
      if( clsTransaction != None ):
        if( clsTransaction.clsResponse == None or clsTransaction.clsResponse.iStatusCode != clsMessage.iStatusCode ):
          clsTransaction.clsResponse = clsMessage
          bRes = True
          if( clsMessage.iStatusCode >= 200 ):
            clsTransaction.iStopTime = time.time()
      self.clsMutex.release()
    
    return bRes
  
  def Execute( self, iTime ):
    clsDeleteList = []

    self.clsMutex.acquire()
    for strKey in self.clsMap:
      clsTransaction = self.clsMap[strKey]
      if( clsTransaction.iStopTime > 0 ):
        if( iTime - clsTransaction.iStopTime >= self.iTimerJ ):
          clsDeleteList.append( strKey )
    
    for strKey in clsDeleteList:
      del self.clsMap[strKey]
    self.clsMutex.release()

  
  def DeleteAll( self ):
    self.clsMutex.acquire()
    self.clsMap.clear()
    self.clsMutex.release()
