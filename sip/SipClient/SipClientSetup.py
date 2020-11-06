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
from ..SipPlatform.XmlUtility import XmlGetDataString, XmlGetDataInt, XmlGetDataBool, XmlGetAttrBool

class SipClientSetup():

  def __init__( self ):
    self.strLocalIp = ''
    self.iUdpPort = 5060
    self.strSipServerIp = ''
    self.strSipDomain = ''
    self.strSipUserId = ''
    self.strSipPassWord = ''
  
  def Read( self, strFileName ):
    try:
      clsTree = et.ElementTree( file=strFileName )
      clsRoot = clsTree.getroot()

      # SIP 설정
      clsSip = clsRoot.find("Sip")
      if( clsSip == None ):
        print( "Sip element is not found" )
        return False
      
      self.strLocalIp = XmlGetDataString( clsSip, "LocalIp", self.strLocalIp )
      self.iUdpPort = XmlGetDataInt( clsSip, "UdpPort", self.iUdpPort )
      self.strSipServerIp = XmlGetDataString( clsSip, "ServerIp", '' )
      self.strSipDomain = XmlGetDataString( clsSip, "Domain", '' )
      self.strSipUserId = XmlGetDataString( clsSip, "UserId", '' )
      self.strSipPassWord = XmlGetDataString( clsSip, "UserPassword", '' )

      if( len(self.strSipUserId) == 0 ):
        print( "Sip -> UserId element is not found" )
        return False

      if( len(self.strSipDomain) == 0 ):
        self.strSipDomain = self.strSipServerIp

      # 로그 설정
      clsLog = clsRoot.find("Log")
      if( clsLog == None ):
        print( "Log element is not found" )
        return False

      strLogFolder = XmlGetDataString( clsLog, "Folder", '' )
      if( len(strLogFolder) == 0 ):
        print( "Log -> Folder element is not found" )
        return False

      Log.SetDirectory( strLogFolder )

      iLogLevel = 0
      clsChild = clsLog.find( "Level" )
      if( clsChild != None ):
        if( XmlGetAttrBool( clsChild, "Debug", False ) ):
          iLogLevel |= LogLevel.DEBUG
        if( XmlGetAttrBool( clsChild, "Info", False ) ):
          iLogLevel |= LogLevel.INFO
        if( XmlGetAttrBool( clsChild, "Network", False ) ):
          iLogLevel |= LogLevel.NETWORK
    
      Log.SetLevel( iLogLevel )
      Log.iMaxLogSize = XmlGetDataInt( clsLog, "MaxSize", 20000000 )

    except Exception as other:
      Log.Print( LogLevel.ERROR, "SipServerSetup.Read(" + strFileName + ") error(" + str(other) + ")" )
      return False

    return True
