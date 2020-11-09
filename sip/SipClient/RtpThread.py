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

import audioop
import pyaudio
import select
import socket
import struct
import time
import threading
from ..SipPlatform.Log import Log, LogLevel

class RtpThread():

  def __init__( self ):
    self.hUdpSocket = None
    self.iUdpPort = 10000
    self.strDestIp = ''
    self.iDestPort = 0
    self.bStopEvent = False
    self.clsAudio = None
    self.clsStream = None
    self.bSendThreadRun = False
    self.bRecvThreadRun = False
    self.bUseTwoAudio = False
  
  def Start( self ):
    self.hUdpSocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    bBind = False
    
    while bBind == False:
      try:
        self.hUdpSocket.bind( ('0.0.0.0', self.iUdpPort) )
        bBind = True
      except:
        self.iUdpPort += 2
    
  def SetDestIpPort( self, strDestIp, iDestPort ):
    self.strDestIp = strDestIp
    self.iDestPort = iDestPort

    if( self.bSendThreadRun or self.bRecvThreadRun ):
      return

    if( self.bUseTwoAudio == False ):
      self.clsAudio = pyaudio.PyAudio()
      self.clsStream = self.clsAudio.open( format = 8, channels = 1, rate = 8000, input = True, output = True, frames_per_buffer = 160 )

    p = threading.Thread( target=RtpSendThread, args=(self,))
    p.daemon = True
    p.start()
    
    p = threading.Thread( target=RtpRecvThread, args=(self,))
    p.daemon = True
    p.start()
  
  def Stop( self ):
    self.bStopEvent = True

    while( self.bSendThreadRun or self.bRecvThreadRun ):
      time.sleep(0.1)

    if( self.bUseTwoAudio == False ):
      self.clsStream.close()
      self.clsAudio.terminate()

  
def RtpSendThread( clsRtpThread ):
  clsRtpThread.bSendThreadRun = True

  if( clsRtpThread.bUseTwoAudio ):
    clsAudio = pyaudio.PyAudio()
    clsStream = clsAudio.open( format = 8, channels = 1, rate = 8000, input = True, frames_per_buffer = 160 )

  iFlags = 0x80
  iPayload = 0
  iSeq = 0
  iTimeStamp = 0
  iSsrc = 200

  while( clsRtpThread.bStopEvent == False ):
    iSeq += 1
    iTimeStamp += 160

    if( clsRtpThread.bUseTwoAudio ):
      arrPcm = clsStream.read( 160 )
    else:
      arrPcm = clsRtpThread.clsStream.read( 160 )

    arrPayload = audioop.lin2ulaw( arrPcm, 2 )
    szPacket = struct.pack( '!BBHII', iFlags, iPayload, iSeq, iTimeStamp, iSsrc ) + arrPayload
    clsRtpThread.hUdpSocket.sendto( szPacket, (clsRtpThread.strDestIp, clsRtpThread.iDestPort) )

  if( clsRtpThread.bUseTwoAudio ):
    clsStream.close()
    clsAudio.terminate()

  clsRtpThread.bSendThreadRun = False

def RtpRecvThread( clsRtpThread ):
  clsRtpThread.bRecvThreadRun = True

  if( clsRtpThread.bUseTwoAudio ):
    clsAudio = pyaudio.PyAudio()
    clsStream = clsAudio.open( format = 8, channels = 1, rate = 8000, output = True, frames_per_buffer = 160 )

  read_list = [ clsRtpThread.hUdpSocket ]
  
  while( clsRtpThread.bStopEvent == False ):
    iRecvLen = 0

    try:
      read_socket_list, write_socket_list, except_socket_list = select.select( read_list, [], [], 1.0 )
      for read_socket in read_socket_list:
        szPacket, clsClientIpPort = read_socket.recvfrom( 8192 )
        iRecvLen = len(szPacket)
    except Exception as other:
      Log.Print( LogLevel.ERROR, "RtpRecvThread exception - " + str(other) )

    if( iRecvLen > 0 ):
      arrPayload = szPacket[12:]
      arrPcm = audioop.ulaw2lin( arrPayload, 2 )

      if( clsRtpThread.bUseTwoAudio ):
        clsStream.write( arrPcm )
      else:
        clsRtpThread.clsStream.write( arrPcm )

  if( clsRtpThread.bUseTwoAudio ):
    clsStream.close()
    clsAudio.terminate()

  clsRtpThread.bRecvThreadRun = False
