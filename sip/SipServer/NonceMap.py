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

import time
import threading
from ..SipPlatform.SipMd5 import SipMd5String

class NonceMap():

  def __init__( self ):
    self.clsMutex = threading.Lock()
    self.clsMap = {}
  
  def GetNewValue( self ):
    iTime = time.time()
    bInsert = False
    i = 0

    while bInsert == False:
      strNonce = SipMd5String( str(i) + "::" + str(iTime) + "::pythonsipserver" )

      self.clsMutex.acquire()
      if( self.clsMap.get( strNonce ) == None ):
        self.clsMap[strNonce] = time.time()
        bInsert = True
      self.clsMutex.release()

      i += 1
    
    return strNonce
  
  def Select( self, strNonce, bRemove ):
    bRes = False

    self.clsMutex.acquire()
    if( self.clsMap.get( strNonce ) != None ):
      bRes = True
      if( bRemove ):
        del self.clsMap[strNonce]
    self.clsMutex.release()

    return bRes
  
  def DeleteTimeout( self, iSecond ):
    iTime = time.time()
    clsDeleteList = []

    self.clsMutex.acquire()
    for strNonce in self.clsMap:
      if( iTime > ( self.clsMap[strNonce] + iSecond ) ):
        clsDeleteList.append( strNonce )
    
    for strNonce in clsDeleteList:
      del self.clsMap[strNonce]
    self.clsMutex.release()
