; bootloader/bootloader.asm
; GT-OS Phase 10.4 Canonical 64-Bit Long Mode Booster Crossover
; Sets up 32-bit protected mode, paves clean 4KB roads, and switches to 64-bit

[org 0x7c00]                 ; Motherboard BIOS loads Sector 0 here in RAM

bits 16                      ; Initialize processing state tracking in 16-bit Real Mode
_start:
    cli                      ; Disable physical hardware CPU interrupt line signals
    cld                      ; Force string instructions to read memory forward cleanly

    ; --- ACTIVATE THE A20 LINE ---
    ; Fast A20 gate switch via System Control Port A to prevent 1MB memory wrap-around
    in al, 0x92
    or al, 2
    out 0x92, al

    ; --- THE 3-LINE CROSSOVER INTERLOCK ---
    lgdt [gdt_descriptor]    ; Load our custom Global Descriptor Table pointer into memory
    mov eax, cr0             ; Copy Control Register 0 into accumulator
    or eax, 0x1              ; Toggle Bit 0 to activate Protected Mode
    mov cr0, eax             ; Flip the hardware processing switch

    ; --- THE FAR JUMP PIPELINE FLUSH ---
    ; Pass execution directly to the 32-bit section using our 32-bit Code Selector (0x08)
    jmp 0x08:init_32bit

; =============================================================================
; 32-BIT PROTECTED MODE EXECUTION ARENA
; =============================================================================
bits 32                      ; Instruct compiler to generate pure 32-bit instructions
init_32bit:
    ; Synchronize all data segment registers to our flat 32-bit Data Selector (0x10)
    mov ax, 0x10
    mov ds, ax
    mov ss, ax
    mov es, ax
    mov fs, ax
    mov gs, ax

    ; --- STAGE 2: BUILD THE 4-LEVEL IDENTITY MAP ROADS ---
    ; Clear the 16KB page table region first to guarantee zero garbage noise
    mov edi, PML4_TABLE
    mov ecx, 4096            ; 4096 double-words = 16 Kilobytes precisely
    xor eax, eax
    rep stosd                ; Directly stream zeros across the RAM cells

    ; Link the root tables together securely past our bootloader sector
    mov eax, PDPT_TABLE
    or eax, 0x3              ; Present + Writable bits
    mov [PML4_TABLE], eax

    mov eax, PD_TABLE
    or eax, 0x3
    mov [PDPT_TABLE], eax

    mov eax, PT_TABLE
    or eax, 0x3
    mov [PD_TABLE], eax

    ; Pave the first 2 Megabytes of physical RAM with full 8-byte entries
    mov edi, PT_TABLE        ; Destination pointer base (0xC000)
    mov ecx, 512             ; Loop exactly 512 times to fill the table
    mov eax, 0x0003          ; Base address 0x0 + Present/Writable bits (0x3)
    xor edx, edx             ; Clear EDX to keep the high 4 bytes of the entry pure 0

.map_pages_loop:
    mov [edi], eax           ; Write low 4 bytes of the page entry
    mov [edi + 4], edx       ; Write high 4 bytes of the page entry (pure 0)
    add edi, 8               ; Advance pointer to the next 8-byte table slot
    add eax, 4096            ; Advance target destination by your 4KB page size
    loop .map_pages_loop     ; Decrement ECX and loop automatically until paved

    ; --- STAGE 3: ACTIVATE THE 64-BIT PAGING ENGINE ---
    ; 1. Load the PML4 root table address (0x9000) into Control Register 3
    mov eax, PML4_TABLE
    mov cr3, eax

    ; 2. Enable Physical Address Extension (PAE) by toggling Bit 5 in Control Register 4
    mov eax, cr4
    or eax, 1 << 5           ; Set PAE bit
    mov cr4, eax

    ; 3. Enable Long Mode inside the Extended Feature Enable Register (EFER MSR)
    mov ecx, 0xC0000080      ; EFER MSR register index number
    rdmsr                    ; Read Model-Specific Register into EDX:EAX
    or eax, 1 << 8           ; Toggle Bit 8 (Long Mode Enable bit)
    wrmsr                    ; Write the updated bits back to the hardware

    ; 4. Turn on Paging by toggling Bit 31 in Control Register 0
    mov eax, cr0
    or eax, 1 << 31          ; Set Paging bit
    mov cr0, eax             ; The physical roads are now live in silicon!

    ; --- THE FINAL 64-BIT FAR JUMP ---
    ; Jump using the 64-bit Long Mode Code Selector (0x18) to clear the pipeline
    jmp 0x18:init_64bit

; =============================================================================
; 64-BIT LONG MODE EXECUTION ARENA
; =============================================================================
bits 64                      ; Instruct the compiler to generate pure 64-bit machine code
init_64bit:
    ; Synchronize all data segments to 0 cleanly for 64-bit execution safety
    xor eax, eax
    mov ds, eax
    mov es, eax
    mov ss, eax
    mov fs, eax
    mov gs, eax

    ; Correct Hardware Display Route: Write using 32-bit register widths to match the screen bus
    mov eax, 0x0F500F36      ; Bright White '6' and 'P' character tokens
    mov ebx, 0xB8000         ; VGA Text Mode Hardware Address Base
    mov [ebx], eax           ; Stream characters cleanly into the video cells

.halt_loop:
    hlt                      ; Freeze execution in a secure 64-bit low-power state
    jmp .halt_loop

; =============================================================================
; THE GLOBAL DESCRIPTOR TABLE (GDT) - THE MIXED 32/64 RUNWAY
; =============================================================================
align 8
gdt_start:
    dq 0x0000000000000000    ; 0x00: Mandatory Null Descriptor
    
    ; 0x08: 32-bit Protected Mode Code Segment Descriptor (Base=0, Limit=0xFFFFF, Flags=0xCF9A)
    dq 0x00CF9A000000FFFF
    
    ; 0x10: 32-bit Protected Mode Data Segment Descriptor (Base=0, Limit=0xFFFFF, Flags=0xCF92)
    dq 0x00CF92000000FFFF
    
    ; 0x18: Canonical 64-bit Long Mode Code Segment Descriptor (L-Bit = 1, Base/Limit ignored)
    dq 0x00209A0000000000

gdt_end:

; The GDT Pointer structure
gdt_descriptor:
    dw gdt_end - gdt_start - 1 ; Size of the GDT (minus 1 byte)
    dd gdt_start               ; Pointer address (ORG 0x7c00 handles the offset automatically)

; Define the safe, unallocated 4KB hardware page table memory addresses
PML4_TABLE equ 0x9000
PDPT_TABLE equ 0xA000
PD_TABLE   equ 0xB000
PT_TABLE   equ 0xC000

; -----------------------------------------------------------------------------
; LEGACY BOOT SECTOR PADDING MATRIX
; -----------------------------------------------------------------------------
times 510 - ($ - $$) db 0    ; Padding: Fill the rest of the 512-byte sector with exact zeros
dw 0xAA55                    ; Mandatory Bios Signature: The 2-byte magic handshake bits
