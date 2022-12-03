CREATE OR REPLACE PROCEDURE PRODUCTO_ADD(
	NOMBRE_PIV IN PRODUCTO.NOMBRE%TYPE,
	STOCK_PIV IN PRODUCTO.STOCK%TYPE,
	VALOR_PIV IN PRODUCTO.VALOR%TYPE,
	IMAGEN_PIV IN PRODUCTO.IMAGEN%TYPE
)
IS 
	SKU_AUX NUMBER;
BEGIN 
	LOCK TABLE PRODUCTO IN ROW EXCLUSIVE MODE;
    
	SELECT NVL(MAX(ID_PRODUCTO)+1,1) INTO SKU_AUX FROM PRODUCTO;
    INSERT INTO PRODUCTO VALUES(SKU_AUX, UPPER(NOMBRE_PIV), STOCK_PIV, VALOR_PIV, IMAGEN_PIV);
    DBMS_OUTPUT.PUT_LINE('Producto ingresado con exito.');
    
	
	EXCEPTION
		WHEN DUP_VAL_ON_INDEX THEN
			DBMS_OUTPUT.PUT_LINE('Se actualizará el stock del producto ingresado.');
			UPDATE PRODUCTO SET STOCK = STOCK + STOCK_PIV WHERE ID_PRODUCTO = SKU_AUX;
			DBMS_OUTPUT.PUT_LINE('Stock actualizado con exito');
			ROLLBACK;
END;


CREATE OR REPLACE PROCEDURE PRODUCTO_DELETE(
	SKU_PEV IN PRODUCTO.ID_PRODUCTO%TYPE
)
IS		
	CONTADOR NUMBER;
	PRODUCTO_EXISTENTE NUMBER;
	EXISTENCIA EXCEPTION;	
    
BEGIN
	SELECT COUNT(*) INTO PRODUCTO_EXISTENTE FROM PRODUCTO P WHERE SKU_PEV = P.ID_PRODUCTO;
    SELECT COUNT(*) INTO CONTADOR FROM PRODUCTO P WHERE SKU_PEV = P.ID_PRODUCTO;
    
	IF PRODUCTO_EXISTENTE = 1 THEN
		FOR I IN 1 .. (CONTADOR) LOOP	
			DELETE FROM PRODUCTO WHERE ID_PRODUCTO = SKU_PEV;
		DBMS_OUTPUT.PUT_LINE('PRODUCTO eliminado correctamente.');	
		END LOOP;
	
	ELSE
		RAISE EXISTENCIA;
	END IF;
	
	EXCEPTION
		WHEN EXISTENCIA THEN
			DBMS_OUTPUT.PUT_LINE('No hay regristro de es PRODUCTO en la base de datos.');
			ROLLBACK;
END;


CREATE OR REPLACE PROCEDURE PRODUCTO_UPDATE(
	SKU_PAS IN PRODUCTO.ID_PRODUCTO%TYPE,
	CANTIDAD_PAS IN PRODUCTO.STOCK%TYPE
)

IS
	CANTIDAD_AUX NUMBER;
	
BEGIN
	LOCK TABLE PRODUCTO IN ROW EXCLUSIVE MODE;
    
	IF CANTIDAD_PAS >=1 THEN
		SELECT STOCK INTO CANTIDAD_AUX FROM PRODUCTO WHERE ID_PRODUCTO = SKU_PAS;
		DBMS_OUTPUT.PUT_LINE('Stock actual: '|| CANTIDAD_AUX);
		CANTIDAD_AUX := CANTIDAD_AUX + CANTIDAD_PAS;
		UPDATE PRODUCTO SET STOCK = STOCK + CANTIDAD_PAS WHERE ID_PRODUCTO = SKU_PAS;
		DBMS_OUTPUT.PUT_LINE('Stock actualizado: '|| CANTIDAD_AUX);
		COMMIT;
	ELSE 
		SELECT STOCK INTO CANTIDAD_AUX FROM PRODUCTO WHERE ID_PRODUCTO = SKU_PAS;
		IF (CANTIDAD_AUX + CANTIDAD_PAS)> 0 THEN
			DBMS_OUTPUT.PUT_LINE('Stock actual: '|| CANTIDAD_AUX);
			CANTIDAD_AUX := CANTIDAD_AUX + CANTIDAD_PAS;
			UPDATE PRODUCTO SET STOCK = CANTIDAD_AUX WHERE ID_PRODUCTO = SKU_PAS;
			DBMS_OUTPUT.PUT_LINE('Stock actualizado: '|| CANTIDAD_AUX);
		ELSE 
			DBMS_OUTPUT.PUT_LINE('Cantidad invalida.');
		END IF;
	END IF;

END;


