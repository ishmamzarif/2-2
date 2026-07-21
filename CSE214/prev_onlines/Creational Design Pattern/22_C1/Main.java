public class Main {
    public static void main(String[] args) {
        BicycleDirector director = new BicycleDirector();

        Bicycle commuter = director.construct("Commuter");
        commuter.printBicycleSpecs();

        Bicycle mountainBeast = director.construct("Mountain Beast");
        mountainBeast.printBicycleSpecs();
    }
}
