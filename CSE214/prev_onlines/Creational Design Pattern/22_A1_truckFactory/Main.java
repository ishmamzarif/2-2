import java.util.*;


interface Transport {
    public void deliver();
}

class Truck implements Transport {
    @Override
    public void deliver() {
        System.out.println("transporting via truck");
    }
}

class Ship implements Transport {
    @Override
    public void deliver() {
        System.out.println("transporting via ship");
    }
}

class TransportFactory {
    public Transport createTransport(String type) throws Exception {
        if (type.equals("Truck")) {
            return new Truck();
        }
        else if (type.equals("Ship")) {
            return new Ship();
        }
        else {
            throw new IllegalArgumentException("Type must be either Truck or Ship");
        }
    }
}

public class Main {
    public static void main(String[] args) throws Exception {
        // Scanner sc = new Scanner(System.in);
        // System.out.print("Enter type of transport you want = ");
        // String type = sc.nextLine();

        // create a factory for building objects
        TransportFactory f = new TransportFactory();
    
        // create a truck
        Transport t = f.createTransport("Truck");
        t.deliver();
        // create a ship 
        Transport s = f.createTransport("Ship");
        s.deliver();
    }
}


