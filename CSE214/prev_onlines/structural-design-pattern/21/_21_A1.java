// Legacy Weather Service, which we cannot modify 
class LegacyWeatherService { 
    public String getWeatherData() { 
        return "Legacy weather data"; 
    } 
} 
 
// Client Interface expected by the application 
interface WeatherProvider { 
    String fetchWeather(); 
} 
 
// Application class that depends on the WeatherProvider interface 
class WeatherApp { 
    private WeatherProvider weatherProvider; 
 
    public WeatherApp(WeatherProvider weatherProvider) { 
        this.weatherProvider = weatherProvider; 
    } 
 
    public void displayWeather() { 
        System.out.println(weatherProvider.fetchWeather()); 
    } 
}

class LegacyWeatherServiceAdapter implements WeatherProvider {
    private LegacyWeatherService adaptee;

    public LegacyWeatherServiceAdapter(LegacyWeatherService legacyWeatherService) {
        this.adaptee = legacyWeatherService;
    }

    public String fetchWeather() {
        return adaptee.getWeatherData();       
    }
}

public class _21_A1 {
    public static void main(String[] args) {
        LegacyWeatherService legacyWeatherService = new LegacyWeatherService();
        LegacyWeatherServiceAdapter legacyWeatherServiceAdapter = new LegacyWeatherServiceAdapter(legacyWeatherService);

        WeatherApp weatherApp = new WeatherApp(legacyWeatherServiceAdapter);
        weatherApp.displayWeather();
    }
}