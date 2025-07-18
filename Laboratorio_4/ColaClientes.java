import java.util.ArrayList;

class Cliente {
    private String nombre;
    private String cedula;

    public Cliente(String nombre, String cedula) {
        this.nombre = nombre;
        this.cedula = cedula;
    }

    public String getNombre() {
        return nombre;
    }

    public String getCedula() {
        return cedula;
    }

    @Override
    public String toString() {
        return "Cliente{nombre='" + nombre + "', cedula='" + cedula + "'}";
    }
}

public class ColaClientes {
    private ArrayList<Cliente> cola;
    private ArrayList<Cliente> historialAtendidos;
    private ArrayList<Integer> tiemposAtencion;

    public ColaClientes() {
        cola = new ArrayList<>();
        historialAtendidos = new ArrayList<>();
        tiemposAtencion = new ArrayList<>();
    }

    // Agrega los clientes a la cola
    public void agregarCliente(Cliente cliente) {
        cola.add(cliente);
    }

    // Atiende al cliente (simula el tiempo de atencion)
    public void atenderCliente() {
        if (!cola.isEmpty()) {
            Cliente atendido = cola.remove(0);
            historialAtendidos.add(atendido);
            int tiempo = (int)(Math.random() * 10 + 1); // 1 a 10 minutos
            tiemposAtencion.add(tiempo);
            System.out.println("Cliente atendido: " + atendido.getNombre() + " | Tiempo: " + tiempo + " min");
        } else {
            System.out.println("No hay clientes en la cola.");
        }
    }

    // El historial de los clientes atendidos
    public ArrayList<Cliente> getHistorialAtendidos() {
        return historialAtendidos;
    }

    // Calcula el promedio de tiempo de atencion
    public double getPromedioTiempo() {
        if (tiemposAtencion.isEmpty()) return 0;
        int suma = 0;
        for (int t : tiemposAtencion) suma += t;
        return (double)suma / tiemposAtencion.size();
    }

    // Busca el cliente en la cola por nombre o cedula
    public Cliente buscarCliente(String criterio) {
        for (Cliente c : cola) {
            if ((c.getNombre() != null && c.getNombre().equalsIgnoreCase(criterio)) ||
                (c.getCedula() != null && c.getCedula().equals(criterio))) {
                return c;
            }
        }
        return null;
    }

    // Muestra los clientes en la cola
    public void mostrarCola() {
        System.out.println("Clientes en la cola:");
        for (Cliente c : cola) {
            System.out.println(c);
        }
    }

    // Muestra el historial de los clientes atendidos
    public void mostrarHistorial() {
        System.out.println("Historial de clientes atendidos:");
        for (Cliente c : historialAtendidos) {
            System.out.println(c);
        }
    }
}

// Clase Main para ejecutar el código
class Main {
    public static void main(String[] args) {
        ColaClientes cola = new ColaClientes();

        cola.agregarCliente(new Cliente("Ana", "123"));
        cola.agregarCliente(new Cliente("Luis", "456"));
        cola.agregarCliente(new Cliente("Maria", "789"));

        cola.mostrarCola();

        cola.atenderCliente();
        cola.atenderCliente();

        cola.mostrarHistorial();

        System.out.println("Promedio de tiempo de atención: " + cola.getPromedioTiempo() + " min");

        Cliente buscado = cola.buscarCliente("Maria");
        if (buscado != null) {
            System.out.println("Cliente encontrado en la cola: " + buscado);
        } else {
            System.out.println("Cliente no está en la cola.");
        }
    }
}