import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime
cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattandensrealtimedatabases-default-rtdb.firebaseio.com/"
})
ref=db.reference("Students")
last_time=datetime.datetime.now().isoformat()
print(last_time)
data={

    "001":
    {
        "Name":"MD OMAR HANIF",
        "Roll":"677791",
        "Staring_year":2017,
        "Total_Attendance":6,
        "Year":4,
        "Last_Attendance": last_time

    }
}

for key,value in data.items():
    ref.child(key).set(value)

