from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_login import current_user, login_user, logout_user
from flask_login import LoginManager

# Connection BD
from config import connection 
# Models:
from authentication.ModelSeller import Admin, Seller
from authentication import autenticacion_bp, autentication_bp

app = Flask(__name__)
login_manager = LoginManager(app)
app.config['SECRET_KEY'] = 'HolaMundo'


@login_manager.user_loader
def load_user(rut):
    curs = connection.cursor()
    curs.execute('SELECT RUT_ADMIN, NOMBRE, EMAIL, CONTRASEÑA FROM ADMINISTRADOR WHERE RUT_ADMIN =: RUT_ADMIN', [rut])
    res = curs.fetchone()
    if (res == None):
        return None
    else:
        return Admin(res[0],res[1])

@autenticacion_bp.route('/login', methods=['POST','GET'])
def loginAdmin():
    if current_user.is_authenticated:
        return redirect(url_for('prodsRegistrados'))
    else:
        if request.method == "POST":
            rut = request.form["rut"]
            passwd = request.form["pswd"]
            cur = connection.cursor()
            cur.execute('SELECT RUT_ADMIN, CONTRASEÑA FROM ADMINISTRADOR a WHERE RUT_ADMIN =: rutForm AND CONTRASEÑA =: passForm', [rut, passwd])
            res = cur.fetchone()
            if res == None:
                flash('invalid password or username.', 'warning')
            else:
                login_user(Admin(res[0],res[1]))
                session['adminSession'] = rut
                return redirect(url_for('prodsRegistrados'))
    return render_template('/auth/login.html')

@autenticacion_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('autenticacion.loginAdmin'))

app.register_blueprint(autenticacion_bp)


#------------------------------------------------------------- REGISTRADOS
#---------------------------------------------------------------------------------MAIN
@app.route('/')
def prodsRegistrados():
    if 'adminSession' in session:
        curs = connection.cursor()
        curs.execute('SELECT * FROM PRODUCTO')
        rows = curs.fetchall()
        curs.close()
        return render_template("Prod_show.html", filas = rows)
    else:
        return redirect(url_for('autenticacion.loginAdmin'))

@app.route('/admin/vendedorRegistrados')
def vendedorRegistrados():
    if 'adminSession' in session:
        curs = connection.cursor()
        curs.execute('SELECT * FROM VENDEDOR')
        rows = curs.fetchall()

        curs.close()
        
        return render_template("SellerShow.html", filas = rows)
    else:
        return redirect(url_for('autenticacion.loginAdmin'))

#------------------------------------------------------------- REGISTRAR
@app.route('/admin/registrarProduct', methods = ['GET', 'POST'])
def registrarProducto():
    if 'adminSession' in session:
        if request.method == 'GET':
                print("Ingrese nuevo producto")         
        elif request.method == 'POST':

            name = request.form["nombre"]
            cantidad = int(request.form["cantidad"])
            
            valor = int(request.form["valor"])
            imgS = request.form["imgs"]

            #print(request.form)
        
            curs = connection.cursor()
            curs.execute(' CALL PRODUCTO_ADD(:NOMBRE_PIV, :STOCK_PIV, :VALOR_PIV, :IMAGEN_PIV)', NOMBRE_PIV=name, STOCK_PIV=cantidad, VALOR_PIV=valor, IMAGEN_PIV=imgS)        
            connection.commit()
            curs.close()
            flash("Producto ingresado") 
            return redirect(url_for('registrarProducto'))
        else:
            return redirect(url_for('inicio'))
        return render_template('Prod_register.html')
    else:
        return redirect(url_for('autenticacion.loginAdmin'))

@app.route('/admin/registrarVendedor', methods = ['GET', 'POST'])
def registrarSeller():
    if 'adminSession' in session:
        if request.method == 'GET':
            print("Ingrese nuevo vendedor")
        elif request.method == 'POST':
            rut = request.form["rut"]
            name = request.form["nombre"]
            email = request.form["email"]
            psw = str(request.form["contraseña"])
        
            curs = connection.cursor()
            #print(request.form)
            curs.execute(' CALL VENDEDOR_CREATE(:RUT_PIC, :NOMBRE_PIC, :EMAIL_PIC, :CONTRASEÑA_PIC)', RUT_PIC = rut, NOMBRE_PIC = name, EMAIL_PIC = email, CONTRASEÑA_PIC = psw)        
            connection.commit()
            curs.close()
            flash("Vendedor registrado")
            return redirect(url_for('registrarSeller'))
        else:
            return redirect(url_for('inicio'))
        return render_template('regVendedor.html')
    else:
        return redirect(url_for('autenticacion.loginAdmin'))


#----------------------------------------------------------------------------DELETE
@app.route('/admin/delete', methods = ['GET', 'POST'])
def deleteProduct():
    if 'adminSession' in session:
        if request.method == 'POST':
            sku = request.form["sku"]
            curs = connection.cursor()
            curs.execute(' CALL PRODUCTO_DELETE(:SKU_PEV)', SKU_PEV=sku)        
            connection.commit()
            curs.close()
            return redirect(url_for('prodsRegistrados'))
        return render_template('Prod_register.html')
    else:
        return redirect(url_for('autenticacion.loginAdmin'))

@app.route('/deleteSeller', methods = ['GET', 'POST'])
def deleteSeller():
    if 'adminSession' in session:
        if request.method == 'POST':
            rut = request.form["rut"]
            curs = connection.cursor()
            curs.execute('CALL VENDEDOR_DELETE(:RUT_PEC)', RUT_PEC=rut)        
            connection.commit()
            curs.close()
            return redirect(url_for('vendedorRegistrados'))
        return render_template('SellerShow.html')
    else:
        return redirect(url_for('autenticacion.loginAdmin'))

#--------------------------------------------------------------------------------------------------- UPDATE
@app.route('/admin/productUpdate', methods = ['GET', 'POST'])
def updateProduct():
    if 'adminSession' in session:
        if request.method == 'GET':
            curs = connection.cursor()
            curs.execute('SELECT * FROM PRODUCTO')
            rows = curs.fetchall()
            curs.close()
            return render_template("updateProduct.html", filas = rows)
        elif request.method == 'POST':
        
            sku = request.form["sku"]
            cantidad = int(request.form["cantidad"])

            print(request.form)
            curs = connection.cursor()
            curs.execute(' CALL PRODUCTO_UPDATE(:SKU_PAS, :CANTIDAD_PAS)', SKU_PAS=sku, CANTIDAD_PAS=cantidad)        
            connection.commit()
            curs.close()
            
            return redirect(url_for('prodsRegistrados'))
        return render_template("updateProduct.html")
    else:
        return redirect(url_for('autenticacion.loginAdmin'))

@app.route('/admin/sellerUpdate', methods = ['GET', 'POST'])
def updateSeller():
    if 'adminSession' in session:
        if request.method == 'GET':
            curs = connection.cursor()
            curs.execute('SELECT * FROM VENDEDOR')
            rows = curs.fetchall()
            curs.close()
            return render_template("updateSeller.html", filas = rows)
        elif request.method == 'POST':
            print(request.form)
            rut = request.form["rut"]
            correo= request.form["correo"]
            pwr = request.form["pass"]
            password = str(pwr)
            
            curs = connection.cursor()
            curs.execute(' CALL VENDEDOR_UPDATE(:RUT_PAC, :CORREO_PADC, :CONTRASEÑA_PADC)', RUT_PAC = rut, CORREO_PADC = correo, CONTRASEÑA_PADC = password)
            connection.commit()
            curs.close()
            flash("Datos actualizados") 
            return redirect(url_for('vendedorRegistrados'))

        return render_template("updateSeller.html")
    else:
        return redirect(url_for('autenticacion.loginAdmin'))
#---------------------------------------------------------------------------------------------------historial
@app.route('/admin/history', methods = ['GET', 'POST'])
def historialVenta():
    if 'adminSession' in session:
        curs = connection.cursor()
        curs.execute('SELECT * FROM REGISTRO_VENTAS')
        rows = curs.fetchall()
        curs.close()
        
        return render_template("historialVentas.html", filas=rows)
    else:
        return redirect(url_for('autenticacion.loginAdmin'))

#------------------------------------------------------------------------------------ VENDEDOR
#------------------------------------------------------------------------------------ log
@login_manager.user_loader
def load_seller(rut):
    curs = connection.cursor()
    curs.execute('SELECT RUT_VENDEDOR, NOMBRE, EMAIL, CONTRASEÑA FROM VENDEDOR WHERE RUT_VENDEDOR =: RUT_VENDEDOR', [rut])
    res = curs.fetchone()
    if (res == None):
        return None
    else:
        return Seller(res[0],res[1])

@autentication_bp.route('/loginseller', methods=['POST','GET'])
def loginSeller():
    if current_user.is_authenticated:
        return redirect(url_for('sellerProds'))
    else:
        if request.method == "POST":
            rut = request.form["rut"]
            passwd = request.form["pswd"]
            cur = connection.cursor()
            cur.execute('SELECT RUT_VENDEDOR, CONTRASEÑA FROM VENDEDOR WHERE RUT_VENDEDOR =: rutForm AND CONTRASEÑA =: passForm', [rut, passwd])
            res = cur.fetchone()
            if res == None:
                flash('invalid password or username.', 'warning')
            else:
                login_user(Seller(res[0],res[1]))
                session['sellerSession'] = rut
                return redirect(url_for('sellerProds'))
        elif request.method == "GET":
            print("--get--")
    return render_template('/auth/loginSeller.html')

@autentication_bp.route("/logoutS")
def logout_seller():
    session.clear()
    return redirect(url_for('autentication.loginSeller'))
app.register_blueprint(autentication_bp)


@app.route('/home')
def sellerProds():
    if 'sellerSession' in session:
        rut = session['sellerSession']
        curs = connection.cursor()
        curs.execute('SELECT * FROM PRODUCTO')
        rows = curs.fetchall()
        curs.close()
        return render_template("Prod_show_seller.html", vendedor=rut, filas = rows)
    else:
        return redirect(url_for('autentication.loginSeller'))
#------------------------------------------------------------------------------------ agregar productos a la boleta
@app.route('/crearBoleta', methods = ['GET', 'POST'])
def crearBoleta():
    if 'sellerSession' in session:
        if request.method =='GET':
            return redirect(url_for('sellerProds'))
        elif request.method == 'POST':
            #pasarle la session
            rut = session['sellerSession']
            sku = int(request.form["sku"])
            cantidad = int(request.form["cantidad"])
            curs = connection.cursor()
            curs.execute('CALL BOLETA_CREATE(:RUT_VENDEDOR, :SKU_P, :STOCK_P)', RUT_VENDEDOR=rut, SKU_P=sku, STOCK_P=cantidad)
            curs.close()
            
            return redirect(url_for('sellerProds'))
    else:
        return redirect(url_for('autentication.loginSeller'))
#------------------------------------------------------------------------------------ Boleta
@app.route('/boleta', methods = ['GET', 'POST'])
def boleta():
    if 'sellerSession' in session:
        rut = session['sellerSession']
        curs = connection.cursor()
        curs.execute('SELECT * FROM BOLETA')
        rows = curs.fetchall()
        curs.close()
        return render_template("SellerBoleta.html", vendedor=rut, filas=rows)
    else:
        return redirect(url_for('autentication.loginSeller'))

@app.route('/registrarVenta', methods=['GET','POST'])
def registrarVenta():
    if 'sellerSession' in session:
        if request.method =='GET':
            return redirect(url_for('sellerProds'))
        elif request.method == 'POST':
            curs = connection.cursor()
            curs.execute('CALL BOLETA_REGISTRO()')
            connection.commit()
            curs.close()
            return redirect(url_for('crearBoleta'))
    else:
        return redirect(url_for('autentication.loginSeller'))


if __name__ == "__main__":
    app.run(debug=True)