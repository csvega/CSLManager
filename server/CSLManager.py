import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter.messagebox import askyesno
import fabFunction as ff
import threading
import sys

class CSLManagerApp:
    def __init__(self, master=None):
        self.master = master
        self.master.title("CSL Manager for Ubuntu Ver.0.8")
        self.master.geometry('560x480')
        self.master.resizable(False, False)
        self.filename = ''

        self.btn1 = tk.Button(self.master, padx=5, pady=5, text='세션초기화', command=self.resetClientFunc)
        self.btn1.place(x=10, y=10)

        self.btn4 = tk.Button(self.master, padx=5, pady=5, text='PC 종료', command=self.powerOffFunc)
        self.btn4.place(x=100, y=10)
        
        self.btn2 = tk.Button(self.master, padx=5, pady=5, text='명령어 사전', command=self.cmdDicFunc)
        self.btn2.place(x=180, y=10)

        self.label5 = tk.Label(self.master, text='PC 백업:')
        self.label5.place(x=10, y=50)
                        
        self.btn3 = tk.Button(self.master, padx=5, pady=5, text='선택 백업', command=self.backupSelFunc)
        self.btn3.place(x=100, y=50)
        
        self.btn3 = tk.Button(self.master, padx=5, pady=5, text='모두 백업', command=self.backupAllFunc)
        self.btn3.place(x=200, y=50)        

        self.listbox1 = tk.Listbox(self.master, selectmode='extended', height=0)
        self.listbox1.place(x=370, y=40)

        self.label1 = tk.Label(self.master, text='원격 명령:')
        self.label1.place(x=10, y=90)

        self.entry1 = tk.Entry(self.master, width=25)
        self.entry1.place(x=70, y=90)

        self.btnRun = tk.Button(self.master, text='실행', command=self.btnRunFunc)
        self.btnRun.place(x=290, y=90)

        self.btnSudo = tk.Button(self.master, text='sudo', command=self.btnSudoFunc)
        self.btnSudo.place(x=290, y=60)

        self.label2 = tk.Label(self.master, text='파일 전송:')
        self.label2.place(x=10, y=140)

        self.entry2 = tk.Entry(self.master, width=25)
        self.entry2.place(x=70, y=140)

        self.btnFile = tk.Button(self.master, text='파일 선택', command=self.selectFileFunc)
        self.btnFile.place(x=290, y=140)

        self.btnSelTrans = tk.Button(self.master, text='선택 전송', command=self.transferSelFunc)
        self.btnSelTrans.place(x=100, y=170)

        self.btnAllTrans = tk.Button(self.master, text='모두 전송', command=self.transferAllFunc)
        self.btnAllTrans.place(x=200, y=170)

        self.label3 = tk.Label(self.master, text='과제 회수:')
        self.label3.place(x=10, y=220)

        btnGetSel = tk.Button(self.master, text='선택 회수', command=self.getFileSelFunc)
        btnGetSel.place(x=100, y=220)

        self.btnGetAll = tk.Button(self.master, text='모두 회수', command=ff.getFileAll)
        self.btnGetAll.place(x=200, y=220)

        self.label4 = tk.Label(self.master, text='사이트 차단:')
        self.label4.place(x=10, y=270)

        self.btnSiteList = tk.Button(self.master, text='목록 열기', command=self.siteListFunc)
        self.btnSiteList.place(x=100, y=270)

        self.btnSiteRule = tk.Button(self.master, text='종료', command=ff.runSiteRule)
        self.btnSiteRule.place(x=200, y=270)

    def confirm(self,msg):
        ans = askyesno(title='확인', message=msg)
        return ans

    def resetClientFunc(self):
        ff.resetClient()
        label2 = tk.Label(self.master, text='총 ' + str(len(ff.clientList)) + '명 접속 중')
        label2.place(x=400, y=10)
       
        self.listbox1.delete(first=0, last=tk.END)
        for idx, client in enumerate(ff.clientList):
            self.listbox1.insert(idx, client)
                
    def checkClientFunc(self):
        stat = ff.checkIP()
        
        if stat:
            label2 = tk.Label(self.master, text='총 ' + str(len(ff.clientList)) + '명 접속 중')
            label2.place(x=400, y=10)
       
            self.listbox1.delete(first=0, last=tk.END)
            for idx, client in enumerate(ff.clientList):
                self.listbox1.insert(idx, client)
        
        # 5초마다 쓰레드 실행
        T = threading.Timer(5, self.checkClientFunc)
        T.start()

    def backupSelFunc(self):
        answer = self.confirm(msg='해당 클라이언트 백업을 실행하시겠습니까?')

        if answer:        
            for ip in self.listbox1.curselection():
                idx = ff.clientList.index(self.listbox1.get(ip))
                ff.backupSel(ff.clientConnection[idx])
                
    def backupAllFunc(self):
        answer = self.confirm(msg='클라이언트 전체 백업을 실행하시겠습니까?')
        if answer:
            ff.backupAll()
        
    def powerOffFunc(self):
        answer = self.confirm(msg='클라이언트 PC 전체를 끄시겠습니까?')
        if answer:
            ff.powerOff()        
        
    def btnRunFunc(self):
        cmd = self.entry1.get()
        print('run:', cmd)
        ff.runAll(cmd)
        self.entry1.delete(0, tk.END)

    def btnSudoFunc(self):
        cmd = self.entry1.get()
        print('sudo:', cmd)
        ff.sudoAll(cmd)
        self.entry1.delete(0, tk.END)

    def selectFileFunc(self):
        self.filename = filedialog.askopenfilename(initialdir='c:\\Users\\bsg\\Downloads\\', title='파일 선택')
        print(self.filename)
        self.entry2.delete(0, tk.END)
        self.entry2.insert(0, self.filename)

    def transferSelFunc(self):
        for ip in self.listbox1.curselection():
            idx = ff.clientList.index(self.listbox1.get(ip))
            ff.transferSel(self.filename, ff.clientConnection[idx])

    def transferAllFunc(self):
        ff.transferAll(self.filename)

    def getFileSelFunc(self):
        for ip in self.listbox1.curselection():
            idx = ff.clientList.index(self.listbox1.get(ip))
            ff.getFileSel(ff.clientList[ip], ff.clientConnection[idx])

    def siteListFunc(self):
        os.system('gedit /home/ubuntu/CSLManager/sitelist.txt')

    def cmdDicFunc(self):
        os.system('gedit /home/ubuntu/CSLManager/command.txt')
    
    def run(self):
        self.checkClientFunc()
        self.master.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = CSLManagerApp(root)
    app.run()
