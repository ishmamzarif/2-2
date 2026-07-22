class GameConfig {
    private int gameRes;
    private int audioVolume;
    private int difficultyLevel;

    private void loadConfig() {
        // load the config from the file
        System.out.println("loading...");
    }
    private GameConfig() {
        loadConfig();
    }

    private static GameConfig gameConfig = null;

    public static GameConfig getInstance() {
        if (gameConfig == null) {
            gameConfig = new GameConfig();
        }
        return gameConfig;
    }
}
public class Main {
    public static void main(String[] args) {
        GameConfig gc1 = GameConfig.getInstance();
        System.out.println("gc1 = " + gc1.hashCode());
        
        GameConfig gc2 = GameConfig.getInstance();
        System.out.println("gc2 = " + gc2.hashCode());
    }
}
