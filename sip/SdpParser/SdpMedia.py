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

from .SdpConnection import SdpConnection

class SdpMedia():

  def __init__( self ):
    self.strMedia = ''
    self.iPort = -1
    self.iNumOfPort = -1
    self.strProtocol = ''
    self.clsFmtList = []
    self.strTitle = ''
    self.clsConnection = SdpConnection()
    self.clsBandWidthList = []
    self.clsAttributeList = []

  def Parse( self, strText ):
    self.Clear()

    iPos = 0
    iStartPos = 0
    iTextLen = len(strText)
    iType = 0
    if( iTextLen == 0 ):
      return -1
    
    while( iPos < iTextLen ):
      if( strText[iPos] == ' ' ):
        self.SetData( strText[iStartPos:iPos], iType )
        iType += 1
        iStartPos = iPos + 1

      iPos += 1
    
    if( iStartPos < iTextLen ):
      self.SetData( strText[iStartPos:], iType )
      iType += 1

    if( iType < 3 ):
      return -1

    return iTextLen
  
  def __str__( self ):
    strText = self.strMedia + " "

    if( self.iNumOfPort == -1 ):
      strText += str(self.iPort) + " "
    else:
      strText += str(self.iPort) + "/" + str(self.iNumOfPort) + " "
    
    strText += self.strProtocol

    for strFmt in self.clsFmtList:
      strText += " " + strFmt
    
    strText += "\r\n"

    if( len(self.strTitle) > 0 ):
      strText += "i=" + self.strTitle + "\r\n"
    
    if( self.clsConnection.Empty() == False ):
      strText += "c="
      strTemp = str(self.clsConnection)
      if( len(strTemp) == 0 ):
        return ''
      strText += strTemp + "\r\n"
    
    for clsBandWidth in self.clsBandWidthList:
      strText += "b="
      strTemp = str(clsBandWidth)
      if( len(strTemp) == 0 ):
        return ''
      strText += strTemp + "\r\n"
    
    for clsAttribute in self.clsAttributeList:
      strText += "b="
      strTemp = str(clsAttribute)
      if( len(strTemp) == 0 ):
        return ''
      strText += strTemp + "\r\n"
    
    return strText


  def Clear( self ):
    self.strMedia = ''
    self.iPort = -1
    self.iNumOfPort = -1
    self.strProtocol = ''
    self.clsFmtList.clear()
    self.strTitle = ''
    self.clsConnection.Clear()
    self.clsBandWidthList.clear()
    self.clsAttributeList.clear()
  
  def AddFmt( self, iPayLoadType ):
    if( self.SelectFmt( iPayLoadType ) ):
      return
    
    self.clsFmtList.append( str(iPayLoadType) )
  
  def SelectFmt( self, iPayLoadType ):
    strPayLoadType = str(iPayLoadType)

    for strFmt in self.clsFmtList:
      if( strFmt == strPayLoadType ):
        return True
    
    return False
  
  def DeleteAttribute( self, strName ):
    clsDeleteList = []
    bRes = False

    for clsAttribute in self.clsAttributeList:
      if( clsAttribute.strName == strName ):
        clsDeleteList.append( clsAttribute )
        bRes = True
    
    for clsAttribute in clsDeleteList:
      self.clsAttributeList.remove( clsAttribute )
    
    return bRes
  
  def DeleteFmtAttribute( self, iPayLoadType ):
    strPayLoadType = str(iPayLoadType)
    bRes = False

    for strFmt in self.clsFmtList:
      if( strPayLoadType == strFmt ):
        self.clsFmtList.remove( strFmt )
        bRes = True
        break
    
    if( bRes ):
      clsDeleteList = []

      for clsAttribute in self.clsAttributeList:
        if( clsAttribute.strName == "rtpmap" or clsAttribute.strName == "fmtp" ):
          strCodec = clsAttribute.strValue.split(' ')[0]
          if( strPayLoadType == strCodec ):
            clsDeleteList.append( clsAttribute )
      
      for clsAttribute in clsDeleteList:
        self.clsAttributeList.remove( clsAttribute )

    return bRes


