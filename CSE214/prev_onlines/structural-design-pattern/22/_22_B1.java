// ===== Implementor (the channel side) =====
interface NotificationSender {
    void sendMessage(String message);
}

// ===== Concrete Implementors (channels — new ones added over time) =====
class EmailSender implements NotificationSender {
    public void sendMessage(String message) {
        System.out.println("[Email] " + message);
    }
}

class SMSSender implements NotificationSender {
    public void sendMessage(String message) {
        System.out.println("[SMS] " + message);
    }
}

class PushSender implements NotificationSender {
    public void sendMessage(String message) {
        System.out.println("[Push] " + message);
    }
}

class WhatsAppSender implements NotificationSender {
    public void sendMessage(String message) {
        System.out.println("[WhatsApp] " + message);
    }
}

// ===== Abstraction (the event side) =====
abstract class Notification {
    protected NotificationSender sender;   // the "bridge" to the channel

    public Notification(NotificationSender sender) {
        this.sender = sender;
    }

    public abstract void notifyUser();
}

// ===== Refined Abstractions (event types — new ones added over time) =====
class BazarConfirmedNotification extends Notification {
    public BazarConfirmedNotification(NotificationSender sender) { super(sender); }
    public void notifyUser() {
        sender.sendMessage("Your monthly bazar has been confirmed.");
    }
}

class BazarDispatchedNotification extends Notification {
    public BazarDispatchedNotification(NotificationSender sender) { super(sender); }
    public void notifyUser() {
        sender.sendMessage("Your bazar is on the way!");
    }
}

class PaymentFailedNotification extends Notification {
    public PaymentFailedNotification(NotificationSender sender) { super(sender); }
    public void notifyUser() {
        sender.sendMessage("URGENT: Your payment failed. Please update your payment method.");
    }
}

// ===== Demo =====
public class _22_B1 {
    public static void main(String[] args) {
        // Same event, different channels
        Notification confirmedByEmail = new BazarConfirmedNotification(new EmailSender());
        Notification confirmedByWhatsApp = new BazarConfirmedNotification(new WhatsAppSender());

        // Different event, different channel
        Notification failedBySMS = new PaymentFailedNotification(new SMSSender());
        Notification dispatchedByPush = new BazarDispatchedNotification(new PushSender());

        confirmedByEmail.notifyUser();
        confirmedByWhatsApp.notifyUser();
        failedBySMS.notifyUser();
        dispatchedByPush.notifyUser();

        // Adding a new channel or a new event type later only means
        // adding one new class on the relevant side — nothing above changes.
    }
}