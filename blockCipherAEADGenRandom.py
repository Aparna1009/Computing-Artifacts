
# FOBOS TV generator
# Generates random test vector for block ciphers 


import array
import os
import re
import binascii
from Crypto import Random
import random

############user defined settings
TRACE_NUM = 220000                          # Number of traces
PDI_LENGTH = 16                            # In byets
SDI_LENGTH = 16                            # In bytes
EXPECTED_OUT = 44                          # Expected output in bytes
DIN_FILE = 'testDin.txt'                   # Desitination file name
PLAINTEXT_FILE = 'plaintext.txt'           # Desitination file name
#FIXED_KEY = 'yes'                          # Fixed key = yes | no
KEY = '123456789009876ABCDFE12456789ABF'   # Fixed key
NPUB_LENGTH = 16
AD_LENGTH = 16
fvrchoicefile = "fvrchoicefile.txt"
	
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
   	random_data = getRandData(PDI_LENGTH)
   	if (random.random()<0.5):
   		fchoicefile.write('0')
   		print intToHex(NPUB_LENGTH) + ' ' + intToHex(AD_LENGTH) + ' '+ intToHex(PDI_LENGTH)	
   		pdi = INST_ACT_KEY + \
            		INST_AUTH_ENC + \
            		INFO_SEG_NPUB + INFO_EOT + intToHex(NPUB_LENGTH)  + 'F6FF59F3A6433E6186624B3BBE83EE7A' + \
            		INFO_SEG_AD + INFO_EOT + intToHex(AD_LENGTH) + 'DEAAA8767C2D7BD33D205DCFC045E4EF' + \
            		INFO_SEG_PT + INFO_ALL + intToHex(PDI_LENGTH) + '7AFF901F8CF275E690F07E465A69A45F'
            		
            	sdi = INST_LOAD_KEY + \
               		INFO_SEG_KEY + INFO_ALL + intToHex(SDI_LENGTH) + 'E533C0E2A36463DE6FF973D8DF3E168D'
               
   	else:
   		fchoicefile.write('1')
      		print intToHex(NPUB_LENGTH) + ' ' + intToHex(AD_LENGTH) + ' '+ intToHex(PDI_LENGTH)
      		pdi = INST_ACT_KEY + \
            		INST_AUTH_ENC + \
            		INFO_SEG_NPUB + INFO_EOT + intToHex(NPUB_LENGTH) + getRandData(NPUB_LENGTH) + \
            		INFO_SEG_AD + INFO_EOT + intToHex(AD_LENGTH) + getRandData(AD_LENGTH) + \
            		INFO_SEG_PT + INFO_ALL + intToHex(PDI_LENGTH) + random_data
      		#fPlain.write(random_data + '\n')
      		#if (FIXED_KEY == 'yes'):
         	#	sdi = INST_LOAD_KEY + \
               #		INFO_SEG_KEY + INFO_ALL + intToHex(SDI_LENGTH) + KEY
      		#else:
         	sdi =  INST_LOAD_KEY + \
                	INFO_SEG_KEY + INFO_ALL + intToHex(SDI_LENGTH) + getRandData(SDI_LENGTH)
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
