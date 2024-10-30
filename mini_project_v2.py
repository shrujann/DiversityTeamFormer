# function to read the file and convert it to a list of dictionaires of all the students. It also converts the cgpa into a float type.
def csv2dict(filename):
    with open(filename, "r") as target:
        linesasList = []
        studentInfo = []
        print(" Reading the lines of the file... ")
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


#removed the codes in gpasort and studentsAsTutorialGroupLists function and combined them into this
def studentsAsTutorialGroupListsSortedByGpa(list):
    sortedInto120Lists = [sorted(list[i:i+50], key=lambda x: x['CGPA']) for i in range(0, len(list), 50)]
    return sortedInto120Lists


#problem now is that for some tutorial groups, it has a team (team 10) that have more than 2 students from the same school (G-18,G30,G-31,G-59,G-61)
def teamFormation(list):
    teamFormedLists = []

    for tutorial_group in list:
        team = []
        numberOfTeams = 0
        numberOfStudentsInTheTeam = 0
        schoolCriteriaRelaxed = False

        while tutorial_group:  # Continue until all students in the tut group are processed
            if numberOfStudentsInTheTeam % 2 == 0:  # for even index, it will try to add students from the start of the list (lowest GPA)
                satisfySchoolCriteria = False
                for i in range(len(tutorial_group)):
                    if len([s for s in team if s['School'] == tutorial_group[i]['School']]) < 2: # max 2 students from the same school
                        added_student = tutorial_group.pop(i) #add student to team and remove them from tut group list
                        team.append(added_student)
                        numberOfStudentsInTheTeam += 1
                        satisfySchoolCriteria = True
                        break  # Stop searching once a valid student is added to team
                
                if not satisfySchoolCriteria:
                    # Relax the criteria to allow students from the same school
                    if not schoolCriteriaRelaxed:
                        school = tutorial_group[i]['School']  # Store the school of the last attempted student
                        print(f" Tutorial Group G-{team[0]['Tutorial Group']} Team Number {numberOfTeams + 1} has more than 2 students from the same school: {school}")
                        schoolCriteriaRelaxed = True
                    for i in range(len(tutorial_group)):
                        added_student = tutorial_group.pop(i)
                        team.append(added_student)
                        numberOfStudentsInTheTeam += 1
                        satisfySchoolCriteria = True
                        break  # Stop searching once a valid student is added to team
                    
            else:  # for odd index, it will try to add students from the end of the list (highest GPA)
                satisfySchoolCriteria = False
                for i in range(len(tutorial_group) - 1, -1, -1): #search for students in reverse order (from bottom to top)
                    if len([s for s in team if s['School'] == tutorial_group[i]['School']]) < 2:
                        added_student = tutorial_group.pop(i)
                        team.append(added_student)
                        numberOfStudentsInTheTeam += 1
                        satisfySchoolCriteria = True
                        break  # Stop searching once a valid student is added to team
                
                if not satisfySchoolCriteria:
                    # Relax the criteria to allow students from the same school
                    if not schoolCriteriaRelaxed:
                        school = tutorial_group[i]['School']  # Store the school of the last attempted student
                        print(f" Tutorial Group G-{team[0]['Tutorial Group']} Team Number {numberOfTeams + 1} has more than 2 students from the same school: {school}")
                        schoolCriteriaRelaxed = True
                    for i in range(len(tutorial_group) - 1, -1, -1):
                        added_student = tutorial_group.pop(i)
                        team.append(added_student)
                        numberOfStudentsInTheTeam += 1
                        satisfySchoolCriteria = True
                        break  # Stop searching once a valid student is added to team

            if numberOfStudentsInTheTeam % 5 == 0:
                numberOfTeams += 1
                for k in team:
                    k["Team"] = numberOfTeams
                teamFormedLists.append(team)
                team = []  # Reset team for the next team allocation

    print(" All the teams have been formed")
    return teamFormedLists



def main():
    studentsInfoAsDictionaries = csv2dict("records.csv")
    print(" Program will now attempt to use merge-sorting on the student data stored in the list ")
    sortedStudentInfoAsDictionaries = merge_sort(studentsInfoAsDictionaries, "Tutorial Group")
    print(" Merge-sorting sucessful! ")
    print(" Attempting to save merge-sorted CSV results into file 'sortedRecords' ")

    with open("sortedRecords.csv", "w+") as target:
        for i in sortedStudentInfoAsDictionaries:
            print(i, file=target)

    print(" Stored sucessfully! ")
    print(" Attempting to sort the values into 120 lists with each tutorial group ")
    sortedTutorialGroups = studentsAsTutorialGroupListsSortedByGpa(sortedStudentInfoAsDictionaries)
    print(" Sucessfully seperated them into their assigned tutorial groups and sorted each tutorial group based on GPA")
    x = teamFormation(sortedTutorialGroups)
    print(" Attempting to save new formed teams into CSV file 'sortedteamRecords'")
    
    # saves the new formed teams into sortedteamRecords.csv and creates a new column "Team Number"
    with open("sortedteamsRecords.csv", "w+") as target:
        target.write("Tutorial Group,Team Number,Student ID,School,Name,Gender,CGPA\n")
        for group in x:
            for student in group:
                line = f"G-{student['Tutorial Group']},team {student['Team']},{student['Student ID']},{student['School']},{student['Name']},{student['Gender']},{student['CGPA']}\n"
                target.write(line)

    print(" Stored sucessfully! ")




main()