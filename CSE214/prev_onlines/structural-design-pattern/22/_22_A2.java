import java.util.ArrayList;
import java.util.List;

// ===== Component =====
interface BazarItem {
    String getName();
    double getPrice();
    double getWeight();
    void display(String indent);
}

// ===== Leaf (a single grocery item) =====
class SingleItem implements BazarItem {
    private String name;
    private double price;
    private double weight;

    public SingleItem(String name, double price, double weight) {
        this.name = name;
        this.price = price;
        this.weight = weight;
    }

    public String getName() { return name; }
    public double getPrice() { return price; }
    public double getWeight() { return weight; }

    public void display(String indent) {
        System.out.printf("%s- %s (price: %.2f, weight: %.2f)%n", indent, name, price, weight);
    }
}

// ===== Composite (a preset package OR a custom package) =====
class BazarPackage implements BazarItem {
    private String name;
    private List<BazarItem> items = new ArrayList<>();

    public BazarPackage(String name) { this.name = name; }

    public void add(BazarItem item) { items.add(item); }

    public String getName() { return name; }

    public double getPrice() {
        double total = 0;
        for (BazarItem item : items) total += item.getPrice();
        return total;
    }

    public double getWeight() {
        double total = 0;
        for (BazarItem item : items) total += item.getWeight();
        return total;
    }

    public void display(String indent) {
        System.out.printf("%s+ %s (total price: %.2f, total weight: %.2f)%n",
                indent, name, getPrice(), getWeight());
        for (BazarItem item : items) item.display(indent + "  ");
    }
}

// ===== Demo =====
public class _22_A2 {
    public static void main(String[] args) {
        // Single items
        SingleItem rice = new SingleItem("Rice", 5.0, 2.0);
        SingleItem oil = new SingleItem("Oil", 3.0, 1.0);
        SingleItem pulse = new SingleItem("Pulse", 2.0, 0.5);

        // Preset packages (made of single items)
        BazarPackage small = new BazarPackage("Small Package");
        small.add(rice);
        small.add(oil);

        BazarPackage family = new BazarPackage("Family Package");
        family.add(rice);
        family.add(oil);
        family.add(pulse);

        // Custom Bazar: mixture of a preset package, a single item,
        // and another preset package (a previously created package
        // would be added the exact same way)
        BazarPackage customBazar = new BazarPackage("My Custom Bazar");
        customBazar.add(small);
        customBazar.add(pulse);
        customBazar.add(family);

        customBazar.display("");
        System.out.printf("%nTotal Price: %.2f, Total Weight: %.2f%n",
                customBazar.getPrice(), customBazar.getWeight());
    }
}
