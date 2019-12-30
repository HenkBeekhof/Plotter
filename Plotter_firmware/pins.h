#ifndef PINS
#define PINS

// For RAMPS 1.4
#define X_STEP_PIN         54
#define X_DIR_PIN          55
#define X_ENABLE_PIN       38         // 0=Enabled
#define X_MIN_PIN           3         // 0=End switch closed
#define X_MAX_PIN           2         // 0=End switch closed

#define Y_STEP_PIN         60
#define Y_DIR_PIN          61
#define Y_ENABLE_PIN       56         // 0=Enabled
#define Y_MIN_PIN          14         // 0=End switch closed
#define Y_MAX_PIN          15         // 0=End switch closed

#define Z_STEP_PIN         46
#define Z_DIR_PIN          48
#define Z_ENABLE_PIN       62         // 0=Enabled
#define Z_MIN_PIN          18         // 0=End switch closed
#define Z_MAX_PIN          19         // 0=End switch closed

#define E_STEP_PIN         26
#define E_DIR_PIN          28
#define E_ENABLE_PIN       24         // 0=Enabled

#define SDSS               53
#define LED_PIN            13

#define FAN_PIN            9

#define PS_ON_PIN          12

#define HEATER_1_PIN       8
#define TEMP_0_PIN         13       // ANALOG NUMBERING
#define TEMP_1_PIN         14       // ANALOG NUMBERING

#define SCL                21       // I2C clock
#define SDA                20       // I2C data

#define FAN                10       // Fan on pin D10

#define SERVO_1            11       // Servo on pin D11
#define SERVO_2            6        // Servo on pin D6
#define SERVO_3            5        // Servo on pin D5
#define SERVO_4            4        // Servo on pin D4

#endif
