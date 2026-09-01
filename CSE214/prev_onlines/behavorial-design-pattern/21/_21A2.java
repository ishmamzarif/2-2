interface NotificationChannel {
    void send(String message);
}

class EmailNotification implements NotificationChannel {
    public void send(String message) {
        System.out.println("Email: " + message);
    }
}

class SmsNotification implements NotificationChannel {
    public void send(String message) {
        System.out.println("SMS: " + message);
    }
}

class AppNotification implements NotificationChannel {
    public void send(String message) {
        System.out.println("App push: " + message);
    }
}

class NotificationService {
    private NotificationChannel channel;

    void setChannel(NotificationChannel channel) {
        this.channel = channel;
    }

    void dispatch(String message) {
        channel.send(message);
    }
}

public class _21A2 {
    public static void main(String[] args) {
        NotificationService service = new NotificationService();

        service.setChannel(new EmailNotification());
        service.dispatch("Transaction: $200 debited");

        service.setChannel(new SmsNotification());
        service.dispatch("Low balance warning");

        service.setChannel(new AppNotification());
        service.dispatch("Promotional offer: 10% cashback");
    }
}