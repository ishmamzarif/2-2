interface Mediator {
    void notifyDevices(String event);
}

class SmartHub implements Mediator {
    private LightSensor sensor;
    private AutomaticBlinds blinds;
    private AirConditioner ac;

    public void setSensor(LightSensor sensor) {
        this.sensor = sensor;
    }
    public void setBlind(AutomaticBlinds blinds) {
        this.blinds = blinds;
    }
    public void setAC(AirConditioner ac) {
        this.ac = ac;
    }

    @Override
    public void notifyDevices(String event) {
        if (event.equals("High Brightness")) {
            System.out.println("Mediator got message of high brightness");
            System.out.println("Closing blinds...");
            blinds.close();
        }
        if (event.equals("closing")) {
            System.out.println("Mediator got message of blinds closing");
            ac.turnOn();
        }
    }

}

class LightSensor {
    private Mediator mediator;
    public LightSensor(Mediator mediator) {
        this.mediator = mediator;
    }

    public void detectHighBrightness() {
        mediator.notifyDevices("High Brightness");
    }
}

class AutomaticBlinds {
    private Mediator mediator;
    private boolean state;
    public AutomaticBlinds(Mediator mediator) {
        this.mediator = mediator;
        state = true;
    }
    public void close() {
        if (state == true) {
            state = false;
            System.out.println("Closing the blinds");
            mediator.notifyDevices("closing");
        }
    }
    public void open() {
        if (state == false) {
            state = true;
            System.out.println("Opening the blinds");
        }
    }
}

class AirConditioner {
    private Mediator mediator;
    private boolean state;
    public AirConditioner(Mediator mediator) {
        this.mediator = mediator;
        state = false;
    }
    public void turnOn() {
        if (state == false) {
            state = true;
            System.out.println("Turning on AC");
        }
    }
    public void turnOff() {
        if (state == true) {
            state = false;
            System.out.println("Turning off AC");
        }
    }
}



public class _22B2 {
    public static void main(String[] args) {
        SmartHub mediator = new SmartHub();
        AutomaticBlinds blinds = new AutomaticBlinds(mediator);
        AirConditioner ac = new AirConditioner(mediator);
        LightSensor sensor = new LightSensor(mediator);

        mediator.setAC(ac);
        mediator.setBlind(blinds);
        mediator.setSensor(sensor);

        sensor.detectHighBrightness();
    }
}