from Tkinter import *
import tkFileDialog
import sys
from Final_Project_27 import *
import random
import os

class Schedule(Frame):
    def __init__(self, parent = None):
        Frame.__init__(self,parent)
        self.parent = parent
        self.pack()
        self.menu()
        self.groups = create_groups()
        self.activities = create_activities()
        self.act_buttons = []
        self.act_button_names = []
        #self.info_box()
        self.makeTitle()

    #This function adds in the Top Menu
    def menu(self):
        self.menubar = Menu(self)

        # create a pulldown menu, and add it to the menu bar
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open       ", command = self.open_file)
        filemenu.add_command(label="Save       ", command = self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Show Activities", command = self.show_activities)
        filemenu.add_command(label="Show Equalization Matrix", command = self.show_matrix)
        filemenu.add_command(label="Test Program      ", command = self.test_matrix)
        filemenu.add_command(label="Export...", command = self.export)
        filemenu.add_command(label="Exit")
        self.menubar.add_cascade(label="File", menu=filemenu)

        # create more pulldown menus
        editmenu = Menu(self.menubar, tearoff=0)
        editmenu.add_command(label = "Add Activity     ", command = self.add_activity)
        editmenu.add_command(label = "Update Eq. Matrix     ", command = self.update_matrix)
        editmenu.add_command(label = "Clear Matrix      ", command = self.clear_matrix)
        editmenu.add_command(label = "Check Schedule      ", command = self.check_schedule)
        
        self.menubar.add_cascade(label="Edit", menu=editmenu)

        #creates find pulldown
        findmenu = Menu(self.menubar, tearoff = 0)
        findmenu.add_command(label = "Clear Find       ", command = self.all_green, accelerator = "Ctrl+C")
        self.bind_all("<Control-c>", self.all_green2)
        findmenu.add_command(label = "Find Activity    ", command = self.find_activity_dialog, accelerator = "Ctrl+F")
        self.bind_all("<Control-f>", self.find_activity_dialog2)
        findmenu.add_command(label = "Find Fillers      ", command = self.find_fillers)
        findmenu.add_command(label = "Find Ladder Sports", command = self.find_ladder)
        findmenu.add_command(label = "Find Water Sports ", command = self.find_water)

        self.menubar.add_cascade(label = "Find Options", menu = findmenu)
        
        helpmenu = Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label="About        ", command = self.show_readme)
        self.menubar.add_cascade(label="Help", menu=helpmenu)

        # display the menu
        self.parent.config(menu=self.menubar)

    def find_fillers(self):
        fillers = [25,26,28,30,31,32,33]
        for period in range(12):
            for group in self.groups:
                if group.get_schedule()[period] in self.activities:
                    if self.activities.index(group.get_schedule()[period]) in fillers:
                        self.act_buttons[period][self.groups.index(group)].config(bg = "blue violet")
                else:
                    if (self.activities.index(group.get_schedule()[period].other_act[0]) in fillers or
                            self.activities.index(group.get_schedule()[period].other_act[1]) in fillers):
                        self.act_buttons[period][self.groups.index(group)].config(bg = "blue violet")
    def find_ladder(self):
        sports = [0,1,2,3,4,5]
        for period in range(12):
            for group in self.groups:
                if group.get_schedule()[period] in self.activities:
                    if self.activities.index(group.get_schedule()[period]) in sports:
                        self.act_buttons[period][self.groups.index(group)].config(bg = "sandy brown")
                else:
                    if (self.activities.index(group.get_schedule()[period].other_act[0]) in sports or
                            self.activities.index(group.get_schedule()[period].other_act[1]) in sports):
                        self.act_buttons[period][self.groups.index(group)].config(bg = "sandy brown")

    def find_water(self):
        sports = [7,8,9,10,11,20,21]
        for period in range(12):
            for group in self.groups:
                if group.get_schedule()[period] in self.activities:
                    if self.activities.index(group.get_schedule()[period]) in sports:
                        self.act_buttons[period][self.groups.index(group)].config(bg = "aquamarine")
                else:
                    if (self.activities.index(group.get_schedule()[period].other_act[0]) in sports or
                            self.activities.index(group.get_schedule()[period].other_act[1]) in sports):
                        self.act_buttons[period][self.groups.index(group)].config(bg = "aquamarine")
                

    def check_schedule(self):
        for period in range(12):
            for group in self.groups:
                group_index = self.groups.index(group)
                if (not (group.get_schedule()[period] == self.activities[10] or
                         group.get_schedule()[period] == self.activities[11] or
                         group.get_schedule()[period] == self.activities[8])):
                    if count_instances(group, group.get_schedule()[period])>1:
                        self.act_buttons[period][group_index].config(bg ="red")
                        for period2 in range(12):
                            if (group.get_schedule()[period2] == group.get_schedule()[period]):
                                self.act_buttons[period2][group_index].config(bg = "red")
                            elif type(group.get_schedule()[period2].other_act) == type([]):
                                if group.get_schedule()[period] in group.get_schedule()[period2].other_act:
                                    self.act_buttons[period2][group_index].config(bg = "red")
                if (search_duplicates_period(self.groups, period, self.activities) > 0):
                    for group2 in self.groups:
                        if (not (group == group2) and group.get_schedule()[period] == group2.get_schedule()[period]
                            and not group.get_schedule()[period] == self.activities[10]
                            and not group.get_schedule()[period] == self.activities[11]):
                                self.act_buttons[period][group_index].config(bg = "red")
                                self.act_buttons[period][self.groups.index(group2)].config(bg = "red")
                        elif (type(group.get_schedule()[period].other_act) == type([]) and not group == group2):
                              if type(group2.get_schedule()[period].other_act) == type([]):
                                  if (group.get_schedule()[period].other_act[0] == group2.get_schedule()[period].other_act[0] or
                                      group.get_schedule()[period].other_act[1] == group2.get_schedule()[period].other_act[1]):
                                      self.act_buttons[period][group_index].config(bg = "red")
                                      self.act_buttons[period][self.groups.index(group2)].config(bg = "red")
                              else:
                                  if group2.get_schedule()[period] in group.get_schedule()[period].other_act:
                                      self.act_buttons[period][group_index].config(bg = "red")
                                      self.act_buttons[period][self.groups.index(group2)].config(bg = "red")
                        elif (type(group2.get_schedule()[period].other_act) == type([]) and not group == group2):
                            if group.get_schedule()[period] in group2.get_schedule()[period].other_act:
                                self.act_buttons[period][group_index].config(bg = "red")
                                self.act_buttons[period][self.groups.index(group2)].config(bg = "red")
                        
    def show_matrix(self):
        top = Toplevel()
        mat_file = open("Equalization Matrix.txt", "r")
        mat_list = eval(mat_file.read())
        mat_file.close()

        w = Canvas(top, width = 800, height = 500)
        
        scrollbar = Scrollbar(top, orient = HORIZONTAL)
        scrollbar.pack(side = BOTTOM, fill = X)

        w.config(xscrollcommand = scrollbar.set, scrollregion = (0,0,2000,2000))
        scrollbar.config(command = w.xview)

        w.pack(side=LEFT, expand = TRUE, fill = BOTH)

        widget_frame = Frame(top)
        group_f = Frame(widget_frame)
        group_f.pack(side = LEFT)
        Label(group_f, text = "").pack(side=TOP)
        for x in range(len(self.groups)):
            Label(group_f, text = self.groups[x].get_name()).pack(side=TOP, anchor = NW)

        for activity in range(len(self.activities)):
            frame = Frame(widget_frame)
            frame.pack(side=LEFT)
            Label(frame, text = self.activities[activity]).pack(side = TOP)
            for group in range(len(self.groups)):
                if activity >= len(mat_list[group]):
                    Label(frame, text = 0).pack(side=TOP)
                else:
                    Label(frame, text = mat_list[group][activity]).pack(side = TOP)
                
        w.create_window(875,240, window = widget_frame)
        
    def test_matrix(self):
        for x in range(5):
            create_master_schedule(self.groups, self.activities)
            for period in range(12):
                for group in range(len(self.groups)):
                    self.act_buttons[period][group].config(text = str(self.groups[group].get_schedule()[period]), bg = "green")
                    self.act_button_names[period][group] = self.groups[group].get_schedule()[period]
            self.update_matrix()

    def clear_matrix(self):
        mat_file = open("Equalization Matrix.txt", "w")
        mat_list = []
        for x in range(20):
            mat_list.append([])
            for y in range(len(self.activities)):
                mat_list[x].append(0)
                
        mat_file.write(str(mat_list))
        mat_file.close()
        
    def update_matrix(self):
        mat_file = open("Equalization Matrix.txt", "r")
        mat_list = eval(mat_file.read())
        mat_file.close()
        for period in range(12):
            for group in range(len(self.groups)):
                if not (self.groups[group].get_schedule()[period] in self.activities[0:34]):
                    if type(self.groups[group].get_schedule()[period].other_act) == type([]):
                        update_index_1 = self.activities.index(self.groups[group].get_schedule()[period].other_act[0])
                        update_index_2 = self.activities.index(self.groups[group].get_schedule()[period].other_act[1])
                        mat_list[group][update_index_1] = mat_list[group][update_index_1] + 1
                        mat_list[group][update_index_2] = mat_list[group][update_index_2] + 1
                    else:
                        for x in range(self.activities.index(self.groups[group].get_schedule()[period])-33):
                            mat_list[group].append(0)
                            update_index = self.activities.index(self.groups[group].get_schedule()[period])
                            mat_list[group][update_index] = mat_list[group][update_index] + 1
                else:
                    update_index = self.activities.index(self.groups[group].get_schedule()[period])
                    mat_list[group][update_index] = mat_list[group][update_index] + 1
        mat_file_2 = open("Equalization Matrix.txt", "w")
        mat_file_2.write(str(mat_list))
        mat_file_2.close()
        
    def export(self):
        export_file = ""
        for group in range(len(self.groups)/2):
            if not (export_file == ""):
                export_file = export_file + "\n"
            for period in range(12):
                export_file = export_file + str(self.groups[group*2+1].get_schedule()[period]) +"\t"
                if period%3 == 2:
                    export_file = export_file + "\t"
        export_file = export_file +"\n"+ "\n"

        for group in range(len(self.groups)/2):
            export_file = export_file + "\n"
            for period in range(12):
                export_file = export_file + str(self.groups[group*2].get_schedule()[period]) +"\t"
                if period%3 == 2:
                    export_file = export_file + "\t"
                
        fileToSave = tkFileDialog.asksaveasfile(mode='w', title = "Choose Export File", defaultextension = ".txt")
        fileToSave.write(export_file)
        fileToSave.close()
        
    #Stored as a list of lists containing the indexes of the different activities in self.activities
    def save_file(self):
        fileToSave = tkFileDialog.asksaveasfile(mode='w', defaultextension = ".txt")
        text2save = []
        other_acts=[]
        for period in range(12):
            text2save.append([])
            for group in range(len(self.groups)):
                if self.groups[group].get_schedule()[period] in self.activities:
                    text2save[period].append(self.activities.index(self.groups[group].get_schedule()[period]))
                else:
                    o_act = self.groups[group].get_schedule()[period]
                    other_acts.append([o_act.get_name(), o_act.get_min_age(), o_act.get_max_age(),
                                      o_act.get_competing_activity(), o_act.not_days, [self.activities.index(o_act.other_act[0]),
                                       self.activities.index(o_act.other_act[1])]])
                    text2save[period].append(100)
        activity_list = []
        for act in self.activities:
            if type(act.get_competing_activity()) == type(None):
                activity_list.append([act.get_name(), act.get_min_age(), act.get_max_age(),
                                      act.get_competing_activity(), act.not_days])
            else:
                comp_act = self.activities.index(act.get_competing_activity())
                activity_list.append([act.get_name(), act.get_min_age(), act.get_max_age(),
                                      comp_act, act.not_days])
        
        fileToSave.write(str([text2save,activity_list, other_acts]))
        fileToSave.close()

    def open_file(self):
        file = tkFileDialog.askopenfile(mode='r',title='Choose a file')
        test = file.read()
        schedule_info = eval(test)
        schedule_indexes = schedule_info[0]
        schedule_activities = schedule_info[1]
        other_activities = schedule_info[2]

        final_acts_info = []
        final_acts = []
        for x in range(len(schedule_activities)):
            final_acts_info.append(eval(str(schedule_activities[x])))
            if type(final_acts_info[x][3]) == type(None):
                final_acts.append(activity(final_acts_info[x][0],final_acts_info[x][1],final_acts_info[x][2],
                                           final_acts_info[x][3],final_acts_info[x][4]))
            else:
                final_acts.append(activity(final_acts_info[x][0],final_acts_info[x][1],final_acts_info[x][2],
                                           self.activities[final_acts_info[x][3]],final_acts_info[x][4]))

        self.activities = final_acts

        other_acts_info = []
        other_acts =[]
        for x in range(len(other_activities)):
            other_acts_info.append(eval(str(other_activities[x])))
            if type(other_acts_info[x][3]) == type(None):
                other_acts.append(activity(other_acts_info[x][0],other_acts_info[x][1],other_acts_info[x][2],
                                           other_acts_info[x][3],other_acts_info[x][4], [self.activities[other_acts_info[x][5][0]],
                                           self.activities[other_acts_info[x][5][1]]]))

        counter = 0
        
        for period in range(12):
            for group in range(len(self.groups)):
                if not schedule_indexes[period][group] == 100:
                    self.act_button_names[period][group] = self.activities[schedule_indexes[period][group]]
                else:
                    self.act_button_names[period][group] = other_acts[counter]
                    counter = counter+1
        
        for period in range(12):
            for group in range(len(self.groups)):
                self.act_buttons[period][group].config(text = str(self.act_button_names[period][group]))
                self.groups[group].get_schedule()[period] = self.act_button_names[period][group]
                
        file.close()
            
    def show_readme(self):
        top = Toplevel()

        w = Canvas(top, width = 600, height = 600)
        
        scrollbar = Scrollbar(top, orient = VERTICAL)
        scrollbar.pack(side = RIGHT, fill = Y)

        w.config(yscrollcommand = scrollbar.set, scrollregion = (0,0,1200,1200))
        scrollbar.config(command = w.yview)

        w.pack(side=LEFT, expand = TRUE, fill = BOTH)

        widget_frame = Frame(top)
        
        readme_font = ("times", 12)
        readme_file = open("Final_README.txt", "r")
        readme_string = readme_file.read()
        Label(widget_frame, text = readme_string, font = readme_font).pack(side = LEFT, anchor = W)
        w.create_window(300, 600, window = widget_frame)
        readme_file.close()

    def all_green(self):
        for period in range(12):
            for group in range(len(self.groups)):
                self.act_buttons[period][group].config(bg = "green")

    def all_green2(self, event):
        for period in range(12):
            for group in range(len(self.groups)):
                self.act_buttons[period][group].config(bg = "green")
                
    def find_activity_dialog(self):
        top = Toplevel()
        find = IntVar()
        find.set(27)
        
        Button(top, text = "FIND", command = lambda: self.find_activity(find.get())).pack(side = BOTTOM)
        
        frame = Frame(top)
        frame.pack(side = LEFT)
        for x in range(len(self.activities)/2):
            Radiobutton(frame, text = str(self.activities[x]), variable = find, value = x).pack(side = BOTTOM)

        frame_2 = Frame(top)
        frame_2.pack(side = LEFT)
        for y in range(len(self.activities)/2, len(self.activities)):
            Radiobutton(frame_2, text = str(self.activities[y]), variable = find, value = y).pack(side = BOTTOM)

    def find_activity_dialog2(self, event):
        top = Toplevel()
        find = IntVar()
        find.set(27)
        
        Button(top, text = "FIND", command = lambda: self.find_activity(find.get())).pack(side = BOTTOM)
        
        frame = Frame(top)
        frame.pack(side = LEFT)
        for x in range(len(self.activities)/2):
            Radiobutton(frame, text = str(self.activities[x]), variable = find, value = x).pack(side = BOTTOM)

        frame_2 = Frame(top)
        frame_2.pack(side = LEFT)
        for y in range(len(self.activities)/2, len(self.activities)):
            Radiobutton(frame_2, text = str(self.activities[y]), variable = find, value = y).pack(side = BOTTOM)
    #finds all periods where a group has the specific activity and turns its background to yellow
    def find_activity(self, activity):
        for period in range(12):
            for group in range(len(self.groups)):
                if self.act_button_names[period][group] == self.activities[activity]:
                    self.act_buttons[period][group].config(bg = "yellow")
                #this next part checks to make sure none of the added half periods have the activity
                #uses the possibility that the class activity has a parameter other_act for just this case of
                #half activity periods
                elif type(self.groups[group].get_schedule()[period].other_act) == type([]):
                    if self.groups[group].get_schedule()[period].other_act[0] == self.activities[activity]:
                        self.act_buttons[period][group].config(bg = "yellow")
                    elif self.groups[group].get_schedule()[period].other_act[1] == self.activities[activity]:
                        self.act_buttons[period][group].config(bg = "yellow")


    #provides another window, containing simply a list of all the activities
    #useful when testing whether an activity was actually added to the overall activities list
    def show_activities(self):
        t = Toplevel()
        frame = Frame(t)
        frame.pack(side = LEFT)
        for x in range(len(self.activities)/2):
            Label(frame, text = str(self.activities[x])).pack(side = BOTTOM)

        frame_2 = Frame(t)
        frame_2.pack(side = LEFT)
        for y in range(len(self.activities)/2, len(self.activities)):
            Label(frame_2, text = str(self.activities[y])).pack(side = BOTTOM)
    

    #creates a pop up window for the user to input a new activity and add it to the overall activities list
    def add_activity(self):
        top = Toplevel()
        act_name = StringVar()
        act_min = IntVar()
        act_max = IntVar()
        
        Label(top, text = "Create a New Activity").grid(row = 0, column = 0)
        Label(top, text = "Activity Name: ").grid(row=1, column=0)
        Entry(top, textvariable = act_name).grid(row=1, column = 1)
        Label(top, text = "Minimum Age for Activity: ").grid(row=2, column = 0)
        Entry(top, textvariable = act_min).grid(row=2, column = 1)
        Label(top, text = "Maximum Age for Activity: ").grid(row=3, column = 0)
        Entry(top, textvariable = act_max).grid(row=3, column=1)

        def change_activity(act):
            self.activities.append(act)
            #top.quit()

        change = Button(top, text = "Add Activity", command = lambda: change_activity(activity(act_name.get(), act_min.get(), act_max.get(), None, [])))
        change.grid(row = 4, column = 0, rowspan = 2)
        
    #One of the first functions called in the constructor and begins the process of actually showing the schedule
    def makeTitle(self):
        titlefont=('times', 30,'bold')
        Label(self, text = "Sherwood Forest Schedule Generator", font = titlefont).pack(side=TOP)
        Button(self, text = "Create New Schedule", command = self.change_schedule).pack(side=LEFT)
        Button(self, text = "Create Partial Schedule", command = self.change_partial).pack(side=LEFT)
        Button(self, text = "Add Rest", command = self.add_other).pack(side=LEFT)
        self.makeSchedule()

    def add_other(self):
        max_had = find_max_had(self.groups, self.activities)
        add_rest(self.groups, self.activities, max_had)
        set_half_activities(self.groups, self.activities, max_had)
        for period in range(12):
            for group in range(len(self.groups)):
                self.act_buttons[period][group].config(text = str(self.groups[group].get_schedule()[period]), bg = "green")
                self.act_button_names[period][group] = self.groups[group].get_schedule()[period]
        
    def change_partial(self):
        create_partial_schedule(self.groups, self.activities)
        for period in range(12):
            for group in range(len(self.groups)):
                self.act_buttons[period][group].config(text = str(self.groups[group].get_schedule()[period]), bg = "green")
                self.act_button_names[period][group] = self.groups[group].get_schedule()[period]
                
    def change_schedule(self):
        dups = False
        create_master_schedule(self.groups, self.activities)
        for period in range(12):
            if search_duplicates_period(self.groups, period, self.activities)>0:
                dups = True
            for group in range(len(self.groups)):
                if self.groups[group].get_schedule()[period] == self.activities[0]:
                    dups = True
                    
                if dups:
                    self.act_buttons[period][group].config(text = str(self.groups[group].get_schedule()[period]), bg = "green")
                else:
                    self.act_buttons[period][group].config(text = str(self.groups[group].get_schedule()[period]), bg = "green")
                self.act_button_names[period][group] = self.groups[group].get_schedule()[period]
    
    def makeSchedule(self):
        create_master_schedule(self.groups, self.activities)
        group_frame = Frame(bg = "white")
        group_frame.pack(side=LEFT, expand=YES)
        self.makeGroups(group_frame)
        for x in range(12):
            frame = Frame()
            if search_duplicates_period(self.groups,x,self.activities)>0 or self.groups[x].get_schedule()[x] == self.activities[0]:
                frame.pack(side=LEFT, expand = YES)
                frame.config(bg="green")
                self.makePeriod(frame, x, True)
            else:
                frame.pack(side=LEFT, expand = YES)
                frame.config(bg="green")
                self.makePeriod(frame, x, False)
            
    def makePeriod(self, frame, period, duplicates):
        labelfont = ('times', 11, 'bold')
        groupfont = ('times', 10, 'bold')
        self.act_buttons.append([])
        self.act_button_names.append([])
        Label(frame, text ="Day "+str(period/3 + 1)+" Period "+str(period%3 + 1), bg = 'white', font=labelfont, relief =RAISED).pack(side=TOP)
        if duplicates:
            for x in range(len(self.groups)):
                self.act_buttons[period].append(Button(frame, text=self.groups[x].get_schedule()[period], bg="green", font=groupfont,
                                                       command=lambda arg = x: self.change_activity(arg,self.groups[x], period)))
                #This is so I can find what the actual text of each button is
                self.act_button_names[period].append(self.groups[x].get_schedule()[period])
                self.act_buttons[period][x].pack(side=TOP,fill=X)
        else:
            for x in range(len(self.groups)):
                self.act_buttons[period].append(Button(frame, text=self.groups[x].get_schedule()[period], bg="green", font=groupfont,
                                                       command=lambda arg = x: self.change_activity(arg,self.groups[x], period)))
                #This is so I can find what the actual text of each button is
                self.act_button_names[period].append(self.groups[x].get_schedule()[period])
                self.act_buttons[period][x].pack(side=TOP,fill=X)

    def makeGroups(self,frame):
        groupfont = ('times', 10, 'bold')
        titlefont = ('times', 11, "bold")
        Label(frame, text = "Groups", font = titlefont, bg = "white").pack(side=TOP)
        for x in range(len(self.groups)):
            Button(frame, text = self.groups[x].get_name(), bg = "white", font=groupfont, command = lambda arg = x: self.group_Button(arg)).pack(side=TOP, fill=X)

    def group_Button(self, group_index):
        info = Toplevel()
        Label(info, text = "Name: "+ str(self.groups[group_index].get_name())).pack(side=TOP, anchor = W)
        Label(info, text = "Age: "+ str(self.groups[group_index].get_age())).pack(side=TOP, anchor = W)
        Label(info, text = "Schedule: "+ str(self.groups[group_index].get_schedule())).pack(side = TOP, anchor = W)
        Button(info, text = "Set Preferences", command = lambda: self.set_preferences_dialog(group_index)).pack(side = TOP, anchor = W)

    def set_preferences_dialog(self, group_index):
        top = Toplevel()
        act_pref_vars =[]

        pref_file = open("Activity_Preferences.txt", "r")
        pref_list = eval(pref_file.read())
        pref_file.close()
        
        Button(top, text = "Change", command = lambda: self.set_preferences(group_index, act_pref_vars)).pack(side=BOTTOM)
        act_font = ('times', 10)
        for x in range(len(self.activities)):
            act_pref_vars.append(IntVar())
            if x < len(pref_list[group_index]):
                act_pref_vars[x].set(pref_list[group_index][x])
            else:
                act_pref_vars[x].set(1)
            
        act_frame_1 = Frame(top)
        act_frame_1.pack(side = LEFT)
        Label(act_frame_1, text = "").pack(side = TOP)
        for y in range(len(self.activities)/2):
            Label(act_frame_1, text = str(self.activities[y]), font = act_font).pack(side = TOP, anchor = W, pady = 2)

        like_1 = Frame(top)
        like_1.pack(side = LEFT)
        Label(like_1, text = "Like", font = act_font).pack(side = TOP)
        for z in range(len(self.activities)/2):
            Radiobutton(like_1, font = act_font, variable = act_pref_vars[z], value = 10).pack(side = TOP)

        neutral_1 = Frame(top)
        neutral_1.pack(side = LEFT)
        Label(neutral_1, text = "Neutral", font = act_font).pack(side = TOP)
        for z in range(len(self.activities)/2):
            Radiobutton(neutral_1, font = act_font, variable = act_pref_vars[z], value = 5).pack(side = TOP)

        dislike_1 = Frame(top)
        dislike_1.pack(side = LEFT)
        Label(dislike_1, text = "Dislike", font = act_font).pack(side = TOP)
        for z in range(len(self.activities)/2):
            Radiobutton(dislike_1, font = act_font, variable = act_pref_vars[z], value = 1).pack(side = TOP)

        act_frame_2 = Frame(top)
        act_frame_2.pack(side = LEFT)
        Label(act_frame_2, text = "").pack(side = TOP)
        for y in range(len(self.activities)/2, len(self.activities)):
            Label(act_frame_2, text = str(self.activities[y]), font = act_font).pack(side = TOP, anchor = W, pady = 2)

        like_2 = Frame(top)
        like_2.pack(side = LEFT)
        Label(like_2, text = "Like", font = act_font).pack(side = TOP)
        for z in range(len(self.activities)/2, len(self.activities)):
            Radiobutton(like_2, font = act_font, variable = act_pref_vars[z], value = 10).pack(side = TOP)

        neutral_2 = Frame(top)
        neutral_2.pack(side = LEFT)
        Label(neutral_2, text = "Neutral", font = act_font).pack(side = TOP)
        for z in range(len(self.activities)/2, len(self.activities)):
            Radiobutton(neutral_2, font = act_font, variable = act_pref_vars[z], value = 5).pack(side = TOP)

        dislike_2 = Frame(top)
        dislike_2.pack(side = LEFT)
        Label(dislike_2, text = "Dislike", font = act_font).pack(side = TOP)
        for z in range(len(self.activities)/2, len(self.activities)):
            Radiobutton(dislike_2, font = act_font, variable = act_pref_vars[z], value = 1).pack(side = TOP)

    def set_preferences(self, group_index, act_pref_vars):
        final_preferences = []
        for x in range(len(act_pref_vars)):
            final_preferences.append(act_pref_vars[x].get())
            
        self.groups[group_index].set_preferences(final_preferences)
        pref_file = open("Activity_Preferences.txt","r")
        pref_list = eval(pref_file.read())
        pref_file.close()
        pref_list[group_index] = final_preferences
        pref_file_2 = open("Activity_Preferences.txt", "w")
        pref_file_2.write(str(pref_list))
        pref_file_2.close()

        
    def change_activity(self, button_index, group, period):
        a_frame = Toplevel()
        possible_activities = []
        var = IntVar()
        var.set(0)

        Button(a_frame, text = "CONFIRM", command = lambda: self.change_button(button_index, period, var.get(), possible_activities)).pack(side = BOTTOM)
        mine = Label(a_frame, text = "The activity is: " + str(self.activities[var.get()]))
        mine.pack(side=BOTTOM)
        for x in self.activities:
            if none_other_groups(period,group,self.groups,x) and not (group.contains(x)):
                possible_activities.append(x)

        """
        pos_acts = Frame(a_frame)
        pos_acts.pack(side = LEFT, anchor = N)
        Label(pos_acts, text = "Legal Activities").pack(side= TOP, anchor = NW)
        for y in range(len(possible_activities)):
            r = Radiobutton(pos_acts, text= possible_activities[y], command = lambda: mine.config(text = "The activity is: "+ str(possible_activities[var.get()])),
                            variable = var, value = y)
            r.pack(side=TOP, anchor = NW)
        """
        all_acts = Frame(a_frame)
        all_acts.pack(side = LEFT)
        Label(all_acts, text = "All Activities").pack(side= TOP)
        
        col_1 = Frame(all_acts)
        col_1.pack(side = LEFT)
        for z in range(len(self.activities)/2):
            r = Radiobutton(col_1, text= self.activities[z], command = lambda: mine.config(text = "The activity is: "+str(self.activities[var.get()-len(possible_activities)])),
                            variable = var, value = z + len(possible_activities))
            r.pack(side=TOP, anchor = W)

        col_2 = Frame(all_acts)
        col_2.pack(side = LEFT)
        for a in range(len(self.activities)/2, len(self.activities)):
            r = Radiobutton(col_2, text= self.activities[a], command = lambda: mine.config(text = "The activity is: "+ str(self.activities[var.get()-len(possible_activities)])),
                            variable = var, value = a + len(possible_activities))
            r.pack(side=TOP, anchor = W)

        Button(a_frame, text = "Create Double Activity", command = lambda: self.double_activity(button_index, period, possible_activities)).pack(side = LEFT)

    def double_activity(self, button_index, period, possible_activities):
        b = Toplevel()
        act_1 = IntVar()
        act_2 = IntVar()
        
        options = Frame(b)
        options.pack(side = BOTTOM, pady = 30)
        act_label = Label(options, text = "The double period is: "+str(self.activities[act_1.get()].get_name()[0:4])+"/"+
              str(self.activities[act_2.get()].get_name()[0:4]))
        act_label.pack(side=LEFT, padx= 20)

        def config_button():
            new_act = activity(str(self.activities[act_1.get()].get_name()[0:4])+"/"+
                               str(self.activities[act_2.get()].get_name()[0:4]), 6, 15, None,[],
                               [self.activities[act_1.get()], self.activities[act_2.get()]])
            
            self.change_button(button_index, period, new_act, possible_activities)
            
        Button(options, text = "CONFIRM", command = config_button).pack(side = LEFT)            

        def config_label():
            act_label.config(text = "The double period is: "+str(self.activities[act_1.get()].get_name()[0:4])+"/"+str(self.activities[act_2.get()].get_name()[0:4]))
            
        col_1 = Frame(b)
        col_1.pack(side = LEFT)
        Label(col_1, text = "Pick one:").pack(side = TOP)
        for z in range(len(self.activities)/2):
            r = Checkbutton(col_1, text= self.activities[z], command = config_label, variable = act_1, onvalue = z)
            r.pack(side=TOP, anchor = W)

        col_2 = Frame(b)
        col_2.pack(side = LEFT)
        Label(col_2, text = "").pack(side=TOP)
        for a in range(len(self.activities)/2, len(self.activities)):
            r = Checkbutton(col_2, text= self.activities[a], command = config_label, variable = act_1, onvalue = a)
            r.pack(side=TOP, anchor = W)

        col_space = Frame(b)
        col_space.pack(side = LEFT, padx = 50)
        
        col_3 = Frame(b)
        col_3.pack(side = LEFT)
        Label(col_3, text = "Pick one:").pack(side = TOP)
        for z in range(len(self.activities)/2):
            r = Checkbutton(col_3, text= self.activities[z], command = config_label, variable = act_2, onvalue = z)
            r.pack(side=TOP, anchor = W)

        col_4 = Frame(b)
        col_4.pack(side = LEFT)
        Label(col_4, text = "").pack(side=TOP)
        for a in range(len(self.activities)/2, len(self.activities)):
            r = Checkbutton(col_4, text= self.activities[a], command = config_label, variable = act_2, onvalue = a)
            r.pack(side=TOP, anchor = W)

        
    def change_button(self, button_index, period, new_index, possible_activities):
        if type(new_index) == type(0):
            if new_index < len(possible_activities):
                self.act_buttons[period][button_index].config(text = str(possible_activities[new_index]), bg = "blue")
                self.groups[button_index].set(period, possible_activities[new_index])
                self.act_button_names[period][button_index] = possible_activities[new_index]
            else:
                act_index = new_index - len(possible_activities)
                self.act_buttons[period][button_index].config(text = str(self.activities[act_index]), bg = "blue")
                self.groups[button_index].set(period, self.activities[act_index])
                self.act_button_names[period][button_index] = self.activities[act_index]
        else:
            self.act_buttons[period][button_index].config(text = str(new_index), bg = "blue")
            self.groups[button_index].set(period, new_index)
            self.act_button_names[period][button_index] = new_index
            

root = Tk()
Schedule(root).mainloop()
