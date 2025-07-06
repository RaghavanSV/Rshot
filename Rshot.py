#Requirements
#pip install pywinrm
#pip install subprocess.run
#


import subprocess
import winrm

GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"
CYAN = "\033[36m"

def banner():
    banner=f"""{RED}
                                                                                                                                                                                     
RRRRRRRRRRRRRRRRR                    hhhhhhh                                       tttt          
R::::::::::::::::R                   h:::::h                                    ttt:::t          
R::::::RRRRRR:::::R                  h:::::h                                    t:::::t          
RR:::::R     R:::::R                 h:::::h                                    t:::::t          
  R::::R     R:::::R    ssssssssss    h::::h hhhhh          ooooooooooo   ttttttt:::::ttttttt    
  R::::R     R:::::R  ss::::::::::s   h::::hh:::::hhh     oo:::::::::::oo t:::::::::::::::::t    
  R::::RRRRRR:::::R ss:::::::::::::s  h::::::::::::::hh  o:::::::::::::::ot:::::::::::::::::t    
  R:::::::::::::RR  s::::::ssss:::::s h:::::::hhh::::::h o:::::ooooo:::::otttttt:::::::tttttt    
  R::::RRRRRR:::::R  s:::::s  ssssss  h::::::h   h::::::ho::::o     o::::o      t:::::t          
  R::::R     R:::::R   s::::::s       h:::::h     h:::::ho::::o     o::::o      t:::::t          
  R::::R     R:::::R      s::::::s    h:::::h     h:::::ho::::o     o::::o      t:::::t          
  R::::R     R:::::Rssssss   s:::::s  h:::::h     h:::::ho::::o     o::::o      t:::::t    tttttt
RR:::::R     R:::::Rs:::::ssss::::::s h:::::h     h:::::ho:::::ooooo:::::o      t::::::tttt:::::t
R::::::R     R:::::Rs::::::::::::::s  h:::::h     h:::::ho:::::::::::::::o      tt::::::::::::::t
R::::::R     R:::::R s:::::::::::ss   h:::::h     h:::::h oo:::::::::::oo         tt:::::::::::tt
RRRRRRRR     RRRRRRR  sssssssssss     hhhhhhh     hhhhhhh   ooooooooooo             ttttttttttt  
                                                                                                                                                                                        
    {RESET}
                                                                  
  Multi-Service Login Checker [RDP + WinRM]
  Author: 0r | For Education & Audit Use Only
  """

    print(banner)
    

def check_rdp_login(host, username, password ,domain):
    try:

        with open(host,'r') as h:
            h_con=h.readlines()
        with open(username,'r') as u:
            u_con=u.readlines()
        with open(password,'r') as p:
            p_con=p.readlines()

        for i in h_con:
            i=i.strip()
            for j in u_con:
                j=j.strip()
                j=domain + "\\" + j
                for k in p_con:
                    k=k.strip()
                    try:
                        result = subprocess.run(["xfreerdp", f"/v:{i}", f"/u:{j}", f"/p:{k}", "/cert-ignore"], capture_output=True, text=True,timeout=10)
                    except subprocess.TimeoutExpired:
                        continue
                    if "connected" in result.stdout.lower():
                        print(f"{GREEN}[+] {i} -> {j}:{k} CONNECTED{RESET}")
                    else:
                        print(f"{RED}[-] {i} -> {j}:{k} NOT VALID{RESET}")
                        #print(result.stdout)
    except Exception as e:
        print(f"error")


def check_winrm_login(host,username,password,domain):
    try:

        with open(host,'r') as h:
            h_con=h.readlines()
        with open(username,'r') as u:
            u_con=u.readlines()
        with open(password,'r') as p:
            p_con=p.readlines()
        

        for i in h_con:
            i=i.strip()
            for j in u_con:
                j=j.strip()
                j=domain + "\\" + j
                for k in p_con:
                    k=k.strip()
                    try:
                        session = winrm.Session(target=i,auth=(j,k),transport='ntlm')
                        response = session.run_cmd('whoami')
                        if response.status_code==0:
                            print(f"{GREEN}[+] {i} -> {j}:{k} CONNECTED{RESET}")
                        else:
                            print(f"{RED}[-] {i} -> {j}:{k} NOT VALID{RESET}")
                    except Exception as e:
                        continue

    except Exception as e:
        print(f"error")


def main():
    banner()
    host=input("Enter Host File Name :")
    username=input("Enter Users File Name :")
    password=input("Enter Passwords File Name :")
    domain=input("Enter Domain Name :")
    q=''
    ch=0
    while q!='N' :
        print("1 : RDP \n2 : winrm\n")
        ch=int(input("Enter the Choice :"))
        if ch == 1:
            check_rdp_login(host,username,password,domain)
        elif ch == 2:
            check_winrm_login(host,username,password,domain)
        q=input("Do You Want To Continue (Y or N):")

main()