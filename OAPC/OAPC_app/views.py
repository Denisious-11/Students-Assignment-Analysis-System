from email.utils import collapse_rfc2231_value
from logging.config import dictConfig
from django.shortcuts import render
import json
from django.core import serializers
from .models import *
from pydoc import doc
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
import pandas as pd
import numpy as np
import numpy.linalg as LA
from datetime import date
from datetime import datetime
import operator
import docx2txt  # text extraction from file
from gensim.parsing.preprocessing import remove_stopwords  # remove stopwords
from sklearn.metrics.pairwise import cosine_similarity
import re
# TF-IDF feature extraction
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
# from nltk.tokenize import sent_tokenize  # sentence tokenization
nltk.download('punkt')


# Create your views here.

##############LOGIN & REGISTER START###########


def display_login(request):
    return render(request, "login.html", {})


def show_register(request):
    return render(request, "register.html", {})


def register(request):
    username = request.GET.get("uname")
    email = request.GET.get("mail")
    password = request.GET.get("pass")

    a = Users.objects.filter(username=username)
    c = a.count()
    if(c == 1):
        return HttpResponse("[INFO]: This username is already TAKEN, Use another one!")
    else:
        b = Users(username=username, email=email, password=password)
        b.save()
        return HttpResponse("Successfully Registered")


def check_login(request):
    username = request.GET.get("uname")
    password = request.GET.get("pass")

    print(username)
    print(password)

    if username == 'ADMIN' and password == 'ADMIN':
        return HttpResponse("Admin Login Successful")
    else:
        d = Users.objects.filter(username=username, password=password)
        c = d.count()
        if c == 1:
            d2 = Users.objects.get(username=username, password=password)
            request.session["uid"] = d2.u_id
            request.session["uname"] = d2.username
            return HttpResponse("Student Login Successful")
        else:
            return HttpResponse("Invalid")

##############LOGIN & REGISTER END#############

# ADMIN START


def a_home_admin(request):
    return render(request, "home_admin.html", {})


def c_view_users_admin(request):
    return render(request, "view_users_admin.html", {})


def users(request):
    d = Users.objects.all()
    # print(d)
    dic = {}
    if d:
        value = serializers.serialize("json", d)
        dic["key"] = json.loads(value)
        print(dic)
        return JsonResponse(dic, safe=False)
    else:
        return HttpResponse("No users")


def delete(request):
    username = request.GET.get("uname")

    f = Users.objects.get(username=username)
    f.delete()
    return HttpResponse("Deleted Successfully")


def m_add_subjects_admin(request):
    return render(request,"add_subjects_admin.html",{})

def add_subjects(request):
    subject_name = request.GET.get("sname")

    k = Subject.objects.filter(subject_name=subject_name)
    c = k.count()
    if(c == 1):
        return HttpResponse("already added this subject")
    else:
        b = Subject(subject_name=subject_name)
        b.save()
        return HttpResponse("subject added successfully")

def n_manage_subjects_admin(request):
    return render(request,"manage_subjects_admin.html",{})

def subjects(request):
    d = Subject.objects.all()
    dic = {}
    if d:
        value = serializers.serialize("json", d)
        dic["key"] = json.loads(value)
        return JsonResponse(dic, safe=False)
    else:
        return HttpResponse("No subjects")

def subject_edit(request):
    subject_id = request.GET.get("s_id")
    subject_name = request.GET.get("s_name")

    e = Subject.objects.get(subject_id=int(subject_id))
    e.subject_name = subject_name
    e.save()

    return HttpResponse("edited successfully")
def subject_delete(request):
    subject_id = request.GET.get("s_id")

    f = Subject.objects.get(subject_id=int(subject_id))
    f.delete()

    return HttpResponse("deleted successfully")


def o_add_assignment_topic_admin(request):
    return render(request,"add_assignment_topic_admin.html",{})

def add_assignment_topic(request):
    topic_name = request.GET.get("tname")
    subject_name = request.GET.get("sname")
    last_date=request.GET.get("ldate")

    k = Topic.objects.filter(topic_name=topic_name)
    c = k.count()
    if(c == 1):
        return HttpResponse("already added this Assignment Topic")
    else:

        b = Topic(topic_name=topic_name, subject_name=subject_name,last_date=last_date)
        b.save()
        return HttpResponse("Assignment Topic added successfully")


def p_manage_assignment_topic_admin(request):
    return render(request,"manage_assignment_topic_admin.html",{})

def topics(request):
    d = Topic.objects.all()
    dic = {}
    if d:
        value = serializers.serialize("json", d)
        dic["key"] = json.loads(value)
        return JsonResponse(dic, safe=False)
    else:
        return HttpResponse("No Assignment Topics")

def topic_edit(request):
    topic_id = request.GET.get("t_id")
    topic_name = request.GET.get("t_name")
    subject_name = request.GET.get("s_name")

    e = Topic.objects.get(topic_id=int(topic_id))
    e.topic_name=topic_name
    e.subject_name = subject_name
    e.save()

    return HttpResponse("edited successfully")

def topic_delete(request):
    topic_id = request.GET.get("t_id")

    f = Topic.objects.get(topic_id=int(topic_id))
    f.delete()

    return HttpResponse("deleted successfully")


def e_view_assignments_admin(request):
    return render(request, "view_assignments_admin.html", {})


def assignments(request):
    d = Assignmentt.objects.all()
    # print(d)
    dic = {}
    if d:
        value = serializers.serialize("json", d)
        dic["key"] = json.loads(value)
        # print(dic)
        return JsonResponse(dic, safe=False)
    else:
        return HttpResponse("No assignments")


def f_check_plagiarism_admin(request):
    return render(request, "check_plagiarism_admin.html", {})


def admin_check_plagiarism(request):
    student_name = request.GET.get("uname")
    # print(student_name)

    k = Assignmentt.objects.get(username=student_name)
    student_file = k.file
    # print("Student file:>>>", student_file)

    file_name_dict = Assignmentt.objects.values('file')
    # print("File List (DICTIONARY)>>>>>>", file_name_dict)

    all_file = [i["file"] for i in file_name_dict]
    # print("list_of_files_name>>>>>>", all_file)

    my_index = all_file.index(student_file)
    # print("my_index:>>>>>>>>>", my_index)

    alldocuments = []
    for i in all_file:
        # print(i)
        text = docx2txt.process(i)
        text = remove_stopwords(text)
        lower_text = text.lower()

        alldocuments.append(lower_text)
    # print(alldocuments)
    # print("length alldocuments:>>>>>>>>>>>>>>>", len(alldocuments))

    vectorizer = TfidfVectorizer()
    result = vectorizer.fit(alldocuments)

    student_file_text = docx2txt.process(student_file)
    student_file_text_after_sw = remove_stopwords(student_file_text)
    student_file_lower_text = student_file_text_after_sw.lower()
    student_file_lower_text = [student_file_lower_text]

    final_resultt = vectorizer.transform(student_file_lower_text)
    # print("student FINAL RESULT::::>>>>", final_resultt)
    final_arrayy = final_resultt.toarray()  # array representation
    # print("student FINAL ARRAY::::>>>>>>>>", final_arrayy)

    df1 = pd.DataFrame(final_arrayy, columns=vectorizer.get_feature_names())
    # print(df1)

    all_file.remove(student_file)
    # print("Other file:>>>>>", all_file)

    cosine_list = []
    for i in all_file:
        # print(i)
        text = docx2txt.process(i)
        text = remove_stopwords(text)
        lower_text = text.lower()
        lower_text = [lower_text]

        final_result = vectorizer.transform(lower_text)
        # print("FINAL RESULT::::>>>>", final_result)
        final_array = final_result.toarray()  # array representation
        # print("FINAL ARRAY::::>>>>>>>>", final_array)

        df2 = pd.DataFrame(final_array, columns=vectorizer.get_feature_names())
        # print(df2)

        cosine = cosine_similarity(df1, df2)
        # print(cosine)
        cosine_list.append(cosine)
    # print(" cosine list:>>>>>>>>>>>>>>>", cosine_list)
    # print("type of cosine list", type(cosine_list))

    global new_cosine_list
    new_cosine_list = []
    for z in cosine_list:
        # print(z)
        # print("type of z:", type(z))
        z = z[0]
        # print(z)
        z = z[0]
        # print(z)
        # print("type of z:", type(z))
        new_cosine_list.append(z)

    print("new cosine list:>>>>>>>>>>>>>>>", new_cosine_list)
    # print("other file list:>>>>>>>>>>>>>", all_file)

    # print(len(new_cosine_list))
    # print(len(all_file))
    global pqr
    for i in range(len(all_file)):
        cos_value = new_cosine_list[i]
        # print(cos_value)
        if(cos_value >= 0.9):
            pqr = "DETECTED"
        else:
            pqr = cos_value
        global file_name
        file_name = all_file[i]
        # print(file_name)

        request = 0
        store(request)
    retrieve(request)

    return JsonResponse(dicc, safe=False)

def take_status(request):
    username = request.GET.get("uname")
    file=request.GET.get("fname")
    print("USER NAME :",username)
    print("FILE :",file)
    q = Assignmentt.objects.filter(username=username,file=file).values('status')
    print("*****************************************************************")
    print("MY Q ::::>>>>>>",q)
    my_status_list = [i["status"] for i in q]
    print("my_status List :::>", my_status_list)
    global final_my_status_list
    final_my_status_list=my_status_list[0]
    print("final_my_status_list::>",final_my_status_list)
  
    return HttpResponse("Nothing")

def show_grade(request):
    get_status=final_my_status_list
    print("TYPE STATUS :",type(get_status))
    get_list=new_cosine_list
    print("GET STATUS::>",get_status)
    print("GET LIST:::>",get_list)

    val1=0.3
    p1=all(x<val1 for x in get_list)
    print("p1:>",p1)
    print(type(p1))

    if (get_status=='On_Time' and p1==True):
        grade="A"
    elif (get_status=='On_Time' and p1==False):
        grade="B"
    elif (get_status=='Late' and p1==True):
        grade="C"
    elif (get_status=='Late' and p1==False):
        grade="D"
    return HttpResponse(grade)


def generate_report_admin(request):
    return render(request, "generate_report_admin.html", {})


def computeLPSArray(pat, M, lps):
    len = 0
    lps[0]
    i = 1
    while i < M:
        if pat[i] == pat[len]:
            len += 1
            lps[i] = len
            i += 1
        else:
            if len != 0:
                len = lps[len-1]
            else:
                lps[i] = 0
                i += 1


def KMPSearch(pat, text, p):

    M = len(pat)
    N = len(text)
    lps = [0]*M
    j = 0
    computeLPSArray(pat, M, lps)

    i = 0
    while i < N:
        if pat[j].lower() == text[i].lower():
            i += 1
            j += 1

        if j == M:
            p += 1
            j = lps[j-1]
            break

        elif i < N and pat[j].lower() != text[i].lower():
            if j != 0:
                j = lps[j-1]
            else:
                i += 1
    return p


def enter_to_Match(request):
    username = matching_student_name
    file = matching_file
    matching_content = my_final_new_list

    va = Match(username=username, file=file, matching_content=matching_content)
    va.save()
    print("saved")


def exit_from_Match(request):
    tt = Match.objects.all()
    global match_dicc
    match_dicc = {}
    if tt:
        value = serializers.serialize("json", tt)
        match_dicc["key"] = json.loads(value)
        # print(match_dicc)
        return JsonResponse(match_dicc, safe=False)
    else:
        return HttpResponse("No records")


# rabin karp
d = 10


def search(rr, other_file, q):
    m = len(rr)
    n = len(other_file)
    p = 0
    t = 0
    h = 1
    i = 0
    j = 0

    for i in range(m-1):
        h = (h*d) % q

    # Calculate hash value for pattern and other_file
    for i in range(m):
        p = (d*p + ord(rr[i])) % q
        t = (d*t + ord(other_file[i])) % q

    # Find the match
    for i in range(n-m+1):
        if p == t:
            for j in range(m):
                if other_file[i+j] != rr[j]:
                    break

            j += 1
            if j == m:
                # print("Pattern is found at position: " + str(i+1))

                return rr

        if i < n-m:
            t = (d*(t-ord(other_file[i])*h) + ord(other_file[i+m])) % q

            if t < 0:
                t = t+q


def report_generation(request):
    student_name = request.GET.get("uname")
    print(student_name)

    k = Assignmentt.objects.get(username=student_name)
    student_file = k.file
    print("Student file:>>>", student_file)

    file_name_dict = Assignmentt.objects.values('file')
    print("File List (DICTIONARY)>>>>>>", file_name_dict)

    all_file = [i["file"] for i in file_name_dict]
    print("list_of_files_name>>>>>>", all_file)

    my_index = all_file.index(student_file)
    print("my_index:>>>>>>>>>", my_index)

    alldocuments = []
    for i in all_file:
        print(i)
        text = docx2txt.process(i)
        text = remove_stopwords(text)
        lower_text = text.lower()

        alldocuments.append(lower_text)
    print(alldocuments)
    print("length alldocuments:>>>>>>>>>>>>>>>", len(alldocuments))

    vectorizer = TfidfVectorizer()
    result = vectorizer.fit(alldocuments)

    student_file_text = docx2txt.process(student_file)
    student_file_text_after_sw = remove_stopwords(student_file_text)
    student_file_lower_text = student_file_text_after_sw.lower()
    student_file_lower_text = [student_file_lower_text]

    final_resultt = vectorizer.transform(student_file_lower_text)
    print("student FINAL RESULT::::>>>>", final_resultt)
    final_arrayy = final_resultt.toarray()  # array representation
    print("student FINAL ARRAY::::>>>>>>>>", final_arrayy)

    df1 = pd.DataFrame(final_arrayy, columns=vectorizer.get_feature_names())
    print(df1)

    all_file.remove(student_file)
    print("Other file:>>>>>", all_file)

    cosine_list = []
    for i in all_file:
        print(i)
        text = docx2txt.process(i)
        text = remove_stopwords(text)
        lower_text = text.lower()
        lower_text = [lower_text]

        final_result = vectorizer.transform(lower_text)
        print("FINAL RESULT::::>>>>", final_result)
        final_array = final_result.toarray()  # array representation
        print("FINAL ARRAY::::>>>>>>>>", final_array)

        df2 = pd.DataFrame(final_array, columns=vectorizer.get_feature_names())
        print(df2)

        cosine = cosine_similarity(df1, df2)
        print(cosine)
        cosine_list.append(cosine)
    print(" cosine list:>>>>>>>>>>>>>>>", cosine_list)
    print("type of cosine list", type(cosine_list))

    new_cosine_list = []
    for z in cosine_list:
        print(z)
        print("type of z:", type(z))
        z = z[0]
        print(z)
        z = z[0]
        print(z)
        print("type of z:", type(z))
        new_cosine_list.append(z)

    print("new cosine list:>>>>>>>>>>>>>>>", new_cosine_list)
    print("other file list:>>>>>>>>>>>>>", all_file)

    high = max(new_cosine_list)
    print("largest cosine similarity value:>>>>>", high)

    # indices = [index for index, element in enumerate(
    #     new_cosine_list) if element == high]
    # print("highest similarity indices:>>>", indices)

    # similarity_files = []
    # for k in indices:
    #     print(k)
    #     p = all_file[k]
    #     print(p)
    #     similarity_files.append(p)
    # print("Similarity files:>>>>>", similarity_files)

    indices = new_cosine_list.index(high)
    print("highest similarity indices:>>>", indices)

    similarity_files = all_file[indices]
    print("Similarity files:>>>>>", similarity_files)

    print("Student file:>>>", student_file)

    ###########applying rabin-karp ALGORITHM###############

    student_file_text = docx2txt.process(student_file)
    # student_file_text = remove_stopwords(student_file_text)
    student_file_text = student_file_text.lower()

    similarity_files_text = docx2txt.process(similarity_files)
    # similarity_files_text = remove_stopwords(similarity_files_text)
    similarity_files_text = similarity_files_text.lower()

    # pattern file----->student file
    # other_file------>similarity file

    pattern_file = student_file_text
    pattern_file = re.sub(r"[^a-zA-Z.]+", ' ', pattern_file)
    print("before remove sw pattern_file:::>>>>>", pattern_file)
    extra_remove_sw = re.compile("\\b(i|ll|me|my|myself|we|our|ours|ourselves|you|your|yours|yourself|yourselves|he|him|his|himself|she|her|hers|herself|it|its|itself|they|them|their|theirs|themselves|what|which|who|whom|this|that|these|those|am|is|are|was|were|be|been|being|have|has|had|having|do|does|did|doing|a|an|the|and|but|if|or|because|as|until|while|of|at|by|for|with|about|against|between|into|through|during|before|after|above|below|to|from|up|down|in|out|on|off|over|under|again|further|then|once|here|there|when|where|why|how|all|any|both|each|few|more|most|other|some|such|no|nor|not|only|own|same|so|than|too|very|s|t|can|will|just|don|should|now)\\W", re.I)
    pattern_file = extra_remove_sw.sub("", pattern_file)
    print("after remove sw pattern_file:::>>>>>", pattern_file)

    other_file = similarity_files_text
    other_file = re.sub(r"[^a-zA-Z.]+", ' ', other_file)
    print("before remove sw other_file:::>>>>>", other_file)
    other_file = extra_remove_sw.sub("", other_file)
    print("after remove sw other_file:::>>>>>", other_file)

    ##############TYPE 2#############
    new_list = []
    sentence_pattern_file = pattern_file.split(".")
    print("sentence_pattern_file>>>>>>>>>>", sentence_pattern_file)
    for rr in sentence_pattern_file:
        # print(rr)
        q = 13
        answer = search(rr, other_file, q)
        print("ANSWER:::::>>>>>", answer)
        new_list.append(answer)
    print("NEW_LIST", new_list)

    first_bad_item = " "
    while(first_bad_item in new_list):
        new_list.remove(first_bad_item)

    global my_final_new_list
    my_final_new_list = []
    for val in new_list:
        if val != None:
            my_final_new_list.append(val)
    print("my_final_new_list", my_final_new_list)

    print("matching file is::::>>>>>>", similarity_files)

    global matching_file
    matching_file = similarity_files
    lmo = Assignmentt.objects.get(file=matching_file)
    global matching_student_name
    matching_student_name = lmo.username
    print("Matching Student Name:>>>", matching_student_name)
    if my_final_new_list == []:
        return HttpResponse("No Matching Contents")
    else:
        request = 0
        enter_to_Match(request)
        exit_from_Match(request)

        return JsonResponse(match_dicc, safe=False)


def match_table_delete(request):
    a = Match.objects.all().delete()

    return HttpResponse("Temporary Match Table Values Deleted")

    # ADMIN END

    # STUDENT START


def b_home_student(request):
    return render(request, "home_student.html", {})


def d_upload_assignment_student(request):
    return render(request, "upload_assignment_student.html", {})

def show_topic_on_subject(request):
    subject_name = request.GET.get("sname")
    q = Topic.objects.filter(subject_name=subject_name)
    dic = {}
    if q:
        value = serializers.serialize("json", q)
        dic["key"] = json.loads(value)
        return JsonResponse(dic, safe=False)
    else:
        return HttpResponse("No Topics")

def last_date_on_topic(request):
    topic_name = request.GET.get("tname")
    q = Topic.objects.filter(topic_name=topic_name)
    dic = {}
    if q:
        value = serializers.serialize("json", q)
        dic["key"] = json.loads(value)
        return JsonResponse(dic, safe=False)
    else:
        return HttpResponse("Not Available")



def upload_assignment(request):
    file_name = request.POST.get("f_upload")
    file1 = request.FILES["f_upload"]
    print("<<<<<<<<<<<<<<<<<", file1)

    assignment_name = request.POST.get("topic_name")
    print("Assignment Name :->",assignment_name)
    submission_last_date=request.POST.get("submission_date")
    print("Submission Last Date :->",submission_last_date)
    username = request.session["uname"]
    print("username:::::::::::::::::::::::::>>>>", username)

    file = file1

    fs = FileSystemStorage("OAPC_app\\static\\files_upload")
    fs.save(file_name, file)

    k = Assignmentt.objects.filter(
        username=username, assignment_name=assignment_name)
    c = k.count()
    if c == 1:
        print("[INFO]: Assignment already submitted")
        return HttpResponse("[INFO]: Assignment already submitted")
    else:
        # date_now= date.today()
        # print("Date Now :>",date_now)
        date_now=datetime.now()
        print(date_now)
        final_date_now=date_now.strftime("%Y-%m-%d")
        print(final_date_now)
        l_date=datetime.strptime(submission_last_date,"%Y-%m-%d")
        s_date=datetime.strptime(final_date_now,"%Y-%m-%d")
        print(l_date)
        print(s_date)

        if (s_date<=l_date):
            my_var="On_Time"
            print(my_var)
        else:
            my_var="Late"
            print(my_var)
        a = Assignmentt(username=username,
                       assignment_name=assignment_name, file=file,status=my_var)
        a.save()
        print("[INFO]: assignment uploaded successfully")

        return render(request, "upload_assignment_student.html")


def g_check_plagiarism_student(request):
    return render(request, "check_plagiarism_student.html", {})


def store(request):
    file = file_name
    cosine_value = pqr

    v = Plagiarism_Value(file=file, cosine_value=cosine_value)
    v.save()
    print("ADDED")


def retrieve(request):
    tt = Plagiarism_Value.objects.all()
    global dicc
    dicc = {}
    if tt:
        value = serializers.serialize("json", tt)
        dicc["key"] = json.loads(value)
        # print(dicc)
        return JsonResponse(dicc, safe=False)
    else:
        return HttpResponse("No records")


def my_plagiarism(request):
    student_name = request.session["uname"]
    print("Student name:>>>", student_name)

    k = Assignmentt.objects.get(username=student_name)
    student_file = k.file
    print("Student file:>>>", student_file)

    file_name_dict = Assignmentt.objects.values('file')
    print("File List (DICTIONARY)>>>>>>", file_name_dict)

    all_file = [i["file"] for i in file_name_dict]
    print("list_of_files_name>>>>>>", all_file)

    my_index = all_file.index(student_file)
    print("my_index:>>>>>>>>>", my_index)

    alldocuments = []
    for i in all_file:
        print(i)
        text = docx2txt.process(i)
        text = remove_stopwords(text)
        lower_text = text.lower()

        alldocuments.append(lower_text)
    print(alldocuments)
    print("length alldocuments:>>>>>>>>>>>>>>>", len(alldocuments))

    vectorizer = TfidfVectorizer()
    result = vectorizer.fit(alldocuments)

    student_file_text = docx2txt.process(student_file)
    student_file_text_after_sw = remove_stopwords(student_file_text)
    student_file_lower_text = student_file_text_after_sw.lower()
    student_file_lower_text = [student_file_lower_text]

    final_resultt = vectorizer.transform(student_file_lower_text)
    print("student FINAL RESULT::::>>>>", final_resultt)
    final_arrayy = final_resultt.toarray()  # array representation
    print("student FINAL ARRAY::::>>>>>>>>", final_arrayy)

    df1 = pd.DataFrame(final_arrayy, columns=vectorizer.get_feature_names())
    print(df1)

    all_file.remove(student_file)
    print("Other file:>>>>>", all_file)

    cosine_list = []
    for i in all_file:
        print(i)
        text = docx2txt.process(i)
        text = remove_stopwords(text)
        lower_text = text.lower()
        lower_text = [lower_text]

        final_result = vectorizer.transform(lower_text)
        print("FINAL RESULT::::>>>>", final_result)
        final_array = final_result.toarray()  # array representation
        print("FINAL ARRAY::::>>>>>>>>", final_array)

        df2 = pd.DataFrame(final_array, columns=vectorizer.get_feature_names())
        print(df2)

        cosine = cosine_similarity(df1, df2)
        print(cosine)
        cosine_list.append(cosine)
    print(" cosine list:>>>>>>>>>>>>>>>", cosine_list)
    print("type of cosine list", type(cosine_list))

    new_cosine_list = []
    for z in cosine_list:
        print(z)
        print("type of z:", type(z))
        z = z[0]
        print(z)
        z = z[0]
        print(z)
        print("type of z:", type(z))
        new_cosine_list.append(z)

    print("new cosine list:>>>>>>>>>>>>>>>", new_cosine_list)
    print("other file list:>>>>>>>>>>>>>", all_file)

    print(len(new_cosine_list))
    print(len(all_file))

    global pqr
    for i in range(len(all_file)):
        cos_value = new_cosine_list[i]
        print(cos_value)
        if(cos_value >= 0.9):
            pqr = "DETECTED"
        else:
            pqr = cos_value
        global file_name
        file_name = all_file[i]
        print(file_name)

        request = 0
        store(request)
    retrieve(request)

    return JsonResponse(dicc, safe=False)


def table_delete(request):
    a = Plagiarism_Value.objects.all().delete()

    return HttpResponse("Temporary Plagiarism Table Values Deleted")

    # STUDENT END
