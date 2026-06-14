// build.rs - GTOS Master Score Leaf & Automated Tape Splice
use std::fs::{File, OpenOptions};
use std::io::{Read, Write, Seek, SeekFrom};

fn main() {
    // Re-run the automation track only if a core source asset changes
    println!("cargo:rerun-if-changed=bootloader/bootloader.bin");
    println!("cargo:rerun-if-changed=target/gtos_core.bin");

    let bootloader_path = "bootloader/bootloader.bin";
    let kernel_path = "target/gtos_core.bin";
    let output_image = "target/gtos.img";

    // 1. Initialize a flat, unallocated 2 Megabyte virtual tape ribbon
    let mut img = OpenOptions::new()
        .write(true)
        .create(true)
        .truncate(true)
        .open(output_image)
        .unwrap();
    img.set_len(2_097_152).unwrap();

    // 2. Stream the 512-byte assembly boot sector cleanly onto Sector 0
    if let Ok(mut boot_file) = File::open(bootloader_path) {
        let mut buffer = [0u8; 512];
        let _ = boot_file.read(&mut buffer);
        img.seek(SeekFrom::Start(0)).unwrap();
        img.write_all(&buffer).unwrap();
    }

    // 3. Measure your core, calculate sector bounds, and print it to Track 2048
    if let Ok(mut kernel_file) = File::open(kernel_path) {
        let mut buffer = Vec::new();
        let _ = kernel_file.read_to_end(&mut buffer);
        
        // Calculate exact physical sector layout density dynamically
        let byte_length = buffer.len();
        let sector_count = (byte_length + 511) / 512;
        
        println!("cargo:warning=🎛️ [THE DECK] Splicing monolithic core track ({} bytes -> {} sectors)", byte_length, sector_count);

        // Map the binary straight to the 1MB physical offset marker
        img.seek(SeekFrom::Start(1_048_576)).unwrap();
        img.write_all(&buffer).unwrap();
    }
}
