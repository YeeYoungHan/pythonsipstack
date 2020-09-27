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

class SipTransactionList():

  def __init__( self ):
    self.MAX_ICT_RESEND_COUNT = 11
    self.arrICTReSendTime = [ 500
      , 1500
      , 3500
      , 7500
      , 11500
      , 15500
      , 19500
      , 23500
      , 27500
      , 31500
      , 32000]
  
  def GetKey( self, clsMessage ):
    iCount = len(clsMessage.clsViaList)
    if( iCount == 0 ):
      return ""
    
    strKey = ""
    strBranch = clsMessage.clsViaList[0].SelectParam( "branch" )
    if( len(strBranch) > 0 ):
      if( strBranch[:7] == "z9hG4bK" ):
        strKey = strBranch[7:] + " " + str(clsMessage.clsCSeq.iDigit)

        if( clsMessage.clsCSeq.strMethod == "ACK" ):
          strKey += "INVITE"
        else:
          strKey += clsMessage.clsCSeq.strMethod
    
    if( len(strKey) == 0 ):
      strKey = str(clsMessage.clsCallId)
    
    return strKey
  
  def GetKey( self, clsMessage, strMethod ):
    iCount = len(clsMessage.clsViaList)
    if( iCount == 0 ):
      return ""
    
    strKey = ""
    strBranch = clsMessage.clsViaList[0].SelectParam( "branch" )
    if( len(strBranch) > 0 ):
      if( strBranch[:7] == "z9hG4bK" ):
        strKey = strBranch[7:] + " " + str(clsMessage.clsCSeq.iDigit) + strMethod
    
    if( len(strKey) == 0 ):
      strKey = str(clsMessage.clsCallId)
    
    return strKey