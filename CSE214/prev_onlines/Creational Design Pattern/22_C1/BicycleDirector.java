// Director: knows the recipes for the standard models,
// so the client only asks for a model name
public class BicycleDirector {

    // single entry point: client names a model, never a recipe method
    public Bicycle construct(String model) {
        switch (model.toLowerCase()) {
            case "commuter":
                return constructCommuter();
            case "mountain beast":
                return constructMountainBeast();
            default:
                throw new IllegalArgumentException("Unknown model: " + model);
        }
    }

    public Bicycle constructCommuter() {
        return Bicycle.BicycleBuilder.getBuilder()
                .withFrame("Aluminum Frame")
                .withGear("Single Speed Gear")
                .withTire("Road Tires")
                .build();
    }

    public Bicycle constructMountainBeast() {
        return Bicycle.BicycleBuilder.getBuilder()
                .withFrame("Carbon Fiber Frame")
                .withGear("12-Speed Gear")
                .withTire("Off-road Grip Tires")
                .build();
    }
}
