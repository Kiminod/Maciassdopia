
import sys

# We need 64 bit wersion
import win32api

# ========
# Not finished
# ========


class Evasion:
    def __init__(self):
        return None
    
    # Function NEED to be finished!!
    def check_all_DLL_names(self):
        SandboxEvidence = []

        if SandboxEvidence:
            return False
        else:
            return True
        
    # Function NEED to be finished!!
    def check_all_processes(self):
        EvidenceOfSandbox = []

        if not EvidenceOfSandbox:
            return True
        else:
            return False
        
    # Function not checked!!
    def disk_size(self):
        minDiskSizeGB = 50

        # I don't know what it is...
        if len(sys.argv) > 1:
            minDiskSizeGB = float(sys.argv[1])

        # checking free disc space (not checked)
        _, diskSizeBytes, _ = win32api.GetDiskFreeSpaceEx()

        diskSizeGB = diskSizeBytes/1073741824

        if diskSizeGB > minDiskSizeGB:
            return True
        else:
            return False
        
    # Function need to be checked!!
    def click_trecker(self):
        count = 0
        minClicks = 10

        if len(sys.argv) == 2:
            minClicks = int(sys.argv[1])
        
        while count < minClicks:
            new_state_left_click = win32api.GetAsyncKeyState(1)
            new_state_right_click = win32api.GetAsyncKeyState(2)

            if new_state_left_click % 2 == 1:
                count += 1
            if new_state_right_click % 2 == 1:
                count += 1

        return True
    
    def main(self):
        if self.disk_size() and self.click_trecker() and self.check_all_processes and self.check_all_DLL_names():
            return True
        else:
            return False
        
def test():
    evasion = Evasion()
    if evasion.main() == True:
        return True
    else:
        return False