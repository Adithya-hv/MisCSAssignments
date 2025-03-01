# Linux 0.11's Interupt Handler Anaysis

So no Linux 0.11 does not use the Interupt Handler system implemented by the BIOS

Once the Bios switchs to protected mode in setup.s line 290:

```{assembly}
# absolute address 0x00000, in 32-bit protected mode.
	# absolute address 0x00000, in 32-bit protected mode.
	#mov	$0x0001, %ax	# protected mode (PE) bit
	#lmsw	%ax		# This is it!
	mov	%cr0, %eax	# get machine status(cr0|MSW)
	bts	$0, %eax	# turn on the PE-bit
	mov	%eax, %cr0	# protection enabled

				# segment-descriptor        (INDEX:TI:RPL)
	.equ	sel_cs0, 0x0008 # select for code segment 0 (  001:0 :00)
	ljmp	$sel_cs0, $0	# jmp offset 0 of code segment 0 in gdt
```

The real mode objects are no longer useful and this also sets up the Global Descriptor Table (GDT) in memory.

This long jump then transfers and starts executing system_32 in head.s

Right after segment registers are set this file calls:

```assembly
call setup_idt
```

in line 25

This call is where the kernel begins the process of installing its own interrupt handlers.
this performs:

```
lea ignore_int,%edx
	movl $0x00080000,%eax
	movw %dx,%ax		/* selector = 0x0008 = cs */
	movw $0x8E00,%dx	/* interrupt gate - dpl=0, present */

	lea idt,%edi
	mov $256,%ecx
```

Building an IDT with 256 entries and loads the IDT into the CPU using the lidt idt_descr instruction.
This is exactly where the system replaces the old BIOS interrupt with its own. Imedeiatly after the gdt is also setup with call setup_gdt
