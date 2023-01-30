PAGINA WEB "TRAVISTOCK" PARA STOCK DE INVENTARIO A UTILIZAR EN NEGOCIOS

dependencias:

1.- pip install flask
2.- pip install Flask-Login
3.- pip install cx-Oracle


oracle:

abrir SQL PLUS escribir:
1.- SHOW USER
2.- ALTER SESSION SET "_ORACLE_SCRIPT" = TRUE;  
3.- CREATE USER "TRAVIS" IDENTIFIED BY "1234";
4.- GRANT DBA TO "TRAVIS";

En la terminal tiene que ir el ; si no tira error.

NAME = SYSTEM
PASS = your system pass

