# Step 1: Read the CSV data from the provided file
students = [] # list of info of students which are stored are dictionaires 

with open("records.csv", 'r') as f:
    lines = f.readlines()  # Read all lines from the file

    # Skip the header and parse each line into a dictionary
    for line in lines[1:]:
        tutorial_group, student_id, name, school, gender, cgpa = line.strip().split(',')

        # Store each student as a dictionary with their details
        students.append({
            'Tutorial Group': tutorial_group,
            'Student ID': student_id,
            'Name': name,
            'School': school,
            'Gender': gender,
            'CGPA': float(cgpa)  # Convert CGPA to float for later use
        })

# Group students by their tutorial groups
from collections import defaultdict

tutorial_groups = defaultdict(list)
for student in students:
    tutorial_groups[student['Tutorial Group']].append(student)



# Now, split each tutorial group into smaller groups of 5 with balanced genders
def split_into_groups(students, group_size=5):
    males = [s for s in students if s['Gender'] == 'Male']
    females = [s for s in students if s['Gender'] == 'Female']

    groups = []
    while len(males) > 0 or len(females) > 0:
        group = []
        for _ in range(group_size // 2):
            if males:
                group.append(males.pop(0))
            if females:
                group.append(females.pop(0))
        groups.append(group)
    
    return groups

# Apply the split function to each tutorial group
result = {group: split_into_groups(students) for group, students in tutorial_groups.items()}

# Print the result
for tutorial_group, student_groups in result.items():
    print(f"\nTutorial Group: {tutorial_group}")
    for i, group in enumerate(student_groups):
        print(f"  Group {i+1}: {group}")


    
