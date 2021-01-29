
#MIT License

#Copyright (c) 2018 Jeremy Ephron Barenholtz

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

from explorecourses import *
from explorecourses import filters
import json
import re


def has_nums(word):
    return any(char.isdigit() for char in word)


def upper_or_num(word):
    return not any(not char.isdigit() and not char.isupper() for char in word)


def get_courses(word_list, subject):
    course_list = []
    prior = ""
    for word in word_list:
        word = word.rstrip(",")
        if upper_or_num(word) and len(word) > 0:
            if word[0].isnumeric():
                if prior != "":
                    course_list.append(prior + word)
                else:
                    course_list.append(subject + word)
            else:
                if has_nums(word):
                    course_list.append(word)
                else:
                    prior = word
        else:
            prior = ""
    return course_list


connect = CourseConnection()

year = "2020-2021"
courses = connect.get_courses_by_department("MATH", year=year)
# courses += connect.get_courses_by_department("MATH", year=year) + connect.get_courses_by_department("PHYSICS", year=year) + connect.get_courses_by_department("CHEM", year=year)
# courses += connect.get_courses_by_department("ECON", year=year)
# courses = connect.get_courses_by_query("all courses")

nodes = []
index_map = dict()
for num, course in enumerate(courses):
    index_map[course.subject + course.code] = num
    node = {"id": course.subject + " " + course.code}
    nodes.append(node)

links = []
for num, course in enumerate(courses):
    print("Course: " + course.subject + " " + course.code)
    split = re.split('Prerequisite:|Prerequisites:', course.description)
    if len(split) > 1:
        print(split[1].split(".")[0].split())
        prereqs = get_courses(split[1].split(".")[0].split(), course.subject)
        for prereq in prereqs:
            if prereq in index_map:
                link = {"source": num, "target": index_map[prereq]}
                links.append(link)

graph = {"nodes": nodes, "links": links}

with open('./web_interface/graph.json', 'w') as outfile:
    json.dump(graph, outfile)

