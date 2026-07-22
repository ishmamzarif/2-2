import java.util.HashMap;
import java.util.Map;
import java.util.function.Supplier;

interface Notification {
    void notifyUser();
}

class SMSNotification implements Notification {
    public void notifyUser() {
        System.out.println("Sending an SMS notification");
    }
}

class EmailNotification implements Notification {
    public void notifyUser() {
        System.out.println("Sending an Email notification");
    }
}

class PushNotification implements Notification {
    public void notifyUser() {
        System.out.println("Sending a Push notification");
    }
}

class NotificationFactory {
    private static final Map<String, Supplier<Notification>> registry = new HashMap<>();

    static {
        registry.put("SMS", SMSNotification::new);
        registry.put("EMAIL", EmailNotification::new);
        registry.put("PUSH", PushNotification::new);
    }

    public static Notification createNotification(String type) {
        Supplier<Notification> constructor = registry.get(type.toUpperCase());
        if (constructor == null) {
            throw new IllegalArgumentException("Unknown notification type: " + type);
        }
        return constructor.get();
    }
}
// Supplier<Notification> is a functional interface
// from java.util.function, produces a type of Notification when called
// only one method get()

// Supplier<Notification> s = SMSNotification::new;
// Notification n = s.get(); // calls new SMSNotification

// why is this more elegant?
// for adding SlackMessage, just go registry.put("SLACK", SlackNotification::new)
// no lengthy if else chain


public class Main {
    public static void main(String[] args) {
        Notification n1 = NotificationFactory.createNotification("SMS");
        n1.notifyUser();

        Notification n2 = NotificationFactory.createNotification("Email");
        n2.notifyUser();

        Notification n3 = NotificationFactory.createNotification("push");
        n3.notifyUser();
    }
}