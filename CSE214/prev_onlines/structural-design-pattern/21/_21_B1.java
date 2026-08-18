interface Purchase {
    double calculatePrice();
}

class BasePurchase implements Purchase {
    private double basePrice;

    public BasePurchase(double basePrice) {
        this.basePrice = basePrice;
    }

    @Override
    public double calculatePrice() {
        return basePrice;
    }
}

abstract class DiscountDecorator implements Purchase {
    protected Purchase purchase;

    public DiscountDecorator(Purchase purchase) {
        this.purchase = purchase;
    }
    public abstract double calculatePrice();
}

class LoyaltyDiscount extends DiscountDecorator {
    public LoyaltyDiscount(Purchase purchase) {
        super(purchase);
    }

    @Override
    public double calculatePrice() {
        return purchase.calculatePrice() * 0.9; // 10% discount
    }
}

class SeasonalDiscount extends DiscountDecorator {
    public SeasonalDiscount(Purchase purchase) {
        super(purchase);
    }

    @Override
    public double calculatePrice() {
        return purchase.calculatePrice() - 100.0; // 15% discount
    }
}

class HighValuePurchaseDiscount extends DiscountDecorator {
    public HighValuePurchaseDiscount(Purchase purchase) {
        super(purchase);
    }

    @Override
    public double calculatePrice() {
        double currentPrice = purchase.calculatePrice();
        if (currentPrice > 10000.0) {
            return currentPrice * 0.98;
        }
        return currentPrice;
    }
}


public class _21_B1 {
    public static void main(String[] args) {
        double basePrice = 12000; // Initial price of the product
        // Create a base purchase
        Purchase purchase = new BasePurchase(basePrice);
        // Apply discounts conditionally
        Purchase discountedPurchase = new LoyaltyDiscount(purchase); // Apply loyalty discount
        discountedPurchase = new SeasonalDiscount(discountedPurchase); // Apply seasonal discount
        discountedPurchase = new HighValuePurchaseDiscount(discountedPurchase); // Apply high-value purchase
        // Calculate final price after all applicable discounts
        double finalPrice = discountedPurchase.calculatePrice();
        System.out.println("Final price after all discounts: " + finalPrice);
    }
}