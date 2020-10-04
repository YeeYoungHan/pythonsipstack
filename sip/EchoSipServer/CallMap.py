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

class CallMap():

  def __init__( self ):
    self.clsMap = {}
    self.clsMutex = threading.Lock()
  
  def Insert( self, strCallId1, strCallId2 ):
    self.clsMutex.acquire()
    if( self.clsMap.get(strCallId1) == None and self.clsMap.get(strCallId2) == None ):
      self.clsMap[strCallId1] = strCallId2
      self.clsMap[strCallId2] = strCallId1
    self.clsMutex.release()

  def Select( self, strCallId ):
    strCallId2 = ''
    self.clsMutex.acquire()
    strValue = self.clsMap.get(strCallId)
    if( strValue != None ):
      strCallId2 = strValue
    self.clsMutex.release()

    return strCallId2
  
  def Delete( self, strCallId ):
    self.clsMutex.acquire()
    strValue = self.clsMap.get(strCallId)
    if( strValue != None ):
      del self.clsMap[strCallId]
      if( self.clsMap.get(strValue) != None ):
        del self.clsMap[strValue]
    self.clsMutex.release()
    