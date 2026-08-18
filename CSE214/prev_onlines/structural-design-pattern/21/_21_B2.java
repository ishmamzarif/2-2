// Component interface representing the basic hardware component
interface Component {
    double getPrice();
    String getDescription();
}

// Concrete Component representing individual hardware components
class HardwareComponent implements Component {
    private String name;
    private double price;

    public HardwareComponent(String name, double price) {
        this.name = name;
        this.price = price;
    }

    @Override
    public double getPrice() {
        return price;
    }

    @Override
    public String getDescription() {
        return name;
    }
}

// Base Decorator
abstract class HardwareDecorator implements Component {
    private Component wrapee;

    public HardwareDecorator(Component c) { 
        this.wrapee = c;
    }
    
    @Override
    public double getPrice() {
        return wrapee.getPrice();
    }
    
    @Override
    public String getDescription() {
        return wrapee.getDescription();
    }
}

// Concrete Decorator 1
class ExtendedWarranty extends HardwareDecorator {
    public ExtendedWarranty(Component c) {
        super(c);
    }
    
    @Override
    public double getPrice() {
        return super.getPrice() + 50.0; // Distinct price
    }

    @Override
    public String getDescription() {
        return super.getDescription() + " + Extended Warranty";
    }
}

// Concrete Decorator 2
class InstallationService extends HardwareDecorator {
    public InstallationService(Component c) {
        super(c);
    }
    
    @Override
    public double getPrice() {
        return super.getPrice() + 30.0; // Distinct price
    }

    @Override
    public String getDescription() {
        return super.getDescription() + " + Installation Service";
    }
}

// Concrete Decorator 3
class PerformanceBoost extends HardwareDecorator {
    public PerformanceBoost(Component c) {
        super(c);
    }
    
    @Override
    public double getPrice() {
        return super.getPrice() + 100.0; // Distinct price
    }

    @Override
    public String getDescription() {
        return super.getDescription() + " + Performance Boost";
    }
}
 
public class _21_B2 {
    public static void main(String[] args) {
        // 1. Create a base component
        Component myGpu = new HardwareComponent("RTX 4090 GPU", 1500.0);
        
        // 2. Dynamically add features using the Decorator pattern
        myGpu = new ExtendedWarranty(myGpu);
        myGpu = new PerformanceBoost(myGpu);
        
        // 3. Display the final stacked results
        System.out.println("=== Custom Hardware Order ===");
        System.out.println("Items: " + myGpu.getDescription());
        System.out.println("Total Price: $" + myGpu.getPrice());
    }
}