import basedatos
import interfaz

def main():
    print("Iniciando ReportPro...")
    basedatos.crear_tablas()
    print("Tablas de base de datos creadas o actualizadas.")
    interfaz.iniciar_interfaz()
    print("Aplicación finalizada.")

if __name__ == "__main__":
    main()
