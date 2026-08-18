// ===== Target interface (fixed, cannot be changed) =====
interface SmartDevice {
    void turnOn();
    void turnOff();
}

// ===== Existing devices (already compatible) =====
class SmartLight implements SmartDevice {
    private boolean isOn = false;
    public void turnOn() {
        if (!isOn) {
            System.out.println("Turning on");
            isOn = true;
        }
    }
    public void turnOff() {
        if (isOn) {
            System.out.println("Turning off");
            isOn = false;
        }
    }
}

class SmartFan implements SmartDevice {
    private boolean isOn = false;
    public void turnOn() {
        if (!isOn) {
            System.out.println("Turning on");
            isOn = true;
        }
    }
    public void turnOff() {
        if (isOn) {
            System.out.println("Turning off");
            isOn = false;
        }
    }
}

class SmartAC implements SmartDevice {
    private boolean isOn = false;
    public void turnOn() {
        if (!isOn) {
            System.out.println("Turning on");
            isOn = true;
        }
    }
    public void turnOff() {
        if (isOn) {
            System.out.println("Turning off");
            isOn = false;
        }
    }
}

// ===== Third-party device 1 (incompatible interface, cannot be modified) =====
class OldSmartBulb {
    private boolean isOn = false;
    public void powerOn() {
        if (!isOn) isOn = true;
    }
    public void powerOff() {
        if (isOn) isOn = false;
    }
}

// ===== Third-party device 2 (incompatible interface, cannot be modified) =====
class LegacyHeater {
    private boolean isHeating = false;
    public void startHeating() {
        if (!isHeating) isHeating = true;
    }
    public void stopHeating() {
        if (isHeating) isHeating = false;
    }
}

// ===== Adapter for OldSmartBulb =====
class OldBulbAdapter implements SmartDevice {
    private OldSmartBulb oldSmartBulb;

    public OldBulbAdapter(OldSmartBulb oldSmartBulb) {
        this.oldSmartBulb = oldSmartBulb;
    }

    public void turnOn() {
        System.out.println("Turning on");
        oldSmartBulb.powerOn();
    }

    public void turnOff() {
        System.out.println("Turning off");
        oldSmartBulb.powerOff();
    }
}

// ===== Adapter for LegacyHeater =====
class LegacyHeaterAdapter implements SmartDevice {
    private LegacyHeater legacyHeater;

    public LegacyHeaterAdapter(LegacyHeater legacyHeater) {
        this.legacyHeater = legacyHeater;
    }

    public void turnOn() {
        System.out.println("Turning on");
        legacyHeater.startHeating();
    }

    public void turnOff() {
        System.out.println("Turning off");
        legacyHeater.stopHeating();
    }
}

// ===== Demo =====
public class _22_B2 {
    public static void main(String[] args) {
        SmartDevice ac = new SmartAC();
        ac.turnOn();
        ac.turnOff();

        SmartDevice oldBulbAdapter = new OldBulbAdapter(new OldSmartBulb());
        oldBulbAdapter.turnOn();
        oldBulbAdapter.turnOff();

        SmartDevice heaterAdapter = new LegacyHeaterAdapter(new LegacyHeater());
        heaterAdapter.turnOn();
        heaterAdapter.turnOff();

        // The voice-command app only ever talks to SmartDevice.
        // Adding another third-party device later just means
        // writing one new adapter class — nothing above changes.
    }
}