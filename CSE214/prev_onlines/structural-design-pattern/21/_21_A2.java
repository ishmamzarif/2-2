import java.util.ArrayList;
import java.util.List;

// ===== Component =====
interface PCComponent {
    double getPrice();
    void display(String indent);
}

// ===== Leaf (a single hardware part) =====
class HardwareComponent implements PCComponent {
    private String name;
    private double price;

    public HardwareComponent(String name, double price) {
        this.name = name;
        this.price = price;
    }

    public double getPrice() { return price; }

    public void display(String indent) {
        System.out.printf("%s- %s ($%.2f)%n", indent, name, price);
    }
}

// ===== Composite (a bundle: components and/or other bundles) =====
class Bundle implements PCComponent {
    private String name;
    private List<PCComponent> components = new ArrayList<>();

    public Bundle(String name) { this.name = name; }

    public void add(PCComponent component) { components.add(component); }
    public void remove(PCComponent component) { components.remove(component); }

    public double getPrice() {
        double total = 0;
        for (PCComponent c : components) total += c.getPrice();
        return total;
    }

    public void display(String indent) {
        System.out.printf("%s+ %s (total: $%.2f)%n", indent, name, getPrice());
        for (PCComponent c : components) c.display(indent + "  ");
    }
}

// ===== Demo =====
public class _21_A2 {
    public static void main(String[] args) {
        PCComponent cpu = new HardwareComponent("CPU", 300);
        PCComponent memory = new HardwareComponent("Memory", 100);
        PCComponent storage = new HardwareComponent("Storage", 80);
        PCComponent gpu = new HardwareComponent("Graphics Card", 500);

        // A basic bundle made of individual components
        Bundle basicGaming = new Bundle("Basic Gaming Setup");
        basicGaming.add(cpu);
        basicGaming.add(memory);
        basicGaming.add(storage);

        // A bigger bundle containing another bundle plus an extra component
        Bundle ultimateGaming = new Bundle("Ultimate Gaming Setup");
        ultimateGaming.add(basicGaming);
        ultimateGaming.add(gpu);

        ultimateGaming.display("");
        System.out.printf("%nTotal Price: $%.2f%n", ultimateGaming.getPrice());

        // Customer removes a component from the inner bundle;
        // the change is reflected automatically in the outer bundle's total
        basicGaming.remove(storage);

        System.out.println("\nAfter removing Storage from Basic Gaming Setup:");
        ultimateGaming.display("");
        System.out.printf("%nTotal Price: $%.2f%n", ultimateGaming.getPrice());
    }
}