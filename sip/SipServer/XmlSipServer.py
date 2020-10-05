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
from ..SipPlatform.XmlUtility import XmlGetDataString, XmlGetDataInt, XmlGetDataBool
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
    self.strName = ''
    self.iFlag = 0
    self.clsRoutePrefixList = []
    self.clsIncomingRouteList = []
  
  def Parse( self, strFileName ):
    self.Clear()

    clsTree = et.ElementTree( file=strFileName )
    clsRoot = clsTree.getroot()

    if( XmlGetDataBool( clsRoot, "Use", False ) == False ):
      return False
    
    self.strIp = XmlGetDataString( clsRoot, "Ip", "" )

  