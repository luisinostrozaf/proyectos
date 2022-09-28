-- Autor: Luis Inostroza
DROP TABLE PELICULA;
DROP TABLE CINE;

CREATE TABLE PELICULA(
	ID_PELICULA VARCHAR2(20) NOT NULL,
	ID_ACTOR VARCHAR2(20),
	NOMBRE_PELICULA VARCHAR2(100),
	PRESUPUESTO NUMBER,
	FECHA_ESTRENO VARCHAR2(50)
);

CREATE TABLE CINE(
	ID_CINE VARCHAR2(20) NOT NULL,
	ID_PELICULA VARCHAR2(20),
	NOMBRE_CINE VARCHAR2(100),
	DIRECCION VARCHAR2(200)
);

ALTER TABLE PELICULA ADD CONSTRAINT PK_PELICULA PRIMARY KEY (ID_PELICULA);
ALTER TABLE CINE ADD CONSTRAINT PK_CINE PRIMARY KEY (ID_CINE);

ALTER TABLE CINE ADD CONSTRAINT FK_CINE FOREIGN KEY (ID_PELICULA) REFERENCES PELICULA(ID_PELICULA);

SELECT * FROM PELICULA;
SELECT * FROM CINE;

---PROCEDIMIENTO PARA LA INSERCION DE UNA PELICULA---

CREATE OR REPLACE PROCEDURE INSERTAR_PELICULA(
	ID_PELI IN PELICULA.ID_PELICULA%TYPE,
	ID_ACT IN PELICULA.ID_ACTOR%TYPE,
	NOMBRE_PELI IN PELICULA.NOMBRE_PELICULA%TYPE,
	PRESUP IN PELICULA.PRESUPUESTO%TYPE,
	FECHA_EST IN PELICULA.FECHA_ESTRENO%TYPE	
)
IS 
	SOBRE_PRESUPUESTO EXCEPTION;
	PELICULA_ESTA EXCEPTION;
	CONTADOR_PELI NUMBER;

BEGIN
	
	LOCK TABLE PELICULA IN ROW EXCLUSIVE MODE;
	IF PRESUP < 50000000 THEN
		SELECT COUNT(*) INTO CONTADOR_PELI FROM PELICULA WHERE ID_PELICULA = ID_PELI;
		IF CONTADOR_PELI = 0 THEN
			INSERT INTO PELICULA  VALUES(ID_PELI, ID_ACT, NOMBRE_PELI, PRESUP, FECHA_EST);
			COMMIT;
			DBMS_OUTPUT.PUT_LINE('LA PELICULA HA SIDO INGRESADA CORRECTAMENTE');
		ELSE
			RAISE PELICULA_ESTA;
		END IF;
	
	ELSE
		RAISE SOBRE_PRESUPUESTO;
	END IF;

	EXCEPTION
		WHEN PELICULA_ESTA THEN
			DBMS_OUTPUT.PUT_LINE('EL ID DE LA PELICULA YA SE ENCUENTRA REGISTRADO');
			ROLLBACK;
		WHEN SOBRE_PRESUPUESTO THEN
			DBMS_OUTPUT.PUT_LINE('LA PELICULA EXCEDE EL PRESUPUESTO PERMITIDO');
			ROLLBACK;

			
END;

BEGIN
	INSERTAR_PELICULA('5001','1','HARRY EL SUCIO POTTER 2',233565,'HOLASHAS');
END;

---PROCEDIMIENTO PARA INCERSION DE CINE---

CREATE OR REPLACE PROCEDURE INSERTAR_CINE(
    ID_CIN IN CINE.ID_CINE%TYPE,
    ID_PEL IN CINE.ID_PELICULA%TYPE,
    NOMBRE_CIN IN CINE.NOMBRE_CINE%TYPE,
    DIRE IN CINE.DIRECCION %TYPE
)
IS 
    CINE_ESTA EXCEPTION;
    CONTADOR_CINE NUMBER;
   	MISMO_NOMBRE EXCEPTION;

BEGIN

    LOCK TABLE CINE IN ROW EXCLUSIVE MODE;
        SELECT COUNT(*) INTO CONTADOR_CINE FROM CINE WHERE ID_CINE = ID_CIN;
        IF CONTADOR_CINE = 0 THEN
            INSERT INTO CINE  VALUES(ID_CIN, ID_PEL, NOMBRE_CIN, DIRE);
            COMMIT;
            DBMS_OUTPUT.PUT_LINE('EL CINE HA SIDO INGRESADO');
        ELSE
            RAISE CINE_ESTA;
        END IF;

    EXCEPTION
        WHEN CINE_ESTA THEN
            DBMS_OUTPUT.PUT_LINE('EL ID DEL CINE YA SE ENCUENTRA REGISTRADO');
            ROLLBACK;

END;

BEGIN
	INSERTAR_CINE('1','1','CINE LAS PELOTAS','SAN MIGUEL 777');
END;



---PROCEDIMIENTO PARA LA ACTUALIZACION DE UNA PELICULA---

CREATE OR REPLACE PROCEDURE ACTUALIZAR_PELICULA(
	ID_PELI IN PELICULA.ID_PELICULA%TYPE,
	ID_ACT IN PELICULA.ID_ACTOR%TYPE,
	NOMBRE_PELI IN PELICULA.NOMBRE_PELICULA%TYPE,
	PRESUP IN PELICULA.PRESUPUESTO%TYPE,
	FECHA_EST IN PELICULA.FECHA_ESTRENO%TYPE	
)
IS 
	SOBRE_PRESUPUESTO EXCEPTION;

BEGIN
	
	LOCK TABLE PELICULA IN ROW EXCLUSIVE MODE;

	IF PRESUP < 50000000 THEN
		UPDATE PELICULA
		SET ID_ACTOR = ID_ACT,
			NOMBRE_PELICULA = NOMBRE_PELI,
			PRESUPUESTO = PRESUP,
			FECHA_ESTRENO = FECHA_EST
		WHERE ID_PELICULA = ID_PELI;
		COMMIT;
		DBMS_OUTPUT.PUT_LINE('LA PELICULA HA SIDO ACTUALIZADA CORRECTAMENTE');

	ELSE
		RAISE SOBRE_PRESUPUESTO;
	END IF;

	EXCEPTION
		WHEN SOBRE_PRESUPUESTO THEN
			DBMS_OUTPUT.PUT_LINE('LA PELICULA EXCEDE EL PRESUPUESTO PERMITIDO');
			ROLLBACK;		
END;

BEGIN
	ACTUALIZAR_PELICULA('1','1','EL HOMBRE QUE ARA�A',3000000,'25/10/2012');
END;

---PROCEDIMIENTO PARA LA ACTUALIZACION DE CINE---

CREATE OR REPLACE PROCEDURE ACTUALIZAR_CINE(
    ID_CIN IN CINE.ID_CINE%TYPE,
    ID_PEL IN CINE.ID_PELICULA%TYPE,
    NOMBRE_CIN IN CINE.NOMBRE_CINE%TYPE,
    DIRE IN CINE.DIRECCION %TYPE	
)
IS 
	NO_EXISTE EXCEPTION;
	CONTADOR_CINE NUMBER;

BEGIN
	
    LOCK TABLE CINE IN ROW EXCLUSIVE MODE;
        SELECT COUNT(*) INTO CONTADOR_CINE FROM CINE WHERE ID_CINE = ID_CIN;
        IF CONTADOR_CINE != 0 THEN
        	UPDATE CINE 
        	SET	NOMBRE_CINE = NOMBRE_CIN,
        		DIRECCION = DIRE
        	WHERE ID_CINE = ID_CIN;
        	DBMS_OUTPUT.PUT_LINE('EL CINE HA SIDO ACTUALIZADO CORRECTAMENTE');
        	COMMIT;

	ELSE
		RAISE NO_EXISTE;
	END IF;

	EXCEPTION
		WHEN NO_EXISTE THEN
			DBMS_OUTPUT.PUT_LINE('EL CINE NO SE ENCUENTRA REGISTRADO');
			ROLLBACK;		
END;

BEGIN
	ACTUALIZAR_CINE('3','3','EL HOMBRE QUE ARA�A','CHUPALO CLAUDIO');
END;

---PROCEDIMIENTO PARA ELIMINACION DE UNA PELICULA---

CREATE OR REPLACE PROCEDURE ELIMINAR_PELICULA(
	ID_PELI IN PELICULA.ID_PELICULA%TYPE,
	ID_ACT IN PELICULA.ID_ACTOR%TYPE	
)
IS
	ID_NOEXISTE EXCEPTION;
	CONTADOR2_CINE NUMBER;
	CONTADOR2_PELI NUMBER;

	
BEGIN
	LOCK TABLE CINE IN ROW EXCLUSIVE MODE;
	SELECT COUNT(*) INTO CONTADOR2_CINE FROM PELICULA WHERE ID_PELICULA = ID_PELI;
	IF CONTADOR2_CINE != 0 THEN
		DELETE FROM CINE
		WHERE CINE.ID_PELICULA = ID_PELI;
		COMMIT;
	ELSE
		RAISE ID_NOEXISTE;
	END IF;
	
	LOCK TABLE PELICULA IN ROW EXCLUSIVE MODE;
	SELECT COUNT(*) INTO CONTADOR2_PELI FROM PELICULA WHERE ID_PELICULA = ID_PELI;
	IF CONTADOR2_PELI != 0 THEN
		DELETE FROM PELICULA 
		WHERE PELICULA.ID_PELICULA = ID_PELI;
		DBMS_OUTPUT.PUT_LINE('LA PELICULA HA SIDO ELIMINADA EXITOSAMENTE');
		COMMIT;
	ELSE
		RAISE ID_NOEXISTE;
	END IF;

	EXCEPTION
		WHEN ID_NOEXISTE THEN
			DBMS_OUTPUT.PUT_LINE('LA PELICULA NO SE ENCUENTRA REGISTRADA');
			ROLLBACK;
			
END;

BEGIN
	ELIMINAR_PELICULA('4','4');
	
END;

---PROCEDIMIENTO PARA LA ELIMINACION DE UN CINE---

CREATE OR REPLACE PROCEDURE ELIMINAR_CINE(
	ID_CIN IN CINE.ID_CINE%TYPE	
)
IS
	ID_NOEXISTE EXCEPTION;
	CONTADOR_CINE NUMBER;

	
BEGIN

	LOCK TABLE CINE IN ROW EXCLUSIVE MODE;
	SELECT COUNT(*) INTO CONTADOR_CINE FROM CINE WHERE ID_CINE = ID_CIN;
	IF CONTADOR_CINE != 0 THEN
		DELETE FROM CINE
		WHERE CINE.ID_CINE = ID_CIN;
		DBMS_OUTPUT.PUT_LINE('EL CINE HA SIDO ELIMINADO EXITOSAMENTE');
		COMMIT;
	ELSE
		RAISE ID_NOEXISTE;
	END IF;

	EXCEPTION
		WHEN ID_NOEXISTE THEN
			DBMS_OUTPUT.PUT_LINE('EL CINE NO SE ENCUENTRA REGISTRADO');
			ROLLBACK;
			
END;

BEGIN
	ELIMINAR_CINE('3');
END;
