import blescan
import bluetooth._bluetooth as bluez

dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)
	print "ble thread started"

except:
	print "error accessing bluetooth device..."
    	sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

class Beacon_receiver:

    def all_receive(self, uptake_number_of_once):
        self.uptake_number_of_once = uptake_number_of_once
        all_beacon_list = blescan.parse_events(sock, self.uptake_number_of_once)
        #print"all"
        #Sprint all_beacon_list
        self.all_beacon_list = all_beacon_list
        #print len(self.all_beacon_list)
        #print self.all_beacon_list

    def select(self, terget_of_beacon_major,terget_of_beacon_minor):
        self.terget_of_beacon_major = terget_of_beacon_major
        self.terget_of_beacon_minor = terget_of_beacon_minor
        selected_data = []
        
        for i in range(len(self.all_beacon_list)):
            if self.all_beacon_list[i][2] == self.terget_of_beacon_major:
                if self.all_beacon_list[i][3] == self.terget_of_beacon_minor:
                    selected_data.append(self.all_beacon_list[i])
            else:
                pass

        #print"-----selected-----"
        #print selected_data
        self.selected_data = selected_data
        #print self.selected_data

    def matrix(self):
        self.number_of_list = len(self.selected_data)
        #print self.number_of_list
        new_list = []
        for k in range(self.number_of_list):
            new_list.append(self.selected_data[k][2])
            new_list.append(self.selected_data[k][3])
            new_list.append(self.selected_data[k][5])
        else:
            pass
        slice_list = [new_list[i:i+3] for i in range(0,len(new_list),3)]
        self.slice_list = slice_list
        #print self.slice_list


    def average(self):
     
        M = 0
        B = 0
        F = 0
        
        for i in range(0, len(self.slice_list)):
            B += self.slice_list[i][2]
            F += 1

        M = B/F

        dataA = []
        #dataA.append(2)
        dataA.append(M)
        #print dataA
        return(dataA)



                      
            
