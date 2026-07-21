// if the things and everything are just strings
// this is just factory isn't it?/
// eita onekjaygay abstractfactory / builder diye kore rakhse
// so check carefully

// ============================================================
// Creational Design Pattern Used: BUILDER PATTERN
//
// The task requires separating the *construction* of a complex
// HolidayPackage object (which has multiple parts: flight, hotel,
// activity, built step by step) from its final *representation*.
// That is exactly the intent of the Builder pattern: a Director
// drives the same construction steps (buildFlight -> buildHotel ->
// buildActivity) against different ConcreteBuilders to produce
// different representations (Relaxation vs Adventure) of the
// HolidayPackage product.
// ============================================================

import java.util.Scanner;

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

// Director: runs the same construction process regardless of which builder is used
class TravelAgencyDirector {
    public HolidayPackage construct(HolidayPackageBuilder builder) {
        builder.buildFlight();
        builder.buildHotel();
        builder.buildActivity();
        return builder.getResult();
    }
}

public class Main {
    public static void main(String[] args) {
        TravelAgencyDirector director = new TravelAgencyDirector();

        // get input
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter which type of HolidayPackage you would like = ");
        String type = sc.nextLine();

        HolidayPackageBuilder builder;
        if (type.equals("Relaxation")) {
            builder = new RelaxationPackageBuilder();
        } else if (type.equals("Adventure")) {
            builder = new AdventurePackageBuilder();
        } else {
            throw new IllegalArgumentException("Package type must be Relaxation or Adventure");
        }

        // same construction process (director.construct), different representation
        HolidayPackage p = director.construct(builder);
        System.out.println(p);
    }
}
