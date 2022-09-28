% Autor: LUIS INOSTROZA FLORES
% Fecha: 17-01-2020


%-------------- EJERCICIO1 ------------------

%1) duplicar cola
duplicar([],[]).
duplicar([C|L1],[C,C|L2]):- duplicar(L1,L2).

% aqui a�adimos el frente que esta en el enunciado para obtener el
% ultimo elemento
frente([]):-write("error").
frente(C):-frente(C,R),write(R).
frente([E|C],E).

%2) obtener el ultimo elemento de la cola
fondo([F|C],S) :- invertir([F|C],Aux), frente(Aux,S).

%3) invertir cola (hacemos uso de concatenar)
invertir([],[]).
invertir([E|Aux],C):- invertir(Aux,Res),concatenar(Res,[E],C).

%4) concatenar listas (en la prueba pusimos unos axiomas extras)
concatenar([],C,C).
concatenar([X|C1],C2,[X|C3]):- concatenar(C1,C2,C3).

% ------------- EJERCICIO2 -------------------

%4) eliminar todas las ocurrencias de una lista
eliminarOcurrencias(_,[],[]).
eliminarOcurrencias(X,[X|L],R):-eliminarOcurrencias(X,L,R).
eliminarOcurrencias(X,[Y|L1],[Z|L2]):-eliminarOcurrencias(X,Y,Z),eliminarOcurrencias(X,L1,L2).
eliminarOcurrencias(_,Atom,Atom).

%1) determinar si un elemento pertenece a una lista
pertenece(X,[X|_]).
pertenece(X,[_|L]):-pertenece(X,L).

%2) determinar la posicion de un elemento en una lista (ARREGLADO)
posicion(1,[A|_],A).
posicion(N,[_|B],A):- Aux is N-1, posicion(Aux,B,A).

%3) numero de repeticiones de un elemento en una lista (ARREGLADO)
repeticiones([],_,0):-!.
repeticiones([L|L1],X,R):-repeticiones(L1,X,R1),L=:=X,R is R1+1,!.
repeticiones([_|L1],X,R):-repeticiones(L1,X,R).

%5) determinar si 2 listas son iguales (ARREGLADO)
iguales([M|N],[P|Q]) :- M=P, iguales(N,Q).
iguales(M,N) :- M=[], N=[].

