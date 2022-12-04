# Li Xi
# CS330, Fall 2022
# Stable Matching Algorithm

import sys
import time


def read_prefs(pref_1_filename, pref_2_filename):
    # For parts 1 an 2.
    # This function reads preferences from two files
    # and returns two-dimensional preference lists and the length, N, of the lists.
    with open(pref_1_filename, 'r') as f:
        hospital_raw = f.read().splitlines()
    with open(pref_2_filename, 'r') as f:
        student_raw = f.read().splitlines()
    N = int(student_raw[0])
    hospital_prefs = [[int(id) for id in x.split(',')]
                      for x in hospital_raw[1:]]
    student_prefs = [[int(id) for id in x.split(',')] for x in student_raw[1:]]
    return N,  hospital_prefs, student_prefs


def read_prefs_q3(com_pref_file, stu_pref_file):
    # This function reads preferences from two files (the first for companies, the second for students)
    # and returns two-dimensional preference lists and the parameters N, M and k.
    with open(com_pref_file, 'r') as f:
        company_raw = f.read().splitlines()
    with open(stu_pref_file, 'r') as f:
        student_raw = f.read().splitlines()
    N = int(student_raw[0])
    parameters = [int(x) for x in company_raw[0].split(',')]
    M = parameters[0]
    k = parameters[1]
    student_prefs = [[int(id) for id in x.split(',')] for x in student_raw[1:]]
    company_prefs = [[int(id) for id in x.split(',')] for x in company_raw[1:]]
    return N, M, k, company_prefs, student_prefs


def inverse_prefs(N, prefs):
    ############################################################
    # Implement inverse preference lists as described in lecture
    ############################################################
    # Creating 2d array using this way may cause some funny effects.
    # rows, cols = (len(prefs),len(prefs))
    # ranks = [[0]*cols]*rows # You'll need to replace this.
    # print(prefs) Convert prefs to hash table or linked list?

    # ranks = list(range(len(prefs)))
    # for i in range(len(prefs)):
    #     ranks[i] = len(prefs) * [0]

    # for i in range(len(prefs)):
    #     for j in range(len(prefs[i])):
    #         #ranks[i][prefs[i][j]] = prefs[i].index(prefs[i][j])
    #         ranks[i][prefs[i][j]] = j
    # print(ranks)
    ranks = list(range(N))
    for i in range(N):
        ranks[i] = len(prefs[0]) * [0]

    for i in range(N):
        for j in range(len(prefs[i])):
            #ranks[i][prefs[i][j]] = prefs[i].index(prefs[i][j])
            ranks[i][prefs[i][j]] = j
    # print(ranks)
    return ranks

# company inverse


def inverse_prefs_question3(M, prefs):
    ranks = list(range(M))
    for i in range(M):
        ranks[i] = len(prefs[0]) * [0]

    for i in range(M):
        for j in range(len(prefs[i])):
            ranks[i][prefs[i][j]] = j

    print(ranks)
    return ranks


def run_GS(N, hospital_prefs, student_prefs, out_name):
    free_hospital = list(range(N))  # This list will be used as a stack
    # (because Python lists provide O(1)-time stack operations).
    # stores the index of each hospital's next unproposed student,
    count = N*[0]
    # going from the left of hospital's preference list
    job = N*[None]  # Stores the hospital currently matched to each student.
    student_ranks = inverse_prefs(N, student_prefs)

    # Gale-Shapley algorithm with hospitals making offers to students
    while free_hospital:  # returns True if list is nonempty
        # Remove the hospital on top of the stack.
        hospital = free_hospital.pop()
        student = hospital_prefs[hospital][count[hospital]]
        #print(hospital, 'proposing to', student)
        count[hospital] += 1
        if job[student] is None:   # student is not paired
            job[student] = hospital
            #print('student is not paired')
        else:
            # slow way to compute
            if student_ranks[student][job[student]] < student_ranks[student][hospital]:
                # if student_prefs[student].index(job[student]) < student_prefs[student].index(hospital):
                ############################################################
                # The code in the if statement runs in linear time!
                # Fix that...
                ############################################################
                #print(student_ranks[student][job[student]], student_ranks[student][hospital])
                #print(student_prefs[student].index(job[student]), student_prefs[student].index(hospital))
                # Add hospital back to free stack
                free_hospital.append(hospital)
            else:
                # student switches to new hospital, old hospital becomes free
                #print('student prefers', hospital)
                # Add student's previous match to "free" stack.
                free_hospital.append(job[student])
                job[student] = hospital
    # write matches to output file
    with open(out_name, 'w') as f:
        for student, hospital in enumerate(job):
            f.write(str(hospital)+','+str(student)+'\n')
    # In addition to writing the output to a file, this code returns a list of jobs given to each student. You can use this for testing.
    return job


############################################################
# PART 2 STARTER CODE
############################################################

def check_stable(N, hospital_prefs, student_prefs, match_file):
    student_rank = inverse_prefs(N, student_prefs)
    hospital_rank = inverse_prefs(N, hospital_prefs)
    with open(match_file, 'r') as f:
        matchings = [[int(id) for id in pair.split(',')]
                     for pair in f.read().splitlines()]
    ########################################
    # Your code goes here!
    # print(student_rank)
    # print(hospital_rank)
    # print(matchings)
    # inverse matchings (hospital, student) to assigned hospital for each student from0 to9

    M = list(range(N))
    # for i in range(N):
    #    M[i] = matchings[i][1]  M needs to be in order from Hospital 0 to Hospital 9
    inverse = list(range(N))
    for i in range(N):
        inverse[matchings[i][1]] = matchings[i][0]
        M[matchings[i][0]] = matchings[i][1]

    # print(M)
    # print(inverse)

    for h in range(N):
        j = 0
        while j < hospital_rank[h][M[h]]:
            r = hospital_prefs[h][j]
            if student_rank[r][h] < student_rank[r][inverse[r]]:
                stable_and_perfect = False
                if stable_and_perfect == False:
                    break
                # print(stable_and_perfect)
            else:
                stable_and_perfect = True
                # print(stable_and_perfect)
            j += 1
    ########################################

    # stable_and_perfect = False  # set this to true if the assignment is stable
    # Note: Make sure that the 1-bit output is the only info your code prints!
    if stable_and_perfect:
        print(1)     # if stable
    else:
        print(0)     # if not stable
    return stable_and_perfect


############################################################
# PART 3 STARTER CODE
############################################################

def find_stable_intern_assignment(N, M, k, company_prefs, student_prefs, out_name):
    # for each student, job[i] is the company they are currently matched to.
    job = N*[-1]
    # Your code goes here!
    #free_student = list(range(N))
    free_company = list(range(M))
    count = N * [0]
    # since student number is always smaller than number of company positions, dummy students should be
    # added to make them equal. Also, either student ranks or company ranks should be converted again
    # so that they have the same row and column for processing.
    student_ranks = inverse_prefs(N, student_prefs)
    company_ranks = inverse_prefs_question3(M, company_prefs)

    while free_company:
        company = free_company.pop()
        # print(company)
        student = company_prefs[company][count[company]]
        # print(student)
        count[company] += 1
        if job[student] == -1:
            job[student] = company
        else:
            # student prefers old company, new company becomes free.
            if student_ranks[student][job[student]] < student_ranks[student][company]:
                free_company.append(company)
                count[job[student]] += 1
                # if the company still have slots open, put it back queue.
                if count[job[student]] < k:
                    free_company.append(job[student])
                else:
                    # if company has k positions filled and the next student prefers the company, then
                    # compare company's preference among these students, and put the least favorite
                    # student back to student list
                    # pseudocode: oldstudent initialized.
                    if company_ranks[[job[student]]][student] < company_ranks[job[student]][oldstudent]:
                        job[oldstudent] = -1
                        job[student] = company
            else:
                # student switches to new company, old company becomes free
                free_company.append(job[student])
                job[student] = company
                count[company] += 1
                # if the company still have slots open, put it back to queue.
                if count[company] < k:
                    free_company.append(company)
                else:
                    if company_ranks[company][student] < company_ranks[company][oldstudent]:
                        job[oldstudent] = -1
                        job[student] = company

                    # if student queue is not empty
                    # while free_student:
                    # student = free_student.pop()
                    # print(student)
                    # print(count)
                    # # find company who has not rejected student
                    # company = student_prefs[student][count[student]]
                    # # print(student, 'proposing to', company)  # company 2, student 10
                    # count[student] += 1  # new proposal by student
                    # if job[student] is None:   # if company is not paired
                    #     job[student] = company
                    #     # print(job[student])    # 2
                    # else:
                    #     # if the student's ith favorite company < student's jth favorite company (prefer i over j)
                    #     if student_ranks[student][job[student]] < student_ranks[student][company]:
                    #         # if company_ranks[company][job[company]] < company_ranks[company][student]:
                    #         free_student.append(job[student])
                    #     else:
                    #         # add previous student match to free stack
                    #         free_student.append(student)
                    #         job[student] = company

                # write matches as output to the file called out_name.
    with open(out_name, 'w') as f:
        for student, company in enumerate(job):
            f.write(str(company)+','+str(student)+'\n')
    return job


############################################################
# Main function. (Do not modify for submission.)
############################################################

def main():
    # Do not modify main() other than using the commented code snippet for printing
    # running time for Q1, if needed
    if (len(sys.argv) < 5):
        return "Error: the program should be called with four arguments"
    hospital_prefs_file = sys.argv[1]
    student_prefs_file = sys.argv[2]
    match_file = sys.argv[3]
    # NB: For parts 1 and 3, match_file is the file to which the *output* is wrtten
    #     For part 2, match_file contains a candidate matching to be tested.
    question = sys.argv[4]
    N, hospital_prefs, student_prefs = read_prefs(
        hospital_prefs_file, student_prefs_file)
    if question == 'Q1':
        start = time.time()
        run_GS(N, hospital_prefs, student_prefs, match_file)
        end = time.time()
        print(end-start)
    elif question == 'Q2':
        check_stable(N, hospital_prefs, student_prefs, match_file)
    elif question == 'Q3':
        company_prefs_file = hospital_prefs_file
        N, M, k, company_prefs, student_prefs = read_prefs_q3(
            company_prefs_file, student_prefs_file)
        find_stable_intern_assignment(
            N, M, k, company_prefs, student_prefs, match_file)
    else:
        print("Missing or incorrect question identifier (the fourth argument should be \'Q1\', \'Q2\', or \'Q3\', without quotes).")
    return


if __name__ == "__main__":
    # example command: python stable_matching.py pref_file_1 pref_file_2 match_name Q1

    # stable_matching.py: filename; do not change this
    # pref_file_1: filename of the first preference list
    # pref_file_2: filename of the second preference list
    # match_name: desired filename for output (or input, for Q2)  matching file
    # Q1: desired question for testing. Can be Q1, Q2, or Q3.
    main()
