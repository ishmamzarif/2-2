interface Tier {
    String name();
    int range();
    boolean moodAllowed();
    Tier promote();
    Tier demote();
}

class Common implements Tier {
    public String name() { return "Common"; }
    public int range() { return 10; }
    public boolean moodAllowed() { return false; }
    public Tier promote() { return new Plus(); }
    public Tier demote() { return this; }
}

class Plus implements Tier {
    public String name() { return "Plus"; }
    public int range() { return 50; }
    public boolean moodAllowed() { return false; }
    public Tier promote() { return new Lux(); }
    public Tier demote() { return new Common(); }
}

class Lux implements Tier {
    public String name() { return "Lux"; }
    public int range() { return 50; }
    public boolean moodAllowed() { return true; }
    public Tier promote() { return this; }
    public Tier demote() { return new Plus(); }
}

class Subscription {
    private Tier tier = new Common();

    void travelCheck(int km) {
        if (km > tier.range()) {
            System.out.println("UNSTABLE at " + km + "km on " + tier.name()
                + " (range 0-" + tier.range() + "km) - ALERT: bring patient back into coverage");
        } else {
            System.out.println("STABLE at " + km + "km on " + tier.name());
        }
    }

    void promote() {
        tier = tier.promote();
        System.out.println("Promoted -> " + tier.name());
    }

    void demote() {
        tier = tier.demote();
        System.out.println("Demoted -> " + tier.name());
    }

    void activateLux(int hours) {
        final Tier prior = tier;
        tier = new Lux();
        System.out.println("Lux activated for " + hours + "h (prior tier: " + prior.name() + ")");
        new Thread(() -> {
            try { Thread.sleep(hours * 200L); } catch (InterruptedException ignored) {}
            tier = prior;
            System.out.println("Lux duration ended -> reverted to " + tier.name());
        }).start();
    }

    void setMood(String mood) {
        if (tier.moodAllowed()) {
            System.out.println("Mood set to " + mood);
        } else {
            System.out.println("Mood control unavailable");
        }
    }
}

public class _22A1 {
    public static void main(String[] args) throws InterruptedException {
        Subscription sub = new Subscription();

        sub.travelCheck(5);
        sub.travelCheck(15);
        sub.travelCheck(0);

        sub.promote();
        sub.travelCheck(30);

        sub.promote();
        sub.travelCheck(40);

        sub.demote();
        sub.demote();
        sub.demote();

        sub.setMood("calm");

        sub.activateLux(1);
        Thread.sleep(50);
        sub.setMood("happy");
        Thread.sleep(300);
        sub.setMood("exhausted");
    }
}