def csv2dict(filename):
    with open(filename, "r") as target:
        linesasList = []
        studentInfo = []
        print(" Reading the lines of the file... ")
        for line in target:
            linesasList.append(line)
        print(" All lines have been read and stored in the variable 'linesasList' ")

        for line in linesasList[1:]:
            tutorial_group, student_id, name, school, gender, cgpa = line.strip().split(',')

            studentInfoAsDict = {
            'Tutorial Group': tutorial_group,
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

def tutorialGroupFilter(data):
    for i in data:
        if i["Tutorial Group"]



