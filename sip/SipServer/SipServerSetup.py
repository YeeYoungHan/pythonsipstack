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

class SipServerSetup():

  def __init__( self ):
    self.strLocalIp = ''
    self.iUdpPort = 5060
    self.strCallPickupId = ''
    self.iStackExecutePeriod = 0.02
    self.iTimerD = 32.0
    self.iTimerJ = 32.0
    self.bIpv6 = False
    self.strRealm = 'SipServer'
    self.iMinRegisterTimeout = 300
    self.strUserXmlFolder = ''
    self.strSipServerXmlFolder = ''
  
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
      self.strRealm = XmlGetDataString( clsSip, "Realm", self.strRealm )
      self.iMinRegisterTimeout = XmlGetDataInt( clsSip, "MinRegisterTimeout", self.iMinRegisterTimeout )
      self.strCallPickupId = XmlGetDataString( clsSip, "CallPickupId", self.strCallPickupId )
      self.iStackExecutePeriod = XmlGetDataInt( clsSip, "StackExecutePeriod", self.iStackExecutePeriod )
      self.iTimerD = XmlGetDataInt( clsSip, "TimerD", self.iTimerD )
      self.iTimerJ = XmlGetDataInt( clsSip, "TimerJ", self.iTimerJ )
      self.bIpv6 = XmlGetDataBool( clsSip, "Ipv6", self.bIpv6 )

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

      # XML 폴더 설정
      clsXmlFolder = clsRoot.find("XmlFolder")
      if( clsXmlFolder == None ):
        print( "XmlFolder element is not found" )
        return False
      
      self.strUserXmlFolder = XmlGetDataString( clsXmlFolder, "User", self.strUserXmlFolder )
      self.strSipServerXmlFolder = XmlGetDataString( clsXmlFolder, "SipServer", self.strSipServerXmlFolder )

    except Exception as other:
      Log.Print( LogLevel.ERROR, "SipServerSetup.Read(" + strFileName + ") error(" + str(other) + ")" )
      return False

    return True

  def IsCallPickupId( self, strId ):
    if( len(self.strCallPickupId) == 0 ):
      return False

    if( self.strCallPickupId == strId ):
      return True
    
    return False

