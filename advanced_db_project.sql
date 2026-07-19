-- Veritabanı Sistemleri Tasarımı ve Optimizasyonu Projesi
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Products (
    ProductID INT PRIMARY KEY AUTO_INCREMENT,
    ProductName VARCHAR(100) NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    StockQuantity INT NOT NULL
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY AUTO_INCREMENT,
    CustomerID INT,
    OrderDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    TotalAmount DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE CASCADE
);

CREATE TABLE OrderItems (
    OrderItemID INT PRIMARY KEY AUTO_INCREMENT,
    OrderID INT,
    ProductID INT,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(10, 2),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);
CREATE VIEW View_Sales_Summary AS
SELECT 
    o.OrderID,
    c.FirstName,
    c.LastName,
    o.OrderDate,
    o.TotalAmount
FROM Orders o
JOIN Customers c ON o.CustomerID = c.CustomerID;

DELIMITER //
CREATE TRIGGER After_OrderItem_Insert
AFTER INSERT ON OrderItems
FOR EACH ROW
BEGIN
    UPDATE Products 
    SET StockQuantity = StockQuantity - NEW.Quantity
    WHERE ProductID = NEW.ProductID;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE Sp_Create_New_Order(
    IN p_CustomerID INT,
    IN p_ProductID INT,
    IN p_Qty INT
)
BEGIN
    DECLARE v_ProductPrice DECIMAL(10,2);
    DECLARE v_OrderID INT;
    

    SELECT Price INTO v_ProductPrice FROM Products WHERE ProductID = p_ProductID;
    
    INSERT INTO Orders (CustomerID, TotalAmount) VALUES (p_CustomerID, (v_ProductPrice * p_Qty));
    SET v_OrderID = LAST_INSERT_ID();
        INSERT INTO OrderItems (OrderID, ProductID, Quantity, UnitPrice) 
    VALUES (v_OrderID, p_ProductID, p_Qty, v_ProductPrice);
    
    SELECT 'Sipariş başarıyla oluşturuldu, stok güncellendi.' AS Status;
END //
DELIMITER ;
