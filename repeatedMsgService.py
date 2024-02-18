from Vclass import Vclass
from datetime import datetime
import sched
import time

class repeatedMsgService:
    vclass = Vclass()
    scheduler = sched.scheduler(time.time, time.sleep)

    def get_time_difference(self,deadline):
        current_year = datetime.now().year
        current_month = datetime.now().month
        get_deadline = datetime.strptime(deadline, "%A, %d %B, %I:%M %p")

        if current_month <= 4 and get_deadline.month == 12:
            current_year -= 1
        get_deadline = get_deadline.replace(year=current_year)
        current_time = datetime.now()
        # current_time = datetime(year=2024,month=1,day=30,hour=00,minute=00) #for Testing
        time_difference = get_deadline - current_time
        return time_difference

    def get_assignment_to_notif(self):
        assignmentList = self.vclass.getAssigmentAreNotYetDue()
        # assignmentList = self.vclass.getAssignmentByTimeStamp("1706547600") #for Testing
        assignmentToNotif = []
        for i, course in enumerate(assignmentList):
            detail_course =  course.detail_course()

            time_difference = self.get_time_difference(detail_course.deadline)
            time_difference_minutes = time_difference.total_seconds() // 60
            time_difference_hour = time_difference.total_seconds() // 3600
            time_difference_days = time_difference.days

            if time_difference_minutes > 0 and time_difference_minutes <= 60: #check if under 1 hour
                    assignmentToNotif.append(course)
            elif time_difference_hour > 0 and 358 <= time_difference_minutes <= 360: # check deadline in 6 hour with tolerance 2 minute 
                    assignmentToNotif.append(course)
            elif time_difference_minutes > 0 and 372 <= time_difference_minutes <= 377: # check deadline in 6 hour 15 minute with tolerance 2 minute
                    assignmentToNotif.append(course)
            elif time_difference_minutes > 0 and 402 <= time_difference_minutes <= 407: # check deadline in 6 hour 45 minute with tolerance 2 minute
                    assignmentToNotif.append(course)
            elif time_difference_minutes > 0 and 1453 <= time_difference_minutes <= 1457: # check deadline in 12 hour 15 minute  with tolerance 2 minute
                    assignmentToNotif.append(course)
            elif time_difference_hour > 0 and 1438 <= time_difference_minutes <= 1442: # check deadline in 12 hour with tolerance 2 minute
                    assignmentToNotif.append(course)
            elif time_difference_minutes > 0 and 1483 <= time_difference_minutes <= 1487: # check deadline in 12 hour 45 minutewith tolerance 2 minute
                    assignmentToNotif.append(course)
        return assignmentToNotif
    
    def get_message(self):
        assignment_list = self.get_assignment_to_notif()
        if assignment_list != []:
              message = ""
              message += "***INFORMASI***\n"
              message += "=======================================\n"
              message += "Terdapat Beberapa Event yang akan habis\n"
              message += "=======================================\n"
              for i,course in enumerate(assignment_list):
                    detail_course = course.detail_course()
                    time_difference = self.get_time_difference(detail_course.deadline)
                    text = ""
                    # text += f"[{i+1}]\n"
                    text += f"[***{course.title}***]\n"
                    text += f"Kursus: {detail_course.course_title}\n"
                    text += f"Deskripsi: {detail_course.description}\n"
                    text += f"Tenggat: {detail_course.deadline}\n"
                    text += f"Pengumpulan: {detail_course.assign_url}\n"
                    text += f"Akan Habis Dalam: {int(time_difference.total_seconds() // 3600)} Jam {int((time_difference.total_seconds() % 3600) / 60)} Menit\n"
                    text += f"===========================================\n"
                    message += f"\n{text}"
        else :
             message = ""
        return message
    