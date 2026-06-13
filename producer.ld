/* producer.ld - GT-OS Phase 10.4 Unified Master Mix Blueprint */
ENTRY(_start)
OUTPUT_FORMAT("binary") /* Erases host OS headers; outputs absolute raw machine code */

SECTIONS
{
    /* 
     * THE 1-MEGABYTE ANCHOR
     * Positions your monolithic Rust kernel at exactly 1MB (0x100000).
     * This keeps the Conductor completely clear of the lower legacy BIOS space,
     * the stack, and your 4-level page directory tracks (0x9000 - 0xCFFF).
     */
    . = 0x100000;

    /* MIX TRACK 1: Executable Instruction Cells */
    .text : ALIGN(4K)
    {
        *(.text._start) /* Enforces that your Rust crossover entry hook is the first byte hit */
        *(.text*)
    }

    /* MIX TRACK 2: Read-Only Invariant Constants */
    .rodata : ALIGN(4K)
    {
        *(.rodata*)
    }

    /* MIX TRACK 3: Initialized Read/Write Memory Layers */
    .data : ALIGN(4K)
    {
        *(.data*)
    }

    /* MIX TRACK 4: Uninitialized Buffer Spaces (Zeroed at Boot) */
    .bss : ALIGN(4K)
    {
        *(.bss*)
        *(COMMON)
    }
}
