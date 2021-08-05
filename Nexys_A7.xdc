# ===================== Data out to DUT  ===================================
set_property -dict {PACKAGE_PIN J2 IOSTANDARD LVCMOS33} [get_ports {din[3]}]
set_property -dict {PACKAGE_PIN J4 IOSTANDARD LVCMOS33} [get_ports {din[2]}]
set_property -dict {PACKAGE_PIN J3 IOSTANDARD LVCMOS33} [get_ports {din[1]}]
set_property -dict {PACKAGE_PIN E6 IOSTANDARD LVCMOS33} [get_ports {din[0]}]
# ===================== Data in from DUT ===================================
set_property -dict {PACKAGE_PIN F3 IOSTANDARD LVCMOS33} [get_ports {dout[0]}]
set_property -dict {PACKAGE_PIN G3 IOSTANDARD LVCMOS33} [get_ports {dout[1]}]
set_property -dict {PACKAGE_PIN G2 IOSTANDARD LVCMOS33} [get_ports {dout[2]}]
set_property -dict {PACKAGE_PIN G1 IOSTANDARD LVCMOS33} [get_ports {dout[3]}]
# ===================== CONTROL SIGNALS ====================================
set_property -dict {PACKAGE_PIN F6 IOSTANDARD LVCMOS33} [get_ports do_ready]
set_property -dict {PACKAGE_PIN E7 IOSTANDARD LVCMOS33} [get_ports do_valid]
set_property -dict {PACKAGE_PIN H1 IOSTANDARD LVCMOS33} [get_ports di_ready]
set_property -dict {PACKAGE_PIN G4 IOSTANDARD LVCMOS33} [get_ports di_valid]
set_property -dict {PACKAGE_PIN K1 IOSTANDARD LVCMOS33} [get_ports rst]
# ======================== CLOCK SIGNAL ====================================
set_property -dict {PACKAGE_PIN H4 IOSTANDARD LVCMOS33} [get_ports clk]
#create_clock -period 50.000 -name sys_clk_pin -waveform {0.000 25.000} -add [get_ports clk]
set_property CLOCK_DEDICATED_ROUTE FALSE [get_nets clk]
# ======================== DEBUG LEDS ====================================
set_property -dict {PACKAGE_PIN H17 IOSTANDARD LVCMOS33} [get_ports {debug_led[0]}]
set_property -dict {PACKAGE_PIN K15 IOSTANDARD LVCMOS33} [get_ports {debug_led[1]}]
set_property -dict {PACKAGE_PIN J13 IOSTANDARD LVCMOS33} [get_ports {debug_led[2]}]
set_property -dict {PACKAGE_PIN N14 IOSTANDARD LVCMOS33} [get_ports {debug_led[3]}]
set_property -dict {PACKAGE_PIN R18 IOSTANDARD LVCMOS33} [get_ports {debug_led[4]}]
set_property -dict {PACKAGE_PIN V17 IOSTANDARD LVCMOS33} [get_ports {debug_led[5]}]
set_property -dict {PACKAGE_PIN U17 IOSTANDARD LVCMOS33} [get_ports {debug_led[6]}]
set_property -dict {PACKAGE_PIN U16 IOSTANDARD LVCMOS33} [get_ports {debug_led[7]}]
set_property -dict {PACKAGE_PIN V16 IOSTANDARD LVCMOS33} [get_ports {debug_led[8]}]
set_property -dict {PACKAGE_PIN T15 IOSTANDARD LVCMOS33} [get_ports {debug_led[9]}]
set_property -dict {PACKAGE_PIN U14 IOSTANDARD LVCMOS33} [get_ports {debug_led[10]}]
set_property -dict {PACKAGE_PIN T16 IOSTANDARD LVCMOS33} [get_ports {debug_led[11]}]
set_property -dict {PACKAGE_PIN V15 IOSTANDARD LVCMOS33} [get_ports {debug_led[12]}]
set_property -dict {PACKAGE_PIN V14 IOSTANDARD LVCMOS33} [get_ports {debug_led[13]}]
set_property -dict {PACKAGE_PIN V12 IOSTANDARD LVCMOS33} [get_ports {debug_led[14]}]
set_property -dict {PACKAGE_PIN V11 IOSTANDARD LVCMOS33} [get_ports {debug_led[15]}]


