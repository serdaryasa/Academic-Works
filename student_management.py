# Nesne Yönelimli Programlama ve Algoritma Laboratuvarı Çalışması

class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
        self.grades = []

    def add_grade(self, grade):
        if 0 <= grade <= 100:
            self.grades.append(grade)
        else:
            print("Geçersiz not!")

    def calculate_average(self):
        if not self.grades:
            return 0
        return sum(self.grades) / len(self.grades)

if __name__ == "__main__":
    student1 = Student("Serdar", "2026001")
    student1.add_grade(85)
    student1.add_grade(90)
    student1.add_grade(78)

    print(f"Öğrenci: {student1.name}")
    print(f"Not Ortalama: {student1.calculate_average():.2f}")
