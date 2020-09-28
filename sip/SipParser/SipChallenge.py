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

from .SipParameter import ParseSipParameter
from ..SipPlatform.StringUtility import DeQuoteString

class SipChallenge():

  def __init__( self ):
    self.strType = ''
    self.strRealm = ''
    self.strDomain = ''
    self.strNonce = ''
    self.strOpaque = ''
    self.strStale = ''
    self.strAlgorithm = ''
    self.strQop = ''
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
      if( strText[iCurPos] == ' ' or strText[iCurPos] == '\t' or strText[iCurPos] == ',' ):
        iCurPos += 1
        continue

      iPos = ParseSipParameter( clsParamList, strText, iCurPos )
      if( iPos == -1 ):
        return -1
      iCurPos = iPos

    for clsParam in clsParamList:
      if( clsParam.strName == "realm" ):
        self.strRealm = DeQuoteString( clsParam.strValue )
      elif( clsParam.strName == "domain" ):
        self.strDomain = DeQuoteString( clsParam.strValue )
      elif( clsParam.strName == "nonce" ):
        self.strNonce = DeQuoteString( clsParam.strValue )
      elif( clsParam.strName == "opaque" ):
        self.strOpaque = DeQuoteString( clsParam.strValue )
      elif( clsParam.strName == "stale" ):
        self.strStale = clsParam.strValue
      elif( clsParam.strName == "algorithm" ):
        self.strAlgorithm = clsParam.strValue
      elif( clsParam.strName == "qop" ):
        self.strQop = DeQuoteString( clsParam.strValue )
      else:
        self.clsParamList.append( clsParam )

  def __str__( self ):
    strText = ""
    strText = SetQuoteString( strText, "realm", self.strRealm )
    strText = SetQuoteString( strText, "domain", self.strDomain )
    strText = SetQuoteString( strText, "nonce", self.strNonce )
    strText = SetQuoteString( strText, "opaque", self.strOpaque )
    strText = SetString( strText, "stale", self.strStale )
    strText = SetString( strText, "algorithm", self.strAlgorithm )
    strText = SetString( strText, "qop", self.strQop )

    for clsParam in self.clsParamList:
      strText = SetString( strText, clsParam.strName, clsParam.strValue )
    
    return self.strType + " " + strText

  def Clear( self ):
    self.strType = ''
    self.strRealm = ''
    self.strDomain = ''
    self.strNonce = ''
    self.strOpaque = ''
    self.strStale = ''
    self.strAlgorithm = ''
    self.strQop = ''
    self.clsParamList.clear()
    
def SetString( strText, strName, strValue ):
  if( len(strValue) == 0 ):
    return strText
  
  if( len(strText) > 0 ):
    strText += ", "

  return strText + strName + "=" + strValue

def SetQuoteString( strText, strName, strValue ):
  if( len(strValue) == 0 ):
    return strText
  
  if( len(strText) > 0 ):
    strText += ", "
  
  return strText + strName + "=\"" + strValue + "\""
  
def ParseSipChallenge( clsList, strText ):
  clsChallenge = SipChallenge()

  iPos = clsChallenge.Parse( strText, 0 )
  if( iPos == -1 ):
    return -1
  
  clsList.append( clsChallenge )