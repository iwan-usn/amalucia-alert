from datetime import datetime

with open('log.txt','a') as myfile:
    currenttime = datetime.now()
    myfile.write('\n--------------------------\n')
    myfile.write(f"the amalucia went by at {currenttime}")