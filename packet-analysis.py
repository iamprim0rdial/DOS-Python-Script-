# Packet analysis using scapy 
def packet_analysis():
    from scapy.all import sniff

    def packet_callback(packet):
        logging.info(f"Packet captured: {packet.summary()}")
    
    sniff(prn=packet_callback, count=10) # Capture 10 packets for analysis


packet_analysis()
