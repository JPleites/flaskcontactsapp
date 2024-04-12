from flask import Flask, render_template, request, url_for, redirect, flash
import pyodbc

"""Variables del entorno de SSMS"""
server = 'JEPPLEITES'
bd = 'Flask_contacts_db'
user = 'jorge'
password = '1502'

"""Conexion a SSMS"""
try:
    conexion = pyodbc.connect(
    'DRIVER={SQL Server};SERVER='+server+';DATABASE='+bd+';UID='+user+';PWD='+password
    )
    print ('Conexion exitosa')
except:
    print ('Error en la conexion')


    
app = Flask(__name__)

"""Settings"""
app.secret_key = 'secretkey'

@app.route('/')
def index():
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Contacts")
    data = cursor.fetchall()
    return render_template('index.html', contacts=data)

"""Añadir Contacto"""
@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        
        cursor=conexion.cursor()
        sql="INSERT INTO Contacts (Nombre, Telefono, Correo) VALUES (?, ?, ?)"
        valores=(name, phone, email)
        
        cursor.execute(sql, valores)
        conexion.commit()
        cursor.close()
        
        flash('Contacto agregado con exito')
        return redirect(url_for('index'))

"""Editar Contacto"""
@app.route('/edit/<id>')
def get_contact(id):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Contacts WHERE Id ="+id)
    data = cursor.fetchall()
    return render_template('edit_contact.html', contact = data[0])

"""Actualizacion"""
@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        cursor=conexion.cursor()
        cursor.execute("""
            UPDATE Contacts 
            SET Nombre = ?,
                Telefono = ?,
                Correo = ?
            WHERE Id = ?
        """, (name, phone, email,id))
        conexion.commit()
    flash('Contacto Actualizado')
    return redirect(url_for('index'))

"""Borrar Contacto"""
@app.route('/delete/<string:id>')
def delete_contact(id):
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM Contacts WHERE id ="+id)
    conexion.commit()
    cursor.close()
    
    flash('Contacto borrado con exito')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port= 3000, debug=True)