// Implementor — the "how" side (e.g. transport method / channel)
interface TransportMethod {
    void dispatchPackage(String orderId);
}

class BikeTransport implements TransportMethod {
    @Override
    public void dispatchPackage(String orderId) {
        System.out.println("Dispatching order " + orderId + " via BIKE COURIER.");
    }
}

// VanTransport.java
class VanTransport implements TransportMethod {
    @Override
    public void dispatchPackage(String orderId) {
        System.out.println("Dispatching order " + orderId + " via DELIVERY VAN.");
    }
}

// DroneTransport.java
class DroneTransport implements TransportMethod {
    @Override
    public void dispatchPackage(String orderId) {
        System.out.println("Dispatching order " + orderId + " via AUTONOMOUS DRONE.");
        System.out.println(" -> Drone safety checks passed. Flight path calculated.");
    }
}

// Abstraction — the "what" side (e.g. delivery type / event type)
abstract class DeliveryOption {
    // The Bridge
    protected TransportMethod transport;

    public DeliveryOption(TransportMethod transport) {
        this.transport = transport;
    }

    // Business logic specific to the delivery type
    public abstract double calculatePrice();
    public abstract String getEstimatedTime();
    
    // The template method that brings it all together
    public void processOrder(String orderId) {
        System.out.println("\n--- Processing Order: " + orderId + " ---");
        System.out.println("Estimated Time: " + getEstimatedTime());
        System.out.println("Delivery Cost: $" + calculatePrice());
        
        // Delegate the actual physical delivery across the bridge
        transport.dispatchPackage(orderId);
    }
}

class StandardDelivery extends DeliveryOption {
    public StandardDelivery(TransportMethod transport) {
        super(transport);
    }

    @Override
    public double calculatePrice() {
        return 2.0; // Standard flat rate
    }

    @Override
    public String getEstimatedTime() {
        return "Within 24 hours";
    }
}

class ScheduledDelivery extends DeliveryOption {
    public ScheduledDelivery(TransportMethod transport) {
        super(transport);
    }

    @Override
    public double calculatePrice() {
        return 7.0; // Premium rate for speed
    }

    @Override
    public String getEstimatedTime() {
        return "Within 34 hours";
    }
}

class ExpressDelivery extends DeliveryOption {
    public ExpressDelivery(TransportMethod transport) {
        super(transport);
    }

    @Override
    public double calculatePrice() {
        return 8.0; // Premium rate for speed
    }

    @Override
    public String getEstimatedTime() {
        return "Within 4 hours";
    }
}

public class _22_C2 {
    public static void main(String[] args) {
        // Setup transport technologies
        TransportMethod bike = new BikeTransport();
        TransportMethod drone = new DroneTransport();

        // 1. A standard delivery order fulfilled by a bike courier
        DeliveryOption order1 = new StandardDelivery(bike);
        order1.processOrder("ORD-1001");

        // 2. An express delivery order fulfilled by the new drone technology
        DeliveryOption order2 = new ExpressDelivery(drone);
        order2.processOrder("ORD-1002");

        // 3. A standard delivery that dynamically switches to a drone for logistics
        DeliveryOption order3 = new StandardDelivery(drone);
        order3.processOrder("ORD-1003");
    }    
}