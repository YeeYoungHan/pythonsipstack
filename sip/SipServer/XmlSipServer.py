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

import xml.etree.ElementTree as et
from ..SipPlatform.Log import Log, LogLevel
from ..SipPlatform.XmlUtility import XmlGetDataString, XmlGetDataInt, XmlGetDataBool, XmlGetAttrString, XmlGetAttrBool
from ..SipUserAgent.SipServerInfo import SipServerInfo

class XmlSipServerFlag():
  INSERT = 0x01
  UPDATE = 0x02
  DELETE = 0x04
  NO_CHANGE = 0x10

class RoutePrefix():

  def __init__( self ):
    self.strPrefix = ''
    self.bDeletePrefix = False

class IncomingRoute():

  def __init__( self ):
    self.strToId = ''
    self.strDestId = ''
  
  def IsEmpty( self ):
    if( len(self.strToId) == 0 or len(self.strDestId) == 0 ):
      return True
    
    return False

class XmlSipServer(SipServerInfo):

  def __init__( self ):
    super().__init__()
    self.strName = ''
    self.iFlag = 0
    self.clsRoutePrefixList = []
    self.clsIncomingRouteList = []
  
  def Parse( self, strFileName ):
    self.Clear()

    try:
      clsTree = et.ElementTree( file=strFileName )
      clsRoot = clsTree.getroot()

      if( XmlGetDataBool( clsRoot, "Use", False ) == False ):
        return False
      
      self.strIp = XmlGetDataString( clsRoot, "Ip", "" )
      self.iPort = XmlGetDataInt( clsRoot, "Port", 5060 )
      self.strDomain = XmlGetDataString( clsRoot, "Domain", "" )
      self.strUserId = XmlGetDataString( clsRoot, "UserId", "" )
      self.strPassWord = XmlGetDataString( clsRoot, "PassWord", "" )
      self.iLoginTimeout = XmlGetDataInt( clsRoot, "LoginTimeout", 3600 )

      clsRPL = clsRoot.find( "RoutePrefixList" )
      if( clsRPL != None ):
        for clsChild in clsRPL:
          if( clsChild.tag == "RoutePrefix" ):
            clsRoutePrefix = RoutePrefix()
            clsRoutePrefix.strPrefix = clsChild.text
            clsRoutePrefix.bDeletePrefix = XmlGetAttrBool( clsChild, "DeletePrefix", False )
            self.clsRoutePrefixList.append( clsRoutePrefix )
      
      clsIRL = clsRoot.find( "IncomingRouteList" )
      if( clsIRL != None ):
        for clsChild in clsIRL:
          if( clsChild.tag == "IncomingRoute" ):
            clsIncomingRoute = IncomingRoute()
            clsIncomingRoute.strToId = XmlGetAttrString( clsChild, "ToId", "" )
            clsIncomingRoute.strDestId = XmlGetAttrString( clsChild, "DestId", "" )
            if( clsIncomingRoute.IsEmpty() == False ):
              self.clsIncomingRouteList.append( clsIncomingRoute )
    except Exception as other:
      Log.Print( LogLevel.ERROR, "XmlSipServer.Parse(" + strFileName + ") error(" + str(other) + ")" )
      return False

    if( len(self.strIp) == 0 ):
      return False
    
    if( len(self.strDomain) == 0 ):
      self.strDomain = self.strIp

    if( self.iPort <= 0 ):
      self.iPort = 5060
    
    return True

  def Clear( self ):
    self.strIp = ''
    self.iPort = 5060
    self.strDomain = ''
    self.strUserId = ''
    self.strPassWord = ''
    self.clsRoutePrefixList.clear()
    self.clsIncomingRouteList.clear()
