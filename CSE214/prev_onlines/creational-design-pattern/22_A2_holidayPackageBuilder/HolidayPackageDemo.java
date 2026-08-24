// Product: the complex object being built
class HolidayPackage {
    private String flight;
    private String hotel;
    private String activity;

    public void setFlight(String flight) { this.flight = flight; }
    public void setHotel(String hotel) { this.hotel = hotel; }
    public void setActivity(String activity) { this.activity = activity; }

    @Override
    public String toString() {
        return "HolidayPackage{" +
                "flight='" + flight + '\'' +
                ", hotel='" + hotel + '\'' +
                ", activity='" + activity + '\'' +
                '}';
    }
}

// Builder interface: defines the construction steps
interface HolidayPackageBuilder {
    void buildFlight();
    void buildHotel();
    void buildActivity();
    HolidayPackage getResult();
}

// Concrete builder: Relaxation Package
class RelaxationPackageBuilder implements HolidayPackageBuilder {
    private HolidayPackage pkg = new HolidayPackage();

    public void buildFlight() { pkg.setFlight("Business Class Flight"); }
    public void buildHotel() { pkg.setHotel("5-Star Resort"); }
    public void buildActivity() { pkg.setActivity("Spa Treatment"); }
    public HolidayPackage getResult() { return pkg; }
}

// Concrete builder: Adventure Package
class AdventurePackageBuilder implements HolidayPackageBuilder {
    private HolidayPackage pkg = new HolidayPackage();

    public void buildFlight() { pkg.setFlight("Economy Flight"); }
    public void buildHotel() { pkg.setHotel("Mountain Cabin"); }
    public void buildActivity() { pkg.setActivity("Hiking Tour"); }
    public HolidayPackage getResult() { return pkg; }
}

// Custom builder: lets the client pick any flight/hotel/activity combo
// (bypasses the Director since there's no fixed recipe for "custom")
class CustomPackageBuilder {
    private HolidayPackage pkg = new HolidayPackage();

    public CustomPackageBuilder buildFlight(String flight) {
        pkg.setFlight(flight);
        return this;
    }

    public CustomPackageBuilder buildHotel(String hotel) {
        pkg.setHotel(hotel);
        return this;
    }

    public CustomPackageBuilder buildActivity(String activity) {
        pkg.setActivity(activity);
        return this;
    }

    public HolidayPackage getResult() {
        return pkg;
    }
}

// Director: runs the same construction process regardless of builder used
class TravelAgencyDirector {
    public HolidayPackage construct(HolidayPackageBuilder builder) {
        builder.buildFlight();
        builder.buildHotel();
        builder.buildActivity();
        return builder.getResult();
    }
}

public class HolidayPackageDemo {
    public static void main(String[] args) {
        TravelAgencyDirector director = new TravelAgencyDirector();

        HolidayPackage relaxation = director.construct(new RelaxationPackageBuilder());
        System.out.println(relaxation);

        HolidayPackage adventure = director.construct(new AdventurePackageBuilder());
        System.out.println(adventure);

        // Custom combo, no Director needed - just call the steps yourself
        HolidayPackage custom = new CustomPackageBuilder()
                .buildFlight("First Class Flight")
                .buildHotel("Beachfront Villa")
                .buildActivity("Scuba Diving")
                .getResult();
        System.out.println(custom);
    }
}