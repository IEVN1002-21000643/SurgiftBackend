from flask import jsonify
from models import db
from sqlalchemy import text
from datetime import datetime
from clases import clsUsuario

def verPseudoperfiles(idU):
    pseudoperfiles=db.session.execute(text(f"SELECT * FROM pseudoperfil where idUsuario={idU}"))
    if pseudoperfiles!=[]:
        data=pseudoperfiles.fetchall()
        pseudoperfilLista=[]
        for fila in data:
            pseudoperfil={"idPseudoperfil": fila[0], "nombre": fila[1], "Caracteristícas": fila[2], "PseudoperfilReal": fila[3]}
            pseudoperfilLista.append(pseudoperfil)
        return jsonify({'Pseudoperfil': pseudoperfilLista, 'exito':True})
    else:
        return jsonify({'message': "Por el momento no tienes pseudoperfiles", 'exito':False})

def verPseudoperfil(idP, idU):
    pseudoperfiles=db.session.execute(text(f"SELECT * FROM pseudoperfil WHERE idUsuario='{idU}' and idPseudoperfil='{idP}'"))
    data=pseudoperfiles.fetchall()
    correo=''
    if data[0][3]!= None:
        correo=data[0][3]
    pseudoperfilLista=[]
    for fila in data:
        pseudoperfil={"idPseudoperfil": fila[0], "nombre": fila[1], "Caracteristícas": fila[2], "idPseudoperfilReal": correo, "idUsuario": idU}
        pseudoperfilLista.append(pseudoperfil)
    return pseudoperfilLista
    
def crearPseudoperfil(idU, nom, car, idPR):
    usuario=clsUsuario.verUsuario(idU)
    if usuario != []:
        if idPR!='':
            db.session.execute(text(f"INSERT INTO pseudoperfil (nombre, caracteristicas, idUsuario, idPseudoperfilReal) VALUES ('{nom}', '{car}', '{idU}', '{idPR}')"))
        else:
            db.session.execute(text(f"INSERT INTO pseudoperfil (nombre, caracteristicas, idUsuario) VALUES ('{nom}', '{car}', '{idU}')"))
        db.session.commit()
        return jsonify({'message': "El pseudoperfil ha sido agregado", 'exito':True})
    else:
        return jsonify({'message': "El usuario no existe", 'exito':False})

def editarPseudoperfil(idU, nom, car, idP, idPR):
    usuario=clsUsuario.verUsuario(idU)
    pseudoperfilReal=clsUsuario.verUsuario(idPR)
    pseudoperfil=verPseudoperfil(idP, idU)
    if usuario !=[]:
        if pseudoperfil != []:
            if pseudoperfilReal != []:
                if(idPR!=''):
                    db.session.execute(text(f"UPDATE pseudoperfil set nombre='{nom}', caracteristicas='{car}', idPseudoperfilReal='{idPR}' WHERE idUsuario='{idU}' and idPseudoperfil='{idP}'"))
                else:
                    db.session.execute(text(f"UPDATE pseudoperfil set nombre='{nom}', caracteristicas='{car}' WHERE idUsuario='{idU}' and idPseudoperfil='{idP}'"))
                db.session.commit()
                return jsonify({'message': "El pseudoperfil ha sido editado correctamente", 'exito':True})
            else:
                return jsonify({'message': "El pseudoperfil que intentas editar no existe", 'exito':False})
        else:
            return jsonify({'message': "El usuario que intentas conectar no existe", 'exito':False})
    else:
        return jsonify({'message': "El usuario no existe", 'exito':False})

def eliminarPseudoperfil(idP, idU):
    usuario=clsUsuario.verUsuario(idU)
    pseudoperfil=verPseudoperfil(idP, idU)
    print(1)
    if usuario !=[]:
        if pseudoperfil != []:
            db.session.execute(text(f"DELETE FROM pseudoperfil WHERE idUsuario='{idU}' and idPseudoperfil='{idP}'"))
            db.session.commit()
            return jsonify({'message': "El pseudoperfil ha sido editado correctamente", 'exito':True})
        else:
            return jsonify({'message': "El pseudoperfil que intentas editar no existe", 'exito':False})
    else:
        return jsonify({'message': "El usuario no existe", 'exito':False})