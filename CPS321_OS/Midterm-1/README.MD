# Linux 0.11's Interrupt Handler Analysis

Linux 0.11 does not use the BIOS's interrupt handler system. Once the BIOS switches the CPU to protected mode, the system's initialization replaces the real-mode interrupt handlers with its own.

## Transition to Protected Mode

The transition occurs in setup.s at line 290:

```
# absolute address 0x00000, in 32-bit protected mode.
	#mov	$0x0001, %ax	# protected mode (PE) bit
	#lmsw	%ax		# This is it!
	mov	%cr0, %eax	# get machine status (cr0|MSW)
	bts	$0, %eax	# turn on the PE-bit
	mov	%eax, %cr0	# protection enabled

				# segment-descriptor        (INDEX:TI:RPL)
	.equ	sel_cs0, 0x0008  # select for code segment 0 (001:0:00)
	ljmp	$sel_cs0, $0	# jump to offset 0 of code segment 0 in GDT
```

At this point, the real mode components including the BIOS interrupt handlers are no longer used. Simultaneously, the Global Descriptor Table (GDT) is set up in memory.

The long jump transfers control to the 32-bit kernel code aka system_32 in head.s. Right after initializing the segment registers, the kernel calls:

```
call setup_idt
```

at line 25, is the start of the kernel’s process for installing its own interrupt handlers.

## Setting Up the Interrupt Descriptor Table (IDT)

Within the setup_idt routine, the following operations occur:

```
setup_idt:
	lea ignore_int,%edx
	movl $0x00080000,%eax
	movw %dx,%ax		/* selector = 0x0008 = cs */
	movw $0x8E00,%dx	/* interrupt gate - dpl=0, present */

	lea idt,%edi
	mov $256,%ecx
rp_sidt:
	movl %eax,(%edi)
	movl %edx,4(%edi)
	addl $8,%edi
	dec %ecx
	jne rp_sidt
	lidt idt_descr
	ret
```

Here’s what happens step by step:

An IDT with 256 entries is built. The IDT is then loaded into the CPU via the lidt idt_descr instruction, which replaces the old BIOS-provided interrupt vectors with the kernel’s own interrupt handling mechanisms.

Immediately after setting up the IDT, the kernel also sets up the GDT by calling:

```
call setup_gdt
```

This ensures that the CPU uses the new GDT, which is essential for the proper operation of the protected-mode environment.
