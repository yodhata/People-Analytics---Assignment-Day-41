**People Analytics Dashboard** 

https://people-analytics-assignment-day-41.streamlit.app

Dashboard ini dibuat sebagai latihan People Analytics menggunakan Streamlit. Aplikasi ini membantu HR dan manajemen memahami kondisi karyawan, faktor-faktor yang memengaruhi kepuasan kerja, serta area berisiko yang perlu intervensi.

Tujuan Project
	1.	Menyajikan gambaran profil tenaga kerja secara ringkas dan interaktif.
	2.	Mengidentifikasi hubungan antara wellbeing, lembur, stress, dan job satisfaction.
	3.	Menemukan segmen karyawan berisiko rendah kepuasan kerja sebagai dasar rekomendasi kebijakan HR.
	4.	Menunjukkan implementasi dasar Streamlit (text, input, layout, metric, chart, table) sebagai portfolio data scientist.


Fitur Utama

1. Executive Overview
	•	Ringkasan metrik utama:
	•	Total karyawan
	•	Rata-rata Job Satisfaction
	•	Rata-rata Stress
	•	Rata-rata Work-Life Balance (WLB)
	•	Komposisi karyawan:
	•	Distribusi gender
	•	Jumlah karyawan per department
	•	Rata-rata Job Satisfaction per department

2. Wellbeing & Workload
	•	Metrik:
	•	Rata-rata jam tidur
	•	Rata-rata workload
	•	Persentase karyawan lembur (haveOT = True)
	•	Visualisasi:
	•	Job Satisfaction vs Work-Life Balance
	•	Job Satisfaction vs Stress Level
	•	Rata-rata Job Satisfaction: Lembur vs Tidak Lembur
	•	Persentase karyawan lembur per department

3. Risk & Segmentation
	•	Flag Low Satisfaction (JobSatisfaction ≤ 3).
	•	Persentase karyawan low satisfaction secara keseluruhan.
	•	Distribusi low satisfaction:
	•	per department
	•	per job level
	•	Membantu mengidentifikasi segmen yang perlu prioritas intervensi.

4. Actions & Playbook
	•	Ringkasan insight analitik:
	•	Dampak stress, WLB, dan lembur terhadap kepuasan kerja.
	•	Perbedaan antar department dan job level.
	•	Rekomendasi strategis berbasis data:
	•	Manajemen lembur.
	•	Program work-life balance & wellbeing.
	•	Pengembangan karier dan monitoring berkelanjutan.


Dataset

File: employee_survey.csv
Contoh kolom utama (setelah preprocessing lowercase dan ganti spasi):
- **EmpID:**	Unique identifier for each employee.
- **Gender:**	Gender of the employee (e.g., Male, Female, Other).
- **Age:**	Age of the employee.
- **MaritalStatus:**	Marital status of the employee (e.g., Single, Married, Divorced, Widowed).
- **JobLevel:**	Job level of the employee (e.g., Intern/Fresher, Junior, Mid, Senior, Lead).
- **Experience:**	Number of years of work experience the employee has.
- **Dept:**	Department where the employee works (e.g., IT, HR, Finance, Marketing, Sales, Legal, Operations, Customer Service).
- **EmpType:**	Type of employment (e.g., Full-Time, Part-Time, Contract).
- **WLB:**	Work-life balance rating (scale from 1 to 5).
- **WorkEnv:**	Work environment rating (scale from 1 to 5).
- **PhysicalActivityHours:**	Number of hours of physical activity per week.
- **Workload:**	Workload rating (scale from 1 to 5).
- **Stress:**	Stress level rating (scale from 1 to 5).
- **SleepHours:**	Number of hours of sleep per night.
- **CommuteMode:**	Mode of commute (e.g., Car, Public Transport, Bike, Walk, Motorbike).
- **CommuteDistance:**	Distance traveled during the commute (in kilometers).
- **NumCompanies:**	Number of different companies the employee has worked for.
- **TeamSize:**	Size of the team the employee is part of.
- **NumReports:**	Number of people reported to by the employee (only applicable for Senior and Lead levels).
- **EduLevel:**	Highest level of education achieved by the employee (e.g., High School, Bachelor, Master, PhD).
- **haveOT:**	Indicator if the employee has overtime (True/False).
- **TrainingHoursPerYear:**	Number of hours of training received per year.
- **JobSatisfaction:**	Rating of job satisfaction (scale from 1 to 5).

Dataset ini bersifat dummy untuk simulasi analisis HR.

