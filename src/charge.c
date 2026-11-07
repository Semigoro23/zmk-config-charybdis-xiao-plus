// SPDX-License-Identifier: MIT
#include <errno.h>
#include <zephyr/device.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/init.h>

/* P0.13 is HICHG, not D13 (P1.01). Leave the optional ISET leg floating. */
static int y13_charge_init(void) {
    const struct device *port = DEVICE_DT_GET(DT_NODELABEL(gpio0));
    if (!device_is_ready(port)) {
        return -ENODEV;
    }
    return gpio_pin_configure(port, 13, GPIO_INPUT);
}
SYS_INIT(y13_charge_init, APPLICATION, 90);
