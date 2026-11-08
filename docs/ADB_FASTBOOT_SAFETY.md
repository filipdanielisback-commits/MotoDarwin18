# ADB and Fastboot: Safe Diagnostics

This guide covers a small set of read-only checks for identifying Android Debug Bridge (ADB) and Fastboot connectivity. It is not a flashing, unlocking, repair, or bootloader-modification guide.

## Before connecting a device

- Only inspect a device you own or have explicit permission to access.
- Use Android SDK Platform-Tools from the official Android Developers site: https://developer.android.com/tools/releases/platform-tools
- Do not download ADB/Fastboot binaries from untrusted mirrors or run unknown scripts.
- Keep personal data backed up. Diagnostic commands below are intended to read status or properties, but USB debugging still grants an authorized computer access to debugging functions.
- Do not share screenshots or logs containing serial numbers, account details, or other identifying information publicly.
- On the phone, approve a USB-debugging authorization prompt only when you recognize and trust the computer.

## Read-only ADB checks

Run these in Windows PowerShell after installing the official Platform-Tools and connecting the phone normally:

```powershell
adb version
adb devices -l
adb get-state
adb shell getprop ro.product.model
adb shell getprop ro.product.device
```

What they do:
- `adb version` prints the installed ADB version.
- `adb devices -l` lists connected devices and their connection/authorization state.
- `adb get-state` reports the connection state.
- The two `getprop` commands read Android properties that may help identify the model and device codename. Properties can be absent or vendor-specific, so do not treat them as sole proof of the exact retail model.

If the device appears as `unauthorized`, stop and review the phone's own authorization prompt. Do not try to bypass authorization.

## Read-only Fastboot checks

Only use these checks if the device is already in Fastboot mode through a normal, documented device procedure. This document intentionally does not explain how to change boot modes.

```powershell
fastboot --version
fastboot devices
fastboot getvar product
```

These commands report the Fastboot tool version, enumerate detected Fastboot devices, and request the product identifier. Output varies by device and may be written to standard error. A missing or unexpected product value is not proof of a hardware fault.

## Commands intentionally excluded

This project documentation does not provide commands or procedures for:
- bootloader unlocking or relocking;
- flashing, booting, erasing, formatting, or changing partitions;
- changing active slots or other boot configuration;
- sideloading packages or installing images;
- bypassing authorization, security checks, or device protections.

Such operations can make a device unusable, erase data, weaken its security, or violate warranty and support terms. Do not copy commands from unrelated device guides and assume they apply to the Moto G60 XT2135-2.

## Interpreting results

ADB/Fastboot detection confirms only that a host tool can communicate with a device in a particular mode. It does **not** demonstrate that Darwin/XNU can boot, that required drivers exist, or that any iOS userland is compatible.

Record observations without publishing device serial numbers or other private identifiers. Separate verified observations from assumptions in the research log.

## Official references

- Android Debug Bridge (ADB): https://developer.android.com/tools/adb
- SDK Platform-Tools: https://developer.android.com/tools/releases/platform-tools
