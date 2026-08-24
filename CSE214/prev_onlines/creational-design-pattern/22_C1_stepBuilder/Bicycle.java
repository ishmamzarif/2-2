import java.util.Objects;

public class Bicycle {
    private String frame;
    private String gear_system;
    private String tire_type;

    // private constructor that only the builder can access
    private Bicycle() {

    }

    public void printBicycleSpecs() {
        System.out.println("Frame: " + frame + ", Gear: " + gear_system + ", Tire: " + tire_type);
    }

    interface FrameBuilder {
        public GearBuilder withFrame(String frame);
    }

    interface GearBuilder {
        public TireBuilder withGear(String gear);
    }

    interface TireBuilder {
        public BicycleBuilder withTire(String tire);
    } 

    static class BicycleBuilder implements GearBuilder, TireBuilder, FrameBuilder {
        private Bicycle bicycle;

        private BicycleBuilder() {
            bicycle = new Bicycle();
        }

        public static FrameBuilder getBuilder() {
            return new BicycleBuilder();
        }

        public GearBuilder withFrame(String frame) {
            bicycle.frame = frame;
            return this;
        }

        public TireBuilder withGear(String gear) {
            bicycle.gear_system = gear;
            return this;
        }

        public BicycleBuilder withTire(String tire) {
            bicycle.tire_type = tire;
            return this;
        }

        public Bicycle build() {
            Objects.requireNonNull(bicycle.frame, "Frame cannot be null");
            Objects.requireNonNull(bicycle.gear_system, "Gear system cannot be null");
            Objects.requireNonNull(bicycle.tire_type, "Tire type cannot be null");
        
            // also could add non-empty check here 

            return bicycle;
        }
    }

}
