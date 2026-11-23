#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_MAX31865.h>
#define heater 9
#define valve 8
#define led_b 7
#define led_r 6
#define led_g 5
#define button 4

// تنظیمات MAX31865
#define RREF      430.0  // مقاومت مرجع
#define RNOMINAL  100.0  // مقاومت نامی سنسور PT100

Adafruit_MAX31865 max31865 = Adafruit_MAX31865(10, 11, 12, 13); // (CS, DI, DO, CLK)

// تنظیمات OLED
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1  // پین ریست استفاده نمی‌شود
#define SSD1306_I2C_ADDRESS 0x3C
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() 
{
  // شروع ارتباط سریال برای دیباگ
  Serial.begin(9600);

  // شروع OLED
  if (!display.begin(SSD1306_I2C_ADDRESS, 0x3C)) 
  { // آدرس پیش‌فرض 0x3C
    Serial.println(F("OLED initialization failed!"));
    for (;;);
  }
 
  pinMode(heater,OUTPUT);
  pinMode(valve,OUTPUT);
  pinMode(led_b,OUTPUT);
  pinMode(led_r,OUTPUT);
  pinMode(led_g,OUTPUT);
  pinMode(button,INPUT_PULLUP);

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setRotation(2);  // چرخش نمایشگر برای نمایش صحیح
  
  // شروع MAX31865
  max31865.begin(MAX31865_4WIRE);  // چهار سیمه
}

void loop() 
{
  // خواندن دما از MAX31865
  float temperature = max31865.temperature(RNOMINAL, RREF);

  // بررسی خطا در سنسور
  if (isnan(temperature) || temperature < -100.0 || temperature > 500.0) 
  {
    Serial.println(F("Error reading temperature!"));
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("Error: Sensor");
    display.display();
    delay(1000);
    return;
  }

  // نمایش روی سریال مانیتور
  Serial.print("Temperature: ");
  Serial.println(temperature);

  // نمایش روی OLED
  display.clearDisplay();
  display.setCursor(0,0);
  display.println("Temperature:");
  display.setTextSize(1);
  display.setCursor(30,10);
  display.print(temperature, 2); // نمایش تا 2 رقم اعشار
  display.println(" C");
  display.display();

  if (temperature < 100)
  {
    digitalWrite(heater,LOW);
    digitalWrite(led_r,HIGH);
    digitalWrite(led_b,LOW);
    display.setTextSize(1);
    display.setCursor(30,30);
    display.print("warming up!");
    display.display();
  }
  else
  {
    digitalWrite(heater,HIGH);
    digitalWrite(led_r,LOW);
    digitalWrite(led_b,HIGH);
    display.setTextSize(1);
    display.setCursor(30,30);
    display.print("ready to drink");
    display.display();
  }

  if (digitalRead(button)== LOW)
  {
    digitalWrite(valve,HIGH);
    for (int i=0 ; i < 6 ; i++)
    {
      digitalWrite(led_g,HIGH);
      delay(50);
      digitalWrite(led_g,LOW);
      delay(50);
    }
  }
  else
  {
    digitalWrite(led_g,LOW);
    digitalWrite(valve,LOW);
  }

  delay(100); // به‌روزرسانی هر ثانیه
}
