-- Veritabanı Yönetim Sistemleri Dersi Uygulaması
CREATE TABLE Students (
    StudentID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Department VARCHAR(50)
);

CREATE TABLE Books (
    BookID INT PRIMARY KEY,
    Title VARCHAR(100),
    Author VARCHAR(100),
    StockCount INT
);

CREATE TABLE BorrowedBooks (
    BorrowID INT PRIMARY KEY,
    StudentID INT,
    BookID INT,
    BorrowDate DATE,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (BookID) REFERENCES Books(BookID)
);

INSERT INTO Students VALUES (1, 'Ahmet', 'Yılmaz', 'Software Engineering');
INSERT INTO Books VALUES (101, 'Introduction to Algorithms', 'Thomas H. Cormen', 5);


SELECT s.FirstName, s.LastName, b.Title 
FROM BorrowedBooks bb
JOIN Students s ON bb.StudentID = s.StudentID
JOIN Books b ON bb.BookID = b.BookID;
