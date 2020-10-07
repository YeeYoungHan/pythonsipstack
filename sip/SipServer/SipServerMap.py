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

from ..SipPlatform.Directory import GetFilePathList
from .XmlSipServer import XmlSipServerFlag, XmlSipServer

class SipServerMap():

  def __init__( self ):
    self.clsMutex = threading.Lock()
    self.clsMap = {}
  
  def Load( self, strXmlFolder ):
    self.clsMutex.acquire()
    for strKey in self.clsMap:
      self.clsMap[strKey].iFlag = XmlSipServerFlag.DELETE
    self.clsMutex.release()

    clsFilePathList = GetFilePathList( strXmlFolder )
    for strPath in clsFilePathList:
      clsXml = XmlSipServer()

      if( clsXml.Parse( strPath ) ):
        clsXml.strName = strPath
        self.Insert( clsXml )
  
  def SetSipUserAgentRegisterInfo( self, clsSipUserAgent ):
    clsDeleteList = []

    self.clsMutex.acquire()
    for strKey in self.clsMap:
      clsSipServer = self.clsMap[strKey]
      if( clsSipServer.iFlag == XmlSipServerFlag.INSERT ):
        clsSipUserAgent.InsertRegisterInfo( clsSipServer )
      elif( clsSipServer.iFlag == XmlSipServerFlag.INSERT ):
        clsSipUserAgent.UpdateRegisterInfo( clsSipServer )
      elif( clsSipServer.iFlag == XmlSipServerFlag.INSERT ):
        clsSipUserAgent.DeleteRegisterInfo( clsSipServer )
        clsDeleteList.append( strKey )
    
    for strKey in clsDeleteList:
      del self.clsMap[strKey]
    self.clsMutex.release()

  
  def Insert( self, clsXml ):
    strKey = self.GetKey( clsXml )

    self.clsMutex.acquire()
    clsSipServer = self.clsMap.get( strKey )
    if( clsSipServer == None ):
      clsXml.iFlag = XmlSipServerFlag.INSERT
      self.clsMap[strKey] = clsXml
    else:
      if( clsSipServer.strDomain != clsXml.strDomain or clsSipServer.strPassWord != clsXml.strPassWord or clsSipServer.iPort != clsXml.iPort ):
        clsXml.iFlag = XmlSipServerFlag.UPDATE
      else:
        clsXml.iFlag = XmlSipServerFlag.NO_CHANGE

      clsSipServer = clsXml
    self.clsMutex.release()

  def Select( self, strIp, strUserId ):
    bRes = False
    strKey = self.GetKeyIpUserId( strIp, strUserId )

    self.clsMutex.acquire()
    if( self.clsMap.get( strKey ) != None ):
      bRes = True
    self.clsMutex.release()

    return bRes
  
  def SelectRoutePrefix( self, strTo ):
    iToLen = len(strTo)
    bRes = False
    clsResSipServer = None
    strResTo = ''

    self.clsMutex.acquire()
    for strKey in self.clsMap:
      clsSipServer = self.clsMap[strKey]
      for clsRoutePrefix in clsSipServer.clsRoutePrefixList:
        iLen = clsRoutePrefix.strPrefix
        if( iToLen >= iLen ):
          strPrefix = strTo[:iLen]
          if( strPrefix == clsRoutePrefix.strPrefix ):
            clsResSipServer = clsSipServer

            if( clsRoutePrefix.bDeletePrefix ):
              strResTo = strTo[iLen:]
            else:
              strResTo = strTo

            bRes = True
            break
      if( bRes ):
        break
    self.clsMutex.release()

    return bRes, clsResSipServer, strResTo
  
  def SelectIncomingRoute( self, strIp, strTo ):
    bRes = False
    iIpLen = len(strIp)
    strResTo = ''

    self.clsMutex.acquire()
    for strKey in self.clsMap:
      clsSipServer = self.clsMap[strKey]
      
      if( iIpLen > 0 and clsSipServer.strIp != strIp ):
        continue

      for clsIncomingRoute in clsSipServer.clsIncomingRouteList:
        if( clsIncomingRoute.strToId == strTo ):
          bRes = True
          strResTo = clsIncomingRoute.strDestId
          break

      if( bRes ):
        break
    self.clsMutex.release()

    return bRes, strResTo
  
  def Set( self, clsServerInfo, iStatus ):
    strKey = GetKey( clsServerInfo )

    self.clsMutex.acquire()
    clsSipServer = self.clsMap.get( strKey )
    if( clsSipServer != None ):
      clsSipServer.bLogin = clsServerInfo.bLogin
    self.clsMutex.release()

  
  def GetKey( self, clsXml ):
    return clsXml.strIp + "_" + clsXml.strUserId
  
  def GetKeyIpUserId( self, strIp, strUserId ):
    return strIp + "_" + strUserId