import csv
import pandas as pd
from random import random
import random as r
import winsound
import clipboard
from kivy.graphics import Color, Ellipse, Line
from kivy.graphics import Line
from win10toast import ToastNotifier
from kivymd.uix.picker import MDTimePicker
from twilio.rest import Client
from kivymd.app import MDApp
from csv import DictWriter
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.label import Label
from kivy.storage.jsonstore import JsonStore
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.core.window import Window
Window.size = {300,500}

# class to call the popup function
class PopupWindow(Widget):
    def btn(self):
        popFun()

# class to build GUI for a popup window
class P(FloatLayout):
    pass

# function that displays the content
def popFun():
    show = P()
    window = Popup(title="popup", content=show,
                   size_hint=(None, None), size=(300, 150))
    window.open()



class MainWindow(Screen):
    def forgotpassword(self):
        sm.current='otpmobile'
    def backbutton(self):
        sm.current='login'
    def validate(self):
        username = ObjectProperty(None)
        pwd = ObjectProperty(None)
        # validating if the email already exists
        users = pd.read_csv('login.csv')
        if self.username.text!='' and self.pwd.text!='':
            if self.username.text not in users['Name'].unique():
                popFun()
            if self.username.text in users['Name'].unique():
                pas=(users.loc[users['Name'] == self.username.text, 'Password'])
                pas.to_csv('pas.csv', index=False, header=True)
                pascsv=pd.read_csv('pas.csv')
                if pascsv["Password"][0]==self.pwd.text:
                    if self.username.text in users['Name'].unique():
                        account = pd.DataFrame([[self.username.text, self.pwd.text]], columns=['Name', 'Password'])
                        account.to_csv('account.csv', index=False, header=True)
                        # switching the current screen to display validation result
                        sm.current = 'homepage'
                        # reset TextInput widget
                        self.username.text = ""
                        self.pwd.text = ""
                else:
                    popFun()
            
        else:
            popFun()
         
 
        
class RegisterWindow(Screen):
    name2 = ObjectProperty(None)
    mobile = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def signupbtn(self):
        # creating a DataFrame of the info
        users = pd.read_csv('login.csv')
        user = pd.DataFrame([[self.name2.text,  self.mobile.text, self.pwd.text]],
                            columns=['Name', 'Mobile', 'Password'])
        if self.mobile.text != "" and self.name2.text!=''and self.pwd.text!='':
            if self.mobile.text not in users['Mobile'].unique():

                # if email does not exist already then append to the csv file
                # change current screen to log in the user now
                user.to_csv('login.csv', mode='a', header=False, index=False)
            self.name2.text = ""
            self.mobile.text = ""
            self.pwd.text = ""
            sm.current = 'main'
        else:
            popFun()  # if values are empty or invalid show pop up

    def backbtn(self):
        sm.current = 'main'

class ForgetpasswordWindow(Screen):
    username = ObjectProperty(None)
    mobile = ObjectProperty(None)
    confirmpwd = ObjectProperty(None)
    def backbutton(self):
        sm.current= 'main'
    def verify(self):
        if (self.newpwd.text and self.confirmpwd.text) != "":
            users = pd.read_csv('login.csv')
            u=self.username.text
            n=self.newpwd.text
            c=self.confirmpwd.text
            index = users.index
            condition = users["Name"] == u
            idx = index[condition]
            idx_list = idx.tolist()
            users.at[idx_list, "Password"] = c
            if n!=c:
                popFun()
                self.confirmpwd.text=''
                self.newpwd.text=''
            else:
                users.to_csv('login.csv', mode='w', header=True, index=False)
                self.username.text=''
                self.confirmpwd.text=''
                self.newpwd.text=''
                sm.current='main'
        else:
            popFun()  # if values are empty or invalid show pop up



#otp genration
otp=""
for i in range(4):
    otp+=str(r.randint(1,9))
    A=otp
with open('otp.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["otp"])
    writer.writerow([A])
def otpformobile():
    return ("Your OTP : {}".format(A))


# class for otp verification
class logDataWindow(Screen):
    #onetimepwd is nothing but for going back
    def onetimepwd(self):
        sm.current= 'main'
    def verifybutton(self):
        otp_val=(self.onetimepassword.text)
        if otp_val==A:
            sm.current= 'forgetpassword'
        else:
            print("failure")

# class for getting mobile number for sending an otp
class otpmobileWindow(Screen):
    name2 = ObjectProperty(None)


    def sendotpmob(self):
        k=self.name2.text
        if k not in users['Name'].unique():
            popFun()  # if values are empty or invalid show pop up
        else:


            #the following line needs your Twilio Account SID and Auth Token
            #client = Client("AC071b2848e866d06d7d91cabd1bda3a34", "f1329791f96d513bd27f9ef97d563708")

            # change the "from_" number to your Twilio number and the "to" number
            # to the phone number you signed up for Twilio with
            client.messages.create(to="<phone no.",
                                            from_="+12568417046",
                                            body=otpformobile())
            sm.current='logdata'
            # self.name.text = ""

    def back(self):
        sm.current= 'main'
    def sendotp():
        sm.current='forgotpassword'


class HomepageWindow(Screen):
    def hp_settings(self):
        sm.current='homepagesettings'
    def wishlistbtn(self):
        sm.current='wishlist'
    def supportbtn(self):
        sm.current='support'
    def shoppinglists(self):
        sm.current='shoppinglists'
    def partiesandevents(self):
        sm.current='partiesandevents'
    def calendar(self):
        sm.current='calendar'


#class for homepage settings window
class homepagesettingsWindow(Screen):
    usertext=ObjectProperty(None)
    mobtext=ObjectProperty(None)
    def backbtn(self):
        sm.current='homepage'
    def on_pre_enter(self):
        account=pd.read_csv("account.csv")
        self.usertext.text=account["Name"][0]
    def changepassword(self):
        sm.current='forgetpassword'
    def deleteaccount(self):
        dele=pd.read_csv("login.csv")
        df3=pd.DataFrame(dele)
        if self.usertext.text in dele['Name'].unique():
            df3.drop(df3[df3['Name']==self.usertext.text].index, inplace = True)
            df3.to_csv("login.csv",index=False )
            sm.current='main'



#class for notification button from homepage
class supportWindow(Screen):
    def backbutton(self):
        sm.current= 'homepage'


#---------------------------------------------------------------------------------------------------------------

#shopping lists starts

#form
class AddNewForm(Widget):
    item_input = ObjectProperty(None)
    title_input= ObjectProperty(None)
    input1 = StringProperty('')
    input2 = StringProperty('')

    store = JsonStore("data.json")
     
    def submit_input(self):
        self.input1 = self.title_input.text
        self.input2 = self.item_input.text
        self.store.put(self.input1, items=self.input2)
        self.title_input.text=''
        self.item_input.text=''
        sm.current='shoppinglists'

    


class shoppinglistviewWindow(Screen):
    item_input = ObjectProperty(None)
    title_input= ObjectProperty(None)
    input1 = StringProperty('')
    input2 = StringProperty('')

    store = JsonStore("data.json")

    def viewnote(self):
        if self.title_input.text=='':
            popFun()
        else:
            store = JsonStore("data.json")
            if store.exists(self.title_input.text):
                h=self.title_input.text
                k=store.get(h)["items"]
                self.item_input.text=k
            else:
                popFun()
        
    def closenote(self):
        if self.title_input.text=='':
            popFun()
        else:
            store = JsonStore("data.json")
            if store.exists(self.title_input.text):
                self.title_input.text=''
                self.item_input.text=''
                sm.current='shoppinglists'
            else:
                popFun()

    
    def delete(self):
        if self.title_input.text=='':
            popFun()
        else:
            store = JsonStore("data.json")
            if store.exists(self.title_input.text):
                h=self.title_input.text
                k=store.get(h)["items"]
                self.store.delete(h)
                self.title_input.text=''
                self.item_input.text=''
                sm.current='shoppinglists'
            else:
                popFun()
           
            
                

                


    def copy(self):
        clipboard.copy(self.item_input.text)
        b=clipboard.paste()
        

      
        
        
class RVItem(Factory.Button):
    def on_release(self):
        pass
   


#recycle view for home screen
class MyRecycleView(RecycleView):

    def __init__(self, **kwargs):
        super(MyRecycleView, self).__init__(**kwargs)
        self.load_data()
        Clock.schedule_interval(self.load_data, 1)

    def load_data(self, *args):
        store = JsonStore("data.json")
        list_data = []
        for item in store:
            list_data.append({'text': item})

        self.data = list_data

#class for shopping lists from homepage
class shoppinglistsWindow(Screen):
    pass


#class for adding shopping lists
class shoppinglistaddWindow(Screen):
    def __init__(self, **kwargs):
        super(shoppinglistaddWindow, self).__init__(**kwargs)
        self.addNewForm = AddNewForm()
        self.add_widget(self.addNewForm)

#shopping lists over
#------------------------------------------------------------------------------------------------------------


#parties and events starts here


class RVitem(Factory.Button):
    def on_release(self):
        pass

#form
class Addnewf(Widget):
    itemin = ObjectProperty(None)
    titlein= ObjectProperty(None)
    inone = StringProperty('')
    intwo = StringProperty('')

    partystore = JsonStore("partydata.json")

    def submitin(self):
        self.inone = self.titlein.text
        self.intwo = self.itemin.text
        self.partystore.put(self.inone, items=self.intwo)
        self.titlein.text = ''
        self.itemin.text = ''
        sm.current='partiesandevents'


class partiesandeventsviewWindow(Screen):
    itemin = ObjectProperty(None)
    titlein= ObjectProperty(None)
    inone = StringProperty('')
    intwo = StringProperty('')

    store = JsonStore("partydata.json")

    def viewnote(self):
        if self.titlein.text=='':
            popFun()
        else:
            store = JsonStore("partydata.json")
            if store.exists(self.titlein.text):
                h=self.titlein.text
                k=store.get(h)["items"]
                self.itemin.text=k
            else:
                popFun()
        
        
    def closenote(self):
        if self.titlein.text=='':
            popFun()
        else:
            store = JsonStore("partydata.json")
            if store.exists(self.titlein.text):
                self.titlein.text=''
                self.itemin.text=''
                sm.current='partiesandevents'
            else:
                popFun()

    def copyparty(self):
        clipboard.copy(self.itemin.text)
        b=clipboard.paste()


    def deleteparty(self):
        if self.titlein.text=='':
            popFun()
        else:    
            store = JsonStore("partydata.json")
            if store.exists(self.titlein.text):
                h=self.titlein.text
                k=store.get(h)["items"]
                self.store.delete(h)
                self.titlein.text=''
                self.itemin.text=''
                sm.current='partiesandevents'
            else:
                popFun()


#recycle view for home screen
class Myrview(RecycleView):

    def __init__(self, **kwargs):
        super(Myrview, self).__init__(**kwargs)
        self.ldata()
        Clock.schedule_interval(self.ldata, 1)

    def ldata(self, *args):
        partystore = JsonStore("partydata.json")
        lisdata = []
        for item in partystore:
            lisdata.append({'text': item})

        self.data = lisdata

#class for shopping lists from homepage
class partiesandeventsWindow(Screen):
    pass


#class for adding shopping lists
class partiesandeventsaddWindow(Screen):
    def __init__(self, **kwargs):
        super(partiesandeventsaddWindow, self).__init__(**kwargs)
        self.addNewF = Addnewf()
        self.add_widget(self.addNewF)

#partiesandevents over
#---------------------------------------------------------------------------------
#Daily expenses coding starts here





class RV(Factory.Button):
    def on_release(self):
        sm.current='dailyexpensesadd'

#form
class Anf(Widget):
    iteminput = ObjectProperty(None)
    titleinput= ObjectProperty(None)
    inputone = StringProperty('')
    inputtwo = StringProperty('')

    dailystore = JsonStore("dailydata.json")


    def submitinput(self):
        self.inputone = self.titleinput.text
        self.inputtwo = self.iteminput.text
        self.dailystore.put(self.inputone, items=self.inputtwo)
        self.titleinput.text = ''
        self.iteminput.text = ''
        sm.current='dailyexpenses'


class dailyexpensesviewWindow(Screen):

    iteminput = ObjectProperty(None)
    titleinput= ObjectProperty(None)
    inputone = StringProperty('')
    inputtwo = StringProperty('')

    dailystore = JsonStore("dailydata.json")

    def viewnotedaily(self):
        if self.titleinput.text=='':
            popFun()
        else:
            dailystore = JsonStore("dailydata.json")
            if dailystore.exists(self.titleinput.text):
                h=self.titleinput.text
                k=dailystore.get(h)["items"]
                self.iteminput.text=k
            else:
                popFun()
        
    def closenotedaily(self):
        if self.titleinput.text=='':
            popFun()
        else:
            dailystore = JsonStore("dailydata.json")
            if dailystore.exists(self.titleinput.text):
                self.titleinput.text=''
                self.iteminput.text=''
                sm.current='dailyexpenses'
            else:
                popFun()
        

    def copydaily(self):
        clipboard.copy(self.iteminput.text)
        b=clipboard.paste()


    def deletedaily(self):
        if self.titleinput.text=='':
            popFun()
        else:
            dailystore = JsonStore("dailydata.json")
            if dailystore.exists(self.titleinput.text):
                h=self.titleinput.text
                k=dailystore.get(h)["items"]
                self.dailystore.delete(h)
                self.titleinput.text=''
                self.iteminput.text=''
                sm.current='dailyexpenses'
            else:
                popFun()


#recycle view for home screen
class Myrecview(RecycleView):

    def __init__(self, **kwargs):
        super(Myrecview, self).__init__(**kwargs)
        self.loaddata()
        Clock.schedule_interval(self.loaddata, 1)

    def loaddata(self, *args):
        dailystore = JsonStore("dailydata.json")
        listdata = []
        for item in dailystore:
            listdata.append({'text': item})

        self.data = listdata


#class for dailyexpenses
class dailyexpensesWindow(Screen):
    pass


#class for adding dailyexpenses
class dailyexpensesaddWindow(Screen):
    def __init__(self, **kwargs):
        super(dailyexpensesaddWindow, self).__init__(**kwargs)
        self.anf = Anf()
        self.add_widget(self.anf)




#class for calculator window
class CalculatorWindow(Screen):
    def calculate(self, calculation):
        if calculation:
            try:
                self.display.text = str(eval(calculation))
            except Exception:
                self.display.text = "Error"
    def back(self):
        sm.current='dailyexpensesview'


#class for locker window
class lockerWindow(Screen):
    def back(self):
        sm.current='dailyexpenses'
    def locker(self):
        #print(self.lock.text)
        account=pd.read_csv("account.csv")
        field_names = ['Name','pin']
        n=account.iloc[0][0]
        k=self.lock.text
        newrow={'Name': n,'pin': k}
        locker=pd.read_csv('lock.csv')
        if n not in locker['Name'].unique():
            with open('lock.csv', 'a',newline='') as f_object:
                dictwriter_object = DictWriter(f_object, fieldnames=field_names,delimiter =',')
                dictwriter_object.writerow(newrow)
                f_object.close()
        locker1=pd.read_csv('lock.csv')   #again and again writing same username pin
        if self.lock.text!='':
            if n in locker1['Name'].unique():
                p=locker1.loc[locker1['Name'] == n, 'pin'] 
                if k==p[0]:
                    sm.current='lockerstore'
                else:
                    popFun()
            else:
                popFun()



class Recyvi(Factory.Button):
    def on_release(self):
        pass

#form
class Afn(Widget):
    ini = ObjectProperty(None)
    intt= ObjectProperty(None)
    infirst = StringProperty('')
    insecond = StringProperty('')

    lockerstore = JsonStore("lockerstore.json")


    def submittingginput(self):
        self.infirst = self.intt.text
        self.insecond = self. ini.text
        self.lockerstore.put(self.infirst, items=self.insecond)
        self.intt.text = ''
        self. ini.text = ''
        sm.current='lockerstore'



class lockerstoreviewWindow(Screen):

    ini = ObjectProperty(None)
    intt= ObjectProperty(None)
    infirst = StringProperty('')
    insecond = StringProperty('')

    lockstore = JsonStore("lockerstore.json")

    def viewnotelocker(self):
        if self.intt.text=='':
            popFun()
        else:
            lockstore = JsonStore("lockerstore.json")
            if lockstore.exists(self.intt.text):
                h=self.intt.text
                k=lockstore.get(h)["items"]
                self.ini.text=k
            else:
                popFun()
        
        
    def closenotelocker(self):
        if self.intt.text=='':
            popFun()
        else:
            lockstore = JsonStore("lockerstore.json")
            if lockstore.exists(self.intt.text):
                self.intt.text=''
                self.ini.text=''
                sm.current='lockerstore'
            else:
                popFun()
        

    def copylocker(self):
        clipboard.copy(self.ini.text)
        b=clipboard.paste()

    def delnotelocker(self):
        if self.intt.text=='':
            popFun()
        else:
            lockstore = JsonStore("lockerstore.json")
            if lockstore.exists(self.intt.text):
                h1=self.intt.text
                self.lockstore.delete(h1)
                sm.current='lockerstore'
            else:
                popFun()

  


#recycle view for home screen
class Minerrec(RecycleView):

    def __init__(self, **kwargs):
        super(Minerrec, self).__init__(**kwargs)
        self.loda()
        Clock.schedule_interval(self.loda, 1)

    def loda(self, *args):
        lockerstore = JsonStore("lockerstore.json")
        lida = []
        for item in lockerstore:
            lida.append({'text': item})

        self.data = lida


#class for dailyexpenses
class lockerstoreWindow(Screen):
    pass


#class for adding dailyexpenses
class lockerstoreaddWindow(Screen):
    def __init__(self, **kwargs):
        super(lockerstoreaddWindow, self).__init__(**kwargs)
        self.afn = Afn()
        self.add_widget(self.afn)




#------------------------------------------------------------------------------------------

#Calendar coding starts here

#class for calendar option in homepage window
class calendarWindow(Screen):
    alarm=ObjectProperty(None)
    def show_time_picker(self):
        from datetime import datetime
        # Must be a datetime object
        now = datetime.now()
        time_dialog = MDTimePicker()
        time_dialog.set_time(now)
        time_dialog.bind(time=self.get_time)
        time_dialog.open()
    def get_time(self, instance, time):
        label= Label(text ="Time for alarm is {}".format(time), font_size ='15sp',
            color =[0, 0, 0, 1],size_hint = (0.2, 0.1),
            pos_hint ={"x":0.4,"y":0.7})
        self.ids.float.add_widget(label)

    def backbtn(self):
        sm.current='homepage'


    def textareas(self):
        #print(self.alarm.text)
        def timer (remider,seconds):
            k=10
            notificator=ToastNotifier()
            notificator.show_toast("Reminder",f"""Alarm will go off in {seconds} Seconds.""",duration=k)
            notificator.show_toast(f"Reminder",remider,duration=k)

        #alarm
        frequency=5500
        duration=1000
        winsound.Beep(frequency,duration)

        words=self.alarm.text
        sec=10
        timer(words,sec)

#class for calendardate window from calendar window
class calendardateWindow(Screen):
    def back(self):
        sm.current='calendar'

#------------------------------------------------------------------
#paint code starts here



class Painter(Widget):
    #global xs,ys
    
    def on_touch_down(self, touch):
        color = (random(), random(), random())
        xs=touch.x
        ys=touch.y
        with self.canvas:
            Color(*color)
            d = 30.
            #Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y),width=3)

    def on_touch_move(self, touch):
        xs=touch.x
        ys=touch.y
        touch.ud['line'].points += [xs,ys]
    
        

        
class paintWindow(Screen):
    pass

    

#-----------------------------------------------------------------------------



class WindowManager(ScreenManager):
    pass


# kv file
kv = Builder.load_file('final.kv')

sm = WindowManager()



sm.add_widget(MainWindow(name='main'))
sm.add_widget(RegisterWindow(name='register'))
sm.add_widget(ForgetpasswordWindow(name='forgetpassword'))
sm.add_widget(logDataWindow(name='logdata'))
sm.add_widget(otpmobileWindow(name='otpmobile'))
sm.add_widget(HomepageWindow(name='homepage'))
sm.add_widget(homepagesettingsWindow(name='homepagesettings'))
sm.add_widget(supportWindow(name='support'))
sm.add_widget(shoppinglistsWindow(name='shoppinglists'))
sm.add_widget(shoppinglistaddWindow(name='shoppinglistadd'))
sm.add_widget(shoppinglistviewWindow(name='shoppinglistview'))
sm.add_widget(partiesandeventsWindow(name='partiesandevents'))
sm.add_widget(partiesandeventsaddWindow(name='partiesandeventsadd'))
sm.add_widget(partiesandeventsviewWindow(name='partiesandeventsview'))
sm.add_widget(dailyexpensesWindow(name='dailyexpenses'))
sm.add_widget(dailyexpensesaddWindow(name='dailyexpensesadd'))
sm.add_widget(dailyexpensesviewWindow(name='dailyexpensesview'))
sm.add_widget(CalculatorWindow(name='Calculator'))
sm.add_widget(lockerWindow(name='locker'))
sm.add_widget(lockerstoreWindow(name='lockerstore'))
sm.add_widget(lockerstoreaddWindow(name='lockerstoreadd'))
sm.add_widget(lockerstoreviewWindow(name='lockerstoreview'))
sm.add_widget(calendarWindow(name='calendar'))
sm.add_widget(calendardateWindow(name='calendardate'))
sm.add_widget(paintWindow(name='paint'))


# reading all the data stored
users = pd.read_csv('login.csv')



# class that builds gui
class HUT(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        return sm


# driver function
if __name__ == "__main__":
    HUT().run()
