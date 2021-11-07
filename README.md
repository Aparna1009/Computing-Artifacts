# Computing-Artifacts
In our work  the Flexible Opensource workbench for Side-channel analysis platform (its acronym is FOBOS) is used to evaluate hardware implementations of Lightweight authenticated ciphers on Field Programmable Gate Arrays (FPGAs). Although majority of the setup follows the [FOBOS 2.0 guide](https://cryptography.gmu.edu/documentation/fobos/introduction.html) there are some modification need to done to ensure that the side-channel attack can be effectively performed on the cryptographic algorithm. In this computing artifact we have included the required files.

In this FOBOS setup, Basys 3 is used as control board, Nexys A7 as Device UnterTest (DUT) and Picoscope 5000 series (5244D) as oscilloscope. A slight modification is performed on the DUT board to measure a voltage/current propotional to the power consumed by the device. This can be done by having  a jumper on the power line (core FPGA voltage).
 
We have used three cryptographic algorithm implemented by GMU to evaluate SCA : [ASCON](https://cryptography.gmu.edu/athena/index.php?id=CAESAR_source_codes) and [GIFT_COFB](https://cryptography.gmu.edu/athena/index.php?id=CAESAR_source_codes) of CAESAR hardware implementation and [Schwaemm using Koggle Stone Adder](https://github.com/vtsal/schwaemm_ksa_lwc_aead) of Lightweight cryptography hardware implementation. We have used the implementation used by CAESAR hardware API and LWC hardware API because the wrapper class provided by the FOBOS is compatible with these APIs.

Once the cryptographic algorithm is identified to be used as function core, we setup control and DUT board. Setting up the control board follows the same procedure as the FOBOS guide. Lets take an example ASCON to be implemented in DUT board, it also follows the same procedure in DUT board setup but there is need of modification in files. They are:
   * Need to modify the wrapper class (FOBOS_DUT.vhd) by modifying the component declaration to reflect the victim core's entity declaration. FOBOS_DUT.vhd file has been included in [ASCON folder](/ASCON). Similar changes need to made during the respective cryptography hardware implementation in DUT board.
   * Need to include the Nexys_A7.xdc constraint file when generating the DUT bitstream. This constraint file is used to map PMOD ports on both boards from which the data transfers are made.

Once the bitstream is generated, we need to send inputs (plaintext, key, nonce, associated data) to the fuction core so that it could encrypt the data. To send the input as testvector it should follow communication protocol based on their hadware implementation either [CAESAR API](https://eprint.iacr.org/2016/626.pdf) or [LWC API](https://cryptography.gmu.edu/athena/LWC/LWC_HW_API.pdf). The function core take the in input data from two FIFOs: (1) SDI FIFO where the key is sent and (2) PDI FIFO where the remaining inputs are sent. These FIFOs follow certain format as shown below:

![instruction](https://github.com/Aparna1009/Computing-Artifacts/blob/main/instruction.PNG)

Fig : Instruction Format



                    
![segment](https://github.com/Aparna1009/Computing-Artifacts/blob/main/segment.PNG)    
                          Fig : Segment Header Format
                          
                          
A script file blockCipherAEADGenRandom.py was created based on the communication protocol and input length (key, nonce, plaintext and associated data length) of the fuction core. The output of the python file are the fixed-vs-random testvectors, plaintext and fvrchoicefile (prints 1's and 0's) based on the specified trace numbers. In each cryptographic folder lists the output files.

Files
-------
fvrchoicefile.txt  ---> prints 1's for random and 0's for fixed testvectors.

plaintext_170000.txt  ---> plaintext for 1700000 traces.

testDin.txt  ---> testvectors for 2000 traces.

T-test leakage assessment
--------------------------
Paramenter are changed in t-test.py based on the number of traces and sampling number with which the power consumption for the algorithm was collected.
