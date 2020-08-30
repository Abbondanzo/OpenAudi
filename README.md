# OpenAudi

This library is designed to provide an RS232 adapter for [OpenAuto](https://github.com/f1xpl/openauto), reading transmitted MMI input controls and converting them into keypresses that the OpenAuto application uses.

## Mappings

The keycode mappings are located in the `mappings.txt` file. I read these directly from the 16th pin on the MMI adapter to the 3rd pin on a female DB9 adapter attached to [this](https://www.amazon.com/dp/B00RVC7N46/) TTL logic converter. I used picocom to grab these mappings.

## Equipment

Not all equipment has to be the same, but here's what I used

-   [MAX3232 RS232 Serial Port to TTL Converter Module DB9 Connector](https://www.amazon.com/dp/B00RVC7N46/)
-   Metal pins from a male DB9 connector. Feel free to use the entire connector, I pulled these from a damaged cable I had lying around
-   Raspberry Pi 3B running OpenAuto Pro (Raspbian also works)
-   Wire and crimp splice connectors
-   (4x) female-to-female jumper wires
-   Audi A6 4F (C6) 2006 model, running a 2G High MMI system
-   Patience

## Adding to OpenAuto

Since we don't care about random keypresses onto the system, [running the script at boot](https://www.raspberrypi.org/documentation/linux/usage/rc-local.md) is advised.
