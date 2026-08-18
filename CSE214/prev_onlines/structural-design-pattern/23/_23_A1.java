// ===== Gift item (Component for the Decorator) =====
interface GiftItem {
    int getPrice();
    String getDetails();
}

class Vase implements GiftItem {
    private String name;
    private int price;

    public Vase(String name, int price) {
        this.name = name;
        this.price = price;
    }

    public int getPrice() { return price; }
    public String getDetails() { return name; }
}

// ===== Decorator (optional wrapping add-on) =====
abstract class Decorator implements GiftItem {
    GiftItem wrappee;
    public Decorator(GiftItem wrappee) {
        this.wrappee = wrappee;
    }
}

class WrapperDecorator extends Decorator {
    public WrapperDecorator(GiftItem wrappee) {
        super(wrappee);
    }
    @Override
    public int getPrice() {
        return wrappee.getPrice() + 2;
    }
    @Override
    public String getDetails() {
        return wrappee.getDetails() + " [WRAPPED]";
    }
}

// ===== Implementor (delivery mode) =====
interface DeliveryMode {
    int getExtraCharge();
    String getTimeOverride(boolean international);
}

class ExpressDelivery implements DeliveryMode {
    public int getExtraCharge() { return 10; }
    public String getTimeOverride(boolean international) {
        return international ? "1 week" : "2 days";
    }
}

class PriorityDelivery implements DeliveryMode {
    public int getExtraCharge() { return 25; }
    public String getTimeOverride(boolean international) {
        return international ? "5 days" : "1 day";
    }
}

// ===== Abstraction (delivery region) =====
abstract class DeliveryRegion {
    protected DeliveryMode mode;   // null = standard delivery, no express/priority

    public DeliveryRegion(DeliveryMode mode) {
        this.mode = mode;
    }

    public abstract int getBaseCharge();
    public abstract String getDefaultTime();
    public abstract boolean isInternational();

    public int getTotalCharge() {
        return getBaseCharge() + (mode == null ? 0 : mode.getExtraCharge());
    }

    public String getEstimatedTime() {
        if (mode == null) return getDefaultTime();
        return mode.getTimeOverride(isInternational());
    }
}

// ===== Refined Abstractions (regions — new ones added over time) =====
class LocalDelivery extends DeliveryRegion {
    private int miles;
    public LocalDelivery(int miles, DeliveryMode mode) {
        super(mode);
        this.miles = miles;
    }
    public int getBaseCharge() { return miles * 1; }
    public String getDefaultTime() { return "1 week"; }
    public boolean isInternational() { return false; }
}

class NationalDelivery extends DeliveryRegion {
    private int miles;
    public NationalDelivery(int miles, DeliveryMode mode) {
        super(mode);
        this.miles = miles;
    }
    public int getBaseCharge() { return miles * 1 + 20; }
    public String getDefaultTime() { return "1-2 weeks"; }
    public boolean isInternational() { return false; }
}

class InternationalDelivery extends DeliveryRegion {
    public InternationalDelivery(DeliveryMode mode) {
        super(mode);
    }
    public int getBaseCharge() { return 500; }
    public String getDefaultTime() { return "2-3 weeks"; }
    public boolean isInternational() { return true; }
}

// ===== Ties a gift item to its (optional) delivery =====
class GiftOrder {
    private GiftItem item;
    private DeliveryRegion delivery;   // null = no delivery requested

    public GiftOrder(GiftItem item, DeliveryRegion delivery) {
        this.item = item;
        this.delivery = delivery;
    }

    public int getTotalCost() {
        int total = item.getPrice();
        if (delivery != null) total += delivery.getTotalCharge();
        return total;
    }

    public void printSummary() {
        System.out.println("Item: " + item.getDetails());
        System.out.println("Total Cost: $" + getTotalCost());
        if (delivery != null) {
            System.out.println("Estimated Delivery Time: " + delivery.getEstimatedTime());
        }
    }
}

// ===== Demo: Case 1 =====
public class _23_A1 {
    public static void main(String[] args) {
        GiftItem vase = new Vase("Decorative Vase", 40);
        GiftItem wrappedVase = new WrapperDecorator(vase);

        DeliveryRegion localDelivery = new LocalDelivery(10, null);   // no express/priority chosen

        GiftOrder order = new GiftOrder(wrappedVase, localDelivery);
        order.printSummary();
    }
}