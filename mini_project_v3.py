import math

# function to read the file and convert it to a list of dictionaires of all the students. It also converts the cgpa into a float type.
def csv2dict(filename):
    with open(filename, "r") as target:
        linesasList = []
        studentInfo = []
        print("\n Reading the lines of the file... ")
        for line in target:
            linesasList.append(line) # to add all the lines of the csv file into a list
        print(" All lines have been read and stored in the variable 'linesasList' ")

        for line in linesasList[1:]:
            # for each value in the CSV file, after the headers, create a dictionary with the following categories for each line.
            tutorial_group, student_id, school, name, gender, cgpa = line.strip().split(',')

            studentInfoAsDict = {
            'Tutorial Group': int(tutorial_group.strip("G-")),
            'Student ID': student_id,
            'Name': name,
            'School': school,
            'Gender': gender,
            'CGPA': float(cgpa)
            }
            
            studentInfo.append(studentInfoAsDict)
        print(" All student data has been stored into the list 'studentInfo' ")
    return studentInfo


def merge_sort(list, key):
    if len(list) <= 1:
        return list
    mid = len(list) // 2
    left = merge_sort(list[:mid],key)
    right = merge_sort(list[mid:],key)
    return merge(left,right, key)


def merge(left, right, key):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][key] <= right[j][key]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def studentsAsTutorialGroupLists(list):
    counter = 0
    sortedInto120Lists = []
    temporaryList = []
    for i in list:
        counter += 1
        if counter % 50 == 0:
            temporaryList.append(i)
            sortedInto120Lists.append(temporaryList)
            temporaryList = []
        else:
            temporaryList.append(i)
    return sortedInto120Lists


def gpasort(list):
    sortedListByGpa = []
    print("\n Attempting to sort the tutorial groups by GPA...")
    for i in list:
        sorted_tutorialGroup = merge_sort(i, "CGPA")
        sortedListByGpa.append(sorted_tutorialGroup)
    print(" Sucessfully sorted all of the groups by GPA ")
    return sortedListByGpa


def genderRatio(teams,candidate):
    if len(teams) == 0:
        return (0,0)
    team = teams + [candidate]
    
    maleRatio = len([s for s in team if s["Gender"] == "Male"])/len(team)
    femaleRatio = len([s for s in team if s["Gender"] == "Female"])/len(team)
    return (maleRatio,femaleRatio)


def teamFormation(list):
    teamFormedLists = []

    for tutorial_group in list:
        team = []
        numberOfTeams = 0
        numberOfStudentsInTheTeam = 0
        schoolCriteriaRelaxed = False

        while tutorial_group:  # Continue until all students in the tut group are processed
            if numberOfStudentsInTheTeam % 2 == 0:  # for even index, it will try to add students from the start of the list (lowest GPA)
                satisfyCriteria = False
                for i in range(len(tutorial_group)):
                    # max 2 students from the same school & 3 students of the same gender
                    if len([s for s in team if s['School'] == tutorial_group[i]['School']]) < 2 and (genderRatio(team,tutorial_group[i])[0]<0.75 and genderRatio(team,tutorial_group[i])[1]<0.75): 
                        added_student = tutorial_group.pop(i) #add student to team and remove them from tut group list
                        team.append(added_student)
                        numberOfStudentsInTheTeam += 1
                        satisfyCriteria = True
                        break  # Stop searching once a valid student is added to team
                
                if not satisfyCriteria:
                    # Relax the criteria to allow students from the same school or of the same gender
                    if not schoolCriteriaRelaxed:
                        print(f" Tutorial Group G-{team[0]['Tutorial Group']} Team {numberOfTeams + 1} does not meet the school or gender criteria")
                        schoolCriteriaRelaxed = True
                    for i in range(len(tutorial_group)):
                        added_student = tutorial_group.pop(i)
                        team.append(added_student)
                        numberOfStudentsInTheTeam += 1
                        satisfyCriteria = True
                        break  # Stop searching once a valid student is added to team
                    
            else:  # for odd index, it will try to add students from the end of the list (highest GPA)
                satisfyCriteria = False
                for i in range(len(tutorial_group) - 1, -1, -1): #search for students in reverse order (from bottom to top)
                    # max 2 students from the same school & 3 students of the same gender 
                    if len([s for s in team if s['School'] == tutorial_group[i]['School']]) < 2 and (genderRatio(team,tutorial_group[i])[0]<0.75 and genderRatio(team,tutorial_group[i])[1]<0.75):
                        added_student = tutorial_group.pop(i)
                        team.append(added_student)
                        numberOfStudentsInTheTeam += 1
                        satisfyCriteria = True
                        break  # Stop searching once a valid student is added to team
                
                if not satisfyCriteria:
                    # Relax the criteria to allow students from the same school or of the same gender
                    if not schoolCriteriaRelaxed:
                        print(f" Tutorial Group G-{team[0]['Tutorial Group']} Team {numberOfTeams + 1} does not meet the school or gender criteria")
                        schoolCriteriaRelaxed = True
                    for i in range(len(tutorial_group) - 1, -1, -1):
                        added_student = tutorial_group.pop(i)
                        team.append(added_student)
                        numberOfStudentsInTheTeam += 1
                        satisfyCriteria = True
                        break  # Stop searching once a valid student is added to team

            if numberOfStudentsInTheTeam % 5 == 0:
                numberOfTeams += 1
                for k in team:
                    k["Team"] = numberOfTeams
                teamFormedLists.append(team)
                team = []  # Reset team for the next team allocation
                schoolCriteriaRelaxed = False # Reset for the next team

    return teamFormedLists


def score(team_list):
    score_list = []
    for team in team_list:
        maleRatio = len([s for s in team if s["Gender"] == "Male"])/len(team)
        femaleRatio = len([s for s in team if s["Gender"] == "Female"])/len(team)
        average_gpa = sum([student["CGPA"] for student in team])/len(team)
        std_gpa = math.sqrt(sum([(student["CGPA"]-average_gpa)**2 for student in team])/sum([student["CGPA"] for student in team]))
        name_dict = {}
        for i in team:
            if i["School"] in name_dict:
                name_dict[i["School"]]+=1
            else:
                name_dict[i["School"]] = 1
        school_count = len(name_dict)
        score = (0.5-maleRatio)**2+(0.5-femaleRatio)**2+std_gpa+(5-school_count)
        score_list.append(score)
    
    return score_list


def main():
    studentsInfoAsDictionaries = csv2dict("records.csv")
    
    print("\n Attempting merge-sorting on the student data stored in the list... ")
    sortedStudentInfoAsDictionaries = merge_sort(studentsInfoAsDictionaries, "Tutorial Group")
    print(" Sorting sucessful! ")
    
    print("\n Attempting to save sorted data into CSV file 'sortedRecords'... ")
    with open("sortedRecords.csv", "w+") as target:
        for i in sortedStudentInfoAsDictionaries:
            print(i, file=target)
    print(" Stored sucessfully! ")
    
    print("\n Attempting to sort the values into 120 lists with each tutorial group...")
    sortedTutorialGroups = studentsAsTutorialGroupLists(sortedStudentInfoAsDictionaries)
    print(" Sucessfully seperated them into their assigned tutorial groups ")
    gpasortedTutorialGroups = gpasort(sortedTutorialGroups)
    
    print("\n Attempting to allocate students into teams of 5 in each tutorial group based on GPA, gender and school criteria...")
    x = teamFormation(gpasortedTutorialGroups)
    print(" All students have been placed into teams!")
    
    a = score(x)
    print(" Total Score:", sum(a))
    
    print("\n Attempting to save allocated teams data into CSV file 'sortedteamRecords'...")
    # saves the new formed teams into sortedteamRecords.csv and creates a new column "Team Number"
    with open("sortedteamsRecords.csv", "w+") as target:
        target.write("Tutorial Group,Student ID,School,Name,Gender,CGPA,Team Assigned\n")
        for group in x:
            for student in group:
                line = f"G-{student['Tutorial Group']},{student['Student ID']},{student['School']},{student['Name']},{student['Gender']},{student['CGPA']},Team {student['Team']}\n"
                target.write(line)
    print(" Stored sucessfully! \n")





main()