// Copyright (c) 2025 Darshan P. All rights reserved.

// This work is licensed under the terms of the MIT license.
// For a copy, see <https://opensource.org/licenses/MIT>.

#include <libusb-1.0/libusb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_DEVICES 128
#define MAX_DESCRIPTOR_SIZE 4096
#define MAX_INTERFACES 8
#define DUMP_FILE "usb_descriptors_dump.txt"

// Descriptor types
#define USB_DT_DEVICE 0x01
#define USB_DT_CONFIG 0x02
#define USB_DT_STRING 0x03
#define USB_DT_INTERFACE 0x04
#define USB_DT_ENDPOINT 0x05
#define USB_DT_DEVICE_QUALIFIER 0x06
#define USB_DT_OTHER_SPEED_CONFIG 0x07
#define USB_DT_INTERFACE_POWER 0x08
#define USB_DT_OTG 0x09
#define USB_DT_DEBUG 0x0A
#define USB_DT_INTERFACE_ASSOCIATION 0x0B
#define USB_DT_SECURITY 0x0C
#define USB_DT_KEY 0x0D
#define USB_DT_ENCRYPTION_TYPE 0x0E
#define USB_DT_BOS 0x0F
#define USB_DT_DEVICE_CAPABILITY 0x10
#define USB_DT_WIRELESS_ENDPOINT_COMP 0x11
#define USB_DT_SUPERSPEED_USB_ENDPOINT_COMP 0x30
#define USB_DT_SUPERSPEED_ISO_ENDPOINT_COMP 0x31

void write_bytes_to_file(FILE *file, const unsigned char *data, int length) {
    for (int i = 0; i < length; ++i) {
        fprintf(file, "0x%02x ", data[i]);
    }
}

int get_descriptor(libusb_device_handle *handle, uint8_t desc_type,
                   uint8_t desc_index, unsigned char *data, int length) {
    return libusb_control_transfer(
        handle,
        LIBUSB_ENDPOINT_IN | LIBUSB_REQUEST_TYPE_STANDARD |
            LIBUSB_RECIPIENT_DEVICE,
        LIBUSB_REQUEST_GET_DESCRIPTOR, (desc_type << 8) | desc_index, 0, data,
        length, 1000);
}

int main() {
    libusb_device **devs;
    libusb_context *ctx = NULL;
    int r;
    ssize_t cnt;

    libusb_device_handle *handle = NULL;
    struct libusb_device_descriptor desc;
    unsigned char buffer[MAX_DESCRIPTOR_SIZE];
    unsigned char string_data[256];

    r = libusb_init(&ctx);
    if (r < 0) {
        fprintf(stderr, "libusb init error\n");
        return 1;
    }

    cnt = libusb_get_device_list(ctx, &devs);
    if (cnt < 0) {
        fprintf(stderr, "Error getting USB device list\n");
        libusb_exit(ctx);
        return 1;
    }

    printf("Connected USB devices:\n");
    int index = 0;
    int device_indices[MAX_DEVICES];

    for (int i = 0; devs[i]; ++i) {
        r = libusb_get_device_descriptor(devs[i], &desc);
        if (r < 0) {
            fprintf(stderr, "Failed to get device descriptor\n");
            continue;
        }

        // Get product name if possible
        libusb_device_handle *temp_handle;
        r = libusb_open(devs[i], &temp_handle);

        printf("[%d] VID: %04x PID: %04x", index, desc.idVendor, desc.idProduct);

        if (r == 0 && temp_handle) {
            if (desc.iProduct > 0) {
                memset(string_data, 0, sizeof(string_data));
                if (libusb_get_string_descriptor_ascii(
                        temp_handle, desc.iProduct, string_data,
                        sizeof(string_data)) > 0) {
                    printf(" - %s", string_data);
                }
            }
            libusb_close(temp_handle);
        }
        printf("\n");

        device_indices[index++] = i;
    }

    if (index == 0) {
        printf("No USB devices found.\n");
        libusb_free_device_list(devs, 1);
        libusb_exit(ctx);
        return 1;
    }

    int choice;
    printf("\nSelect a device by number: ");
    scanf("%d", &choice);

    if (choice < 0 || choice >= index) {
        printf("Invalid choice.\n");
        libusb_free_device_list(devs, 1);
        libusb_exit(ctx);
        return 1;
    }

    libusb_device *selected_dev = devs[device_indices[choice]];

    r = libusb_open(selected_dev, &handle);
    if (r != 0 || !handle) {
        fprintf(stderr, "Failed to open device: %s\n", libusb_error_name(r));
        libusb_free_device_list(devs, 1);
        libusb_exit(ctx);
        return 1;
    }

    FILE *out = fopen(DUMP_FILE, "w");
    if (!out) {
        perror("fopen");
        libusb_close(handle);
        libusb_free_device_list(devs, 1);
        libusb_exit(ctx);
        return 1;
    }

    // Array to track which interfaces had kernel drivers attached
    int kernel_driver_active[MAX_INTERFACES] = {0};
    int num_interfaces = 0;

    // Get number of interfaces from configuration
    r = libusb_get_device_descriptor(selected_dev, &desc);
    if (r == 0 && desc.bNumConfigurations > 0) {
        struct libusb_config_descriptor *config;
        r = libusb_get_config_descriptor(selected_dev, 0, &config);
        if (r == 0) {
            num_interfaces = config->bNumInterfaces;
            libusb_free_config_descriptor(config);
        }
    }

    // Limit to MAX_INTERFACES
    if (num_interfaces > MAX_INTERFACES) num_interfaces = MAX_INTERFACES;
    if (num_interfaces == 0)
        num_interfaces = 1;  // Assume at least one interface

    // Claim interfaces and remember which had kernel drivers
    for (int i = 0; i < num_interfaces; i++) {
        kernel_driver_active[i] = libusb_kernel_driver_active(handle, i);
        if (kernel_driver_active[i]) {
            libusb_detach_kernel_driver(handle, i);
        }
        libusb_claim_interface(handle, i);
    }

    // Get device descriptor
    memset(buffer, 0, sizeof(buffer));
    r = get_descriptor(handle, USB_DT_DEVICE, 0, buffer, 18);
    if (r > 0) {
        write_bytes_to_file(out, buffer, r);
    }

    // Get BOS descriptor (USB 3.0+)
    memset(buffer, 0, sizeof(buffer));
    r = get_descriptor(handle, USB_DT_BOS, 0, buffer, sizeof(buffer));
    if (r > 0) {
        write_bytes_to_file(out, buffer, r);
    }

    // Get device qualifier descriptor
    memset(buffer, 0, sizeof(buffer));
    r = get_descriptor(handle, USB_DT_DEVICE_QUALIFIER, 0, buffer,
                       sizeof(buffer));
    if (r > 0) {
        write_bytes_to_file(out, buffer, r);
    }

    // Get string descriptors
    for (int i = 0; i < 4; i++) {  // Common index: 0=languages, 1=manufacturer,
                                   // 2=product, 3=serial
        memset(buffer, 0, sizeof(buffer));
        r = get_descriptor(handle, USB_DT_STRING, i, buffer, sizeof(buffer));
        if (r > 0) {
            write_bytes_to_file(out, buffer, r);
        }
    }

    // Get all configuration descriptors
    r = libusb_get_device_descriptor(selected_dev, &desc);
    if (r == 0) {
        for (int cfg_idx = 0; cfg_idx < desc.bNumConfigurations; ++cfg_idx) {
            struct libusb_config_descriptor *config;
            r = libusb_get_config_descriptor(selected_dev, cfg_idx, &config);
            if (r != 0) {
                fprintf(stderr, "Failed to get config descriptor %d\n", cfg_idx);
                continue;
            }

            // Get full configuration descriptor with all interfaces, endpoints,
            // etc.
            memset(buffer, 0, sizeof(buffer));
            r = get_descriptor(handle, USB_DT_CONFIG, cfg_idx, buffer,
                               config->wTotalLength);
            if (r > 0) {
                write_bytes_to_file(out, buffer, r);
            }

            libusb_free_config_descriptor(config);
        }
    }

    // Get Other Speed Configuration descriptor
    for (int cfg_idx = 0; cfg_idx < desc.bNumConfigurations; ++cfg_idx) {
        memset(buffer, 0, sizeof(buffer));
        r = get_descriptor(handle, USB_DT_OTHER_SPEED_CONFIG, cfg_idx, buffer,
                           sizeof(buffer));
        if (r > 0) {
            write_bytes_to_file(out, buffer, r);
        }
    }

    // Release all claimed interfaces
    for (int i = 0; i < num_interfaces; i++) {
        libusb_release_interface(handle, i);
        // Reattach kernel driver if it was active before
        if (kernel_driver_active[i]) {
            libusb_attach_kernel_driver(handle, i);
        }
    }

    fclose(out);
    printf("\n✅ Descriptor dump complete. File saved to: %s\n", DUMP_FILE);

    libusb_close(handle);
    libusb_free_device_list(devs, 1);
    libusb_exit(ctx);
    return 0;
}