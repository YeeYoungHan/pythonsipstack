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

class SipServerSetup():

  def __init__( self ):
    self.strLocalIp = ''
    self.iUdpPort = 5060
    self.iUdpThreadCount = 10
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
    clsTree = et.ElementTree( file=strFileName )
    clsRoot = clsTree.getroot()

    clsSip = clsRoot.find("Sip")
    if( clsSip == None ):
      print( "Sip element is not found" )
      return False
    
    self.strLocalIp = GetDataString( clsSip, "LocalIp", self.strLocalIp )
    self.iUdpPort = GetDataInt( clsSip, "UdpPort", self.iUdpPort )
    self.iUdpThreadCount = GetDataInt( clsSip, "UdpThreadCount", self.iUdpThreadCount )
    self.strRealm = GetDataString( clsSip, "Realm", self.strRealm )
    self.iMinRegisterTimeout = GetDataInt( clsSip, "MinRegisterTimeout", self.iMinRegisterTimeout )
    self.strCallPickupId = GetDataString( clsSip, "CallPickupId", self.strCallPickupId )
    self.iStackExecutePeriod = GetDataInt( clsSip, "StackExecutePeriod", self.iStackExecutePeriod )
    self.iTimerD = GetDataInt( clsSip, "TimerD", self.iTimerD )
    self.iTimerJ = GetDataInt( clsSip, "TimerJ", self.iTimerJ )
    self.bIpv6 = GetDataBool( clsSip, "Ipv6", self.bIpv6 )

    clsLog = clsRoot.find("Log")
    if( clsLog == None ):
      print( "Log element is not found" )
      return False

    strLogFolder = GetDataString( clsLog, "Folder", '' )
    if( len(strLogFolder) == 0 ):
      print( "Log -> Folder element is not found" )
      return False

    Log.SetDirectory( strLogFolder )

    iLogLevel = 0
    clsChild = clsLog.find( "Level" )
    if( clsChild != None ):
      if( GetAttrString( clsChild, "Debug" ) == "true" ):
        iLogLevel |= LogLevel.DEBUG
      if( GetAttrString( clsChild, "Info" ) == "true" ):
        iLogLevel |= LogLevel.INFO
      if( GetAttrString( clsChild, "Network" ) == "true" ):
        iLogLevel |= LogLevel.NETWORK
    
    Log.SetLevel( iLogLevel )
    Log.iMaxLogSize = GetDataInt( clsLog, "MaxSize", 20000000 )

    return True

  def IsCallPickupId( self, strId ):
    if( len(self.strCallPickupId) == 0 ):
      return False

    if( self.strCallPickupId == strId ):
      return True
    
    return False

def GetDataString( clsParent, strName, strValue ):
  clsChild = clsParent.find( strName )
  if( clsChild != None ):
    return clsChild.text
  
  return strValue

def GetDataInt( clsParent, strName, iValue ):
  clsChild = clsParent.find( strName )
  if( clsChild != None ):
    return int(clsChild.text)
  
  return iValue

def GetDataBool( clsParent, strName, iValue ):
  clsChild = clsParent.find( strName )
  if( clsChild != None and clsChild.text.lower() == "true" ):
    return True
  
  return False

def GetAttrString( clsNode, strName ):
  strAttr = clsNode.attrib.get( strName )
  if( strAttr != None ):
    return strAttr
  
  return ''