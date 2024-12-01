import os
import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
from fpdf import FPDF
import datetime
from PIL import Image, ImageTk  


USERNAME = "anusha"
PASSWORD = "123456"


file_path = "projectt.csv"


def create_empty_csv(file_path):
    if not os.path.isfile(file_path):
        columns = ['studentname', 'subjectname', 'semesterno', 'grade']
        empty_df = pd.DataFrame(columns=columns)
        empty_df.to_csv(file_path, index=False)
        print(f"Created a new CSV file with columns: {columns} at {file_path}")
    else:
        print(f"Using existing CSV file: {file_path}")

class StudentGradesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f4f7")

        
        create_empty_csv(file_path)

        
        self.bg_image = Image.open("login.jpg")  
        self.bg_image = self.bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        
        self.bg_label = tk.Label(root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)  

       
        login_frame = tk.Frame(root, bg="#e9f3fb", bd=2, relief="ridge")
        login_frame.pack(expand=True, padx=20, pady=20)
        tk.Label(login_frame, text="Login", font=("Arial", 16, "bold"), bg="#e9f3fb").pack(pady=10)

        
        tk.Label(login_frame, text="Username:", bg="#e9f3fb").pack(pady=5)
        self.username_entry = tk.Entry(login_frame, width=30, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        
        tk.Label(login_frame, text="Password:", bg="#e9f3fb").pack(pady=5)
        self.password_entry = tk.Entry(login_frame, show="*", width=30, font=("Arial", 12))
        self.password_entry.pack(pady=5)

       
        login_button = tk.Button(login_frame, text="Login", command=self.login, bg="#4CAF50", fg="white", width=15, font=("Arial", 12))
        login_button.pack(pady=20)
        self.add_hover_effect(login_button)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == USERNAME and password == PASSWORD:
            self.user_name = username
            self.log_user_activity("Login successful")
            self.open_dashboard_page()  
            self.root.withdraw() 
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def open_dashboard_page(self):
        dashboard_window = tk.Toplevel(self.root)
        dashboard_window.title("Dashboard")
        dashboard_window.geometry("700x500")
        dashboard_window.configure(bg="#f7f9fb")

        
        self.bg_label_dashboard = tk.Label(dashboard_window, image=self.bg_photo)
        self.bg_label_dashboard.place(relwidth=1, relheight=1)

       
        header = tk.Frame(dashboard_window, bg="#dce3f0", bd=2, relief="solid")
        header.pack(fill="x", pady=10)

        
        self.df = pd.read_csv(file_path)
        total_students = len(self.df['studentname'].unique())

        
        tk.Label(dashboard_window, text=f"Total Students: {total_students}", font=("Arial", 12)).pack(pady=10)

        
        search_button = tk.Button(dashboard_window, text="Go to Search", command=self.open_search_page, bg="#4CAF50", fg="white", width=15, font=("Arial", 12))
        search_button.pack(pady=20)
        self.add_hover_effect(search_button)

        
        tk.Button(dashboard_window, text="Log Activity", command=self.view_activity_log, bg="#2196F3", fg="white", width=15, font=("Arial", 12)).pack(pady=10)

    def open_search_page(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Student Grades Search")
        search_window.geometry("700x500")
        search_window.configure(bg="#f7f9fb")

        
        self.bg_label_search = tk.Label(search_window, image=self.bg_photo)
        self.bg_label_search.place(relwidth=1, relheight=1)

        
        header = tk.Frame(search_window, bg="#dce3f0", bd=2, relief="solid")
        header.pack(fill="x", pady=10)
        
       
        self.marquee_text = "Welcome to the Student Grades Portal! "
        self.marquee_label = tk.Label(header, text=self.marquee_text, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white")
        self.marquee_label.pack(fill='x')
        
       
        self.marquee_text = self.marquee_text + " " * 20 
        self.move_marquee()

        
        form_frame = tk.Frame(search_window, bg="#e9f3fb", bd=2, relief="ridge")
        form_frame.pack(pady=20, padx=20, fill="x")
        tk.Label(form_frame, text="Student Name:", bg="#e9f3fb").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.student_name_entry = tk.Entry(form_frame, width=30, font=("Arial", 12))
        self.student_name_entry.grid(row=0, column=1, padx=10, pady=10)
        tk.Label(form_frame, text="Semester No:", bg="#e9f3fb").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.semester_no_entry = tk.Entry(form_frame, width=30, font=("Arial", 12))
        self.semester_no_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(form_frame, text="Search", command=self.search, bg="#2196F3", fg="white", width=15, font=("Arial", 12)).grid(row=2, columnspan=2, pady=15)

        
        self.result_frame = tk.Frame(search_window, bg="white", bd=2, relief="solid")
        self.result_frame.pack(pady=20, padx=20, fill="both", expand=True)

       
        save_button = tk.Button(search_window, text="Save as PDF", command=self.save_as_pdf, bg="#4CAF50", fg="white", width=15, font=("Arial", 12))
        save_button.pack(pady=10)
        self.add_hover_effect(save_button)

    def move_marquee(self):
        self.marquee_text = self.marquee_text[1:] + self.marquee_text[0]
        self.marquee_label.config(text=self.marquee_text)
        self.marquee_label.after(300, self.move_marquee)  

    def add_hover_effect(self, widget):
        def on_enter(event):
            widget['bg'] = "#45a049"  
        def on_leave(event):
            widget['bg'] = "#4CAF50"  
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def search(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        student_name = self.student_name_entry.get().strip()
        semester_no = self.semester_no_entry.get().strip()

        if not student_name and not semester_no:
            messagebox.showwarning("Input Required", "Please enter either Student Name, Semester No, or both.")
            return

        try:
            create_empty_csv(file_path)
            self.df = pd.read_csv(file_path)
            self.df.columns = self.df.columns.str.strip().str.lower()

            query = pd.Series([True] * len(self.df))
            if student_name:
                query &= self.df['studentname'].str.lower() == student_name.lower()
            if semester_no:
                query &= self.df['semesterno'] == int(semester_no)

            self.search_result = self.df[query]

            if self.search_result.empty:
                messagebox.showinfo("No Results", "No records found for the given criteria.")
                return

            
            tk.Label(self.result_frame, text="Student Name", bg="#dce3f0", font=("Arial", 10, "bold"), width=20, borderwidth=2, relief="solid").grid(row=0, column=0, padx=1, pady=1)
            tk.Label(self.result_frame, text="Semester No", bg="#dce3f0", font=("Arial", 10, "bold"), width=15, borderwidth=2, relief="solid").grid(row=0, column=1, padx=1, pady=1)
            tk.Label(self.result_frame, text="Subject Name", bg="#dce3f0", font=("Arial", 10, "bold"), width=25, borderwidth=2, relief="solid").grid(row=0, column=2, padx=1, pady=1)
            tk.Label(self.result_frame, text="Grade", bg="#dce3f0", font=("Arial", 10, "bold"), width=10, borderwidth=2, relief="solid").grid(row=0, column=3, padx=1, pady=1)

            
            for idx, row in self.search_result.iterrows():
                tk.Label(self.result_frame, text=row['studentname'], font=("Arial", 10), width=20, borderwidth=2, relief="solid").grid(row=idx + 1, column=0, padx=1, pady=1)
                tk.Label(self.result_frame, text=row['semesterno'], font=("Arial", 10), width=15, borderwidth=2, relief="solid").grid(row=idx + 1, column=1, padx=1, pady=1)
                tk.Label(self.result_frame, text=row['subjectname'], font=("Arial", 10), width=25, borderwidth=2, relief="solid").grid(row=idx + 1, column=2, padx=1, pady=1)
                tk.Label(self.result_frame, text=row['grade'], font=("Arial", 10), width=10, borderwidth=2, relief="solid").grid(row=idx + 1, column=3, padx=1, pady=1)

        except Exception as e:
            messagebox.showerror("Error", f"Error while searching: {str(e)}")

    def save_as_pdf(self):
        try:
          
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            
            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, "Student Grades Report", ln=True, align="C")
            pdf.ln(10)

           
            pdf.set_font("Arial", "B", 12)
            pdf.cell(50, 10, "Student Name", border=1, align="C")
            pdf.cell(30, 10, "Semester No", border=1, align="C")
            pdf.cell(80, 10, "Subject Name", border=1, align="C")
            pdf.cell(30, 10, "Grade", border=1, align="C")
            pdf.ln()

            
            pdf.set_font("Arial", size=12)
            last_student = None 

            for idx, row in self.search_result.iterrows():
               
                if row['studentname'] != last_student:
                    pdf.cell(50, 10, row['studentname'], border=1, align="C")
                    last_student = row['studentname']
                else:
                    pdf.cell(50, 10, "", border=1, align="C")  

                pdf.cell(30, 10, str(row['semesterno']), border=1, align="C")
                pdf.cell(80, 10, row['subjectname'], border=1, align="C")
                pdf.cell(30, 10, str(row['grade']), border=1, align="C")
                pdf.ln()

           
            total_grade = self.search_result['grade'].astype(float).sum()
            avg_grade = total_grade / len(self.search_result)
            pdf.ln(10)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(200, 10, f"Average Grade: {avg_grade:.2f}", ln=True, align="C")

            
            save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
            if save_path:
                pdf.output(save_path)
                messagebox.showinfo("Success", "PDF saved successfully.")
            else:
                messagebox.showwarning("No file selected", "Please select a location to save the file.")

        except Exception as e:
            messagebox.showerror("Error", f"Error saving PDF: {str(e)}")

    def log_user_activity(self, activity):
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {activity} by {self.user_name}\n"
        with open("activity_log.txt", "a") as log_file:
            log_file.write(log_message)

    def view_activity_log(self):
        
        try:
            with open("activity_log.txt", "r") as log_file:
                log_content = log_file.read()
            log_window = tk.Toplevel(self.root)
            log_window.title("Activity Log")
            log_window.geometry("600x400")
            log_text = tk.Text(log_window, wrap="word", height=20, width=70)
            log_text.insert("1.0", log_content)
            log_text.config(state="disabled")
            log_text.pack(padx=10, pady=10)
        except FileNotFoundError:
            messagebox.showwarning("No Activity Log", "No activity log file found.")


root = tk.Tk()
app = StudentGradesApp(root)
root.mainloop()