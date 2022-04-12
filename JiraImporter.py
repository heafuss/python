import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter import Frame
from jira import JIRA
#import createIssue
import csv


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        

        # configure the root window
        self.title('My Awesome App')
        self.geometry('640x480')
        
        # label
        self.lbluser = ttk.Label(self, text="User", width =10)
        self.lbluser.grid(row=0,column=0)
        #username
        self.txtuser = ttk.Entry(self,width=15)
        self.txtuser.grid(row=0,column=1)

        #password Label
        self.lblpassword = ttk.Label(self, text="Password", width =10)
        self.lblpassword.grid(row=1,column=0)
        
        #password text box
        self.txtpassword = ttk.Entry(self,show="*",width=15)
        self.txtpassword.grid(row=1,column=1)

        # Login button
        self.btnlogin = ttk.Button(self, text='Login')
        self.btnlogin['command'] = self.btnlogin_clicked
        self.btnlogin.grid(row=2,column=1)
        
        self.lblfilename = ttk.Label(self,text="Filename",width = 10)
        self.lblfilename.grid(row=4,column=0)

       

        self.lblfileselected = ttk.Label(self,text='',width = 30)
        self.lblfileselected.grid(row=4,column=1)

        self.btnchoosefile = ttk.Button(self,text='Browse')
        self.btnchoosefile['command'] = self.btnbrowse_clicked
        self.btnchoosefile.grid(row=4,column=3)

        self.lblsummary = ttk.Label(self,text='Summary',width = 10)
        self.lblsummary.grid(row=5,column=0)

        self.txtsummary = ttk.Entry(self,width=15)
        self.txtsummary.grid(row=5,column=1)

        self.lbldescription = ttk.Label(self,text='Description',width=15)
        self.lbldescription.grid(row=6,column=0)

        self.txtdesc = ttk.Entry(self,width=30)
        self.txtdesc.grid(row=6,column=1)
        
        self.lbllabel = ttk.Label(self,text="Label",width=15)
        self.lbllabel.grid(row=7,column=0)

        self.txtlabel = ttk.Entry(self,width=15)
        self.txtlabel.grid(row=7,column=1)


        self.btnCreateIssue = ttk.Button(self,text="Create Issue")
        self.btnCreateIssue['command'] = self.btnCreateIssue_clicked
        self.btnCreateIssue.grid(row=8,column=1)


    def btnCreateIssue_clicked(self):
        self.createIssue(self.file,str(self.selected_project.get()),self.txtsummary.get(),self.txtdesc.get(),'Task',self.txtlabel.get())

    def btnbrowse_clicked(self):
        self.file = filedialog.askopenfilename(filetypes=[('CSV', '*.csv')])
        self.lblfileselected.config(text=self.file)
        self.importCSV(file)

    def btnlogin_clicked(self):
        self.login()
        self.get_projects()         

    def get_projects(self):
        #listbox
        self.selected_project = tk.StringVar()

        projects = self.jira.projects()
        
        self.combobox = ttk.Combobox(self,textvariable=self.selected_project,height=6)
        self.combobox['values']= projects
        self.combobox.grid(row=3,column=1)

    def login(self):
        server = 'http://localhost:8080'
        username = self.txtuser.get()
        password = self.txtpassword.get()

        jira_options = {
        'server': server,
        }

        self.jira = JIRA(options=jira_options, basic_auth=(username,password))
        self.get_projects()
    def importCSV(self,csvfile):
        with open(csvfile) as csv_file:
          csv_reader = csv.DictReader(csv_file)
          for row in csv_reader:
              print(row["Summary"])
              

    def createIssue(self,csvfile,project,summary,description,issuetype,label):
        arrlabel = [label]
        keyissue = self.jira.create_issue(project = project, summary = summary, description = description, issuetype = issuetype, labels = arrlabel)
        with open(csvfile) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                task = {
                    'project' : {'key':project},
                    'summary' : row["Summary"],
                    'description': row["STIGID"] + ":" + row["FIX Text"],
                    'issuetype' : { 'name' : 'Sub-task' },
                    'parent':{'id':keyissue.id},
                    'labels':arrlabel,
                }
                self.jira.create_issue(fields=task)
            showinfo("done")




                


if __name__ == "__main__":
    app = App()
    app.mainloop()