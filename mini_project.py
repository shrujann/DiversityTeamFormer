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
            tutorial_group, student_id, name, school, gender, cgpa = line.strip().split(',')

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

studentsInfoAsDictionaries = csv2dict("records.csv")

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

print(" Program will now attempt to use merge-sorting on the student data stored in the list ")
sortedStudentInfoAsDictionaries = merge_sort(studentsInfoAsDictionaries, "Tutorial Group")
print(" Merge-sorting sucessful! ")

print(" Attempting to save merge-sorted CSV results into file 'sortedRecords' ")

with open("sortedRecords.csv", "w+") as target:
    for i in sortedStudentInfoAsDictionaries:
        print(i, file=target)

print(" Stored sucessfully! ")

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

print(" Attempting to sort the values into 120 lists with each tutorial group ")
sortedTutorialGroups = studentsAsTutorialGroupLists(sortedStudentInfoAsDictionaries)
print(" Sucessfully seperated them into their assigned tutorial groups ")

# Now that we have the 120 sorted tutorial groups in 120 different lists we can attempt on forming the 10 teams in each group.
def gpasort(list):
    sortedListByGpa = []
    print(" Attempting to sort the tutorial groups by GPA.")
    for i in list:
        sorted_tutorialGroup = merge_sort(i, "CGPA")
        sortedListByGpa.append(sorted_tutorialGroup)
    print(" Sucessfully sorted all of the groups by GPA ")
    return sortedListByGpa

gpasortedTutorialGroups = gpasort(sortedTutorialGroups)


# Now that it is sorted by GPA in each tutorial group we can proceed. gpasortedTutorialGroups[0] -> Tut Group 1
# Thoughts:
# Add the lowest gpa into the group, subsequently add the highest GPA. Continue for the first 5. Repeat.



    






                


