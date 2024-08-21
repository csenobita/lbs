import io
from tkinter import Tk, Frame, LabelFrame, Entry, Button, Checkbutton, StringVar, filedialog, Label
from PIL import Image, ImageTk
import firebase_admin
from firebase_admin import credentials, storage, db
import datetime

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattandensrealtimedatabases-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattandensrealtimedatabases.appspot.com"  # Ensure the bucket name is correct
})

# Initialize references
ref = db.reference("Students")
bucket = storage.bucket()  # Ensure this is defined

# Initialize Tkinter
root1 = Tk()
root1.title("Student Page")

# Initialize Tkinter Variables after root window is created
student_name_reg_page_var = StringVar()
student_roll_reg_page_var = StringVar()
student_reg_number_page_var = StringVar()
student_email_reg_page_var = StringVar()
student_mobile_reg_page_var = StringVar()
student_college_name_reg_page_var = StringVar()
student_address_reg_page_var = StringVar()
img = None

def create_entry(frame, label_text, x, y, font, text_variable):
    label_frame = LabelFrame(frame, text=label_text, font=font, width=280, height=45, bd=0, fg="black", bg="cyan")
    label_frame.place(x=x, y=y)
    entry = Entry(label_frame, font=font, bd=0, width=30, textvariable=text_variable)
    entry.place(x=2, y=1)
    return entry

def student_reg_page_data_fill_example():
    # Define what happens when the checkbox is checked
    pass

def upload_image():
    global img
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
        img = Image.open(file_path)
        img = img.resize((200, 200))  # Resize image if needed
        img_tk = ImageTk.PhotoImage(img)

        image_label.config(image=img_tk)
        image_label.image = img_tk

def upload_image_to_firebase():
    if img:
        try:
            # Save image to a BytesIO object
            image_io = io.BytesIO()
            img.save(image_io, format='PNG')
            image_io.seek(0)

            # Create a unique filename for the image
            roll_number = student_roll_reg_page_var.get()
            if not roll_number:
                print("Roll number is not provided. Image not uploaded.")
                return None

            blob = bucket.blob(f'photos/{roll_number}.png')
            blob.upload_from_file(image_io, content_type='image/png')
            blob.make_public()

            return blob.public_url
        except Exception as e:
            print(f"Error uploading image to Firebase: {e}")
            return None
    return None

def database_student_reg_page():
    try:
        image_url = upload_image_to_firebase()
        print(f"Image URL: {image_url}")

        data = {
            student_roll_reg_page_var.get(): {
                "Name": student_name_reg_page_var.get(),
                "Roll": student_roll_reg_page_var.get(),
                "Reg_Number": student_reg_number_page_var.get(),
                "Email": student_email_reg_page_var.get(),
                "Phone": student_mobile_reg_page_var.get(),
                "College_name": student_college_name_reg_page_var.get(),
                "Address": student_address_reg_page_var.get(),
                "Last_Attendance": datetime.datetime.now().isoformat(),
                "Image_URL": image_url  # Save the image URL
            }
        }

        ref.update(data)
        print("Data pushed to Firebase")
    except Exception as e:
        print(f"Error pushing data to Firebase: {e}")

def main():
    global image_label

    min_window_size_wh = 700
    min_window_size_ht = 400
    root1.geometry(f"{min_window_size_wh}x{min_window_size_ht}+600+200")
    root1.resizable(False, False)

    lable2_frame = Frame(root1, bg="cyan", width=min_window_size_wh, height=min_window_size_ht)
    lable2_frame.pack()

    student_lable_frame = LabelFrame(lable2_frame, text="Student Reg:", width=min_window_size_wh,
                                     height=min_window_size_ht, bd=8, bg="cyan", fg="green", font=("Arial", 14))
    student_lable_frame.place(x=0, y=0)

    student_check_button = Checkbutton(student_lable_frame, text="Fill Data", font=("Arial", 14),
                                       command=student_reg_page_data_fill_example, bd=0, activebackground="cyan",
                                       bg='cyan')
    student_check_button.place(x=10, y=345)

    # Entry Widgets
    create_entry(student_lable_frame, "Student Name", 10, 5, ("Arial", 14), student_name_reg_page_var)
    create_entry(student_lable_frame, "Roll Number", 10, 50, ("Arial", 14), student_roll_reg_page_var)
    create_entry(student_lable_frame, "Reg Number", 10, 100, ("Arial", 14), student_reg_number_page_var)
    create_entry(student_lable_frame, "Email", 10, 150, ("Arial", 14), student_email_reg_page_var)
    create_entry(student_lable_frame, "Mobile Number", 10, 200, ("Arial", 14), student_mobile_reg_page_var)
    create_entry(student_lable_frame, "College Name", 10, 250, ("Arial", 14), student_college_name_reg_page_var)
    create_entry(student_lable_frame, "Address", 10, 300, ("Arial", 14), student_address_reg_page_var)

    # Divider
    student_bd_1_2 = LabelFrame(student_lable_frame, bd=8, width=5, height=380, bg="cyan")
    student_bd_1_2.place(x=300, y=-8)

    # Signup Button
    student_sign_up_button = Button(student_lable_frame, text='Student Sign Up', command=database_student_reg_page,
                                    fg="green", bg="cyan", activebackground="green", cursor="hand2")
    student_sign_up_button.place(x=410, y=330)

    # Image Upload Button
    upload_button = Button(student_lable_frame, text="Upload Image", command=upload_image, fg="green", bg="cyan",
                           cursor="hand2")
    upload_button.place(x=415, y=300)

    # Image Display Label
    image_label = Label(student_lable_frame, bg="cyan")
    image_label.place(x=400, y=10, width=200, height=200)

    root1.mainloop()

if __name__ == "__main__":
    main()
