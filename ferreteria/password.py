import os
import django
from django.conf import settings

# 1. Configuramos un entorno mínimo de Django para poder usar los hashers sin un proyecto completo
if not settings.configured:
    settings.configure(
        SECRET_KEY='temp-secret-key-para-script',
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
        ],
    )

django.setup()

from django.contrib.auth.hashers import make_password, check_password

def main():
    print("=" * 50)
    print("       GENERADOR DE HASH DE CONTRASEÑAS - DJANGO")
    print("=" * 50)
    
    # 2. Solicitamos la contraseña por terminal
    password = input("\nIngresa la contraseña que deseas hashear: ")
    
    if not password.strip():
        print("❌ La contraseña no puede estar vacía.")
        return

    # 3. Generamos el hash (Django usa por defecto PBKDF2 con SHA256 o Argon2 según configuración)
    hashed_password = make_password(password)
    
    print("\n" + "-" * 50)
    print("RESULTADO:")
    print(f"🔑 Hash generado: \n{hashed_password}")
    print("-" * 50)
    
    # 4. Opcional: Verificación interactiva del hash
    verificar = input("\n¿Deseas probar la verificación del hash? (s/n): ").strip().lower()
    if verificar == 's':
        intentar_pass = input("Ingresa la contraseña para verificar: ")
        if check_password(intentar_pass, hashed_password):
            print(" ¡Éxito! La contraseña coincide con el hash.")
        else:
            print("❌ Error: La contraseña no coincide.")

if __name__ == "__main__":
    main()