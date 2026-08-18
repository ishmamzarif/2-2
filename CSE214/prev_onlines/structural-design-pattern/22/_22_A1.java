interface Notification {
    public String send(String msg);
}

class EmailNotification implements Notification {
    public String send(String msg) {
        return "Sending Email Notification" + msg;
    }
}


class PushNotification implements Notification {
    public String send(String msg) {
        return "Sending Push Notification" + msg;
    }
}


class SMSNotification implements Notification {
    public String send(String msg) {
        return "Sending SMS Notification" + msg;
    }
}

abstract class NotificationDecorator implements Notification {
    protected Notification n;
    public NotificationDecorator(Notification n) {
        this.n = n;
    }
}

class EncryptedNotificationDecorator extends NotificationDecorator {
    public EncryptedNotificationDecorator(Notification n) {
        super(n);
    }
    public String send(String msg) {
        return super.n.send(msg) + " with Encryption";
    }
}

class PriorityLabelDecorator extends NotificationDecorator {
    public PriorityLabelDecorator(Notification n) {
        super(n);
    }
    public String send(String msg) {
        return super.n.send(msg) + " with Priority";
    }
}

class LogggingDecorator extends NotificationDecorator {
    public LogggingDecorator(Notification n) {
        super(n);
    }
    public String send(String msg) {
        return super.n.send(msg) + " with Logging Feature";
    }
} 

public class _22_A1 {
    public static void main(String[] args) {
        Notification n = new EmailNotification();
        System.out.println(n.send("Hello"));

        EncryptedNotificationDecorator encryptedNotification = new EncryptedNotificationDecorator(n);
        System.out.println(encryptedNotification.send("Hello"));
    }
}






// ===== Component =====
interface Notifier {
    void send(String message);
}

// ===== Concrete Components (the 3 notification channels) =====
class EmailNotifier implements Notifier {
    public void send(String message) {
        System.out.println("Email: " + message);
    }
}

class SMSNotifier implements Notifier {
    public void send(String message) {
        System.out.println("SMS: " + message);
    }
}

class PushNotifier implements Notifier {
    public void send(String message) {
        System.out.println("Push: " + message);
    }
}

// ===== Decorator base class =====
abstract class NotifierDecorator implements Notifier {
    protected Notifier wrappee;
    public NotifierDecorator(Notifier wrappee) {
        this.wrappee = wrappee;
    }
}

// ===== Concrete Decorators (the 3 toggleable features) =====
class EncryptionDecorator extends NotifierDecorator {
    public EncryptionDecorator(Notifier wrappee) { super(wrappee); }
    public void send(String message) {
        wrappee.send("[ENCRYPTED] " + message);
    }
}

class PriorityDecorator extends NotifierDecorator {
    public PriorityDecorator(Notifier wrappee) { super(wrappee); }
    public void send(String message) {
        wrappee.send("[HIGH PRIORITY] " + message);
    }
}

class LoggingDecorator extends NotifierDecorator {
    public LoggingDecorator(Notifier wrappee) { super(wrappee); }
    public void send(String message) {
        wrappee.send(message);
        System.out.println("Log: notification recorded for audit");
    }
}

// ===== Demo =====
class Demo {
    public static void main(String[] args) {
        // Base: user picked Email as the channel
        Notifier notifier = new EmailNotifier();

        // User toggled ON: Encryption, Priority Label, Logging
        // (any subset, in any order, could be applied here)
        notifier = new EncryptionDecorator(notifier);
        notifier = new PriorityDecorator(notifier);
        notifier = new LoggingDecorator(notifier);

        notifier.send("Motion detected at front door");
    }
}