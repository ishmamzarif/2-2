interface PaymentStrategy {
    void pay(double amount);
}

class CreditCardPayment implements PaymentStrategy {
    public void pay(double amount) {
        System.out.println("Paid " + amount + " using Credit Card");
    }
}

class BkashPayment implements PaymentStrategy {
    public void pay(double amount) {
        System.out.println("Paid " + amount + " using BKash");
    }
}

class CryptoPayment implements PaymentStrategy {
    public void pay(double amount) {
        System.out.println("Paid " + amount + " using Cryptocurrency");
    }
}

class Checkout {
    private PaymentStrategy strategy;

    void setPaymentStrategy(PaymentStrategy strategy) {
        this.strategy = strategy;
    }

    void checkout(double amount) {
        strategy.pay(amount);
    }
}

public class _21A1 {
    public static void main(String[] args) {
        Checkout checkout = new Checkout();

        checkout.setPaymentStrategy(new CreditCardPayment());
        checkout.checkout(100);

        checkout.setPaymentStrategy(new BkashPayment());
        checkout.checkout(50);

        checkout.setPaymentStrategy(new CryptoPayment());
        checkout.checkout(0.002);
    }
}
