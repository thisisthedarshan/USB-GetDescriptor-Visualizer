// Copyright (c) 2025 Darshan P. All rights reserved.

// This work is licensed under the terms of the MIT license.
// For a copy, see <https://opensource.org/licenses/MIT>.

#include <libusb-1.0/libusb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_DEVICES 128
#define MAX_DESCRIPTOR_SIZE 4096

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

// Print descriptor type as string
const char *descriptor_type_str(uint8_t type) {
    switch (type) {
        case USB_DT_DEVICE:
            return "Device";
        case USB_DT_CONFIG:
            return "Configuration";
        case USB_DT_STRING:
            return "String";
        case USB_DT_INTERFACE:
            return "Interface";
        case USB_DT_ENDPOINT:
            return "Endpoint";
        case USB_DT_DEVICE_QUALIFIER:
            return "Device Qualifier";
        case USB_DT_OTHER_SPEED_CONFIG:
            return "Other Speed Config";
        case USB_DT_INTERFACE_POWER:
            return "Interface Power";
        case USB_DT_OTG:
            return "OTG";
        case USB_DT_DEBUG:
            return "Debug";
        case USB_DT_INTERFACE_ASSOCIATION:
            return "Interface Association";
        case USB_DT_SECURITY:
            return "Security";
        case USB_DT_KEY:
            return "Key";
        case USB_DT_ENCRYPTION_TYPE:
            return "Encryption Type";
        case USB_DT_BOS:
            return "BOS";
        case USB_DT_DEVICE_CAPABILITY:
            return "Device Capability";
        case USB_DT_WIRELESS_ENDPOINT_COMP:
            return "Wireless Endpoint Companion";
        case USB_DT_SUPERSPEED_USB_ENDPOINT_COMP:
            return "SuperSpeed USB Endpoint Companion";
        case USB_DT_SUPERSPEED_ISO_ENDPOINT_COMP:
            return "SuperSpeed ISO Endpoint Companion";
        default:
            return "Unknown";
    }
}

void print_hex(const unsigned char *data, int length) {
    for (int i = 0; i < length; ++i) {
        if (i % 16 == 0) printf("\n%04x: ", i);
        printf("0x%02x ", data[i]);
    }
    printf("\n");
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

        printf("[%d] VID: %04x PID: %04x\n", index, desc.idVendor,
               desc.idProduct);
        device_indices[index++] = i;
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

    // Claim the first interface to ensure we can access all descriptors
    int current_config;
    r = libusb_get_configuration(handle, &current_config);
    if (r == 0) {
        // Attempt to detach kernel driver if one is active
        for (int i = 0; i < 1; i++) {
            if (libusb_kernel_driver_active(handle, i)) {
                libusb_detach_kernel_driver(handle, i);
            }
            libusb_claim_interface(handle, i);
        }
    }

    // Get device descriptor
    memset(buffer, 0, sizeof(buffer));
    r = get_descriptor(handle, USB_DT_DEVICE, 0, buffer, 18);
    if (r > 0) {
        printf("\n🔹 %s Descriptor (%d bytes):",
               descriptor_type_str(USB_DT_DEVICE), r);
        print_hex(buffer, r);
    }

    // Get BOS descriptor (USB 3.0+)
    memset(buffer, 0, sizeof(buffer));
    r = get_descriptor(handle, USB_DT_BOS, 0, buffer, sizeof(buffer));
    if (r > 0) {
        printf("\n🔹 %s Descriptor (%d bytes):", descriptor_type_str(USB_DT_BOS),
               r);
        print_hex(buffer, r);
    }

    // Get device qualifier descriptor
    memset(buffer, 0, sizeof(buffer));
    r = get_descriptor(handle, USB_DT_DEVICE_QUALIFIER, 0, buffer,
                       sizeof(buffer));
    if (r > 0) {
        printf("\n🔹 %s Descriptor (%d bytes):",
               descriptor_type_str(USB_DT_DEVICE_QUALIFIER), r);
        print_hex(buffer, r);
    }

    // Get string descriptors
    for (int i = 0; i < 4; i++) {  // Common index: 0=languages, 1=manufacturer,
                                   // 2=product, 3=serial
        memset(buffer, 0, sizeof(buffer));
        r = get_descriptor(handle, USB_DT_STRING, i, buffer, sizeof(buffer));
        if (r > 0) {
            printf("\n🔹 %s Descriptor %d (%d bytes):",
                   descriptor_type_str(USB_DT_STRING), i, r);
            print_hex(buffer, r);
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
                printf("\n🔹 %s Descriptor %d (Total length: %d bytes):",
                       descriptor_type_str(USB_DT_CONFIG), cfg_idx, r);
                print_hex(buffer, r);
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
            printf("\n🔹 %s Descriptor %d (%d bytes):",
                   descriptor_type_str(USB_DT_OTHER_SPEED_CONFIG), cfg_idx, r);
            print_hex(buffer, r);
        }
    }

    // Release interfaces
    for (int i = 0; i < 1; i++) {
        libusb_release_interface(handle, i);
    }

    libusb_close(handle);
    libusb_free_device_list(devs, 1);
    libusb_exit(ctx);
    return 0;
}