import fabric
import os
import time
from pathlib import WindowsPath


clientConfig = fabric.Config(overrides = { 'run': {'in_stream': False }, 'sudo': {'password': 'wjdqh'} } )

clientList, clientConnection, clientGroup = [], [], []
tclientList, tclientConnection, tclientGroup = [], [], []

def createDirectory(folder):
    try:
        if not os.path.exists(folder):
            os.makedirs(folder,0o777)
    except OSError:
        print('[Error] 디렉토리 생성에 실패하였습니다! - ',folder)


# 클라이언트 목록 지움
def resetClient():
    global clientList,clientConnection,clientGroup
    clientList, clientConnection, clientGroup = [], [], []

    folder = WindowsPath('C:\\Manager\\')
    createDirectory(folder)
    
    print('===== 클라이언트 연결 리셋 시작 =====')
    for ipFile in os.listdir(folder):
        os.remove(folder+ipFile)
    print('===== 클라이언트 연결 리셋 완료 =====')


# 클라이언트 체크 (/home/ubuntu/student 에 목록 생성: 클라이언트에서 자기 ip 보내줌)
def checkIP():
    global clientList,clientConnection,clientGroup,clientConfig
    global tclientList,tclientConnection,tclientGroup
    
    tclientList, tclientConnection, tclientGroup = [], [], []

    folder = 'C:\\Manager\\students\\'
    try:
        createDirectory(folder)
    except:
        pass

    allIP = os.listdir(folder)
    
    # 클라이언트와 최근 7초 이내 통신이 있었는지 확인.
    now = int(time.time())
    for ip in allIP:
        fileGenTime = int(os.path.getctime(folder + ip))
        diff = now - fileGenTime

        tclientList.append(ip[:-3])
#        if diff<=7:
#            tclientList.append(ip[:-3])
#        else:
#            os.remove(folder+ip)
            

    tclientList.sort(key=lambda x: int(x[x.rfind('.')+1:]))
    
    if tclientList == clientList:
        return False
                
    for conIP in tclientList:
        try:
            tclientConnection.append(fabric.Connection(host=conIP, user='stu', port=22, connect_kwargs={'password': 'wjdqh'}, config=clientConfig))
        except:
            print('[Error] 클라이언트 연결중 오류가 발생하였습니다! -',conIP)

    tclientGroup = fabric.ThreadingGroup.from_connections(tclientConnection)
    
    clientList, clientConnection, clientGroup = tclientList, tclientConnection, tclientGroup
    #print(*clientConnection)
    
    return True


def backupSel(client):
    print('===== 선택된 클라이언트 백업 시작 =====')
    try:
        client.sudo('mv /etc/ubuntu/reset.tar /etc/ubuntu/reset_old.tar')
    except:
        print('[Warning] 기존 백업 파일이 없습니다!')

    try:
        client.sudo('tar cvpf /etc/ubuntu/reset.tar /home/ubuntu/')
    except:
        print('[Error] 백업 중 문제가 발생하였습니다!')        
    print('===== 선택된 클라이언트 백업 완료 =====')    
    
        
def backupAll():
    global clientGroup
    print('===== 모든 클라이언트 백업 시작 =====')
    try:
        clientGroup.sudo('mv /etc/ubuntu/reset.tar /etc/ubuntu/reset_old.tar')
    except:
        print('[Warning] 기존 백업 파일이 없습니다!')

    try:
        clientGroup.sudo('tar cvpf /etc/ubuntu/reset.tar /home/ubuntu/')
    except:
        print('[Error] 백업 중 문제가 발생하였습니다!')        

    print('===== 모든 클라이언트 백업 완료 =====')


def powerOff():  
    global clientGroup
    print('===== 전체 PC OFF 시작 =====')
    try:
        clientGroup.sudo('shutdown -h now')
    except:
        pass
    print('===== 전체 PC OFF 완료 =====')
    

def runAll(cmd):
    global clientGroup
    print('===== 원격 명령어 전송 시작 =====')
    try:
        clientGroup.run(cmd)
    except:
        print('[Error] 명령어 전송 중 문제가 발생하였습니다!')
    print('===== 원격 명령어 전송 완료 =====')


def sudoAll(cmd):
    global clientGroup
    print('===== 원격 명령어(sudo) 전송 시작 =====')
    try:
        clientGroup.sudo(cmd)
    except:
        pass
    print('===== 원격 명령어(sudo) 전송 완료 =====')


def transferAll(filename):
    global clientGroup
    clientFoldername = r'C:/Users/stu/Desktop/'
    #filename = filename

    print(clientFoldername)
    print(filename)

    print('===== 모든 클라이언트 파일 전송 시작 =====')
#    try:
    temp=clientGroup.put(filename, clientFoldername)
    print(temp.stderr)
#    except:
#        print('[Error] 파일 전송 중 오류가 발생하였습니다. -', filename)
    print('===== 모든 클라이언트 파일 전송 완료 =====')


def transferSel(filename, client):
    clientFoldername = 'C:\\Users\\stu\\Desktop\\과제제출\\'
    filename = Path(filename)

    print('===== 선택된 클라이언트 파일 전송 시작 =====')
    print(filename,'-->', client)
    try:
        client.put(filename, clientFoldername)
    except:
        print('[Error] 파일 전송 중 문제가 발생하였습니다!')
    print('===== 선택된 클라이언트 파일 전송 완료 =====')


def getFileSel(ip, client):
    print('===== 선택된 클라이언트 파일 회수 시작 =====')
    print(ip,'--> Server')
    clientFoldername = 'C:\\Users\\stu\\Desktop\\과제제출\\'
    serverFoldername = 'C:\\Users\\bsg\\Desktop\\과제제출\\'
    try:
        output = client.run('dir/B '+clientFoldername)
        files = output.stdout.strip().split('\n')
        for file in files:
            try:
                if file!='':
                    client.get(clientFoldername+file, serverFoldername+ip+'_'+file)
                else:
                    client.get(clientFoldername+file, serverFoldername+ip+'_파일없음')
            except:
                pass
    except:
        print('[Error] 폴더를 찾을 수 없습니다!')

    print('===== 선택된 클라이언트 파일 회수 완료 =====')


def getFileAll():
    global clientList,clientConnection
    print('===== 모든 클라이언트 파일 회수 시작 =====')
    clientFoldername = "C:\\Users\\stu\\Desktop\\과제제출\\"
    serverFoldername = "C:\\Users\\bsg\\Desktop\\과제제출\\"

    for idx,client in enumerate(clientConnection):
        print(clientList[idx],'--> Server')
        try:
            result = client.run('dir/B '+clientFoldername)
            
            allfiles = result.stdout.strip().split('\n')
            print('ALL'+allfiles)

            for file in allfiles:
                print(clientFoldername+file)
                print(serverFoldername+clientList[idx]+'_'+file)
                try:
                    if file!='':
                        print(33333)
                        temp=client.get('"'+clientFoldername+file+'"', serverFoldername+clientList[idx]+'_'+file)
                        print(temp.stderr)
                    else:
                        print(4444)
                        temp=client.get('"'+clientFoldername+file+'"', '"'+serverFoldername+clientList[idx]+'_파일없음(미제출)'+'"')
                        print(temp.stderr)
                except:
                    print('[Error] 파일을 가져오는 중 문제가 발생했습니다.', temp.stderr)
        except:
            print('[Error] 폴더를 찾을 수 없습니다!')

    print('===== 모든 클라이언트 파일 회수 완료 =====')


def runSiteRule():
    global clientList,clientConnection,clientGroup
    print('===== 사이트 정책 초기화 =====')
    #clientGroup.sudo('iptables -F && iptables -P OUTPUT ACCEPT')

    print('===== 사이트 차단 정책 적용 시작 =====')
    f=open('/home/ubuntu/CSLManager/sitelist.txt')
    sites = f.readlines()
    f.close()

    for site in sites:
        site = site.strip()
        print(site)
        if site=='' or site=='\n' or site[0]=='#':
            pass
        else:
            cmd = f'iptables -A OUTPUT -d {site} -j DROP'
            print('차단 정책 적용 중... ', cmd)
            try:
                clientGroup.sudo(cmd)
            except:
                print('[Error] iptables 명령어(sudo) 실행 중 문제가 발생하였습니다!')

    print('===== 사이트 차단 정책 적용 완료 =====')



'''
sudo iptables -w -I OUTPUT  -p all -m string --hex-string "youtube|03|com" --algo bm -j YOUTUBE
sudo iptables -w -I FORWARD -p all -m string --hex-string "youtube|03|com" --algo bm -j YOUTUBE

sudo iptables -w -I OUTPUT  -p all -m string --hex-string "googlevideo|03|com" --algo bm -j YOUTUBE
sudo iptables -w -I FORWARD -p all -m string --hex-string "googlevideo|03|com" --algo bm -j YOUTUBE
'''