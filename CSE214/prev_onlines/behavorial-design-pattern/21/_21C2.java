abstract class OrderState {
    String name;
    OrderState(String name) { this.name = name; }

    void confirm(Order order) { invalid("confirm"); }
    void ship(Order order) { invalid("ship"); }
    void deliver(Order order) { invalid("deliver"); }
    void cancel(Order order) { invalid("cancel"); }

    void invalid(String action) {
        System.out.println("Cannot " + action + " order from " + name + " state");
    }
}

class PlacedState extends OrderState {
    PlacedState() { super("Placed"); }
    void confirm(Order order) {
        System.out.println("Order confirmed");
        order.setState(new ConfirmedState());
    }
    void cancel(Order order) {
        System.out.println("Order cancelled");
        order.setState(new CancelledState());
    }
}

class ConfirmedState extends OrderState {
    ConfirmedState() { super("Confirmed"); }
    void ship(Order order) {
        System.out.println("Order shipped");
        order.setState(new ShippedState());
    }
    void cancel(Order order) {
        System.out.println("Order cancelled");
        order.setState(new CancelledState());
    }
}

class ShippedState extends OrderState {
    ShippedState() { super("Shipped"); }
    void deliver(Order order) {
        System.out.println("Order delivered");
        order.setState(new DeliveredState());
    }
}

class DeliveredState extends OrderState {
    DeliveredState() { super("Delivered"); }
}

class CancelledState extends OrderState {
    CancelledState() { super("Cancelled"); }
}

class Order {
    private OrderState state = new PlacedState();

    void setState(OrderState state) {
        this.state = state;
    }

    String status() { return state.name; }

    void confirm() { state.confirm(this); }
    void ship() { state.ship(this); }
    void deliver() { state.deliver(this); }
    void cancel() { state.cancel(this); }
}

public class _21C2 {
    public static void main(String[] args) {
        Order order = new Order();
        System.out.println("Status: " + order.status());

        order.confirm();
        System.out.println("Status: " + order.status());

        order.deliver();
        System.out.println("Status: " + order.status());

        order.ship();
        System.out.println("Status: " + order.status());

        order.deliver();
        System.out.println("Status: " + order.status());

        Order cancelledOrder = new Order();
        cancelledOrder.cancel();
        System.out.println("Status: " + cancelledOrder.status());

        cancelledOrder.ship();
    }
}