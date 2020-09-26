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

from .SipChallenge import SetString
from .SipChallenge import SetQuoteString
from .SipParameter import ParseSipParameter
from ..SipPlatform.StringUtility import DeQuoteString

class SipCredential():

  def __init__( self ):
    self.strType = ''
    self.strUserName = ''
    self.strRealm = ''
    self.strNonce = ''
    self.strUri = ''
    self.strResponse = ''
    self.strAlgorithm = ''
    self.strCnonce = ''
    self.strOpaque = ''
    self.strQop = ''
    self.strNonceCount = ''
    self.clsParamList = []
  
  def Parse( self, strText, iStartPos ):
    self.Clear()

    iPos = iStartPos
    iTextLen = len(strText)

    while( iPos < iTextLen ):
      if( strText[iPos] == ' ' or strText[iPos] == '\t' ):
        self.strType = strText[iStartPos:iPos]
        iPos += 1
        break
      iPos += 1

    if( len(self.strType) == 0 ):
      return -1

    iCurPos = iPos
    clsParamList = []

    while( iCurPos < iTextLen ):
      if( strText[iPos] == ' ' or strText[iPos] == '\t' or strText[iPos] == ',' ):
        iCurPos += 1
        continue

      iPos = ParseSipParameter( clsParamList, strText, iCurPos )
      if( iPos == -1 ):
        return -1
      iCurPos = iPos

    iCount = len(self.clsParamList)

    for i in range( 0, iCount ):
      if( clsParamList[i].strName == "username" ):
        self.strUserName = DeQuoteString( clsParamList[i].strValue )
      elif( clsParamList[i].strName == "realm" ):
        self.strRealm = DeQuoteString( clsParamList[i].strValue )
      elif( clsParamList[i].strName == "nonce" ):
        self.strNonce = DeQuoteString( clsParamList[i].strValue )
      elif( clsParamList[i].strName == "uri" ):
        self.strUri = DeQuoteString( clsParamList[i].strValue )
      elif( clsParamList[i].strName == "response" ):
        self.strResponse = DeQuoteString( clsParamList[i].strValue )
      elif( clsParamList[i].strName == "algorithm" ):
        self.strAlgorithm = clsParamList[i].strValue
      elif( clsParamList[i].strName == "cnonce" ):
        self.strCnonce = DeQuoteString( clsParamList[i].strValue )
      elif( clsParamList[i].strName == "opaque" ):
        self.strOpaque = DeQuoteString( clsParamList[i].strValue )
      elif( clsParamList[i].strName == "qop" ):
        self.strOop = clsParamList[i].strValue
      elif( clsParamList[i].strName == "nc" ):
        self.strNonceCount = clsParamList[i].strValue
      else:
        self.clsParamList.append( clsParamList[i] )

  def __str__( self ):
    strText = self.strType
    strText += SetQuoteString( "username", self.strUserName )
    strText += SetQuoteString( "realm", self.strRealm )
    strText += SetQuoteString( "nonce", self.strNonce )
    strText += SetQuoteString( "uri", self.strUri )
    strText += SetQuoteString( "response", self.strResponse )
    strText += SetString( "algorithm", self.strAlgorithm )
    strText += SetQuoteString( "cnonce", self.strCnonce )
    strText += SetQuoteString( "opaque", self.strOpaque )
    strText += SetString( "qop", self.strQop )
    strText += SetString( "nc", self.strNonceCount )

    iCount = len(self.clsParamList)
    for i in range( 0, iCount ):
      strText += SetString( clsParamList[i].strName, clsParamList[i].strValue )
    
    return strText

  def Clear( self ):
    self.strType = ''
    self.strUserName = ''
    self.strRealm = ''
    self.strNonce = ''
    self.strUri = ''
    self.strResponse = ''
    self.strAlgorithm = ''
    self.strCnonce = ''
    self.strOpaque = ''
    self.strQop = ''
    self.strNonceCount = ''
    self.clsParamList.clear()