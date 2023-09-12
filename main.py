import numpy as np
from flask import Flask, render_template, request, redirect, flash, url_for
app = Flask(__name__)
app.secret_key = 'key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/InsertarDatos', methods=['POST'])
def insertar_datos():
    if request.method == 'POST':
        cadena = request.form['cadena']
        cadenaParaDescifrar = request.form['cadenaCifrada']
        valoresParaDescifrar = request.form['valoresCifrados']
        cadenaAux = cadena
        # Matriz de transformación
        t = np.array([[7, 9, 6], [6, 7, 5], [8, 10, 7]], int)
        # Cálculo de la inversa de T
        tInv = np.linalg.inv(t).astype(int)
        if cadena != "":
            a = np.array([])
            for indice in range(len(cadena)):
                a = np.append(a, ord(cadena[indice]))
            if (len(cadena) % 3 != 0):
                relleno = 3 - (len(cadena) % 3)
                while relleno > 0:
                    relleno -= 1
                    # Para rellenar utilizo el espacio
                    a = np.append(a, 32)
            cadena = ""
            # Array n filas y 3 columnas
            a = a.reshape(int(a.size / 3), 3)
            # Transpuesta
            a = a.T
            # Matriz transformada cifrada
            c = t @ a
            # Valores originales
            valoresOriginales = "Valores Originales: [["
            for x in np.nditer(a.reshape(1, a.size)):
                valoresOriginales += str(int(x))
                valoresOriginales += ' '
            valoresOriginales += ']]'
            # Cadena y valores cifrados
            cadenaCifrada = "Cadena Cifrada: "
            valoresCifrados = "Valores Cifrados: [["
            for x in np.nditer(c.reshape(1, c.size)):
                cadenaCifrada += chr(int(x))
                valoresCifrados += str(int(x))
                valoresCifrados += ' '
            valoresCifrados += ']]'
            # Cadena original
            cadenaOriginal = 'Cadena original: ' + cadenaAux
            # Mensajes de respuesta
            flash(cadenaOriginal)
            flash(valoresOriginales)
            flash(cadenaCifrada)
            flash(valoresCifrados)
            return redirect(url_for('index'))
        elif cadenaParaDescifrar != "":
            c = np.array([])
            for indice in range(len(cadenaParaDescifrar)):
                c = np.append(c, ord(cadenaParaDescifrar[indice]))
            c = c.reshape(3, int(c.size / 3))
            b = tInv @ c
            valoresDescifrados = "Valores Descifrados: [["
            for x in np.nditer(b.reshape(1, b.size)):
                valoresDescifrados += str(int(x))
                valoresDescifrados += ' '
            valoresDescifrados += ']]'
            cadenaDescifrada = "Cadena Descifrada: "
            b = b.T
            for x in np.nditer(b.reshape(1, b.size)):
                cadenaDescifrada += chr(int(x))
            cadenaParaDescifrar = ""
            # Mensajes de respuesta
            flash(cadenaDescifrada)
            flash(valoresDescifrados)
            return redirect(url_for('index'))
        else:
            c = np.array([])
            y = valoresParaDescifrar.split()
            valoresParaDescifrar = ""
            for x in y:
                c = np.append(c, int(x))
            # Valores para descifrar
            c = c.reshape(3, int(c.size / 3))
            # Matriz transformada (descifrada):
            b = tInv @ c
            valoresDescifrados = "Valores Descifrados: [["
            for x in np.nditer(b.reshape(1, b.size)):
                valoresDescifrados += str(int(x))
                valoresDescifrados += ' '
            valoresDescifrados += ']]'
            # Obtener cadena descifrada
            cadenaDescifrada = "Cadena Descifrada: "
            b = b.T
            for x in np.nditer(b.reshape(1, b.size)):
                cadenaDescifrada += chr(int(x))
            # Mensajes de respuesta
            flash(cadenaDescifrada)
            flash(valoresDescifrados)
            return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True,port=5000)
