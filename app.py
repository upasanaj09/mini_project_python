SUPABASE_URL="https://fgdnspotvzgulaswynkp.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZnZG5zcG90dnpndWxhc3d5bmtwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU2MzU0MjUsImV4cCI6MjA5MTIxMTQyNX0.lQvpkzseu6QFsFiFj5Hjs8fnREUXsmackTdsduvU_3o"

from supabase import create_client
import streamlit as st

db=create_client(SUPABASE_URL, SUPABASE_KEY)

st.title('P1 - Student Records')

# INSERT - run once, then comment out
students=[
    {"name":"Ali Hassan", "email":"ali@uni.edu","age":20, "gpa":3.8},
    {"name":"Siti Aishah", "email":"siti@uni.edu","age":21, "gpa":3.2},
    {"name":"Raj Kumar", "email":"raj@uni.edu","age":19, "gpa":2.9},
    {"name":"Lin Wei", "email":"lin@uni.edu","age":22, "gpa":3.5},
 ]
db.table('students').insert(students).execute()
ids={r['name']:r['id'] for r in db.table('students').select('id,name').execute().data}

enrollments=[
    {"student_id":ids["Ali Hassan"], "course":"RDBMS", "grade":"A"},
    {"student_id":ids["Ali Hassan"], "course":"Networks", "grade":"B"},
    {"student_id":ids["Siti Aishah"], "course":"RDBMS", "grade":"B"},
    {"student_id":ids["Raj Kumar"], "course":"RDBMS", "grade":"C"},
    {"student_id":ids["Lin Wei"], "course":"Networks", "grade":"A"},
]
db.table('enrollments').insert(enrollments).execute()

#Select all
st.subheader('All Students')
st.dataframe(db.table('students').select('*').execute().data)

#WHERE-high GPA
st.subheader('GPA>=3.5')
st.dataframe(db.table('students').select('name,gpa').gte('gpa',3.5).execute().data)

# JOIN via FK
st.subheader('RDBMS Enrollments(JOIN)')
st.dataframe(db.table('enrollments').select('grade,students(name)').eq('course','RDBMS').execute().data)

# UPDATE
db.table('students').update({'gpa':3.9}).eq('name', 'Ali Hassan').execute()
st.write('Ali updated:', db.table('students').select('name,gpa').eq('name','Ali Hassan').execute().data)

