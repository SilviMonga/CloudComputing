sudo /opt/homebrew/bin/qemu-system-aarch64 \
  -accel hvf -cpu cortex-a57 -M virt,highmem=off -m 2G -smp 4 \
  -drive file=/opt/homebrew/Cellar/qemu/8.2.1/share/qemu/edk2-aarch64-code.fd,if=pflash,format=raw,readonly=on \
  -drive file=ubuntu-raw.img,if=none,format=raw,id=hd0 \
  -device virtio-blk-device,drive=hd0,serial="dummyserial" \
  -device virtio-net-device,netdev=net0 \
  -netdev user,id=net0,hostfwd=tcp::8888-:22,hostfwd=tcp::8080-:8080 \
  -vga none -device ramfb -cdrom ubuntu-20.04.5-live-server-arm64.iso \
  -device usb-ehci -device usb-kbd -device usb-mouse -usb -nographic