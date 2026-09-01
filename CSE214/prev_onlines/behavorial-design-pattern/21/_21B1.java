interface TrafficState {
    void next(TrafficLight light);
    String name();
    int duration();
}

class RedState implements TrafficState {
    public String name() { return "RED"; }
    public int duration() { return 5; }
    public void next(TrafficLight light) {
        light.setState(new YellowState());
    }
}

class YellowState implements TrafficState {
    public String name() { return "YELLOW"; }
    public int duration() { return 2; }
    public void next(TrafficLight light) {
        light.setState(new GreenState());
    }
}

class GreenState implements TrafficState {
    public String name() { return "GREEN"; }
    public int duration() { return 10; }
    public void next(TrafficLight light) {
        light.setState(new RedState());
    }
}

class TrafficLight {
    private TrafficState state = new RedState();

    void setState(TrafficState state) {
        this.state = state;
    }

    void run(int steps) throws InterruptedException {
        for (int i = 0; i < steps; i++) {
            System.out.println("Light is " + state.name() + " for " + state.duration() + "s");
            Thread.sleep(state.duration() * 200L);
            state.next(this);
        }
    }
}

public class _21B1 {
    public static void main(String[] args) throws InterruptedException {
        TrafficLight light = new TrafficLight();
        light.run(4);
    }
}