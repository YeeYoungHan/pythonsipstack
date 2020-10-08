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

import os
import xml.etree.ElementTree as et
from ..SipPlatform.Log import Log, LogLevel
from ..SipPlatform.XmlUtility import XmlGetDataString, XmlGetDataBool

class XmlUser():

  def __init__( self ):
    # SIP 사용자 아이디
    self.strId = ''

    # SIP 비밀번호
    self.strPassWord = ''

    # 착신거부 ( Do Not Disturb )
    self.bDnd = False

    # 착신전환 ( Call Forward )
    self.strCallForward = ''

    # 그룹 아이디
    self.strGroupId = ''
  
  def Parse( self, strFileName ):
    self.Clear()

    # 파일이 존재하지 않으면 사용자가 존재하지 않다고 리턴한다.
    if( os.path.isfile( strFileName ) == False ):
      return False

    try:
      clsTree = et.ElementTree( file=strFileName )
      clsRoot = clsTree.getroot()

      self.strId = XmlGetDataString( clsRoot, "Id", "" )
      self.strPassWord = XmlGetDataString( clsRoot, "PassWord", "" )
      self.bDnd = XmlGetDataBool( clsRoot, "DND", False )
      self.strCallForward = XmlGetDataString( clsRoot, "CallForward", "" )
      self.strGroupId = XmlGetDataString( clsRoot, "GroupId", "" )
    except Exception as other:
      Log.Print( LogLevel.ERROR, "XmlUser.Parse(" + strFileName + ") error(" + str(other) + ")" )
      return False

    if( len(self.strId) == 0 ):
      return False
    
    return True
  
  def Clear( self ):
    self.strId = ''
    self.strPassWord = ''
    self.bDnd = False
    self.strCallForward = ''
    self.strGroupId = ''

def SelectUser( strUserId, strXmlFolder ):
  clsUser = XmlUser()

  strFileName = strXmlFolder + "/" + strUserId + ".xml"
  if( clsUser.Parse( strFileName ) ):
    return clsUser
  
  return None
