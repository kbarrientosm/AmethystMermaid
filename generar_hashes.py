from werkzeug.security import generate_password_hash

empleados = {
    "Mariana": "DemoMariana2026!",
    "Daniela": "DemoDaniela2026!",
    "Andrea": "DemoAndrea2026!"
}

for nombre, contrasena in empleados.items():
    hash_contrasena = generate_password_hash(contrasena)
    print(f"{nombre}: {hash_contrasena}")