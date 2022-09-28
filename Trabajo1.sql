--Autor: Luis Inostroza Flores
--Ejercicio 1
select BusinessEntityID, FirstName, LastName, 
case
when PersonType ='SC' THEN 'Store Contact'
when PersonType ='IN' THEN 'Individual Customer'
when PersonType ='EM' THEN 'Employee'
when PersonType ='SP' THEN 'Sales Person'
when PersonType ='VC' THEN 'Vendor Contact'
when PersonType ='GC' THEN 'General Contact'
end as PersonTypeName from Person.Person

--Ejercicio 2
select
    Sales.SalesOrderHeader.CustomerID,
    Person.Person.LastName,
    Person.Person.FirstName,
    FORMAT(OrderDate, 'dd-MM-yy') as OrderDate, 
    FORMAT(DueDate, 'dd-MM-yy') as DueDate,
    FORMAT(ShipDate,'dd-MM-yy') as ShipDate,
    Production.Product.Name,
    CASE Status 
        WHEN 1 THEN 'In process'
        WHEN 2 THEN 'Aproved'
        WHEN 3 THEN 'Backordered'
        WHEN 4 THEN 'Rejected'
        WHEN 5 THEN 'Shipped'
        When 6 THEN 'Cancelled'
    end as Status,
    Sales.SalesOrderHeader.SalesOrderID
    SubTotal,
    TaxAmt,
    TotalDue
from Sales.SalesOrderHeader
INNER JOIN Sales.Customer ON Sales.SalesOrderHeader.CustomerID = Sales.Customer.CustomerID
INNER JOIN Sales.SalesOrderDetail ON Sales.SalesOrderHeader.SalesOrderID = Sales.SalesOrderDetail.SalesOrderID
INNER JOIN Production.Product ON Production.Product.ProductID = Sales.SalesOrderDetail.ProductID 
INNER JOIN Person.Person ON Sales.Customer.CustomerID = Person.Person.BusinessEntityID

--Ejercicio 3
select Name Nombre_Envio, count(*) Cantidad_productos, count (*)*100 / sum(count(*)) over() Porcentaje from Sales.SalesOrderHeader inner join Purchasing.ShipMethod
on Sales.SalesOrderHeader.ShipMethodID = Purchasing.ShipMethod.ShipMethodID group by Purchasing.ShipMethod.ShipMethodID, Purchasing.ShipMethod.Name

--Ejercicio 4
Select AVG(OrderQty) Promedio from Sales.SalesOrderDetail;

--Ejercicio 5
Select Name Nombre_Producto, ProductID Numero_ID from Production.Product where ProductID = any (Select ProductID from Sales.SalesOrderDetail group by ProductID);

--Ejercicio 6
Select Name Nombre_Producto, ProductID Numero_ID  from Production.Product where not ProductID = any (Select ProductID from Sales.SalesOrderDetail group by ProductID);

--Ejercicio 7
select sum(LineTotal) as  from  Sales.SalesOrderDetail group by SalesOrderID having sum(LineTotal)>5000

--Ejercicio 8
Select SalesOrderID, OrderDate , ShipDate, datediff(day,OrderDate, ShipDate) pp from Sales.SalesOrderHeader
select avg(DATEDIFF(day, orderDate, shipDate)) from Sales.SalesOrderHeader;

--Ejercicio 9
Select CONVERT(VARCHAR, ORDERDATE, 3) AS FECHA, CONVERT(VARCHAR, SHIPDATE, 6) AS FECHA FROM Sales.SalesOrderHeader;

--Ejercicio 10
select * from Sales.SalesOrderHeader where TotalDue > 1500 and (SalesPersonID = '279' or TerritoryID = '6');

--Ejercicio 11
Select FirstName Nombre_Cliente, Name Nombre_Producto from Person.Person INNER join Sales.Customer
on Person.Person.BusinessEntityID = Sales.Customer.CustomerID INNER join Sales.SalesOrderHeader
on Sales.Customer.CustomerID = Sales.SalesOrderHeader.CustomerID INNER join Sales.SalesOrderDetail
on Sales.SalesOrderHeader.SalesOrderID = Sales.SalesOrderDetail.SalesOrderID INNER join Production.Product
on Sales.SalesOrderDetail.ProductID = Production.Product.ProductID;