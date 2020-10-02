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

from .SdpAttribute import SdpAttribute
from .SdpAttributeCrypto import SdpAttributeCrypto
from .SdpBandWidth import SdpBandWidth
from .SdpConnection import SdpConnection
from .SdpMedia import SdpMedia
from .SdpOrigin import SdpOrigin
from .SdpTime import SdpTime

class SdpMessage():

  def __init__( self ):
    self.strVersion = ''
    self.strSessionName = ''
    self.strSessionInformation = ''
    self.strUri = ''
    self.strTimeZone = ''
    self.clsOrigin = SdpOrigin()
    self.clsConnection = SdpConnection()
    self.clsEmailList = []
    self.clsPhoneList = []
    self.clsBandWidthList = []
    self.clsTimeList = []
    self.clsAttributeList = []
    self.clsMediaList = []

  def Parse( self, strText ):
    self.Clear()

    iPos = 0
    iStartPos = 0
    iTextLen = len(strText)
    clsMedia = None

    while( iPos < iTextLen ):
      if( strText[iPos] == '\r' ):
        if( strText[iStartPos] == 'v' ):
          self.strVersion = strText[iStartPos+2:iPos]
        elif( strText[iStartPos] == 'o' ):
          if( self.clsOrigin.Parse( strText[iStartPos+2:iPos] ) == -1 ):
            return -1
        elif( strText[iStartPos] == 's' ):
          self.strSessionName = strText[iStartPos+2:iPos]
        elif( strText[iStartPos] == 'i' ):
          if( clsMedia == None ):
            self.strSessionInformation = strText[iStartPos+2:iPos]
        elif( strText[iStartPos] == 'u' ):
          self.strUri = strText[iStartPos+2:iPos]
        elif( strText[iStartPos] == 'e' ):
          self.clsEmailList.append( strText[iStartPos+2:iPos] )
        elif( strText[iStartPos] == 'p' ):
          self.clsPhoneList.append( strText[iStartPos+2:iPos] )
        elif( strText[iStartPos] == 'c' ):
          if( clsMedia != None ):
            if( clsMedia.clsConnection.Parse( strText[iStartPos+2:iPos] ) == -1 ):
              return -1
          else:
            if( self.clsConnection.Parse( strText[iStartPos+2:iPos] ) == -1 ):
              return -1
        elif( strText[iStartPos] == 'b' ):
          clsBandWidth = SdpBandWidth()
          if( clsBandWidth.Parse( strText[iStartPos+2:iPos] ) == -1 ):
            return -1
          
          if( clsMedia != None ):
            clsMedia.clsBandWidthList.append( clsBandWidth )
          else:
            self.clsBandWidthList.append( clsBandWidth )
        elif( strText[iStartPos] == 't' ):
          clsTime = SdpTime()
          if( clsTime.Parse( strText[iStartPos+2:iPos] ) == -1 ):
            return -1
          self.clsTimeList.append( clsTime )
        elif( strText[iStartPos] == 'r' ):
          iCount = len(self.clsTimeList)
          if( iCount > 0 ):
            self.clsTimeList[iCount-1].clsRepeatTimeList.append( strText[iStartPos+2:iPos] )
        elif( strText[iStartPos] == 'z' ):
          self.strTimeZone = strText[iStartPos+2:iPos]
        elif( strText[iStartPos] == 'a' ):
          clsAttribute = SdpAttribute()
          if( clsAttribute.Parse( strText[iStartPos+2:iPos] ) == -1 ):
            return -1
          
          if( clsMedia != None ):
            clsMedia.clsAttributeList.append( clsAttribute )
          else:
            self.clsAttributeList.append( clsAttribute )
        elif( strText[iStartPos] == 'm' ):
          clsMedia = SdpMedia()
          if( clsMedia.Parse( strText[iStartPos+2:iPos] ) == -1 ):
            return -1
          self.clsMediaList.append( clsMedia )

        iPos += 1
        iStartPos = iPos + 1
      iPos += 1
    
    return iPos
  
  def __str__( self ):
    strText = ''

    if( len(self.strVersion) > 0 ):
      strText += "v=" + self.strVersion + "\r\n"
    
    if( self.clsOrigin.Empty() == False ):
      strOrigin = str(self.clsOrigin)
      if( len(strOrigin) == 0 ):
        return ''
      strText += "o=" + strOrigin + "\r\n"
    
    if( len(self.strSessionName) > 0 ):
      strText += "s=" + self.strSessionName + "\r\n"
    
    if( len(self.strSessionInformation) > 0 ):
      strText += "i=" + self.strSessionInformation + "\r\n"
    
    if( len(self.strUri) > 0 ):
      strText += "u=" + self.strUri + "\r\n"
    
    for strEmail in self.clsEmailList:
      strText += "e=" + strEmail + "\r\n"
    
    for strPhone in self.clsPhoneList:
      strText += "p=" + strPhone + "\r\n"
    
    if( self.clsConnection.Empty() == False ):
      strConnection = str(self.clsConnection)
      if( len(strConnection) == 0 ):
        return ''
      strText += "c=" + strConnection + "\r\n"
    
    for clsBandWidth in self.clsBandWidthList:
      strBandWidth = str(clsBandWidth)
      if( len(strBandWidth) == 0 ):
        return ''
      strText += "b=" + strBandWidth + "\r\n"
    
    for clsTime in self.clsTimeList:
      strTime = str(clsTime)
      if( len(strTime) == 0 ):
        return ''
      strText += "t=" + strTime
    
    if( len(self.strTimeZone) > 0 ):
      strText += "z=" + self.strTimeZone + "\r\n"
    
    for clsAttribute in self.clsAttributeList:
      strAttribute = str(clsAttribute)
      if( len(strAttribute) == 0 ):
        return ''
      strText += "a=" + strAttribute + "\r\n"
    
    for clsMedia in self.clsMediaList:
      strMedia = str(clsMedia)
      if( len(strMedia) == 0 ):
        return ''
      strText += "m=" + strMedia
    
    return strText

  def Clear( self ):
    self.strVersion = ''
    self.strSessionName = ''
    self.strSessionInformation = ''
    self.strUri = ''
    self.strTimeZone = ''
    self.clsOrigin.Clear()
    self.clsConnection.Clear()
    self.clsEmailList.clear()
    self.clsPhoneList.clear()
    self.clsBandWidthList.clear()
    self.clsTimeList.clear()
    self.clsAttributeList.clear()
    self.clsMediaList.clear()
    
  def SelectMedia( self, strName ):
    for clsMedia in self.clsMediaList:
      if( clsMedia.strName == strName ):
        return clsMedia
    
    return None