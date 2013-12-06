import random
from array import array

def add_Chef(groups, activities, max_had):
    for period in range(6,9):
        group = get_group(groups, activities, activities[22], 11, 19, max_had[22])
        while not count_instances(groups[group], activities[22]) == 0:
            group = get_group(groups, activities, activities[22], 11, 19, max_had[22])
        groups[group].get_schedule()[period] = activities[22]

def add_Crafts(groups, activities, max_had):
    for period in range(12):
        group = get_group(groups, activities, activities[23], 0, 19, max_had[23])
        while not count_instances(groups[group], activities[23]) == 0:
            group = get_group(groups, activities, activities[23], 11, 19, max_had[23])
        if not groups[group].get_schedule()[period] == activities[8] and not groups[group].get_schedule()[period] == activities[10]:
            groups[group].get_schedule()[period] = activities[23]
        
def add_mandatory_sports(groups, activities, max_had):
    counter_range = 100
    #For Bad/Ping
    for x in range(len(groups)-1):
        period = random.randrange(12)
        counter = 0
        group = random.randrange(2,len(groups))
        while (activities[2] in groups[group].get_schedule() or activities[3] in groups[group].get_schedule()) and counter <= counter_range:
            group = random.randrange(2,len(groups))
            counter = counter + 1
        counter = 0
        while not (none_other_groups(period, groups[group], groups, activities[2])) and counter <= counter_range:
            period = random.randrange(12)
            counter = counter + 1
        if counter <=counter_range and count_instances(groups[group], activities[2]) == 0 and count_instances(groups[group], activities[3]) == 0 and groups[group].get_schedule()[period] == activities[0]:
            groups[group].get_schedule()[period] = activities[2]

    #For Ping/Bad
    for x in range(len(groups)-1):
        period = random.randrange(12)
        counter = 0
        group = random.randrange(len(groups))
        while (activities[3] in groups[group].get_schedule() or activities[2] in groups[group].get_schedule()) and counter <= counter_range:
            group = random.randrange(len(groups))
            counter = counter + 1
        counter = 0
        while not (none_other_groups(period, groups[group], groups, activities[3])) and counter <= counter_range:
            period = random.randrange(12)
            counter = counter + 1
        if counter <=counter_range and count_instances(groups[group], activities[3]) == 0 and count_instances(groups[group], activities[2]) == 0 and groups[group].get_schedule()[period] == activities[0]:
            groups[group].get_schedule()[period] = activities[3]
    
    #For Archery
    add_activities(groups, activities, activities[1], max_had)
    #For Tennis
    add_activities(groups, activities, activities[4], max_had)
    #For Golf
    add_activities(groups, activities, activities[5], max_had)
    #For Horseshoes
    add_activities(groups, activities, activities[6], max_had)

            
def add_Nature_Engineering(groups, activities, max_had):
    counter_range = 100
    #For Nature
    add_activities(groups, activities, activities[12], max_had)
    #For Engineering
    add_activities(groups, activities, activities[13], max_had)

def add_Swimming(groups, activities, max_had):
    counter_range = 100
    #the nits will have swimming every day during second period
    for period in range(4):
        groups[0].get_schedule()[(period*3)+1] = activities[10]
        groups[1].get_schedule()[(period*3)+1] = activities[10]

    groups[18].get_schedule()[8] = activities[11]
    groups[19].get_schedule()[8] = activities[11]

    for period in range(12):
        counter_range = 30
        counter = 0
        if not (period%3 == 1 or period == 8):
            while search_period(groups, period, activities[10]) < 3 and counter<counter_range:
                group = get_swim_group(groups, activities, period)
                group.get_schedule()[period] = activities[10]
                counter = counter + 1
            counter = 0
            while search_period(groups, period, activities[11]) < 2 and counter<counter_range:
                group = get_swim_group(groups, activities, period)
                group.get_schedule()[period] = activities[11]
                counter = counter + 1

def get_swim_group(groups, activities, period):
    pos_groups = []
    for group in groups:
        if group.get_age() <= 10:
            if (count_instances(group, activities[10]) + count_instances(group, activities[11]) < 3 and
                good_period_swim(group, period, activities)):
                pos_groups.append(group)
        elif group.get_age()>10:
            if (count_instances(group, activities[10]) + count_instances(group, activities[11]) < 2 and
                good_period_swim(group, period, activities)):
                pos_groups.append(group)

    ret_group = pos_groups[random.randrange(len(pos_groups))]

    return ret_group

def good_period_swim(group, period, activities):
    good = False
    if period%3 == 2 and not period == 8 and not group.get_schedule()[period] == activities[8]: #third period
        if (not (group.get_schedule()[period-1] == activities[10]) and
                not (group.get_schedule()[period-2] == activities[10]) and
                not (group.get_schedule()[period-1] == activities[11]) and
                not (group.get_schedule()[period-2] == activities[11])):
            
           good = True
    elif not (period == 8) and period%3 == 0 and not group.get_schedule()[period] == activities[8]: #period%3 == 0: first period
        if (not (group.get_schedule()[period+1] == activities[10]) and
                not (group.get_schedule()[period+2] == activities[10]) and
                not (group.get_schedule()[period+2] == activities[11]) and
                not (group.get_schedule()[period+1] == activities[11])):

            good = True

    return good

def add_Sailing(groups, activities, max_had):
    counter_range = 100
    #for Sailing
    for x in range(len(groups)):
        #need just periods 1, 4, 7, 10
        period = (random.randrange(4)*3) + 1
        counter = 0
        group = get_group(groups, activities, activities[8], 10, 19, max_had[8])
        while activities[8] in groups[group].get_schedule() and counter <= counter_range:
            group = get_group(groups, activities, activities[8], 10, 19, max_had[8])
            counter = counter + 1
        counter = 0
        while not ((none_other_groups(period, groups[group], groups, activities[8])) and (none_other_groups(period+1, groups[group], groups, activities[8]))) and counter <= counter_range:
            period = (random.randrange(4)*3) + 1
            counter = counter + 1
        if counter <=counter_range and count_instances(groups[group], activities[8]) == 0 and groups[group].get_schedule()[period] == activities[0] and groups[group].get_schedule()[period+1] == activities[0]:
            groups[group].get_schedule()[period] = activities[8]
            groups[group].get_schedule()[period+1] = activities[8]

def add_other_waterfront(groups, activities, max_had):
    counter_range = 100
    #For Kayaking
    add_activity_doubles(groups, activities, activities[9], max_had)
    #For Boating
    add_activity_doubles(groups, activities, activities[7], max_had)
            
def create_groups():
    group_list = []
    group_list.append(group("Nit Boys                ", 6, None,[]))#0
    group_list.append(group("Nit Girls               ", 6, None,[]))#1
    group_list.append(group("Novice Green Boys       ", 7, None,[]))#2
    group_list.append(group("Novice Green Girls      ", 7, None,[]))#3
    group_list.append(group("Novice White Boys       ", 8, None,[]))#4
    group_list.append(group("Novice White Girls      ", 8, None,[]))#5
    group_list.append(group("Midget Green Boys       ", 9, None,[]))#6
    group_list.append(group("Midget Green Girls      ", 9, None,[]))#7
    group_list.append(group("Midget White Boys       ", 10, None,[]))#8
    group_list.append(group("Midget White Girls      ", 10, None,[]))#9
    group_list.append(group("Junior Green Boys       ", 11, None,[]))#10
    group_list.append(group("Junior Green Girls      ", 11, None,[]))#11
    group_list.append(group("Junior White Boys       ", 12, None,[]))#12
    group_list.append(group("Junior White Girls      ", 12, None,[]))#13
    group_list.append(group("Intermediate Green Boys ", 13, None,[]))#14
    group_list.append(group("Intermediate Green Girls", 13, None,[]))#15
    group_list.append(group("Intermediate White Boys ", 14, None,[]))#16
    group_list.append(group("Intermediate White Girls", 14, None,[]))#17
    group_list.append(group("Senior Boys             ", 15, None,[]))#18
    group_list.append(group("Senior Girls            ", 15, None, []))#19

    return group_list

def create_activities():
    activities_list = []
    #this is a none activity, so I can populate the original schedule with a basically empty
    #two dimmensional array, must be the first activity in the list, so that I can add
    #and delete activities to the list, without modiying the index of the none activity.
    #I had to hardcode in the location of the none object, which is why I do not want
    #its index to change.
    activities_list.append(activity("None    ", 6, 15, None, []))#0
    #these are the mandatory activities for each week
    activities_list.append(activity("Archery ", 11, 15, None, []))#1
    activities_list.append(activity("Bad/Ping", 7, 15, None, []))#2
    activities_list.append(activity("Ping/Bad", 7, 15, None, []))#3
    activities_list.append(activity("Tennis  ", 6, 15, None, [6]))#4
    activities_list.append(activity("Golf    ", 9, 14, None, [0]))#5
    activities_list.append(activity("Shoes   ", 6, 10, None, []))#6
    #these are the waterfront activities that use the same couselors
    activities_list.append(activity("Boating ", 6, 15, None, []))#7
    activities_list.append(activity("Sailing ", 11, 15, None, []))#8
    activities_list.append(activity("Kayak   ", 9, 15, None, []))#9
    #these are the two swimming activities that people can have multiple times a week
    activities_list.append(activity("Swim P  ", 6, 15, None, []))#10
    activities_list.append(activity("Swim MP ", 6, 15, None, []))#11
    #both should have a group every period
    activities_list.append(activity("Nature  ", 6, 15, None, [0]))#12
    activities_list.append(activity("Engr    ", 6, 15, None, []))#13
    #these both use the baseball field
    activities_list.append(activity("Softball", 11, 15, None, []))#14
    activities_list.append(activity("Kickball", 6, 11, None, []))#15
    #these both use the basketball courts
    activities_list.append(activity("B-ball  ", 11, 15, None, []))#16
    activities_list.append(activity("STH     ", 6, 15, None, []))#17
    #these both use the soccer field
    activities_list.append(activity("Soccer  ", 6, 15, None, []))#18
    activities_list.append(activity("Lax     ", 11, 15, None, []))#19
    #these are very similar
    activities_list.append(activity("BP-Play ", 6, 15, None, []))#20
    activities_list.append(activity("MP-Play ", 6, 15, None, []))#21
    #the rest can be used to fill out the schedule
    activities_list.append(activity("Chef    ", 11, 15, None, [0,1,2,3,4,5,9,10,11]))#22
    activities_list.append(activity("Crafts  ", 6, 15, None, []))#23
    activities_list.append(activity("GB      ", 6, 8, None, [2,5,8,11]))#24
    activities_list.append(activity("Bowling ", 6, 15, None, [0]))#25
    activities_list.append(activity("F golf  ", 6, 15, None, []))#26
    activities_list.append(activity("M-Arts  ", 6, 15, None, []))#27
    activities_list.append(activity("V-ball  ", 6, 15, None, []))#28
    activities_list.append(activity("Music   ", 6, 15, None, []))#29
    activities_list.append(activity("CTF     ", 6, 15, None, []))#30
    activities_list.append(activity("Play    ", 6, 11, None, []))#31
    activities_list.append(activity("Bocci   ", 6, 11, None, []))#32
    activities_list.append(activity("S-Hunt  ", 6, 15, None, []))#33

    
    return activities_list

class activity:
    def __init__(self, name, min_age, max_age, competing_activity, not_days, other_act = None):
        self.name = name
        self.min_age = min_age
        self.max_age = max_age
        self.competing_activity = competing_activity
        self.not_days = not_days
        self.other_act = other_act 
        
    def __repr__(self):
        return str(self.name)

    def get_max_age(self):
        return self.max_age

    def get_name(self):
        return self.name
    
    def __eq__(self,other):
        return self.name == other.name
    
    def get_min_age(self):
        return self.min_age

    def get_competing_activity(self):
        return self.competing_activity

    #creates a recipricol relationship, so only have to add it for one activity and it will be added for both
    #activities. This should save code.
    def add_competing_activity(self, activity):
        self.competing_activity = activity
        activity.competing_activity = self


class group:
    def __init__(self, name, age, schedule, preferences):
        self.name = name
        self.age = age
        self.schedule = schedule
        self.preferences = preferences
        
    def __repr__(self):
        return str(self.name) + "    " + str(self.schedule)

    def __call__(self, name, age, schedule):
        return self.get_schedule()
    
    def __eq__(self, other):
        return self.name == other.name

    def contains(self, activity):
        for act in range(len(self.schedule)):
            if type(self.schedule[act].other_act) == type(None):
                if activity == self.schedule[act]:
                    return True
            else:
                if activity in self.schedule[act].other_act:
                    return True
        return False
    
    def add_schedule(self, input_list):
        self.schedule = input_list

    def get_schedule(self):
        return self.schedule

    def set(self, period, activity):
        self.schedule[period] = activity

    def get_age(self):
        return self.age

    def get_name(self):
        return self.name

    def get_preference(self, act_index):
        return self.preferences[act_index]

    def get_list_preferences(self):
        return self.preferences

    def set_preferences(self, preference_list):
        self.preferences = preference_list
    
def create_master_schedule(group_list, activities_list):
    all_groups = group_list
    all_activities = activities_list
    final_schedule = []
    max_had = find_max_had(group_list, activities_list)
    pref_file = open("Activity_Preferences.txt", "r")
    pref_string = pref_file.read()
    pref_list = eval(pref_string)
    pref_file.close()
    
    no = all_activities[0]
    for group in all_groups:
        group.add_schedule([no, no, no, no, no, no, no, no, no, no, no, no])

    for group in range(len(all_groups)):
        group_list[group].set_preferences(pref_list[group])
        
    #set the double activities
    set_doubles(all_groups, all_activities)

    #start adding the rest of the activities
    add_Chef(all_groups, all_activities, max_had)
    add_Sailing(all_groups, all_activities, max_had)
    add_mandatory_sports(all_groups, all_activities, max_had)
    add_Nature_Engineering(all_groups, all_activities, max_had)
    add_Swimming(all_groups, all_activities, max_had)
    add_Crafts(all_groups, all_activities, max_had)
    add_other_waterfront(all_groups, all_activities, max_had)
    add_doubles(all_groups, all_activities, max_had)
    add_rest(all_groups, all_activities, max_had)
    set_half_activities(all_groups, all_activities, max_had)
    check_mandatory_every_period(all_groups, all_activities)

def create_partial_schedule(group_list, activities_list):
    all_groups = group_list
    all_activities = activities_list
    final_schedule = []
    max_had = find_max_had(group_list, activities_list)
    pref_file = open("Activity_Preferences.txt", "r")
    pref_string = pref_file.read()
    pref_list = eval(pref_string)
    pref_file.close()
    
    no = all_activities[0]
    for group in all_groups:
        group.add_schedule([no, no, no, no, no, no, no, no, no, no, no, no])

    for group in range(len(all_groups)):
        group_list[group].set_preferences(pref_list[group])
        
    #set the double activities
    set_doubles(all_groups, all_activities)

    #start adding the rest of the activities
    add_Chef(all_groups, all_activities, max_had)
    add_Sailing(all_groups, all_activities, max_had)
    add_mandatory_sports(all_groups, all_activities, max_had)
    add_Nature_Engineering(all_groups, all_activities, max_had)
    add_Swimming(all_groups, all_activities, max_had)
    add_Crafts(all_groups, all_activities, max_had)
    add_other_waterfront(all_groups, all_activities, max_had)
    add_doubles(all_groups, all_activities, max_had)
    check_mandatory_every_period(all_groups, all_activities)

def check_mandatory_every_period(groups, activities):
    man_every = [1, 4,5, 12,13,23,27]
    fillers = [25,26,28,30,31,32,33]
    for period in range(12):
        for x in man_every:
            if search_period(groups, period, activities[x]) == 0:
                for group in groups:
                    if group.get_schedule()[period] in activities and not period in activities[x].not_days:
                        if (activities.index(group.get_schedule()[period]) in fillers and
                                group.get_age()<= activities[x].get_max_age() and
                                group.get_age() >= activities[x].get_min_age() and
                                not group.contains(activities[x]) and
                                search_period(groups, period, activities[x]) == 0):
                            print group.get_name(), activities[x], period
                            group.get_schedule()[period] = activities[x]
                    

def set_half_activities(groups, activities, max_had):
    always_half = [24,26,29,30,32]
    pos_half = [15, 16, 17, 25, 27, 28]
    group_pos = []
          
    for period in range(12):
        for group in groups[:-2]:
            if group.get_schedule()[period] in activities:
                if activities.index(group.get_schedule()[period]) in always_half:
                    all_pos = always_half + pos_half
                    all_pos.remove(activities.index(group.get_schedule()[period]))
                    tochange2 = []
                    
                    for x in range(len(all_pos)):
                        if (not (all_pos[x] == activities.index(group.get_schedule()[period])) and
                                count_instances(group, activities[all_pos[x]]) == 0 and
                                activities[all_pos[x]].get_max_age()>=group.get_age()):
                            
                            for other_group in groups[:-2]:
                                if (other_group.get_schedule()[period] in activities and not(other_group == group) and
                                        group.get_schedule()[period].get_max_age() >= other_group.get_age() and
                                        count_instances(other_group, group.get_schedule()[period]) == 0 and
                                        count_instances(group, activities[all_pos[x]]) == 0):
                                    
                                    if activities.index(other_group.get_schedule()[period]) in all_pos:
                                            tochange2.append([all_pos[x],other_group])
                
                    if len(tochange2)>0:
                        info = random.randrange(len(tochange2))
                        other_group = tochange2[info][1]
                        
                        old_act_1 = group.get_schedule()[period]
                        old_act_2 = other_group.get_schedule()[period]
                        
                        if count_instances(other_group, old_act_1) == 0 and count_instances(group, old_act_2) == 0:
                            new_act_1 = activity(old_act_1.get_name()[0:4]+"/"+old_act_2.get_name()[0:4],6,15,None,[],
                                                 [old_act_1, old_act_2])
                            new_act_2 = activity(old_act_2.get_name()[0:4]+"/"+old_act_1.get_name()[0:4],6,15,None,[],
                                                 [old_act_2, old_act_1])
                            group.get_schedule()[period] = new_act_1
                            other_group.get_schedule()[period] = new_act_2
                            
def add_doubles(groups, activities, max_had):
    add_activity_doubles(groups, activities, activities[14],max_had)
    add_activity_doubles(groups, activities, activities[15],max_had)
    add_activity_doubles(groups, activities, activities[16],max_had)
    add_activity_doubles(groups, activities, activities[17],max_had)
    add_activity_doubles(groups, activities, activities[18],max_had)
    add_activity_doubles(groups, activities, activities[19],max_had)
    add_activity_doubles(groups, activities, activities[20],max_had)
    add_activity_doubles(groups, activities, activities[21],max_had)
    
def set_doubles(groups, activities):
    #Boating and kayaking
    activities[7].add_competing_activity(activities[9])
    #Kickball and softball
    activities[14].add_competing_activity(activities[15])
    #Basketball and STH
    activities[16].add_competing_activity(activities[17])
    #Lacrosse and Soccer
    activities[18].add_competing_activity(activities[19])
    #BP play and MP play, simply because they are very similar activities
    activities[20].add_competing_activity(activities[21])
    #Bad/Ping and Ping/Bad
    activities[2].add_competing_activity(activities[3])

def add_activity_doubles(groups, activities, activity, max_had):
    counter_range = 100
    #For activities that have another activity they can't be done with
    other_activity = activity.get_competing_activity()

    max_age = activity.get_max_age()
    min_age = activity.get_min_age()
    group_min = 0
    group_max = 20
    youngest = True

    for group in groups:
        if group.get_age() >= min_age and youngest:
            group_min = groups.index(group)
            youngest = False
        if group.get_age() <=max_age:
            group_max = groups.index(group)

    for x in range(len(groups)):
        period = get_period(groups, activities, activity)
        counter = 0
        group = get_group(groups, activities, activity, group_min, group_max, max_had[activities.index(activity)])
        #group = random.randrange(group_min, group_max)
        while not ((none_other_groups(period, groups[group], groups, activity)) and (none_other_groups(period, groups[group], groups, other_activity))) and counter <= counter_range:
            group = get_group(groups, activities, activity, group_min, group_max, max_had[activities.index(activity)])
            counter = counter + 1
        counter = 0
        while not (none_other_groups(period, groups[group], groups, activity) and none_other_groups(period, groups[group], groups, other_activity)) and counter <= counter_range:
            period = get_period(groups, activities, activity)
            counter = counter + 1
        if counter <=counter_range and count_instances(groups[group], activity) == 0 and count_instances(groups[group], other_activity) == 0 and groups[group].get_schedule()[period] == activities[0]:
            groups[group].get_schedule()[period] = activity
    
def add_activities(groups, activities, activity, max_had):
     counter_range = 100
     #For all activiites that don't have a special requirement for period scheduling
     #i.e. sailing, swimming, or any of the ones that require the same field
     max_age = activity.get_max_age()
     min_age = activity.get_min_age()
     group_min = 0
     group_max = 20
     youngest = True
     for group in groups:
         if group.get_age() >= min_age and youngest:
             group_min = groups.index(group)
             youngest = False
         if group.get_age() <=max_age:
             group_max = groups.index(group)
     
     for x in range(len(groups)):
        period = get_period(groups, activities, activity)
        counter = 0
        group = get_group(groups, activities, activity, group_min, group_max, max_had[activities.index(activity)])
        while (activity in groups[group].get_schedule()) and counter <= counter_range:
            group = get_group(groups, activities, activity, group_min, group_max, max_had[activities.index(activity)])
            counter = counter + 1
        counter = 0
        while not none_other_groups(period, groups[group], groups, activity) and counter <= counter_range:
            period = get_period(groups, activities, activity)
            counter = counter + 1
        if counter <=counter_range and count_instances(groups[group], activity) == 0 and groups[group].get_schedule()[period] == activities[0]:
            groups[group].get_schedule()[period] = activity

            
def add_rest(groups, activities, max_had):
    counter_range = 100
    for group in groups:
        for i in range(12):
            if group.get_schedule()[i] == activities[0]:
                activity = get_activity(groups, activities, group, i, max_had[24:])
                counter = 0
                while not ((none_other_groups(i, group, groups, activity)) and count_instances(group, activity) == 0 and not i in activity.not_days) and counter <= counter_range:
                    activity = get_activity(groups, activities, group, i, max_had[24:])
                    counter = counter + 1
                if count_instances(group, activity) == 0:
                    group.get_schedule()[i] = activity

#this is to be used with the add_rest function, so that given a period and a group, it selects the best
#activity to even out the equalization matrix, and based on preferences. Needs to be as efficient as
#possible though, since the program has already slowed down considerably
def get_activity(groups, activities, group, period, max_had):
    choosing_bag = []
    group_index = groups.index(group)
    
    mat_file = open("Equalization Matrix.txt", "r")
    mat_list = eval(mat_file.read())
    mat_file.close()
        
    for act_index in range(len(activities[24:])):
        #this part adds the activity to the choosing bag 10 times, if the activity does not have its preferences
        #set. This will usually occur when you add an activity to the activities list, while the program is running
        if act_index+24 >=len(groups[group_index].get_list_preferences()):
            choosing_bag = choosing_bag+([act_index]*10)
        else:
            #if the activity does have a preference set to it by the user, than it will add the activity on either
            #once for a dislike, 5 times for a neutral, or ten times for a like
            choosing_bag = choosing_bag+([act_index]*groups[group_index].get_preference(act_index+24))
        #this part adds in the activity to the choosing bag, based on how many less times the group
        #has had the particular activiy. Takes into account the equalization matrix here.
        if len(mat_list[group_index])>act_index+24:
            if mat_list[group_index][act_index+24] < max_had[act_index][0]:
                choosing_bag = choosing_bag+([act_index]*(max_had[act_index][0] - mat_list[group_index][act_index+24])*5)
        else:
            choosing_bag = choosing_bag + ([act_index]*5)


    my_act = random.randrange(len(choosing_bag))
    counter = 0
    while not(activities[choosing_bag[my_act]+24].get_min_age()<= group.get_age() and activities[choosing_bag[my_act]+24].get_max_age() >= group.get_age()) and counter<=40:
        my_act = random.randrange(len(choosing_bag))
        counter = counter+1
    return activities[choosing_bag[my_act]+24]

#takes the parameter not_days from the activities class and checks if its empty
#if it isn't empty then it selects a random period and tests it against the not days
#it continues to check it against not_days until it finds a good period and then returns it
def get_period(groups, activities, activity):
    if activity.not_days == []:
        return random.randrange(12)
    else:
        period = random.randrange(12)
        while period in activity.not_days:
            period = random.randrange(12)
        return period

#picks a group based on their preferences
#uses a weighted, random pick approach, where a group is given a higher possibility of
#reiceing the activity, if they have it set as one of their preferences.
def get_group(groups, activities, activity, group_min, group_max, max_had):
    choosing_bag = []

    mat_file = open("Equalization Matrix.txt", "r")
    mat_list = eval(mat_file.read())
    mat_file.close()
    
    act_index = activities.index(activity)

    for group in range(group_min, group_max+1):
        #if not(mat_list[group][act_index] == max_had[0] or max_had[0]-max_had[1] >=2):
        choosing_bag = choosing_bag + [group]*groups[group].get_preference(act_index)
        if mat_list[group][act_index] < max_had[0]:
            choosing_bag = choosing_bag+ [group]*((max_had[0]-mat_list[group][act_index])*5)
            
    return_group = choosing_bag[random.randrange(len(choosing_bag))]
    return return_group
        
def count_instances(group, activity):
    count = 0
    for i in range(12):
        if group.get_schedule()[i] == activity:
            count = count + 1
        if type(group.get_schedule()[i].other_act) == type([]):
            if activity in group.get_schedule()[i].other_act:
                count = count + 1
                
    return count
    
def none_other_groups(period, my_group, other_groups, activity):
    for group in other_groups:
        if type(group.get_schedule()[period].other_act) == type(None):
            if group.get_schedule()[period] == activity and not group == my_group:
                return False
        else:
            if activity in group.get_schedule()[period].other_act:
                return False
    return True

#this part searches through the different groups to find the most times a single group has had each activity
#and stores that at the same index as the activity - 23 in the list max_had.

def find_max_had(groups, activities):
    mat_file = open("Equalization Matrix.txt", "r")
    mat_list = eval(mat_file.read())
    mat_file.close()
    
    max_had = []
    for x in range(len(activities)):
        max_had.append([0,0])
    
    for check_index in range(len(activities)):
        for group1 in range(len(groups)):
            if check_index<len(mat_list):
                if max_had[check_index][0] < mat_list[group1][check_index]:
                    max_had[check_index][0] = mat_list[group1][check_index]
            else:
                max_had[check_index][0] = 3
                
    for check_min in range(len(activities)):
        for group2 in range(len(groups)):
            if check_min<len(mat_list):
                if max_had[check_min][1] > mat_list[group2][check_min]:
                    max_had[check_min][1] = mat_list[group2][check_min]
            else:
                max_had[check_min][1] = 2
                
    return max_had

                
#recursively searches for a new activity that is within the groups age range
def new_activity(cur_act, old_act, group, activities):
    if group.get_age()<=activities[cur_act].get_max_age() and group.get_age()>= activities[cur_act].get_min_age() and old_act != cur_act:
        return activities[cur_act]
    else:
        new_act = random.randrange(0,len(activities))
        return new_activity(new_act, cur_act, group, activities)

def search_period(groups, period, activity):
    count = 0
    for group in groups:
        if type(group.get_schedule()[period].other_act) == type(None):
            if group.get_schedule()[period] == activity:
                count = count + 1
        else:
            if activity in group.get_schedule()[period].other_act:
                count = count + 1
    return count
    
#this method is to simply allow me to test my schedule and prove its correctness
def search_duplicates_period(groups, period, activities):
    #this method should search for duplicates within one column of the schedule
    count = 0
    name = ""
    for j in range(len(groups)):
        for i in range(len(groups)):
            #so that it doesn't register that Swim P and Swim MP since more than 1 group can have it in a period
            if not (groups[j].get_schedule()[period] == activities[10] or groups[j].get_schedule()[period] == activities[11]):
                if groups[j].get_schedule()[period] == groups[i].get_schedule()[period] and j != i:
                    count = count + 1
                elif (type(groups[j].get_schedule()[period].other_act) == type([]) and
                        type(groups[i].get_schedule()[period].other_act) == type([]) and j !=i):
                    if (groups[j].get_schedule()[period].other_act[0] == groups[i].get_schedule()[period].other_act[0] or
                            groups[j].get_schedule()[period].other_act[1] == groups[i].get_schedule()[period].other_act[1]):
                        count = count + 1
                elif (type(groups[j].get_schedule()[period].other_act) == type([]) and not
                        type(groups[i].get_schedule()[period].other_act) == type([]) and j !=i):
                    if groups[i].get_schedule()[period] in groups[j].get_schedule()[period].other_act:
                        count = count + 1
                elif (type(groups[i].get_schedule()[period].other_act) == type([]) and not
                        type(groups[j].get_schedule()[period].other_act) == type([]) and j !=i):
                    if groups[j].get_schedule()[period] in groups[i].get_schedule()[period].other_act:
                        count = count + 1

    return count



"""
groups = create_groups()
activities = create_activities()
create_master_schedule(groups, activities)

#for i in range(12):
#    print "For period " + str(i+1) + " there are: " + str(search_duplicates_period(groups, i, activities)) + " duplicates."

for group in groups:
    print group

"""
