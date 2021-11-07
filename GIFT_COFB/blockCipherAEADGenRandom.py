
#############################################################################
#                                                                           #
#   Copyright 2019 CERG                                                     #
#                                                                           #
#   Licensed under the Apache License, Version 2.0 (the "License");         #
#   you may not use this file except in compliance with the License.        #
#   You may obtain a copy of the License at                                 #
#                                                                           #
#       http://www.apache.org/licenses/LICENSE-2.0                          #
#                                                                           #
#   Unless required by applicable law or agreed to in writing, software     #
#   distributed under the License is distributed on an "AS IS" BASIS,       #
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.#
#   See the License for the specific language governing permissions and     #
#   limitations under the License.                                          #
#                                                                           #
#############################################################################
# FOBOS TV generator
# Generates random test vector for block ciphers 
# Author : Abubakr Abdulgadir
# June 2018

import array
import os
import re
import binascii
from Crypto import Random
import random

############user defined settings
TRACE_NUM = 2000                        # Number of traces
PDI_LENGTH = 16                            # In byets
SDI_LENGTH = 16                            # In bytes
EXPECTED_OUT = 44                          # Expected output in bytes
DIN_FILE = 'testDin_2000.txt'                   # Desitination file name
PLAINTEXT_FILE = 'plaintext_2000.txt'           # Desitination file name
#FIXED_KEY = 'yes'                          # Fixed key = yes | no
KEY = '86956D73FCCB1FF7CC44D54890C1C2AA'   # Fixed key
NPUB_LENGTH = 16
AD_LENGTH = 16
fvrchoicefile = "fvrchoicefile_2000.txt"
	
####header data - See Fobos protocol
PDI_HEADER = '00C0'
SDI_HEADER = '00C1'
CMD = '0080'
START = '0001'
EXPECTED_OUT_CMD = '0081'

####AEAD header data - See CAESER Hardware API
## AEAD Instructions
INST_AUTH_ENC = '20000000'
INST_AUTH_DEC = '30000000'
INST_LOAD_KEY = '40000000'
INST_ACT_KEY  = '70000000' 
INST_HASH = '80000000'

## Segment Header
INFO_SEG_AD  = '1'
INFO_SEG_PT  = '4'
INFO_SEG_KEY = 'C'
INFO_SEG_NPUB = 'D' # We think this is IV

INFO_EOT = '200'
INFO_ALL = '700'



###########################################################

pdiLength = format(PDI_LENGTH, '04x').upper() ##format into 4 hex digits
sdiLength = format(SDI_LENGTH, '04x').upper()
adLength = format(AD_LENGTH, '04x').upper()
expectedOut = format(EXPECTED_OUT, '04x').upper()


def intToHex(integer):
  hexString = hex(integer)[2:]
  if len(hexString) == 1 :
    hexString = '000' + hexString
  elif len(hexString) == 2:
    hexString = '00' + hexString
  elif len(hexString) == 3:
    hexString = '0' + hexString
  return hexString

def convertToHex(hexString):
   hexString = ''.join( [ "%02X " % ord( val ) for val in hexString] ).strip()
   hexString = ''.join( hexString.split(" ") )
   hexBytes = []
   for dataByte in range(0, len(hexString), 2):
      hexBytes.append( hexString[dataByte:dataByte+2])		
   return hexBytes

def generateRandomData(blockSize):
   randomBytes = []
   randomBytes = convertToHex(Random.get_random_bytes(blockSize))
   return randomBytes

def getRandData(blockSize):
   data = []
   data = generateRandomData(blockSize)
   return  ''.join(data)


def main():
   fDin = open(DIN_FILE,'w')
   fPlain = open(PLAINTEXT_FILE,'w')
   fchoicefile = open(fvrchoicefile,'w')
   for pdi in range(0,TRACE_NUM):
   	random_data = ""
   	if (random.random()<0.5):
   		fchoicefile.write('0')
   		random_data = 'F1989C9C57BAC42010071AF304C93339'
   		print intToHex(NPUB_LENGTH) + ' ' + intToHex(AD_LENGTH) + ' '+ intToHex(PDI_LENGTH)	
   		pdi = INST_ACT_KEY + \
            		INST_AUTH_ENC + \
            		INFO_SEG_NPUB + INFO_EOT + intToHex(NPUB_LENGTH)  + '6ECB9B9C86875A08BE33F2EADAD9A8F4' + \
            		INFO_SEG_AD + INFO_EOT + intToHex(AD_LENGTH) + '3DA6B3B637EAD6232E4916B04CDBAB2A' + \
            		INFO_SEG_PT + INFO_ALL + intToHex(PDI_LENGTH) + random_data
            		
            	sdi = INST_LOAD_KEY + \
               		INFO_SEG_KEY + INFO_ALL + intToHex(SDI_LENGTH) + '86956D73FCCB1FF7CC44D54890C1C2AA'
               
   	else:
   		fchoicefile.write('1')
      		print intToHex(NPUB_LENGTH) + ' ' + intToHex(AD_LENGTH) + ' '+ intToHex(PDI_LENGTH)
      		random_data = getRandData(PDI_LENGTH)
      		pdi = INST_ACT_KEY + \
            		INST_AUTH_ENC + \
            		INFO_SEG_NPUB + INFO_EOT + intToHex(NPUB_LENGTH) + '6ECB9B9C86875A08BE33F2EADAD9A8F4' + \
            		INFO_SEG_AD + INFO_EOT + intToHex(AD_LENGTH) + '3DA6B3B637EAD6232E4916B04CDBAB2A' + \
            		INFO_SEG_PT + INFO_ALL + intToHex(PDI_LENGTH) + random_data
      		#fPlain.write(random_data + '\n')
      		#if (FIXED_KEY == 'yes'):
         	#	sdi = INST_LOAD_KEY + \
               #		INFO_SEG_KEY + INFO_ALL + intToHex(SDI_LENGTH) + KEY
      		#else:
         	sdi =  INST_LOAD_KEY + \
                	INFO_SEG_KEY + INFO_ALL + intToHex(SDI_LENGTH) + '86956D73FCCB1FF7CC44D54890C1C2AA'
      	print "PDI"
      	print pdi
      	print "PDI bytes: " + str(len(pdi)/2)
      	print "SDI bytes: " + str(len(sdi)/2)
      	data = SDI_HEADER + intToHex(len(sdi)/2) + sdi + PDI_HEADER + intToHex(len(pdi)/2) + pdi + EXPECTED_OUT_CMD + expectedOut + CMD + START + '\n'
      	#print "random data numbers"
      	res = ' '.join(random_data[i:i+2] for i in range(0, len(random_data), 2))
      	fDin.write(data)
      	fPlain.write(res + '\n')

   fDin.close()
   fPlain.close()
   fchoicefile.close()

if __name__ == '__main__':
    main()
